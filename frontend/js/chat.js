let chatHistory = [];

function initChat() {
    chatHistory = [];
    addChatMessage('ai', '您好！我是心脏健康助手。您可以向我咨询关于心脏健康的任何问题，比如：\n\n• 如何预防心脏病？\n• 饮食建议\n• 运动指导\n• 症状解读\n\n请问有什么可以帮助您的？');
}

function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    addChatMessage('user', message);
    input.value = '';
    
    const typingId = showTyping();
    
    setTimeout(async () => {
        hideTyping(typingId);
        
        try {
            chatHistory.push({ role: 'user', content: message });
            
            const response = await fetch(`${API_BASE}/chat`, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                },
                body: JSON.stringify({ message, history: chatHistory })
            });
            
            if (response.ok) {
                const data = await response.json();
                addChatMessage('ai', data.response);
                chatHistory.push({ role: 'assistant', content: data.response });
            } else {
                addChatMessage('ai', '抱歉，AI服务暂时不可用，请稍后再试。');
            }
        } catch (error) {
            addChatMessage('ai', '抱歉，发生了一些问题，请稍后再试。');
        }
    }, 1000);
}

function addChatMessage(type, content) {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `message ${type}`;
    
    const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    
    div.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-${type === 'ai' ? 'heartbeat' : 'user'}"></i>
        </div>
        <div>
            <div class="message-content">${content.replace(/\n/g, '<br>')}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

function showTyping() {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'message ai';
    div.id = 'typing-' + Date.now();
    
    div.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-heartbeat"></i>
        </div>
        <div>
            <div class="message-content">
                <div class="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div.id;
}

function hideTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}
