"""Flask app for adopt app."""

from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdef"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///adopt"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
app.app_context().push()
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def list_pets():
    
    pets = Pet.query.all()

    return render_template('homepage.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet_form():

    form = AddPetForm() 

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data or None
        age = form.age.data
        notes = form.notes.data
        available = form.available.data or None
    
        new_pet = Pet(name=name, species=species, photo_url=photo_url,
                      age=age, notes=notes, available=available)
        
        db.session.add(new_pet)
        db.session.commit()

        flash(f'{new_pet.name} has been added.')

        return redirect('/')

    else:
        return render_template('add_pet_form.html', form=form)


@app.route('/<int:id>', methods=['GET', 'POST'])
def show_and_edit_pet(id):

    pet = Pet.query.get_or_404(id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data 

        db.session.commit()

        flash(f'{pet.name} has been updated.')

        return redirect('/')
    
    else:
        return render_template('edit_pet_form.html', form=form, pet=pet)

