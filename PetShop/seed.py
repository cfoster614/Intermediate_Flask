from models import Pet, db
from app import app

db.drop_all()
db.create_all()

db.session.add_all([
    Pet(name = 'Mr. Paws', species = 'cat', photo_url = 'https://cdn.pixabay.com/photo/2016/02/10/16/37/cat-1192026_1280.jpg', age = '1', notes = 'Mr. Paws is a friendly little kitten. He loves playing with his fishy toy and climbing up the legs of his humans!'),
    Pet(name = 'Luna', species = 'cat', photo_url = 'https://cdn.pixabay.com/photo/2017/02/15/12/12/cat-2068462_1280.jpg', age = '2', notes = 'Luna enjoys long naps in the sun and gourmet food. She is looking for a human to pamper and spoil her.', available = False),
    Pet(name = 'Hawkeye', species = 'dog', photo_url = 'https://cdn.pixabay.com/photo/2018/09/17/20/55/dog-3684793_1280.jpg', age = '10', notes = 'Hawkeye is an old soul that wants some walks around the park followed by some quality time on the couch with his favorite chew.')
])

db.session.commit()