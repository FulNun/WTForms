from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, URL, AnyOf, NumberRange
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adopt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.String(200))
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, default=True)

class AddPetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired(), AnyOf(['cat', 'dog', 'porcupine'])])
    photo_url = StringField('Photo URL', validators=[URL()])
    age = IntegerField('Age', validators=[NumberRange(min=0, max=30)])
    notes = TextAreaField('Notes')

@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data
        )
        db.session.add(new_pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html', form=form)

@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('pet_detail', pet_id=pet_id))
    return render_template('pet_detail.html', pet=pet, form=form)

if __name__ == '__main__':
    db.create_all()  # Create database tables
    app.run(debug=True)
