
#Imports
from crypt import methods
from email.policy import default
from flask import (
    Flask,
    render_template, 
    request,
    url_for, 
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

#Configurations
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres@localhost:5432/appointments"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Animals(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    pet = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime)
        
db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/create', methods = ['GET', 'POST'])
def insert():
    if request.method=='POST':
        name = request.form.get('name')
        pet = request.form['pet']
        date = request.form['date']
    animal = Animals(name=name, pet=pet, date=date)
    db.session.add(animal)
    db.session.commit()
    db.session.close()

    return render_template('index.html')            

#Run Script
if __name__ == '__main__':
    app.run(debug=True, port=5001)
