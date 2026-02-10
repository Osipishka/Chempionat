from flask import Flask, render_template, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from api import db_api
import os

app = Flask(__name__)
app.secret_key = '12345'

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

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/add_game', methods=['POST'])
def add_game():
    if request.method == 'POST':
        # Обработка добавления игры
        title = request.form.get('title')
        genre = request.form.get('genre')
        developer = request.form.get('developer')
        rating = request.form.get('rating')
        cost = request.form.get('cost')
        
        # Проверяем основные поля
        if not title or not genre or not developer or not rating or not cost:
            return redirect('/admin')
        
        # Обрабатываем картинку
        img_path = 'images/Default.png'
        
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                filename = file.filename
                file.save(os.path.join('static', 'images', filename))
                img_path = f'images/{filename}'
        
        # Конвертируем числа
        try:
            rating_int = int(rating)
            cost_int = int(cost)
        except:
            return redirect('/admin')
        
        # Добавляем в БД
        db_api.create_game(title, img_path, genre, developer, rating_int, cost_int)
    return redirect('/admin')

@app.route('/find_game', methods=['GET'])
def find_game():
    """Найти игру по ID для редактирования"""
    game_id = request.args.get('id')
    
    if not game_id:
        return redirect('/admin')
    
    try:
        game_id_int = int(game_id)
        game = db_api.get_game_by_id(game_id_int)
        
        if game:
            # Возвращаем страницу админа с предзаполненной формой
            return render_template('edit_form.html', game=game)
        else:
            return redirect('/admin')
            
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
    
    # Обрабатываем картинку
    img_path = 'images/Default.png'
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
    db_api.edit_game(game_id_int, title, img_path, genre, developer, rating_int, cost_int)
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
    games = db_api.get_all_games()   
    return render_template('Catalog.html', games=games)

if __name__ == '__main__':
    app.run(debug=True)