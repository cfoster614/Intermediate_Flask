from models import Cupcake, db
from app import app

db.drop_all()
db.create_all()

db.session.add_all([
    Cupcake(flavor = 'Vanilla', size = 'Large', rating = 5),
    Cupcake(flavor = 'Chocolate', size = 'Large', rating = 4, image = 'https://cdn.pixabay.com/photo/2018/08/15/11/17/muffin-3607780_1280.jpg')
])

db.session.commit()

