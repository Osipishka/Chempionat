// Переключение темы
const themeToggle = document.getElementById('themeToggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeToggle.textContent = '☀️';
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeToggle.textContent = '🌙';
    }
});

// Бургер меню
const burgerBtn = document.getElementById('burgerBtn');
const mobileNav = document.getElementById('mobileNav');

burgerBtn.addEventListener('click', () => {
    mobileNav.classList.toggle('active');
    burgerBtn.classList.toggle('active');
});

// Слайдер
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const indicators = document.querySelectorAll('.indicator');
const prevBtn = document.querySelector('.prev');
const nextBtn = document.querySelector('.next');

function showSlide(n) {
    slides.forEach(slide => slide.classList.remove('active'));
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    currentSlide = (n + slides.length) % slides.length;
    
    slides[currentSlide].classList.add('active');
    indicators[currentSlide].classList.add('active');
    
    const offset = -currentSlide * 100;
    document.querySelector('.slides').style.transform = `translateX(${offset}%)`;
}

prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));

// Автопрокрутка слайдера
setInterval(() => showSlide(currentSlide + 1), 5000);

// Подсказки поиска
const genreSearch = document.getElementById('genreSearch');
const suggestions = document.getElementById('suggestions');

const genres = [
    'Экшен', 'Ролевая игра', 'Стратегия', 'Симулятор', 
    'Приключение', 'Гонки', 'Спорт', 'Хоррор'
];

genreSearch.addEventListener('input', function() {
    const value = this.value.toLowerCase();
    suggestions.innerHTML = '';
    
    if (value) {
        const filtered = genres.filter(genre => 
            genre.toLowerCase().includes(value)
        );
        
        filtered.forEach(genre => {
            const div = document.createElement('div');
            div.textContent = genre;
            div.className = 'suggestion-item';
            div.addEventListener('click', () => {
                genreSearch.value = genre;
                suggestions.innerHTML = '';
            });
            suggestions.appendChild(div);
        });
    }
});