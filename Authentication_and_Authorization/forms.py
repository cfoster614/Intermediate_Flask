from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired


class RegisterUser(FlaskForm):
    """Form for registering a user."""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First name", validators=[InputRequired()])
    last_name = StringField("Last name", validators=[InputRequired()])
    
    
class LoginUser(FlaskForm):
    """Login a user."""
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    
    
class FeedbackForm(FlaskForm):
    """Create feedback."""
    id = HiddenField("Id")
    title = StringField("Title", validators=[InputRequired()]) 
    content = StringField("Content", validators=[InputRequired()]) 