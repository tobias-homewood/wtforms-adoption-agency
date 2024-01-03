"""Flask app for adopt app."""

from flask import (
    Flask,
    url_for,
    render_template,
    redirect,
    flash,
    jsonify,
    request,
    session,
)
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm


def create_app(db_url="postgresql:///adopt", testing=False):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["TESTING"] = testing
    app.config["DEBUG"] = True
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

    if not testing:
        connect_db(app)
        with app.app_context():
            db.create_all()

    from flask_debugtoolbar import DebugToolbarExtension

    app.config["SECRET_KEY"] = "SECRET!"
    debug = DebugToolbarExtension(app)

    @app.route("/")
    def list_pets():
        """List all pets."""

        pets = Pet.query.all()
        return render_template("pet_list.html", pets=pets)


    @app.route("/add", methods=["GET", "POST"])
    def add_pet():
        """Add a pet."""

        form = AddPetForm()

        if form.validate_on_submit():
            data = {k: v for k, v in form.data.items() if k != "csrf_token"}
            new_pet = Pet(**data)
            # new_pet = Pet(name=form.name.data, age=form.age.data, ...)
            db.session.add(new_pet)
            db.session.commit()
            flash(f"{new_pet.name} added.")
            return redirect(url_for('list_pets'))

        else:
            # re-present form for editing
            return render_template("pet_add_form.html", form=form)

    @app.route("/<int:pet_id>", methods=["GET", "POST"])
    def edit_pet(pet_id):
        """Edit pet."""

        pet = Pet.query.get_or_404(pet_id)
        form = EditPetForm(obj=pet)

        if form.validate_on_submit():
            pet.notes = form.notes.data
            pet.available = form.available.data
            pet.photo_url = form.photo_url.data
            db.session.commit()
            flash(f"{pet.name} updated.")
            return redirect(url_for('list_pets'))

        else:
        # failed; re-present form for editing
            return render_template("pet_edit_form.html", form=form, pet=pet)
    
    return app
    
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
