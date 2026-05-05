
function initTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('themeIcon');
    if (!icon) return;

    const saved = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', saved);
    
    if (saved === 'light') {
        icon.classList.replace('fa-moon', 'fa-sun');
    } else {
        icon.classList.replace('fa-sun', 'fa-moon');
    }
}

function toggleTheme() {
    const html = document.documentElement;
    const icon = document.getElementById('themeIcon');
    if (!icon) return;

    let current = html.getAttribute('data-theme');
    let next = current === 'dark' ? 'light' : 'dark';

    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);

    if (next === 'light') {
        icon.classList.replace('fa-moon', 'fa-sun');
    } else {
        icon.classList.replace('fa-sun', 'fa-moon');
    }
}

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    if (menu) {
        menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
    }
}

function logout() {
    alert('已退出登录');
    window.location.href = 'login.html';
}

function goToChat() {
    window.location.href = 'chat.html';
}

function scrollNews(direction) {
    const container = document.getElementById('newsContainer');
    if (container) {
        container.scrollBy({ left: direction * 300, behavior: 'smooth' });
    }
}

window.onload = function () {
    initTheme();
};