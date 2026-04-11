const API_BASE = 'http://localhost:8000';
let currentUsername = '';

const formFields = [
    { name: 'heart_disease', label: '心脏病史', type: 'select', options: ['No', 'Yes'] },
    { name: 'bmi', label: 'BMI指数', type: 'number', step: '0.1', placeholder: '24.5' },
    { name: 'smoking', label: '吸烟', type: 'select', options: ['No', 'Yes'] },
    { name: 'alcohol_drinking', label: '饮酒', type: 'select', options: ['No', 'Yes'] },
    { name: 'stroke', label: '中风史', type: 'select', options: ['No', 'Yes'] },
    { name: 'physical_health', label: '身体不适天数(30天内)', type: 'number', min: 0, max: 30, placeholder: '0' },
    { name: 'mental_health', label: '心理不适天数(30天内)', type: 'number', min: 0, max: 30, placeholder: '0' },
    { name: 'diff_walking', label: '行走困难', type: 'select', options: ['No', 'Yes'] },
    { name: 'sex', label: '性别', type: 'select', options: ['男', '女'] },
    { name: 'age_category', label: '年龄组', type: 'select', options: ['18-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80+'] },
    { name: 'race', label: '种族', type: 'select', options: ['白人', '黑人', '亚洲人', '西班牙裔', '其他'] },
    { name: 'diabetic', label: '糖尿病', type: 'select', options: ['No', 'Yes'] },
    { name: 'physical_activity', label: '规律运动', type: 'select', options: ['No', 'Yes'] },
    { name: 'gen_health', label: '健康自评', type: 'select', options: ['优秀', '很好', '好', '一般', '差'] },
    { name: 'sleep_time', label: '睡眠时间(小时)', type: 'number', min: 0, max: 24, placeholder: '7' },
    { name: 'asthma', label: '哮喘', type: 'select', options: ['No', 'Yes'] },
    { name: 'kidney_disease', label: '肾病', type: 'select', options: ['No', 'Yes'] },
    { name: 'skin_cancer', label: '皮肤癌', type: 'select', options: ['No', 'Yes'] }
];

// 新闻数据 - 现在从API获取
let currentNewsStart = 1;
let currentNewsEnd = 2;
let isLoadingNews = false;

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    checkLogin();
    initNews();
    initForms();
});

// 切换移动端菜单
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    mobileMenu.classList.toggle('active');
}

// 主题切换
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme');
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    updateThemeIcon(next);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    icon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// 检查登录状态
function checkLogin() {
    const username = sessionStorage.getItem('username');
    if (username) {
        currentUsername = username;
        document.getElementById('currentUser').textContent = username;
        document.getElementById('userAvatar').textContent = username.charAt(0).toUpperCase();
    } else {
        // 未登录，重定向到登录页面
        window.location.href = 'login.html';
    }
}

function logout() {
    sessionStorage.removeItem('username');
    currentUsername = '';
    window.location.href = 'login.html';
}

