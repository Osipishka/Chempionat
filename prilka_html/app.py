from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from api import db_api

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/Catalog')
def catalog():
    games = db_api.get_all_games()
    return render_template('Catalog.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)