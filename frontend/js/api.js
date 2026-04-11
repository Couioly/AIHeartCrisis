async function submitHealthData() {
    try {
        const formData = getFormData();
        const response = await fetch(`${API_BASE}/submit`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('数据提交成功！', 'success');
            predictRisk(result.record_id);
        } else {
            showToast(result.detail || '提交失败', 'error');
        }
    } catch (error) {
        showToast('网络错误', 'error');
    }
}

async function predictRisk(recordId) {
    try {
        const response = await fetch(`${API_BASE}/predict/${recordId}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult(result);
        } else {
            showToast(result.detail || '预测失败', 'error');
        }
    } catch (error) {
        showToast('网络错误', 'error');
    }
}

function displayResult(result) {
    const panel = document.getElementById('resultPanel');
    const score = result.risk_score * 100;
    
    document.getElementById('riskScore').style.setProperty('--percent', score);
    document.getElementById('riskValue').textContent = Math.round(score) + '%';
    
    const riskLabel = document.getElementById('riskLabel');
    const badge = document.getElementById('riskBadge');
    let level = '', badgeClass = '';
    
    if (score < 33) {
        level = '低风险';
        badgeClass = 'badge-low';
    } else if (score < 66) {
        level = '中等风险';
        badgeClass = 'badge-medium';
    } else {
        level = '高风险';
        badgeClass = 'badge-high';
    }
    
    riskLabel.textContent = level;
    badge.textContent = level;
    badge.className = `risk-badge ${badgeClass}`;
    
    let detailedAnalysis = '';
    if (result.detailed_analysis) {
        for (const [key, value] of Object.entries(result.detailed_analysis)) {
            const fieldName = fieldMapping[key] || key;
            detailedAnalysis += `<strong>${fieldName}:</strong> ${value}<br>`;
        }
    }
    
    document.getElementById('analysisText').innerHTML = result.analysis || '暂无详细分析';
    if (detailedAnalysis) {
        document.getElementById('detailedAnalysisText').innerHTML = detailedAnalysis;
        document.getElementById('detailedAnalysisSection').style.display = 'block';
    }
    document.getElementById('recommendationText').textContent = result.recommendations || '暂无建议';
    document.getElementById('doubaoAnalysisText').textContent = result.doubao_analysis || 'AI深度分析中...';
    
    panel.classList.add('show');
}

async function loadHistory() {
    const tbody = document.getElementById('historyBody');
    try {
        const response = await fetch(`${API_BASE}/history`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        if (!response.ok) {
            if (response.status === 401) {
                showToast('请先登录', 'error');
                return;
            }
            throw new Error('获取历史记录失败');
        }
        
        const history = await response.json();
        
        if (history.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="empty-state" style="text-align: center;">
                        <div style="padding: 40px; color: var(--text-secondary);">
                            <i class="fas fa-history" style="font-size: 48px; opacity: 0.3; margin-bottom: 16px;"></i>
                            <div>暂无历史记录</div>
                        </div>
                    </td>
                </tr>
            `;
            return;
        }
        
        tbody.innerHTML = history.map(item => {
            const score = Math.round((item.risk_score || 0) * 100);
            const badgeClass = score < 33 ? 'badge-low' : score < 66 ? 'badge-medium' : 'badge-high';
            const level = score < 33 ? '低' : score < 66 ? '中' : '高';
            
            return `
                <tr>
                    <td>${formatDate(item.created_at)}</td>
                    <td><span class="risk-badge ${badgeClass}">${level}</span></td>
                    <td>${score}%</td>
                    <td>${item.age || '-'}岁</td>
                    <td>${item.sex === '1' ? '男' : '女'}</td>
                    <td>
                        <button class="btn-icon" onclick="viewRecord(${item.id})" title="查看详情">
                            <i class="fas fa-eye"></i>
                        </button>
                        <button class="btn-icon" onclick="deleteRecord(${item.id})" title="删除" style="color: var(--error);">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        showToast(error.message || '加载失败', 'error');
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="empty-state" style="text-align: center;">
                    <div style="padding: 40px; color: var(--text-secondary);">
                        <i class="fas fa-exclamation-circle" style="font-size: 48px; opacity: 0.3; margin-bottom: 16px;"></i>
                        <div>加载失败</div>
                    </div>
                </td>
            </tr>
        `;
    }
}

async function viewRecord(id) {
    try {
        const response = await fetch(`${API_BASE}/record/${id}`, {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        if (!response.ok) throw new Error('获取记录失败');
        
        const record = await response.json();
        
        let content = '';
        
        for (const [key, value] of Object.entries(record)) {
            const fieldName = fieldMapping[key] || key;
            let displayValue = value;
            
            if (key === 'sex') displayValue = value === '1' ? '男' : '女';
            if (key === 'risk_score') displayValue = Math.round(value * 100) + '%';
            
            content += `<strong>${fieldName}:</strong> ${displayValue}<br>`;
        }
        
        showToast('查看详情功能开发中', 'info');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function deleteRecord(id) {
    if (!confirm('确定要删除这条记录吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE}/record/${id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        
        if (!response.ok) throw new Error('删除失败');
        
        showToast('删除成功', 'success');
        loadHistory();
    } catch (error) {
        showToast(error.message, 'error');
    }
}