// Toast提示
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? 'fa-check-circle' : type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle';
    toast.innerHTML = `<i class="fas ${icon}"></i><span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px) translateX(-50%)';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// 页面切换
function switchPage(page) {
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));

    // 激活对应导航
    document.querySelectorAll('.nav-item').forEach(item => {
        if (item.getAttribute('onclick')?.includes(`'${page}'`)) {
            item.classList.add('active');
        }
    });

    document.getElementById(`page-${page}`).classList.add('active');

    if (page === 'history') loadHistory();
}

// 加载新闻数据
async function loadNews() {
    // 检查登录状态，未登录时不加载新闻
    if (!currentUsername) {
        const container = document.getElementById('newsContainer');
        container.innerHTML = '<div class="empty-state"><i class="fas fa-lock"></i><p>请先登录查看新闻</p></div>';
        return;
    }
    
    if (isLoadingNews) return;
    
    isLoadingNews = true;
    const container = document.getElementById('newsContainer');
    container.innerHTML = '<div class="empty-state"><i class="fas fa-spinner fa-spin"></i><p>加载中...</p></div>';
    try {
        const res = await fetch(`${API_BASE}/api/news`);
        const result = await res.json();

        if (result.code === 200 && result.data) {
            container.innerHTML = '';
            const articles = result.data;

            articles.forEach((article, index) => {
                const item = document.createElement('div');
                item.className = 'news-item';
                
                // 统一使用"新闻资讯"标签
                const tag = '新闻资讯';
                
                // 使用文章的实际发布时间
                const date = article.publish_time || new Date().toISOString().split('T')[0];

                // 先设置innerHTML，使用img标签来显示图片
                item.innerHTML = `
                    <div class="news-thumb">
                        <span class="news-tag">${tag}</span>
                        ${article.image_url ? `<img src="http://localhost:8000/api/proxy/image?url=${encodeURIComponent(article.image_url)}" alt="${article.title}" class="news-image">` : '<div class="news-image-placeholder"><i class="fas fa-image"></i></div>'}
                    </div>
                    <div class="news-content">
                        <div class="news-meta">${date}</div>
                        <h3 class="news-headline">${article.title}</h3>
                        <p class="news-excerpt">${article.content || '暂无摘要'}</p>
                    </div>
                `;

                // 处理图片加载
                if (article.image_url) {
                    console.log('尝试加载图片:', article.image_url);
                    console.log('使用代理加载:', `http://localhost:8000/api/proxy/image?url=${encodeURIComponent(article.image_url)}`);
                    const img = item.querySelector('.news-image');
                    if (img) {
                        img.onload = function() {
                            console.log('图片加载成功');
                        };
                        
                        img.onerror = function() {
                            console.error('图片加载失败，显示默认图片');
                            // 替换为默认图片
                            const placeholder = document.createElement('div');
                            placeholder.className = 'news-image-placeholder';
                            placeholder.innerHTML = '<i class="fas fa-image"></i>';
                            img.parentElement.replaceChild(placeholder, img);
                        };
                    }
                }

                // 添加点击事件，在新窗口打开链接
                item.style.cursor = 'pointer';
                item.addEventListener('click', function() {
                    window.open(article.url, '_blank');
                });
                container.appendChild(item);
            });
        } else {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>加载失败，请重试</p></div>';
        }
    } catch (err) {
        // 根据错误类型判断是网络错误还是服务器异常
        const errorMessage = err.message || '';
        if (errorMessage.includes('ECONNREFUSED') || errorMessage.includes('connect') || errorMessage.includes('Server')) {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>服务器异常，请稍后重试</p></div>';
        } else {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>网络错误，请检查网络连接</p></div>';
        }
        console.error('News load error:', err);
    } finally {
        isLoadingNews = false;
    }
}

// 初始化新闻
async function initNews() {
    await loadNews();
}

// 刷新新闻
function refreshNews() {
    loadNews();
}

// 滚动新闻
function scrollNews(direction) {
    // 这里可以添加新闻滚动逻辑
    console.log('滚动新闻:', direction);
}

