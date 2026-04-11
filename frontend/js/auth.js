function toggleAuthMode() {
    const wrapper = document.querySelector('.cards-wrapper');
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    wrapper.classList.toggle('register-mode');
    
    setTimeout(() => {
        loginForm.classList.toggle('hidden');
        registerForm.classList.toggle('hidden');
    }, 300);
}

async function handleLogin(e) {
    e.preventDefault();
    
    const btn = e.target.querySelector('.btn-main');
    const spinner = btn.querySelector('.spinner');
    const btnText = btn.querySelector('span:not(.spinner)');
    
    spinner.style.display = 'inline-block';
    btnText.textContent = '登录中...';
    btn.disabled = true;
    
    try {
        const formData = {
            username: document.getElementById('loginUsername').value,
            password: document.getElementById('loginPassword').value
        };
        
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            currentUser = result;
            localStorage.setItem('token', result.token);
            showToast('登录成功！欢迎回来', 'success');
            switchToMainApp();
        } else {
            showToast(result.detail || '登录失败', 'error');
        }
    } catch (error) {
        showToast('网络错误，请检查后端服务是否启动', 'error');
    } finally {
        spinner.style.display = 'none';
        btnText.textContent = '登录';
        btn.disabled = false;
    }
}

async function handleRegister(e) {
    e.preventDefault();
    
    const password = document.getElementById('regPassword').value;
    const confirm = document.getElementById('regConfirm').value;
    
    if (password !== confirm) {
        showToast('两次密码输入不一致', 'error');
        return;
    }
    
    const btn = e.target.querySelector('.btn-main');
    const spinner = btn.querySelector('.spinner');
    const btnText = btn.querySelector('span:not(.spinner)');
    
    spinner.style.display = 'inline-block';
    btnText.textContent = '注册中...';
    btn.disabled = true;
    
    try {
        const formData = {
            username: document.getElementById('regUsername').value,
            password: password,
            email: document.getElementById('regEmail').value
        };
        
        const response = await fetch(`${API_BASE}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('注册成功！请登录', 'success');
            toggleAuthMode();
        } else {
            showToast(result.detail || '注册失败', 'error');
        }
    } catch (error) {
        showToast('网络错误，请检查后端服务是否启动', 'error');
    } finally {
        spinner.style.display = 'none';
        btnText.textContent = '创建账户';
        btn.disabled = false;
    }
}

function checkAuth() {
    const token = localStorage.getItem('token');
    if (token) {
        currentUser = { username: '用户', token };
        switchToMainApp();
        return true;
    }
    return false;
}

function logout() {
    currentUser = null;
    localStorage.removeItem('token');
    showToast('已安全退出', 'info');
    switchToAuthPage();
}
