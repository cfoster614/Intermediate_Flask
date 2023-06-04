from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

DEFAULT_IMG = 'https://cdn.pixabay.com/photo/2016/07/21/14/18/dog-1532627_1280.png'
  
class Pet(db.Model):
    """Pet."""
    
    __tablename__ = 'pets'
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    name = db.Column(db.String(20),
                     nullable = False)
    
    species = db.Column(db.Text,
                        nullable = False)
    photo_url = db.Column(db.Text)
    
    age = db.Column(db.Integer)
    
    notes = db.Column(db.Text)
    
    available = db.Column(db.Boolean, 
                          default = True,
                          nullable = False)