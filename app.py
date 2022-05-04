
#Imports
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

#Configurations
app = Flask(__name__)

#Run Script
if __name__ == '__main__':
    app.run(debug=True, port=5001)
