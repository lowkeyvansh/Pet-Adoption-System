from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    breed = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    adopted = db.Column(db.Boolean, default=False)

class PetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=150)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
    breed = StringField('Breed', validators=[DataRequired(), Length(min=2, max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

db.create_all()

@app.route('/')
def home():
    pets = Pet.query.filter_by(adopted=False).all()
    return render_template('index.html', pets=pets)

@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
    form = PetForm()
    if form.validate_on_submit():
        new_pet = Pet(
            name=form.name.data,
            age=form.age.data,
            breed=form.breed.data,
            description=form.description.data
        )
        db.session.add(new_pet)
        db.session.commit()
        flash('Pet added successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('add_pet.html', form=form)

@app.route('/adopt_pet/<int:id>', methods=['POST'])
def adopt_pet(id):
    pet = Pet.query.get_or_404(id)
    pet.adopted = True
    db.session.commit()
    flash('Pet adopted successfully!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
