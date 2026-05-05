
const API_BASE_URL = 'https://heart-crisis.vip.cpolar.top/api';

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

function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    if (!container) {
        const toastDiv = document.createElement('div');
        toastDiv.id = 'toastContainer';
        toastDiv.style.cssText = 'position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 9999;';
        document.body.appendChild(toastDiv);
    }
    
    const toast = document.createElement('div');
    const bgColor = type === 'success' ? '#27ae60' : type === 'error' ? '#e74c3c' : '#3498db';
    toast.style.cssText = `
        background: ${bgColor};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease;
    `;
    
    const icon = type === 'success' ? '✓' : type === 'error' ? '✕' : 'ℹ';
    toast.innerHTML = `<span style="margin-right: 8px">${icon}</span><span>${message}</span>`;
    
    document.getElementById('toastContainer').appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getCurrentUser() {
    return sessionStorage.getItem('username');
}

function setCurrentUser(username) {
    sessionStorage.setItem('username', username);
}

function logout() {
    sessionStorage.removeItem('username');
    showToast('已退出登录', 'success');
    window.location.href = 'index.html';
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

async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${url}`, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API请求失败:', error);
        throw error;
    }
}

async function login(username, password) {
    return await apiRequest('/login', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
}

async function register(username, password) {
    return await apiRequest('/register', {
        method: 'POST',
        body: JSON.stringify({ username, password })
    });
}

async function getNews() {
    return await apiRequest('/news');
}

async function submitQuestionnaire(data) {
    return await apiRequest('/user/questionnaires/submit', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

async function aiPredict(data) {
    return await apiRequest('/ai-predict', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}

async function getQuestionnaires(username) {
    return await apiRequest(`/questionnaires/user?username=${encodeURIComponent(username)}`);
}

async function getQuestionnaireDetail(questionnaireId) {
    return await apiRequest(`/questionnaires/id?questionnaire_id=${questionnaireId}`);
}

async function getHistoryAnalysis(questionnaireId) {
    return await apiRequest(`/user/history?questionnaire_id=${questionnaireId}`);
}

async function getUserHistoryList(username) {
    return await apiRequest(`/user/history/list?username=${encodeURIComponent(username)}`);
}

async function aiChat(messages, userId) {
    return await apiRequest('/ai/ai-chat', {
        method: 'POST',
        body: JSON.stringify({ messages, user_id: userId })
    });
}

async function uploadMedicalReport(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE_URL}/medical-report/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('上传失败:', error);
        throw error;
    }
}

async function saveMedicalReport(username, medicalData) {
    return await apiRequest('/medical-report/save', {
        method: 'POST',
        body: JSON.stringify({ username, medical_data: medicalData })
    });
}

async function getLatestMedicalReport(username) {
    return await apiRequest(`/medical-report/latest?username=${encodeURIComponent(username)}`);
}

function updateUserDisplay() {
    const username = getCurrentUser();
    const userDisplay = document.getElementById('currentUser');
    const userAvatar = document.getElementById('userAvatar');
    
    if (userDisplay && username) {
        userDisplay.textContent = username;
    }
    if (userAvatar && username) {
        userAvatar.textContent = username.charAt(0).toUpperCase();
    }
}

window.onload = function () {
    initTheme();
    updateUserDisplay();
};