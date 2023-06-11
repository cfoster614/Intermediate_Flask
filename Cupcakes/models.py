from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
  
DEFAULT_IMG = 'https://cdn.pixabay.com/photo/2017/05/04/21/23/cupcakes-2285209_1280.jpg'

class Cupcake(db.Model):
    """Cupcake."""
    
    __tablename__ = 'cupcakes'
    
    id = db.Column(db.Integer,
                   primary_key = True,
                   autoincrement = True)
    flavor = db.Column(db.Text,
                       nullable = False)
    size = db.Column(db.Text,
                     nullable = False)
    rating = db.Column(db.Float,
                       nullable = False)
    image = db.Column(db.Text,
                      nullable = False,
                      default = DEFAULT_IMG)
    

    def serialize(self):
        """Serialize a self SQLAlchemy obj to dictionary"""

        return {
            'id' : self.id,
            'flavor' : self.flavor,
            'size' : self.size,
            'rating' : self.rating,
            'image' : self.image
        }
    
