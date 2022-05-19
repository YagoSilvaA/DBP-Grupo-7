#Imports

from collections import UserList
from hashlib import new
import os
from email.policy import default
import re
from sqlite3 import Row
from typing import final
from xmlrpc.client import TRANSPORT_ERROR
from config import Config
from flask_wtf.csrf import CSRFProtect
from flask import (
    Flask,
    flash,
    redirect,
    render_template, 
    request,
    url_for, 
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (
    UserMixin,
    login_user, 
    LoginManager, 
    login_required, 
    logout_user, 
    current_user
)
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash

#Configurations
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
#Managing Log in
LogManager = LoginManager(app)


@LogManager.user_loader
def load_user(id):
    return Users.id_get(db, id)

#Security Token
csrf = CSRFProtect()

#Models
class Appointments(db.Model):
    __tablename__ = 'Appointments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    pet = db.Column(db.String(100), nullable = False)
    date = db.Column(db.DateTime)
    owner_id = db.Column(db.String, db.ForeignKey('Users.username'))



class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    password = db.Column(db.String(150), nullable = False)
    citas = db.relationship('Appointments', backref='owner')

    def __init__(self, id, username, password) -> None:
            self.id = id
            self.username = username
            self.password = password
      
    @classmethod
    def password_verification(self, hashed_password, password):
        return check_password_hash(hashed_password, password)
    
    @classmethod
    def authentication(self,db,user):
        try: 
            con = psycopg2.connect(database='appointments', user = 'postgres', password = '123456789')
            cursor = con.cursor()
            sql = """SELECT id, username, password FROM "Users"
                    WHERE username = '{}' """.format(user.username)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = Users(row[0], row[1], Users.password_verification(row[2], user.password))
                return user
            else:
                return None
        except psycopg2.DatabaseError as e:
            raise Exception(e)
    
    @classmethod
    def id_get(self,db,id):
        try: 
            con = psycopg2.connect(database='appointments', user = 'postgres', password = '123456789')
            cursor = con.cursor()
            sql = """SELECT id, username FROM "Users"
                    WHERE id = '{}' """.format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                log_user = Users(row[0], row[1], None)
                return log_user
            else:
                return None
        except psycopg2.DatabaseError as e:
            raise Exception(e)

db.create_all()
## CRUD
@app.route('/')
def Loginroute():
    return redirect(url_for('register'))


@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    appointments = Appointments.query.order_by(Appointments.date.asc()).all()
    return render_template("index.html", appointments = appointments)

@app.route('/create', methods = ['GET', 'POST'])
def insert():
    try:
        if request.method=='POST':
            con = psycopg2.connect(database='appointments', user = 'postgres', password = '123456789')
            cursor = con.cursor()
            name = request.form.get('name')
            pet = request.form['pet']
            date = request.form['date']
            owner_id = request.form['owner']
        
            if len(name)<=0:
                flash('Ingresar nombre')
                return redirect(url_for('/index'))
            if len(pet) <= 0:
                flash('Ingresar Animal/raza')
                return redirect(url_for('/index'))
            if len(date) <= 0:
                flash('Ingresar fecha')
                return redirect(url_for('/index'))            
            nxdate = date[0:10]
            nxdate2 = date[11:13]
            nxdate3 = nxdate + ' ' + nxdate2
            sql = """SELECT FROM "Appointments" WHERE to_char(date,'yyyy-mm-dd HH24')='{}' """.format(nxdate3)
            cursor.execute(sql)
            row = cursor.fetchall()
        
            if row:
                flash('Ya existe una cita a esa fecha y hora')
                return redirect(url_for('index'))
            else:
                animal = Appointments(name=name, pet=pet, date=date, owner_id=owner_id)
                db.session.add(animal)
                db.session.commit()
                return redirect(url_for('/index'))
    except:
        
        db.session.rollback()
    finally:
        db.session.close()

    return redirect('/index')        

@app.route('/delete', methods = ['POST'])
def delete():
  #  try:
  #      name = request.form.get('name')
  #      animal = Appointments.query.filter_by(name = name).first()
  #      db.session.delete(animal)
  #      db.session.commit()
  #  except:
  #      flash("Usuario no encontrado")
  #      db.session.rollback()
  #  finally:
  #      db.session.close()

    try:
        name = request.form.get('name')
        usuario = request.form['owner']
        animal = Appointments.query.filter_by(name = name).first()
        user_id = Appointments.query.filter_by(owner_id = usuario).first()
        if animal != None:
            if user_id == animal: 
                db.session.delete(animal)
                db.session.commit()
            else:
                flash("No eres su dueño")
        else:
            flash("Mascota no encontrada ")

    except:
        db.session.rollback()

    finally:
         db.session.close()

    return redirect('/index')


@app.route('/updatedate', methods = ['POST'])
def updatedate():
    try:
        con = psycopg2.connect(database='appointments', user = 'postgres', password = '123456789')
        cursor = con.cursor()
        

        newdate = request.form.get("newdate")
        nxdate = newdate[0:10]
        nxdate2 = newdate[11:13]
        nxdate3 = nxdate + ' ' + nxdate2
        
        sql = """SELECT FROM "Appointments" WHERE to_char(date,'yyyy-mm-dd HH24')='{}' """.format(nxdate3)
       
        cursor.execute(sql)
        row = cursor.fetchall()
        
        if row:
            flash('Ya existe una cita a esa fecha y hora')
        else:
            appid = request.form.get("appid")
            appointment = Appointments.query.filter_by(id=appid).first()
            appointment.date = newdate
            db.session.commit()
    
    except:
        db.session.rollback
    return redirect('/index')


#Error handling

@app.errorhandler(404)
def error404(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error500(e):
    return render_template("500.html"), 500


@app.errorhandler(401)
def error401(e):
    return render_template("401.html"), 401


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        user = Users(0, request.form.get('username'), request.form.get('password'))
        logged_user = Users.authentication(db,user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('index'))
            else:
                flash("Incorrect password")
                return render_template('auth/login.html')
        else:
            flash("non-existent user")
        return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        if Users.query.filter_by(username = username).first() != None:
            flash("Already an existing user")
        else:
            hash_password = generate_password_hash(request.form.get('password'))
            user = Users( None ,username, hash_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('auth/register.html')
# user page

@app.route('/user/')
def user():
    return render_template('user.html')

# User Log out
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

#Run Script
if __name__ == '__main__':
    csrf.init_app(app)
    app.run(debug=True, port=5001)