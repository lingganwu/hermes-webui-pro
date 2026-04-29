/**
 * Hermes WebUI Pro - Application Logic
 * Premium AI Agent Dashboard
 */

// State Management
const state = {
    currentPage: 'dashboard',
    messages: [],
    soultrace: {
        answers: [],
        currentQuestion: 0,
        totalQuestions: 10,
        isActive: false,
        result: null
    },
    metrics: {
        sessions: 0,
        messages: 0,
        models: 0,
        uptime: 0
    },
    ws: null
};

// API Configuration
const API_BASE = window.location.origin;
const WS_URL = `ws://${window.location.hostname}:8765`;

// Initialize WebSocket
function initWebSocket() {
    try {
        state.ws = new WebSocket(WS_URL);
        
        state.ws.onopen = () => {
            console.log('WebSocket connected');
            showToast('Connected to gateway', 'success');
        };
        
        state.ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            } catch (e) {
                console.error('WebSocket message error:', e);
            }
        };
        
        state.ws.onclose = () => {
            console.log('WebSocket disconnected');
            setTimeout(initWebSocket, 5000);
        };
        
        state.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };
    } catch (e) {
        console.log('WebSocket not available, using REST API');
    }
}

// Handle WebSocket Messages
function handleWebSocketMessage(data) {
    switch (data.type) {
        case 'metrics':
            updateMetrics(data.payload);
            break;
        case 'chat_response':
            appendMessage(data.payload, 'assistant');
            hideTypingIndicator();
            break;
        case 'soultrace_update':
            handleSoultraceUpdate(data.payload);
            break;
    }
}

// Page Navigation
function showPage(pageName) {
    state.currentPage = pageName;
    
    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === pageName) {
            item.classList.add('active');
        }
    });
    
    // Show/hide pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    const targetPage = document.getElementById(`page-${pageName}`);
    if (targetPage) {
        targetPage.classList.add('active');
        targetPage.style.animation = 'none';
        targetPage.offsetHeight; // Trigger reflow
        targetPage.style.animation = null;
    }
    
    // Load page-specific data
    if (pageName === 'dashboard') {
        fetchMetrics();
    }
}

// Dashboard Functions
async function fetchMetrics() {
    try {
        const response = await fetch(`${API_BASE}/api/metrics`);
        if (response.ok) {
            const data = await response.json();
            updateMetrics(data);
        } else {
            // Use mock data for demo
            updateMetrics({
                sessions: 42,
                messages: 1337,
                models: 4,
                uptime: '12h 34m',
                cpu: 23,
                memory: { used: 4.2, total: 16 },
                disk: { used: 128, total: 512 }
            });
        }
    } catch (e) {
        // Use mock data for demo
        updateMetrics({
            sessions: 42,
            messages: 1337,
            models: 4,
            uptime: '12h 34m',
            cpu: 23,
            memory: { used: 4.2, total: 16 },
            disk: { used: 128, total: 512 }
        });
    }
}

function updateMetrics(data) {
    // Update stat cards with animation
    animateCounter('stat-sessions', data.sessions || 0);
    animateCounter('stat-messages', data.messages || 0);
    animateCounter('stat-models', data.models || 0);
    
    const uptimeEl = document.getElementById('stat-uptime');
    if (uptimeEl) {
        uptimeEl.textContent = data.uptime || '0h';
    }
    
    // Update system metrics
    if (data.cpu !== undefined) {
        const cpuValue = document.getElementById('cpu-value');
        const cpuBar = document.getElementById('cpu-bar');
        if (cpuValue) cpuValue.textContent = `${data.cpu}%`;
        if (cpuBar) cpuBar.style.width = `${data.cpu}%`;
    }
    
    if (data.memory) {
        const memPercent = (data.memory.used / data.memory.total * 100).toFixed(0);
        const memValue = document.getElementById('memory-value');
        const memBar = document.getElementById('memory-bar');
        if (memValue) memValue.textContent = `${data.memory.used} GB / ${data.memory.total} GB`;
        if (memBar) memBar.style.width = `${memPercent}%`;
    }
    
    if (data.disk) {
        const diskPercent = (data.disk.used / data.disk.total * 100).toFixed(0);
        const diskValue = document.getElementById('disk-value');
        const diskBar = document.getElementById('disk-bar');
        if (diskValue) diskValue.textContent = `${data.disk.used} GB / ${data.disk.total} GB`;
        if (diskBar) diskBar.style.width = `${diskPercent}%`;
    }
}

