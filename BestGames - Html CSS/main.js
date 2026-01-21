// Открытие/закрытие мобильного меню
const burgerBtn = document.getElementById('burgerBtn');
const mobileMenu = document.getElementById('mobileMenu');

if (burgerBtn && mobileMenu) {
    burgerBtn.addEventListener('click', () => {
        mobileMenu.classList.toggle('active');
        burgerBtn.classList.toggle('active');
    });
}

// Переключение темы
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.querySelector('.theme-toggle__icon');

if (themeToggle) {
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        document.body.classList.toggle('light-theme');
        
        if (document.body.classList.contains('light-theme')) {
            themeIcon.textContent = '☀️';
        } else {
            themeIcon.textContent = '🌙';
        }
    });
}

// Простой слайдер
const slides = document.querySelectorAll('.slider__slide');
const indicators = document.querySelectorAll('.slider__indicator');
const prevBtn = document.querySelector('.slider__btn--prev');
const nextBtn = document.querySelector('.slider__btn--next');

let currentSlide = 0;

function showSlide(index) {
    // Скрываем все слайды
    slides.forEach(slide => slide.classList.remove('slider__slide--active'));
    indicators.forEach(ind => ind.classList.remove('slider__indicator--active'));
    
    // Показываем нужный слайд
    currentSlide = (index + slides.length) % slides.length;
    slides[currentSlide].classList.add('slider__slide--active');
    indicators[currentSlide].classList.add('slider__indicator--active');
    
    // Сдвигаем слайды
    const offset = -currentSlide * 100;
    document.querySelector('.slider__wrapper').style.transform = `translateX(${offset}%)`;
}

// Добавляем обработчики
if (prevBtn && nextBtn) {
    prevBtn.addEventListener('click', () => showSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => showSlide(currentSlide + 1));
}

// Обработчики для индикаторов
indicators.forEach((indicator, index) => {
    indicator.addEventListener('click', () => showSlide(index));
});

// Автопрокрутка слайдера
setInterval(() => {
    showSlide(currentSlide + 1);
}, 5000);