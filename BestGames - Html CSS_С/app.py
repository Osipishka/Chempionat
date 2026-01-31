from flask import Flask, render_template, request, redirect
import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 


app.config['SQLALCHEMY_DATABESE_URI'] = 'mysql+pymysql://root:852963@localhost/best_game_data'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)












conn = sqlite3.connect('best_game_data.db', check_same_thread=False)
cur = conn.cursor()

def add_user(user_name, user_fullName, user_login, user_password, user_bitrhday):
    cur.execute('INSERT INTO users(user_name, user_fullName, user_login, user_password, user_bitrhday) VALUES (?, ?, ?, ?, ?)', [user_name, user_fullName, user_login, user_password, user_bitrhday])
    conn.commit()


def get_user_by_id(user_id):
    cur.execute(f'SELECT * FROM users WHERE id = {user_id}')
    return cur.fetchone()


def get_user_by_email(user_login):
    cur.execute(f'SELECT * FROM users WHERE email = ?', [user_login])
    return cur.fetchone()


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

@app.route('/register', methods=['GET', 'POST'])
@app.route('/register.html')
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        fullname = request.form.get('fullName')
        name = request.form.get('name') 
        password = request.form.get('pass')
        birthday = request.form.get('birthday')
        user = get_user_by_email(login)
        if user is None:
            add_user(login, fullname, name, password, birthday)
            return redirect('/profile')
        else:
            print('Такой пользователь уже есть')
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