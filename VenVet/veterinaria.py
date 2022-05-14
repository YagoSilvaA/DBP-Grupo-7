
#Imports
##from crypt import methods
##from crypt import methods
from email.policy import default
from typing import final
from flask import (
    Flask,
    redirect,
    render_template, 
    request,
    url_for, 
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    UserMixin, 
    login_user, 
    LoginManager, 
    login_required, 
    logout_user, 
    current_user)
import sys

#Configurations
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123456789@localhost:5432/appointments"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

#Models

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)

class Appointments(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    pet = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime)
        
db.create_all()
## CRUD
appointments = Appointments.query.all()
@app.route('/', methods=['GET', 'POST'])
def index():
    appointments = Appointments.query.all()
    return render_template("index.html", appointments = appointments)

@app.route('/create', methods = ['GET', 'POST'])
def insert():
    try:
        if request.method=='POST':
            name = request.form.get('name')
            pet = request.form['pet']
            date = request.form['date']
            animal = Appointments(name=name, pet=pet, date=date)
            db.session.add(animal)
            db.session.commit()
    except:

        db.session.rollback()
    finally:
        db.session.close()

    return redirect('/')        

@app.route('/delete', methods = ['POST'])
def delete():
    name = request.form.get('name')
    animal = Appointments.query.filter_by(name = name).first()
    db.session.delete(animal)
    db.session.commit()
    return redirect('/')


@app.route('/updatedate', methods = ['POST'])
def updatedate():
    newdate = request.form.get("newdate")
    olddate = request.form.get("olddate")
    appointment = Appointments.query.filter_by(date=olddate).first()
    appointment.date = newdate
    db.session.commit()
    return redirect('/')


#Error handling

@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def error500(e):
    return render_template("500.html"), 500

# user page
@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username = username)
#Run Script
if __name__ == '__main__':
    app.run(debug=True, port=5001)
