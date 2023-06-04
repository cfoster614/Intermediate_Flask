from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange

class AddPetForm(FlaskForm):
    """Form for adding a pet."""
    pet_name = StringField("Pet Name",
                           validators=[InputRequired()])
    species = StringField("Species",
                          validators=[AnyOf(message="Must be a dog, cat, or porcupine", values= ['dog', 'cat', 'porcupine'])])
    photo_url = StringField("Photo URL",
                            validators=[Optional(), URL(message="Invalid URL.")])
    age = FloatField("Age in Years",
                     validators=[Optional(),
                                 NumberRange(min=0, max=30, message='Age must be between 0 and 30')])
    notes = StringField("Notes",
                        validators=[Optional()])
    
class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL",
                            validators=[Optional(), URL(message="Invalid URL.")])
    notes = StringField("Notes",
                        validators=[Optional()])
    available = BooleanField("Available for Adoption")