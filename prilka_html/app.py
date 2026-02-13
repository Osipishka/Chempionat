from flask import Flask, render_template, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from api import db_api
import os

app = Flask(__name__)
app.secret_key = '12345'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', )
def register():
    return render_template('register.html')

@app.route('/reg', methods=['POST'])
def reg():
    if request.method == 'POST':
        login = request.form.get('login')
        pas = request.form.get('password')
    
    if not login or not pas:
        return render_template('register.html')
    db_api.reg_user(login=login, password=pas)
    return redirect('/')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_user', methods=['POST'])
def login_user():
    if request.method == 'POST':
     
        login = request.form.get('login')
        password = request.form.get('password')

        if not login or not password:
            return render_template('login.html', error="Заполните все поля")

        user = db_api.login_user(login=login, password=password)

        if user:
            # Успешный вход
            session['user_id'] = user['id']
            session['login'] = user['login']
            session['role'] = user['role']
            
            if user['role'] == 'admin':
                return redirect('/admin')
            else:
                return redirect('/profile')
        else:
            return render_template('login.html', error="Неверный логин или пароль")
    
    return redirect('/')

@app.route('/profile')
def get_user():
    
    return render_template('profile.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_game', methods=['POST'])
def add_game():
    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        dev = request.form.get('developer')
        rating = request.form.get('rating')
        cost = request.form.get('cost')

        img_path = 'images/Default.png'

        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = file.filename
                file.save(os.path.join('static', 'images', filename))
                img_path = f'images/{filename}'

        db_api.create_game(title, img_path, genre, dev, rating=int(rating), cost=int(cost))
    return redirect('/admin')

@app.route('/find_game', methods=['POST'])
def find_game():
    """Найти игру по ID для редактирования"""
    game_id = request.form.get('id')
    
    if not game_id:
        return redirect('/admin')
    
    try:
        game_id_int = int(game_id)
        game = db_api.get_game_by_id(game_id_int)
        
        if game:
            # Возвращаем ту же страницу, но с данными игры
            return render_template('admin.html', game=game)
        else:
            # Игра не найдена
            return render_template('admin.html', error="Игра не найдена")
            
    except:
        return redirect('/admin')

@app.route('/edit_game', methods=['POST'])
def edit_game():
    """Обработка формы редактирования"""
    game_id = request.form.get('id')
    title = request.form.get('title')
    genre = request.form.get('genre')
    developer = request.form.get('developer')
    rating = request.form.get('rating')
    cost = request.form.get('cost')
    
    if not all([game_id, title, developer, rating, cost]):
        return redirect('/admin')
    
    # Получаем текущую игру
    current_game = db_api.get_game_by_id(int(game_id))
    
    # Обрабатываем картинку
    img_path = current_game['image_url'] if current_game else 'images/Default.png'
    
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename:
            filename = file.filename
            file.save(os.path.join('static', 'images', filename))
            img_path = f'images/{filename}'
    
    # Конвертируем числа
    try:
        game_id_int = int(game_id)
        rating_int = int(rating)
        cost_int = int(cost)
    except:
        return redirect('/admin')
    
    # Обновляем игру
    success = db_api.edit_game(
        game_id=game_id_int,
        title=title,
        img=img_path,
        genre=genre,
        dev=developer,
        rating=rating_int,
        cost=cost_int
    )
    return redirect('/admin')


@app.route('/delete_game', methods=['POST'])
def delete_game():
        game_id = request.form.get('id')
        
        if not game_id:
            return redirect('/admin')
        
        game_id_int = int(game_id)

        db_api.delete_game(game_id_int)
    
        return redirect('/admin')

@app.route('/Catalog', methods=['GET', 'POST'])
def catalog():
    # Получаем номер страницы из GET-параметра (по умолчанию 1)
    page = request.args.get('page', 1, type=int)
    
    # Получаем игры с пагинацией
    data = db_api.get_games_paginated(page=page, per_page=8)
    
    return render_template('Catalog.html', 
                          games=data['games'],
                          page=data['page'],
                          total_pages=data['total_pages'])

if __name__ == '__main__':
    app.run(debug=True)