from flask import Flask, request, render_template, redirect, url_for  
from models import db, connect_db, Pet
import logging
from forms import AddPetForm, EditPetForm

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
app = Flask(__name__)  
app.config['SECRET_KEY'] = "scamp" 
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route("/")
def main_page():
    pets = Pet.query.all()
    return render_template('pet-page.html', pets=pets)

@app.route("/add", methods = ["GET", "POST"])
def add_pet():
    """Pet add form; handle adding."""
    form = AddPetForm()
    
    if form.validate_on_submit():
        name = form.pet_name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        
        if not photo_url:
            new_pet = Pet(name = name, species = species, photo_url = 'https://cdn.pixabay.com/photo/2016/07/21/14/18/dog-1532627_1280.png', age = age, notes = notes)
        
        else:
             new_pet = Pet(name = name, species = species, photo_url = photo_url, age = age, notes = notes)
             
        db.session.add(new_pet)
        db.session.commit()
        return redirect('/')
    
    else:
        return render_template('/Forms/add_pet_form.html', form=form)
    

@app.route("/<int:pet_id>/details", methods=["GET", "POST"])
def pet_details(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    
    
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        return redirect("/")
    
    else:
        return render_template('pet-details.html', pet=pet, form=form)
    