// 上传体检报告
function uploadReport() {
    const fileInput = document.getElementById('reportFile');
    const file = fileInput.files[0];
    
    if (!file) {
        showToast('请选择要上传的文件', 'error');
        return;
    }
    
    // 模拟上传过程
    showToast('正在上传报告...', 'info');
    
    setTimeout(() => {
        showToast('报告上传成功！', 'success');
        
        // 更新报告列表
        const reportList = document.getElementById('reportList');
        reportList.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: space-between; padding: 16px; background: var(--bg-card); border: 1px solid var(--border); border-radius: 12px;">
                <div>
                    <div style="font-weight: 500; margin-bottom: 4px;">${file.name}</div>
                    <div style="font-size: 12px; color: var(--text-secondary);">上传时间: ${new Date().toLocaleString()}</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <button class="btn-icon" title="查看">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="btn-icon" title="删除">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        `;
        
        // 清空文件输入
        fileInput.value = '';
    }, 1500);
}

// 初始化表单
function initForms() {
    const surveyGrid = document.getElementById('surveyGrid');
    const riskGrid = document.getElementById('riskGrid');

    surveyGrid.innerHTML = '';
    riskGrid.innerHTML = '';

    formFields.forEach(field => {
        surveyGrid.appendChild(createField(field, 'survey'));
        riskGrid.appendChild(createField(field, 'risk'));
    });
}

function createField(field, prefix) {
    const div = document.createElement('div');
    div.className = 'form-group';

    const label = document.createElement('label');
    label.textContent = field.label;
    div.appendChild(label);

    let input;
    if (field.type === 'select') {
        input = document.createElement('select');
        input.name = field.name;
        input.id = `${prefix}_${field.name}`;
        field.options.forEach(opt => {
            const option = document.createElement('option');
            option.value = opt;
            option.textContent = opt === 'Yes' ? '是' : opt === 'No' ? '否' : opt;
            input.appendChild(option);
        });
    } else {
        input = document.createElement('input');
        input.type = 'number';
        input.name = field.name;
        input.id = `${prefix}_${field.name}`;
        if (field.step) input.step = field.step;
        if (field.min !== undefined) input.min = field.min;
        if (field.max !== undefined) input.max = field.max;
        if (field.placeholder) input.placeholder = field.placeholder;
    }

    input.required = true;
    div.appendChild(input);
    return div;
}

// 收集表单数据
function collectData(prefix) {
    const data = {};
    formFields.forEach(field => {
        const el = document.getElementById(`${prefix}_${field.name}`);
        data[field.name] = el.value;
    });
    
    // 映射中文选项到英文值
    if (data.sex === '男') data.sex = 'Male';
    if (data.sex === '女') data.sex = 'Female';
    
    if (data.race === '白人') data.race = 'White';
    if (data.race === '黑人') data.race = 'Black';
    if (data.race === '亚洲人') data.race = 'Asian';
    if (data.race === '西班牙裔') data.race = 'Hispanic';
    if (data.race === '其他') data.race = 'Other';
    
    if (data.gen_health === '优秀') data.gen_health = 'Excellent';
    if (data.gen_health === '很好') data.gen_health = 'Very good';
    if (data.gen_health === '好') data.gen_health = 'Good';
    if (data.gen_health === '一般') data.gen_health = 'Fair';
    if (data.gen_health === '差') data.gen_health = 'Poor';
    
    return data;
}

// 提交健康数据
async function handleSurveySubmit(e) {
    e.preventDefault();
    const btn = document.getElementById('surveyBtn');
    const data = collectData('survey');
    data.username = currentUsername;

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div> 保存中...';

    try {
        const res = await fetch(`${API_BASE}/api/user/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();

        if (result.code === 200) {
            showToast('数据保存成功', 'success');
            document.getElementById('surveyForm').reset();
        } else {
            showToast(result.message || '保存失败', 'error');
        }
    } catch (err) {
        showToast('保存失败，请检查网络', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-save"></i> 保存数据';
    }
}

// AI预测
async function handleRiskPredict(e) {
    e.preventDefault();
    const btn = document.getElementById('riskBtn');
    const resultPanel = document.getElementById('predictResult');
    const data = collectData('risk');
    data.username = currentUsername;

    btn.disabled = true;
    btn.innerHTML = '<div class="spinner"></div> 分析中...';
    resultPanel.classList.remove('show');

    try {
        const res = await fetch(`${API_BASE}/api/ai-predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await res.json();

        if (result.code === 200) {
            showResult(result.data);
            showToast('预测完成', 'success');
        } else {
            showToast(result.message || '预测失败', 'error');
        }
    } catch (err) {
        // 根据错误类型判断是网络错误还是服务器异常
        const errorMessage = err.message || '';
        if (errorMessage.includes('ECONNREFUSED') || errorMessage.includes('connect') || errorMessage.includes('Server')) {
            showToast('服务器异常，请稍后重试', 'error');
        } else {
            showToast('网络错误，请检查网络连接', 'error');
        }
    } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic"></i> 开始预测';
    }
}

// 显示预测结果
function showResult(data) {
    const resultPanel = document.getElementById('predictResult');
    const riskScore = document.getElementById('riskScore');
    const riskPercent = document.getElementById('riskPercent');
    const riskDesc = document.getElementById('riskDesc');
    const riskBadge = document.getElementById('riskBadge');

    // 提取风险百分比数值
    const percentText = data.heart_disease_risk || '0%';
    // 确保只显示一个百分号
    const cleanedPercentText = percentText.replace(/%+$/, '%');
    // 提取纯数字用于计算
    const percent = parseInt(cleanedPercentText.replace('%', ''));
    
    riskScore.style.setProperty('--percent', percent);
    riskPercent.textContent = cleanedPercentText;

    let riskLevel, badgeClass, desc;
    if (percent < 15) {
        riskLevel = '低风险';
        badgeClass = 'badge-low';
        desc = '您的心脏健康状况良好，请继续保持健康的生活方式。';
    } else if (percent < 40) {
        riskLevel = '中等风险';
        badgeClass = 'badge-medium';
        desc = '您有一定的心脏病风险，建议调整生活方式并定期检查。';
    } else {
        riskLevel = '高风险';
        badgeClass = 'badge-high';
        desc = '您的心脏病风险较高，建议立即咨询医生并采取预防措施。';
    }

    riskBadge.textContent = riskLevel;
    riskBadge.className = `risk-badge ${badgeClass}`;
    riskDesc.textContent = desc;

    // 显示详细分析和建议
    let analysisHTML = '';
    if (data.analysis) {
        analysisHTML += `
            <div class="analysis-section">
                <h4>风险分析</h4>
                <p>${data.analysis}</p>
            </div>
        `;
    }
    
    if (data.suggestions) {
        analysisHTML += `
            <div class="analysis-section">
                <h4>健康建议</h4>
                <p>${data.suggestions}</p>
            </div>
        `;
    }
    
    // 检查是否已存在分析区域
    let analysisContainer = resultPanel.querySelector('.analysis-container');
    if (!analysisContainer) {
        analysisContainer = document.createElement('div');
        analysisContainer.className = 'analysis-container';
        resultPanel.appendChild(analysisContainer);
    }
    
    analysisContainer.innerHTML = analysisHTML;

    resultPanel.classList.add('show');
}

// 加载历史记录
async function loadHistory() {
    const container = document.getElementById('historyTableWrap');
    container.innerHTML = '<div class="empty-state"><i class="fas fa-spinner fa-spin"></i><p>加载中...</p></div>';

    try {
        const res = await fetch(`${API_BASE}/api/user/history-list?username=${currentUsername}`);
        const result = await res.json();

        if (result.code === 200 && result.data && result.data.length > 0) {
            renderHistoryTable(result.data);
        } else {
            container.innerHTML = '<div class="empty-state"><i class="fas fa-inbox"></i><p>暂无历史记录</p></div>';
        }
    } catch (err) {
        container.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-circle"></i><p>加载失败，请重试</p></div>';
    }
}

function renderHistoryTable(data) {
    const container = document.getElementById('historyTableWrap');
    const headers = ['时间', 'BMI', '吸烟', '饮酒', '运动', '睡眠', '心脏病史', '中风', '糖尿病', '哮喘', '肾病', '皮肤癌'];

    let html = '<table><thead><tr>';
    headers.forEach(h => html += `<th>${h}</th>`);
    html += '</tr></thead><tbody>';

    data.slice(0, 10).forEach(row => {
        // 处理时间字段，防止显示Invalid Date
        let dateStr = '未知时间';
        if (row.created_at) {
            const date = new Date(row.created_at);
            if (!isNaN(date.getTime())) {
                dateStr = date.toLocaleDateString();
            }
        }
        
        html += `<tr onclick="loadHistoryAnalysis(${row.id})" style="cursor: pointer;">
            <td>${dateStr}</td>
            <td>${row.bmi}</td>
            <td>${row.smoking === 'Yes' ? '是' : '否'}</td>
            <td>${row.alcohol_drinking === 'Yes' ? '是' : '否'}</td>
            <td>${row.physical_activity === 'Yes' ? '是' : '否'}</td>
            <td>${row.sleep_time}小时</td>
            <td>${row.heart_disease === 'Yes' ? '是' : '否'}</td>
            <td>${row.stroke === 'Yes' ? '是' : '否'}</td>
            <td>${row.diabetic === 'Yes' ? '是' : '否'}</td>
            <td>${row.asthma === 'Yes' ? '是' : '否'}</td>
            <td>${row.kidney_disease === 'Yes' ? '是' : '否'}</td>
            <td>${row.skin_cancer === 'Yes' ? '是' : '否'}</td>
        </tr>`;
    });

    html += '</tbody></table>';
    container.innerHTML = html;
}

// 加载历史分析结果
async function loadHistoryAnalysis(userHealthId) {
    const resultPanel = document.getElementById('historyAnalysisResult');
    resultPanel.style.display = 'block';
    resultPanel.classList.remove('show');
    
    // 显示加载状态
    document.getElementById('historyRiskPercent').textContent = '加载中...';
    document.getElementById('historyRiskDesc').textContent = '正在获取分析结果...';
    document.getElementById('historyRiskBadge').textContent = '加载中';
    document.getElementById('historyRiskBadge').className = 'risk-badge';
    
    // 清空之前的分析内容
    let analysisContainer = resultPanel.querySelector('.analysis-container');
    if (analysisContainer) {
        analysisContainer.innerHTML = '';
    }
    
    try {
        const res = await fetch(`${API_BASE}/api/user/history-analysis?user_health_id=${userHealthId}`);
        const result = await res.json();

        // 检查响应体中的code字段
        if (result.code === 404) {
            showToast('该记录未进行AI分析', 'warning');
            resultPanel.style.display = 'none';
            return;
        } else if (result.code === 500) {
            showToast('获取分析结果异常', 'error');
            resultPanel.style.display = 'none';
            return;
        } else if (result.code === 200 && result.data) {
            showHistoryResult(result.data);
        } else {
            showToast('获取分析结果失败', 'error');
            resultPanel.style.display = 'none';
        }
    } catch (err) {
        showToast('获取分析结果失败，请检查网络', 'error');
        resultPanel.style.display = 'none';
    }
}

// 显示历史分析结果
function showHistoryResult(data) {
    const resultPanel = document.getElementById('historyAnalysisResult');
    const riskScore = document.getElementById('historyRiskScore');
    const riskPercent = document.getElementById('historyRiskPercent');
    const riskDesc = document.getElementById('historyRiskDesc');
    const riskBadge = document.getElementById('historyRiskBadge');

    // 提取风险百分比数值
    const percentText = data.heart_disease_risk || '0%';
    // 确保只显示一个百分号
    const cleanedPercentText = percentText.replace(/%+$/, '%');
    // 提取纯数字用于计算
    const percent = parseInt(cleanedPercentText.replace('%', ''));
    
    riskScore.style.setProperty('--percent', percent);
    riskPercent.textContent = cleanedPercentText;

    let riskLevel, badgeClass, desc;
    if (percent < 15) {
        riskLevel = '低风险';
        badgeClass = 'badge-low';
        desc = '您的心脏健康状况良好，请继续保持健康的生活方式。';
    } else if (percent < 40) {
        riskLevel = '中等风险';
        badgeClass = 'badge-medium';
        desc = '您有一定的心脏病风险，建议调整生活方式并定期检查。';
    } else {
        riskLevel = '高风险';
        badgeClass = 'badge-high';
        desc = '您的心脏病风险较高，建议立即咨询医生并采取预防措施。';
    }

    riskBadge.textContent = riskLevel;
    riskBadge.className = `risk-badge ${badgeClass}`;
    riskDesc.textContent = desc;

    // 显示详细分析和建议
    let analysisHTML = '';
    if (data.analysis) {
        analysisHTML += `
            <div class="analysis-section">
                <h4>风险分析</h4>
                <p>${data.analysis}</p>
            </div>
        `;
    }
    
    if (data.suggestions) {
        analysisHTML += `
            <div class="analysis-section">
                <h4>健康建议</h4>
                <p>${data.suggestions}</p>
            </div>
        `;
    }
    
    // 检查是否已存在分析区域
    let analysisContainer = resultPanel.querySelector('.analysis-container');
    if (!analysisContainer) {
        analysisContainer = document.createElement('div');
        analysisContainer.className = 'analysis-container';
        resultPanel.appendChild(analysisContainer);
    }
    
    analysisContainer.innerHTML = analysisHTML;

    resultPanel.classList.add('show');
}

// AI聊天相关
let chatMessages = [];

function handleChatKeydown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendChatMessage();
    }
}

function sendQuickMessage(message) {
    document.getElementById('chatInput').value = message;
    sendChatMessage();
}

function addMessageToUI(role, content) {
    const messagesContainer = document.getElementById('chatMessages');
    const welcomeEl = document.getElementById('chatWelcome');
    
    if (welcomeEl) {
        welcomeEl.style.display = 'none';
    }

    // 显示聊天消息容器，隐藏滚动条
    messagesContainer.style.display = 'flex';
    messagesContainer.style.flexDirection = 'column';
    messagesContainer.style.gap = '16px';
    messagesContainer.style.flex = '1';
    messagesContainer.style.overflowY = 'auto';
    messagesContainer.style.padding = '24px';
    messagesContainer.style.scrollbarWidth = 'none'; // Firefox
    messagesContainer.style.msOverflowStyle = 'none'; // IE/Edge
    messagesContainer.style.overflowX = 'hidden';

    // 隐藏滚动条 (Chrome, Safari, Opera)
    messagesContainer.style.WebkitOverflowScrolling = 'touch';
    messagesContainer.style.background = 'var(--bg-primary)';

    // 添加CSS来隐藏滚动条
    const style = document.createElement('style');
    style.textContent = `
        .chat-messages::-webkit-scrollbar {
            display: none !important;
        }
        .chat-messages::-webkit-scrollbar-track {
            display: none !important;
        }
        .chat-messages::-webkit-scrollbar-thumb {
            display: none !important;
        }
        .chat-messages {
            -ms-overflow-style: none !important;
            scrollbar-width: none !important;
        }
    `;
    document.head.appendChild(style);

    const messageEl = document.createElement('div');
    messageEl.className = `message ${role}`;
    messageEl.style.maxWidth = '80%';
    messageEl.style.padding = '16px 20px';
    messageEl.style.borderRadius = '18px';
    messageEl.style.fontSize = '15px';
    messageEl.style.lineHeight = '1.6';
    messageEl.style.wordWrap = 'break-word';
    
    if (role === 'assistant') {
        messageEl.style.alignSelf = 'flex-start';
        messageEl.style.background = 'var(--bg-card)';
        messageEl.style.color = 'var(--text-primary)';
        messageEl.style.borderBottomLeftRadius = '6px';
        messageEl.innerHTML = formatMessage(content);
    } else {
        messageEl.style.alignSelf = 'flex-end';
        messageEl.style.background = 'var(--accent)';
        messageEl.style.color = 'white';
        messageEl.style.borderBottomRightRadius = '6px';
        messageEl.textContent = content;
    }
    
    messagesContainer.appendChild(messageEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function addLoadingMessage() {
    const messagesContainer = document.getElementById('chatMessages');
    const loadingEl = document.createElement('div');
    loadingEl.className = 'message assistant loading';
    loadingEl.id = 'loadingMessage';
    loadingEl.innerHTML = '<span></span><span></span><span></span>';
    messagesContainer.appendChild(loadingEl);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function removeLoadingMessage() {
    const loadingEl = document.getElementById('loadingMessage');
    if (loadingEl) {
        loadingEl.remove();
    }
}

function formatMessage(content) {
    return content
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSendBtn');
    const message = input.value.trim();

    if (!message) return;

    input.value = '';
    input.style.height = 'auto';
    sendBtn.disabled = true;

    chatMessages.push({ role: 'user', content: message });
    addMessageToUI('user', message);
    addLoadingMessage();

    try {
        const res = await fetch(`${API_BASE}/api/ai/ai-chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                messages: chatMessages,
                user_id: currentUsername
            })
        });

        const result = await res.json();
        removeLoadingMessage();

        if (result.code === 200 && result.data && result.data.response) {
            const assistantMessage = result.data.response;
            chatMessages.push({ role: 'assistant', content: assistantMessage });
            addMessageToUI('assistant', assistantMessage);
        } else {
            addMessageToUI('assistant', '抱歉，服务暂时不可用，请稍后再试。');
        }
    } catch (err) {
        removeLoadingMessage();
        // 根据错误类型判断是网络错误还是服务器异常
        const errorMessage = err.message || '';
        if (errorMessage.includes('ECONNREFUSED') || errorMessage.includes('connect') || errorMessage.includes('Server')) {
            addMessageToUI('assistant', '服务器异常，请稍后重试。');
        } else {
            addMessageToUI('assistant', '网络错误，请检查网络连接后重试。');
        }
        console.error('Chat error:', err);
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}

// 自动调整输入框高度
document.getElementById('chatInput').addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
});