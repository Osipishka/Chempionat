from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('FlaskDataBase.db', check_same_thread=False)
cursor = conn.cursor()

def check_user(email, password):
    """Проверяет существование пользователя"""
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    return user

@app.route('/')
def home():
   return render_template('login.html')

@app.route('/default')
def default():
   return render_template('default.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('pass')
        user = check_user(email, password)
        
        if user:
            return redirect('/admin')
        else:
            return render_template('login.html', error='Неверный email или пароль')
    
    return redirect('/')

@app.route('/admin')
def admin():
   return render_template('admin.html')

app.run(debug=True)