from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('pass')
        print(login, password)
    return render_template('login.html') 

@app.route('/register')
@app.route('/register.html')
def register():
    return render_template('register.html')

# Профиль
@app.route('/profile')
@app.route('/profile.html')
def profile():
    return render_template('profile.html')

# Каталог
@app.route('/catalog')
@app.route('/catalog.html')
@app.route('/Catalog.html')  # если с заглавной буквы
def catalog():
    return render_template('catalog.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)