function animateCounter(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const start = parseInt(element.textContent) || 0;
    const duration = 1000;
    const startTime = performance.now();
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.round(start + (targetValue - start) * easeOut);
        
        element.textContent = current.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
}

// Chat Functions
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    appendMessage(message, 'user');
    input.value = '';
    input.style.height = 'auto';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                history: state.messages.slice(-10)
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            appendMessage(data.response, 'assistant');
        } else {
            // Simulate response for demo
            setTimeout(() => {
                appendMessage("I'm Hermes, your AI assistant. This is a demo response. Connect to the backend API for full functionality.", 'assistant');
            }, 1500);
        }
    } catch (e) {
        // Simulate response for demo
        setTimeout(() => {
            appendMessage("I'm Hermes, your AI assistant. This is a demo response. Connect to the backend API for full functionality.", 'assistant');
        }, 1500);
    }
    
    hideTypingIndicator();
}

function appendMessage(text, role) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const senderName = role === 'user' ? 'You' : 'Hermes';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                ${role === 'user' 
                    ? '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>'
                    : '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>'
                }
            </svg>
        </div>
        <div class="message-content">
            <div class="message-header">
                <span class="message-sender">${senderName}</span>
                <span class="message-time">${time}</span>
            </div>
            <div class="message-text">${escapeHtml(text)}</div>
        </div>
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Store message
    state.messages.push({ role, content: text, timestamp: new Date() });
}

function showTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'flex';
}

function hideTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'none';
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// SoulTrace Functions
async function startAssessment() {
    state.soultrace.answers = [];
    state.soultrace.currentQuestion = 0;
    state.soultrace.isActive = true;
    
    document.getElementById('soultrace-start').style.display = 'none';
    document.getElementById('soultrace-result').style.display = 'none';
    document.getElementById('soultrace-question').style.display = 'block';
    
    try {
        const response = await fetch(`${API_BASE}/api/soultrace`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ answers: [] })
        });
        
        if (response.ok) {
            const data = await response.json();
            handleSoultraceUpdate(data);
        } else {
            // Use mock data for demo
            handleSoultraceUpdate({
                question: "I prefer to analyze problems logically rather than rely on intuition.",
                current: 1,
                total: 10
            });
        }
    } catch (e) {
        // Use mock data for demo
        handleSoultraceUpdate({
            question: "I prefer to analyze problems logically rather than rely on intuition.",
            current: 1,
            total: 10
        });
    }
}

async function handleAnswer(score) {
    state.soultrace.answers.push(score);
    state.soultrace.currentQuestion++;
    
    if (state.soultrace.currentQuestion >= state.soultrace.totalQuestions) {
        // Assessment complete
        try {
            const response = await fetch(`${API_BASE}/api/soultrace`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ answers: state.soultrace.answers })
            });
            
            if (response.ok) {
                const data = await response.json();
                state.soultrace.result = data;
                renderResult(data);
            } else {
                // Use mock result for demo
                const mockResult = generateMockResult();
                state.soultrace.result = mockResult;
                renderResult(mockResult);
            }
        } catch (e) {
            // Use mock result for demo
            const mockResult = generateMockResult();
            state.soultrace.result = mockResult;
            renderResult(mockResult);
        }
    } else {
        // Next question
        try {
            const response = await fetch(`${API_BASE}/api/soultrace`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ answers: state.soultrace.answers })
            });
            
            if (response.ok) {
                const data = await response.json();
                handleSoultraceUpdate(data);
            } else {
                // Mock next question
                const mockQuestions = [
                    "I prefer to analyze problems logically rather than rely on intuition.",
                    "I find it easy to understand and manage my emotions.",
                    "I enjoy exploring new ideas and abstract concepts.",
                    "I prefer working in teams rather than alone.",
                    "I am comfortable with uncertainty and ambiguity.",
                    "I value creativity over efficiency.",
                    "I am drawn to helping others solve their problems.",
                    "I enjoy taking risks to achieve greater rewards.",
                    "I prefer structured environments over flexible ones.",
                    "I am motivated by personal growth and self-improvement."
                ];
                
                handleSoultraceUpdate({
                    question: mockQuestions[state.soultrace.currentQuestion] || "Question not available",
                    current: state.soultrace.currentQuestion + 1,
                    total: 10
                });
            }
        } catch (e) {
            // Mock next question
            handleSoultraceUpdate({
                question: "I enjoy exploring new ideas and abstract concepts.",
                current: state.soultrace.currentQuestion + 1,
                total: 10
            });
        }
    }
}

