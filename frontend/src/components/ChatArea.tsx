import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Loader2 } from 'lucide-react';
import axios from 'axios';

interface Message {
    type: 'user' | 'bot';
    content: string;
    sources?: any[];
}

const ChatArea: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        { type: 'bot', content: "Hello! I am your RAG assistant. Ask me anything about your documents, and I'll find the answer for you." }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || loading) return;

        const userMsg = input.trim();
        setMessages(prev => [...prev, { type: 'user', content: userMsg }]);
        setInput('');
        setLoading(true);

        try {
            const response = await axios.post('http://localhost:8080/query', { query: userMsg });
            setMessages(prev => [...prev, { 
                type: 'bot', 
                content: response.data.answer,
                sources: response.data.sources 
            }]);
        } catch (error) {
            setMessages(prev => [...prev, { type: 'bot', content: "[ERROR] Failed to connect to the backend server. Please ensure the API is running." }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <section className="chat-area-main" style={areaStyle}>
            <div className="chat-messages-container" style={messagesContainerStyle}>
                {messages.map((msg, i) => (
                    <div 
                        key={i} 
                        className={`message-wrapper ${msg.type}`}
                        style={{
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: msg.type === 'user' ? 'flex-end' : 'flex-start',
                            marginBottom: '20px',
                            width: '100%',
                            animation: 'bubble-in 0.3s ease'
                        }}
                    >
                        <div 
                            className="message-bubble"
                            style={{
                                maxWidth: '80%',
                                padding: '12px 18px',
                                borderRadius: '18px',
                                fontSize: '14px',
                                lineHeight: '1.5',
                                background: msg.type === 'user' ? 'var(--vscode-accent)' : 'var(--vscode-sidebar)',
                                color: msg.type === 'user' ? 'white' : 'var(--vscode-text)',
                                border: msg.type === 'user' ? 'none' : '1px solid var(--vscode-border)',
                                borderBottomRightRadius: msg.type === 'user' ? '4px' : '18px',
                                borderBottomLeftRadius: msg.type === 'bot' ? '4px' : '18px'
                            }}
                        >
                            {msg.type === 'bot' && (
                                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '8px', opacity: 0.8, fontSize: '11px' }}>
                                    <Bot size={14} style={{ marginRight: '5px' }} />
                                    <span>RAG ASSISTANT</span>
                                </div>
                            )}
                            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                            {msg.sources && msg.sources.length > 0 && (
                                <div className="sources-list" style={sourcesStyle}>
                                    Sources: {Array.from(new Set(msg.sources.map(s => s.source))).join(', ')}
                                </div>
                            )}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start', marginBottom: '20px' }}>
                        <div style={{ padding: '12px 18px', borderRadius: '18px', borderBottomLeftRadius: '4px', background: 'var(--vscode-sidebar)', border: '1px solid var(--vscode-border)', color: 'var(--vscode-text)' }}>
                            <div style={{ display: 'flex', alignItems: 'center', fontSize: '12px', opacity: 0.8 }}>
                                <Loader2 size={14} className="animate-spin" style={{ marginRight: '8px' }} />
                                <span>Developing response...</span>
                            </div>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-outer" style={inputOuterStyle}>
                <div className="chat-input-row" style={inputRowStyle}>
                    <textarea
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && !e.shiftKey) {
                                e.preventDefault();
                                handleSend();
                            }
                        }}
                        placeholder="Type your question here..."
                        rows={1}
                        style={inputStyle}
                    />
                    <button 
                        onClick={handleSend} 
                        disabled={loading} 
                        style={{
                            ...sendButtonStyle,
                            opacity: input.trim() ? 1 : 0.4,
                            cursor: input.trim() ? 'pointer' : 'not-allowed'
                        }}
                    >
                        <Send size={18} />
                    </button>
                </div>
            </div>
        </section>
    );
};

// Styles
const areaStyle: React.CSSProperties = { 
    flex: 1, 
    display: 'flex', 
    flexDirection: 'column', 
    background: 'var(--vscode-bg)', 
    overflow: 'hidden',
    position: 'relative'
};
const messagesContainerStyle: React.CSSProperties = { 
    flex: 1, 
    overflowY: 'auto', 
    padding: '30px 40px',
    display: 'flex',
    flexDirection: 'column'
};
const inputOuterStyle: React.CSSProperties = {
    padding: '20px 40px',
    background: 'linear-gradient(transparent, var(--vscode-bg) 30%)',
    position: 'sticky',
    bottom: 0
};
const inputRowStyle: React.CSSProperties = { 
    background: 'var(--vscode-sidebar)', 
    border: '1px solid var(--vscode-border)', 
    borderRadius: '24px', 
    display: 'flex', 
    alignItems: 'center', 
    padding: '8px 20px',
    maxWidth: '800px',
    margin: '0 auto',
    boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
};
const inputStyle: React.CSSProperties = { 
    flex: 1, 
    background: 'transparent', 
    border: 'none', 
    color: 'var(--vscode-text)', 
    resize: 'none', 
    outline: 'none', 
    fontSize: '14px',
    padding: '8px 0',
    maxHeight: '150px'
};
const sendButtonStyle: React.CSSProperties = { 
    background: 'var(--vscode-accent)', 
    border: 'none', 
    color: 'white', 
    borderRadius: '50%',
    width: '32px',
    height: '32px',
    display: 'flex', 
    justifyContent: 'center',
    alignItems: 'center',
    marginLeft: '10px',
    transition: 'all 0.2s ease'
};
const sourcesStyle: React.CSSProperties = { 
    fontSize: '11px', 
    marginTop: '10px', 
    paddingTop: '8px', 
    borderTop: '1px solid rgba(255,255,255,0.1)', 
    opacity: 0.6 
};

export default ChatArea;
