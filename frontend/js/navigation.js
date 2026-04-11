function switchToMainApp() {
    document.getElementById('authPage').style.display = 'none';
    document.getElementById('mainApp').style.display = 'block';
    document.getElementById('userName').textContent = currentUser.username;
    initForm();
    showPage('home');
}

function switchToAuthPage() {
    document.getElementById('authPage').style.display = 'flex';
    document.getElementById('mainApp').style.display = 'none';
}

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    document.querySelectorAll('.nav-item, .mobile-nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    document.getElementById(pageId + 'Page').classList.add('active');
    
    document.querySelectorAll(`.nav-item[data-page="${pageId}"], .mobile-nav-item[data-page="${pageId}"]`).forEach(item => {
        item.classList.add('active');
    });
    
    if (pageId === 'history') {
        loadHistory();
    }
    
    document.querySelector('.mobile-menu').classList.remove('active');
}

function toggleMobileMenu() {
    document.querySelector('.mobile-menu').classList.toggle('active');
}
