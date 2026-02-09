// Базовая логика JS для админ-панели

const apiBase = '/school-api'; // замените на реальный путь
let token = localStorage.getItem('adminToken') || null;
let currentPage = 1;
let currentCourseId = null;

// Проверка авторизации при загрузке
if (token) {
    showSection('courses-section');
    loadCourses();
    loadStudentCourseFilter();
    // Добавляем кнопку "Студенты" в секцию курсов
    document.querySelector('#courses-section').insertAdjacentHTML('afterbegin', '<button id="to-students">Студенты</button>');
    document.getElementById('to-students').addEventListener('click', () => showSection('students-section'));
} else {
    showSection('login-section');
}

// Авторизация
document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    clearErrors();

    if (!email || !password) {
        showError('login-email', 'Обязательное поле');
        showError('login-password', 'Обязательное поле');
        return;
    }

    // Для тренировки — хардкод админских данных
    if (email === 'andrej.osipov.07@bk.ru' && password === '852963') {
        token = 'fake-token-for-testing';
        localStorage.setItem('adminToken', token);
        showSection('courses-section');
        loadCourses();
        loadStudentCourseFilter();
    } else {
        showError('login-email', 'Некорректные данные');
    }
});

// Выход
document.getElementById('logout').addEventListener('click', () => {
    localStorage.removeItem('adminToken');
    token = null;
    showSection('login-section');
});

// Загрузка списка курсов
async function loadCourses(page = 1) {
    currentPage = page;
    // Здесь будет реальный fetch к API
    // const response = await fetch(`${apiBase}/courses?page=${page}`, {
    //     headers: { Authorization: `Bearer ${token}` }
    // });

    // Симуляция данных
    const data = {
        data: [
            { id: 1, name: 'Курс 1', description: 'Описание курса', hours: 5, price: '150.00', start_date: '01-01-2026', end_date: '31-01-2026', img: 'mpic_course1.jpg' },
            // можно добавить ещё для теста
        ],
        pagination: { total: 2, current: 1, per_page: 5 }
    };

    const tbody = document.querySelector('#courses-table tbody');
    tbody.innerHTML = '';

    data.data.forEach(course => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${course.id}</td>
            <td>${course.name}</td>
            <td>${course.description}</td>
            <td>${course.hours}</td>
            <td>${course.price}</td>
            <td>${course.start_date}</td>
            <td>${course.end_date}</td>
            <td><img src="${course.img}" width="50" alt="обложка"></td>
            <td>
                <button onclick="editCourse(${course.id})">Редактировать</button>
                <button onclick="deleteCourse(${course.id})">Удалить</button>
                <button onclick="viewLessons(${course.id}, '${course.name.replace(/'/g, "\\'")}')">Уроки</button>
                <button onclick="printCertificates(${course.id})">Сертификаты</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    renderPagination(data.pagination, 'courses-pagination', loadCourses);
}

// Добавление нового курса
document.getElementById('add-course-btn').addEventListener('click', () => {
    document.getElementById('course-form-title').textContent = 'Добавить курс';
    document.getElementById('course-form').reset();
    document.getElementById('course-id').value = '';
    showSection('course-form-section');
});

