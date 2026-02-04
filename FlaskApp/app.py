from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('FlaskDataBase.db', check_same_thread=False)
cursor = conn.cursor()

def check_user(email, password):
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    return user

@app.route('/get_courses_for_select')
def get_courses_for_select():
    try:
        cursor.execute("SELECT ID, Name FROM Courses ORDER BY Name")
        courses = cursor.fetchall()
        result = [{'ID': row[0], 'Name': row[1]} for row in courses]
        return jsonify(result)
    except Exception as e:
        print("Ошибка:", e)
        return jsonify([]), 500


# Маршрут для сохранения нового студента
@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        course = request.form.get('course', '').strip()
        date = request.form.get('date')
        status = request.form.get('status')

        if not full_name or not email or not course or not date or not status:
            return jsonify({'success': False, 'error': 'Заполните все поля'}), 400

        # Можно добавить валидацию email (простая)
        if '@' not in email:
            return jsonify({'success': False, 'error': 'Некорректный email'}), 400

        cursor.execute("""
            INSERT INTO Students (Email, Name, Course, Date, Status)
            VALUES (?, ?, ?, ?, ?)
        """, (email, full_name, course, date, status))
        
        conn.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        conn.rollback()
        print("Ошибка добавления студента:", e)
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/showAllStudents', methods=['GET'])
def show_all_students():
    cursor.execute('SELECT * FROM Students')
    students = cursor.fetchall()
    
    # Преобразуем в HTML таблицу
    html = '<table border="1">'
    html += '<tr><th>ID</th><th>Email</th><th>Name</th><th>Course</th><th>Date</th><th>Status</th></tr>'
    
    for student in students:
        html += f'''
        <tr>
            <td>{student[0]}</td>
            <td>{student[1]}</td>
            <td>{student[2]}</td>
            <td>{student[3]}</td>
            <td>{student[4]}</td>
            <td>{student[5]}</td>
        </tr>
        '''
    
    html += '</table>'
    return html

@app.route('/get_first_five_students')
def get_first_five_students():
    try:
        # 1. Проверяем, существует ли таблица и сколько в ней строк
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Students'")
        if not cursor.fetchone():
            return "<p style='color:red;'>Таблица Students НЕ существует в базе!</p>"

        cursor.execute("SELECT COUNT(*) FROM Students")
        count = cursor.fetchone()[0]
        print(f"Количество студентов в базе: {count}")  # ← смотри в терминал!

        # 2. Пробуем простой запрос
        cursor.execute("""
            SELECT ID, Email, Name, Course, Date, Status
            FROM Students
            ORDER BY ID DESC
            LIMIT 5
        """)
        students = cursor.fetchall()

        print(f"Получено студентов: {len(students)}")  # ← тоже в терминал

        html = ''

        for student in students:
            # student — кортеж, обращаемся по индексам
            name = student[2] if student[2] else "—"
            email = student[1] if student[1] else "—"
            course = student[3] if student[3] else "—"
            date = student[4] if student[4] else "—"
            status_text = student[5] if student[5] else "Ожидает оплаты"

            status_lower = status_text.lower()
            status_class = 'paid'
            if 'ожидает' in status_lower:
                status_class = 'pending'
            elif 'ошибк' in status_lower or 'ошибка' in status_lower:
                status_class = 'error'

            html += f'''
            <div class="student-card">
                <div class="student-info">
                    <h3 class="student-name">{name}</h3>
                    <p class="student-email">{email}</p>
                </div>
                <div class="student-course">
                    <span class="course-label">Курс:</span>
                    <span class="course-name">{course}</span>
                </div>
                <div class="student-meta">
                    <div class="meta-item">
                        <span class="label">Дата записи:</span>
                        <span class="value">{date}</span>
                    </div>
                    <div class="meta-item">
                        <span class="label">Статус:</span>
                        <span class="status {status_class}">{status_text}</span>
                    </div>
                </div>
            </div>
            '''

        if not students:
            html = '<p style="text-align:center; color:#777; padding:20px;">В базе нет студентов</p>'

        html += '''
        <div class="pagination">
            <button class="page-btn prev" disabled>← Назад</button>
            <span class="page-info">Страница 1 из ?</span>
            <button class="page-btn next">Вперёд →</button>
        </div>
        '''

        return html

    except Exception as e:
        # Выводим полную ошибку и в терминал, и в браузер
        import traceback
        error_msg = traceback.format_exc()
        print("КРИТИЧЕСКАЯ ОШИБКА В /get_first_five_students:")
        print(error_msg)
        return f'''
        <div style="color:red; padding:20px; background:#ffebee; border:1px solid #c62828; border-radius:8px;">
            <h3>Ошибка на сервере (500)</h3>
            <pre>{error_msg}</pre>
            <p>Посмотрите также консоль терминала, где запущен Flask.</p>
        </div>
        '''

@app.route('/findStudentByName', methods=['POST'])
def search_students():
        search = request.form.get('name', '').strip()
        if not search:
            return jsonify([])
        cursor.execute(""" 
        SELECT ID, Email, Name, Course, Date, Status
        FROM Students
        WHERE Name LIKE ?
        """, (f'%{search}',))
        students = cursor.fetchall()
    
    # Возвращаем JSON, который JS сможет обработать
        result = []
        for s in students:
            result.append({
                'id': s[0],
                'email': s[1],
                'name': s[2],
                'course': s[3],
                'date': s[4],
                'status': s[5]
            })
    
        return jsonify(result)


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