function handleSoultraceUpdate(data) {
    if (data.question) {
        document.getElementById('question-text').textContent = data.question;
        document.getElementById('question-current').textContent = data.current;
        document.getElementById('question-total').textContent = data.total;
        
        const progress = (data.current / data.total * 100);
        document.getElementById('question-progress-bar').style.width = `${progress}%`;
    }
    
    if (data.result) {
        renderResult(data.result);
    }
}

function generateMockResult() {
    const colors = {
        white: Math.floor(Math.random() * 30) + 20,
        blue: Math.floor(Math.random() * 30) + 20,
        black: Math.floor(Math.random() * 30) + 10,
        red: Math.floor(Math.random() * 30) + 10,
        green: Math.floor(Math.random() * 30) + 10
    };
    
    // Normalize to 100%
    const total = Object.values(colors).reduce((a, b) => a + b, 0);
    Object.keys(colors).forEach(key => {
        colors[key] = Math.round(colors[key] / total * 100);
    });
    
    const archetypes = {
        white: "The Strategist",
        blue: "The Analyst", 
        black: "The Architect",
        red: "The Innovator",
        green: "The Harmonizer"
    };
    
    const dominant = Object.entries(colors).reduce((a, b) => a[1] > b[1] ? a : b)[0];
    
    return {
        archetype: archetypes[dominant],
        description: `You are ${archetypes[dominant]}, characterized by your strong ${dominant} energy. You approach challenges with a unique blend of analytical thinking and creative problem-solving.`,
        colors: colors,
        dominant: dominant,
        link: '#'
    };
}

function renderResult(data) {
    document.getElementById('soultrace-question').style.display = 'none';
    document.getElementById('soultrace-result').style.display = 'block';
    
    document.getElementById('result-archetype').textContent = data.archetype || 'Unknown';
    document.getElementById('result-description').textContent = data.description || '';
    
    if (data.link) {
        document.getElementById('result-link').href = data.link;
    }
    
    // Render color distribution bars
    const colorsContainer = document.getElementById('color-bars');
    colorsContainer.innerHTML = '';
    
    const colorMap = {
        white: { label: 'White', color: '#ffffff' },
        blue: { label: 'Blue', color: '#3b82f6' },
        black: { label: 'Black', color: '#6b7280' },
        red: { label: 'Red', color: '#ef4444' },
        green: { label: 'Green', color: '#22c55e' }
    };
    
    if (data.colors) {
        Object.entries(data.colors).forEach(([key, value]) => {
            const colorInfo = colorMap[key];
            const barItem = document.createElement('div');
            barItem.className = 'color-bar-item';
            barItem.innerHTML = `
                <span class="color-bar-label">${colorInfo.label}</span>
                <div class="color-bar-track">
                    <div class="color-bar-fill" style="width: ${value}%; background: ${colorInfo.color}"></div>
                </div>
                <span class="color-bar-value">${value}%</span>
            `;
            colorsContainer.appendChild(barItem);
        });
    }
    
    // Draw radar chart
    drawRadarChart(data.colors || {});
}

