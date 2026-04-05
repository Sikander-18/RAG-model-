// Theme Toggling
const themeToggle = document.getElementById('theme-toggle');
const body = document.body;

themeToggle.addEventListener('click', () => {
    if (body.classList.contains('theme-dark-plus')) {
        body.classList.remove('theme-dark-plus');
        body.classList.add('theme-cyberpunk');
        themeToggle.querySelector('span').textContent = 'Theme: Cyberpunk Neon';
    } else {
        body.classList.remove('theme-cyberpunk');
        body.classList.add('theme-dark-plus');
        themeToggle.querySelector('span').textContent = 'Theme: Classic Dark+';
    }
});

// Mock Log Simulation
const terminalLogs = document.getElementById('terminal-logs');
const mockLogs = [
    "[INFO] Checking Ollama connection...",
    "[SUCCESS] Connected to Ollama (Mistral-7B).",
    "[INFO] Scanning raw_documents folder...",
    "[INFO] Found 1 new file: 'research_paper.docx'",
    "[INFO] Starting conversion to markdown...",
    "[INFO] Conversion complete. Chunking text...",
    "[SUCCESS] 24 chunks indexed in ChromaDB."
];

let logIndex = 0;

function addLog() {
    if (logIndex < mockLogs.length) {
        // Remove cursor
        const cursor = terminalLogs.querySelector('.cursor');
        if (cursor) cursor.remove();

        const logLine = document.createElement('div');
        logLine.className = 'log-line ' + (mockLogs[logIndex].includes('SUCCESS') ? 'success' : 'info');
        logLine.textContent = mockLogs[logIndex];
        terminalLogs.appendChild(logLine);

        // Re-add cursor
        const newCursor = document.createElement('div');
        newCursor.className = 'log-line cursor';
        newCursor.textContent = '_';
        terminalLogs.appendChild(newCursor);

        // Scroll to bottom
        terminalLogs.scrollTop = terminalLogs.scrollHeight;
        
        logIndex++;
        setTimeout(addLog, Math.random() * 3000 + 2000);
    }
}

// Start simulation after a delay
setTimeout(addLog, 5000);

// Auto-grow textarea (Simple)
const chatInput = document.getElementById('chat-input');
chatInput.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = chatInput.scrollHeight + 'px';
});

// Mock Send Message
const sendBtn = document.getElementById('send-btn');
const chatMessages = document.getElementById('chat-messages');

sendBtn.addEventListener('click', () => {
    const text = chatInput.value.trim();
    if (text) {
        // Add user message
        const userMsg = document.createElement('div');
        userMsg.className = 'message user';
        userMsg.innerHTML = `
            <div class="avatar">U</div>
            <div class="content"><p>${text}</p></div>
        `;
        chatMessages.appendChild(userMsg);
        
        chatInput.value = '';
        chatInput.style.height = 'auto';
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Mock bot response
        setTimeout(() => {
            const botMsg = document.createElement('div');
            botMsg.className = 'message bot';
            botMsg.innerHTML = `
                <div class="avatar">AI</div>
                <div class="content"><p>Thinking...</p></div>
            `;
            chatMessages.appendChild(botMsg);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 1000);
    }
});
