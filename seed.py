from models import Pet, db, connect_db
from app import create_app

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create some example pets
    pet1 = Pet(name="Fluffy", species="Cat", age=3)
    pet2 = Pet(name="Buddy", species="Dog", age=5)
    pet3 = Pet(name="Nibbles", species="Rabbit", age=2)

    # Add the pets to the database
    db.session.add_all([pet1, pet2, pet3])
    db.session.commit()