// Сохранение курса
document.getElementById('course-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErrors();

    const formData = new FormData();
    formData.append('name', document.getElementById('course-name').value);
    formData.append('description', document.getElementById('course-description').value);
    formData.append('hours', document.getElementById('course-hours').value);
    formData.append('price', document.getElementById('course-price').value);
    formData.append('start_date', document.getElementById('course-start-date').value);
    formData.append('end_date', document.getElementById('course-end-date').value);

    const file = document.getElementById('course-image').files[0];
    if (file) formData.append('image', file);

    const id = document.getElementById('course-id').value;
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${apiBase}/courses/${id}` : `${apiBase}/courses`;

    // Здесь будет реальный fetch
    // const response = await fetch(url, {
    //     method,
    //     body: formData,
    //     headers: { Authorization: `Bearer ${token}` }
    // });

    showSection('courses-section');
    loadCourses(currentPage);
});

document.getElementById('cancel-course').addEventListener('click', () => showSection('courses-section'));

// Редактирование курса
window.editCourse = async (id) => {
    // Симуляция получения данных курса
    const course = {
        id: id,
        name: 'Курс 1',
        description: 'Описание курса',
        hours: 5,
        price: '150.00',
        start_date: '01-01-2026',
        end_date: '31-01-2026'
    };

    document.getElementById('course-id').value = course.id;
    document.getElementById('course-name').value = course.name;
    document.getElementById('course-description').value = course.description;
    document.getElementById('course-hours').value = course.hours;
    document.getElementById('course-price').value = course.price;
    document.getElementById('course-start-date').value = course.start_date;
    document.getElementById('course-end-date').value = course.end_date;
    document.getElementById('course-form-title').textContent = 'Редактировать курс';
    showSection('course-form-section');
};

// Удаление курса (заглушка)
window.deleteCourse = async (id) => {
    if (confirm('Удалить курс?')) {
        // await fetch(`${apiBase}/courses/${id}`, { method: 'DELETE', headers: { Authorization: `Bearer ${token}` } });
        loadCourses(currentPage);
    }
};

// Переход к урокам курса
window.viewLessons = (courseId, courseName) => {
    currentCourseId = courseId;
    document.getElementById('course-name-lessons').textContent = courseName;
    showSection('lessons-section');
    loadLessons(courseId);
};

// Загрузка уроков (симуляция)
async function loadLessons(courseId) {
    // Симуляция
    const data = [
        { id: 1, name: 'Урок 1', description: 'Содержание урока', video_link: 'https://super-tube.cc/video/v23189', hours: 2 }
    ];

    const tbody = document.querySelector('#lessons-table tbody');
    tbody.innerHTML = '';

    data.forEach(lesson => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${lesson.id}</td>
            <td>${lesson.name}</td>
            <td>${lesson.description}</td>
            <td>${lesson.video_link || '-'}</td>
            <td>${lesson.hours}</td>
            <td>
                <button onclick="editLesson(${lesson.id})">Редактировать</button>
                <button onclick="deleteLesson(${lesson.id})">Удалить</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

document.getElementById('add-lesson-btn').addEventListener('click', () => {
    document.getElementById('lesson-form-title').textContent = 'Добавить урок';
    document.getElementById('lesson-form').reset();
    document.getElementById('lesson-id').value = '';
    document.getElementById('lesson-course-id').value = currentCourseId;
    showSection('lesson-form-section');
});

// Сохранение урока
document.getElementById('lesson-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    clearErrors();

    const courseId = document.getElementById('lesson-course-id').value;
    // Здесь будет отправка на сервер

    showSection('lessons-section');
    loadLessons(courseId);
});

document.getElementById('cancel-lesson').addEventListener('click', () => showSection('lessons-section'));

document.getElementById('back-to-courses').addEventListener('click', () => showSection('courses-section'));

// Загрузка фильтра курсов для студентов
async function loadStudentCourseFilter() {
    // Симуляция
    const select = document.getElementById('student-course-filter');
    select.innerHTML = '<option value="">Все курсы</option><option value="1">Курс 1</option>';
}

document.getElementById('student-course-filter').addEventListener('change', (e) => {
    loadStudents(e.target.value);
});

// Загрузка студентов (симуляция)
async function loadStudents(courseId = '') {
    // Симуляция
    const data = [
        { email: 'student@example.com', name: 'Иван Иванов', course: 'Курс 1', date: '2026-01-01', payment_status: 'оплачено' }
    ];

    const tbody = document.querySelector('#students-table tbody');
    tbody.innerHTML = '';

    data.forEach(student => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${student.email}</td>
            <td>${student.name}</td>
            <td>${student.course}</td>
            <td>${student.date}</td>
            <td>${student.payment_status}</td>
            <td>
                <button onclick="printCertificate(1, 1)">Распечатать сертификат</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// Пагинация
function renderPagination(pagination, containerId, loadFunction) {
    const div = document.getElementById(containerId);
    div.innerHTML = '';
    for (let i = 1; i <= pagination.total; i++) {
        const a = document.createElement('a');
        a.textContent = i;
        a.href = '#';
        if (i === pagination.current) a.classList.add('active');
        a.addEventListener('click', (e) => {
            e.preventDefault();
            loadFunction(i);
        });
        div.appendChild(a);
    }
}

// Вспомогательные функции
function showSection(sectionId) {
    const sections = ['login-section', 'courses-section', 'course-form-section', 'lessons-section', 'lesson-form-section', 'students-section'];
    sections.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.display = id === sectionId ? 'block' : 'none';
    });

    if (sectionId === 'students-section') loadStudents();
}

function showError(fieldId, message) {
    const input = document.getElementById(fieldId);
    const errorEl = document.getElementById(`${fieldId}-error`);
    if (input) input.classList.add('field-error');
    if (errorEl) errorEl.textContent = message;
}

function clearErrors() {
    document.querySelectorAll('.error').forEach(el => el.textContent = '');
    document.querySelectorAll('input, textarea').forEach(el => el.classList.remove('field-error'));
}

// Заглушка для печати сертификата
window.printCertificate = (studentId, courseId) => {
    alert(`Сертификат для студента ${studentId} на курс ${courseId} сгенерирован. Номер: XXXXXXXXXXX1`);
};

window.printCertificates = (courseId) => {
    alert(`Генерация сертификатов для курса ${courseId}...`);
};