function drawRadarChart(colors) {
    const canvas = document.getElementById('radar-chart');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 40;
    
    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    const colorKeys = ['white', 'blue', 'black', 'red', 'green'];
    const colorValues = [colors.white || 0, colors.blue || 0, colors.black || 0, colors.red || 0, colors.green || 0];
    const maxVal = Math.max(...colorValues, 1);
    
    const angleStep = (Math.PI * 2) / 5;
    const startAngle = -Math.PI / 2;
    
    // Draw background pentagon grid
    for (let i = 1; i <= 5; i++) {
        const r = radius * (i / 5);
        ctx.beginPath();
        for (let j = 0; j < 5; j++) {
            const angle = startAngle + angleStep * j;
            const x = centerX + r * Math.cos(angle);
            const y = centerY + r * Math.sin(angle);
            if (j === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    
    // Draw axis lines
    for (let i = 0; i < 5; i++) {
        const angle = startAngle + angleStep * i;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(centerX + radius * Math.cos(angle), centerY + radius * Math.sin(angle));
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    
    // Draw data polygon
    ctx.beginPath();
    for (let i = 0; i < 5; i++) {
        const angle = startAngle + angleStep * i;
        const r = radius * (colorValues[i] / maxVal);
        const x = centerX + r * Math.cos(angle);
        const y = centerY + r * Math.sin(angle);
        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    }
    ctx.closePath();
    
    // Create gradient fill
    const gradient = ctx.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius);
    gradient.addColorStop(0, 'rgba(102, 126, 234, 0.8)');
    gradient.addColorStop(1, 'rgba(118, 75, 162, 0.4)');
    ctx.fillStyle = gradient;
    ctx.fill();
    
    // Draw border
    ctx.strokeStyle = 'rgba(102, 126, 234, 0.8)';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Add glow effect
    ctx.shadowColor = 'rgba(102, 126, 234, 0.5)';
    ctx.shadowBlur = 20;
    ctx.stroke();
    ctx.shadowBlur = 0;
    
    // Draw data points
    const pointColors = ['#ffffff', '#3b82f6', '#6b7280', '#ef4444', '#22c55e'];
    for (let i = 0; i < 5; i++) {
        const angle = startAngle + angleStep * i;
        const r = radius * (colorValues[i] / maxVal);
        const x = centerX + r * Math.cos(angle);
        const y = centerY + r * Math.sin(angle);
        
        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fillStyle = pointColors[i];
        ctx.fill();
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.lineWidth = 2;
        ctx.stroke();
        
        // Glow effect on points
        ctx.shadowColor = pointColors[i];
        ctx.shadowBlur = 10;
        ctx.fill();
        ctx.shadowBlur = 0;
    }
    
    // Draw labels
    const labels = ['White', 'Blue', 'Black', 'Red', 'Green'];
    const labelColors = ['#ffffff', '#3b82f6', '#6b7280', '#ef4444', '#22c55e'];
    
    for (let i = 0; i < 5; i++) {
        const angle = startAngle + angleStep * i;
        const labelR = radius + 25;
        const x = centerX + labelR * Math.cos(angle);
        const y = centerY + labelR * Math.sin(angle);
        
        ctx.fillStyle = labelColors[i];
        ctx.font = '12px Inter, sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(labels[i], x, y);
    }
}

// Utility Functions
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100px)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function formatTime(date) {
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Auto-refresh metrics
function startMetricsRefresh() {
    setInterval(fetchMetrics, 30000); // Refresh every 30 seconds
}

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    // Initialize WebSocket
    initWebSocket();
    
    // Setup navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            if (page) {
                showPage(page);
            }
        });
    });
    
    // Setup chat input
    const chatInput = document.getElementById('chat-input');
    if (chatInput) {
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Auto-resize textarea
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });
    }
    
    // Load initial data
    fetchMetrics();
    startMetricsRefresh();
    
    // Hide loading overlay
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.classList.remove('show');
    }
    
    console.log('Hermes WebUI Pro initialized');
});

// Export functions for global access
window.showPage = showPage;
window.sendMessage = sendMessage;
window.startAssessment = startAssessment;
window.handleAnswer = handleAnswer;
