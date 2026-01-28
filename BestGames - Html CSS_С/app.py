from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/register')
@app.route('/register.html')
def register():
    return render_template('register.html')

# Вход
@app.route('/login')
@app.route('/login.html')
def login():
    return render_template('login.html')

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

# Обслуживаем статические файлы (CSS, JS, изображения)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Обработка 404 ошибки
@app.errorhandler(404)
def page_not_found(e):
    # Можно вернуть свою страницу 404
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)