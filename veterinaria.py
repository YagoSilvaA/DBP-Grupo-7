
#Imports

from flask import Flask, request, render_template

from flask_sqlalchemy import SQLAlchemy


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
    def __repr__(self):
        return f'Todo: id={self.id}, description={self.description}'

db.create_all()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/insert', methods = ['POST'])
def insert():
    if request.form:
        name = request.form['name']
        pet = request.form['pet']
        date = request.form['date']
        

#Run Script
if __name__ == '__main__':
    app.run(debug=True, port=5001)
