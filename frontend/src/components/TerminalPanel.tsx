import React, { useState, useEffect, useRef } from 'react';

const TerminalPanel: React.FC = () => {
    const [logs, setLogs] = useState<string[]>([
        "[INFO] Initializing system interface...",
        "[INFO] Waiting for live websocket connection..."
    ]);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        // Connect to the backend WebSocket
        const socket = new WebSocket('ws://localhost:8080/ws/logs');

        socket.onopen = () => {
            setLogs(prev => [...prev, "[SUCCESS] Real-time log connection established."]);
        };

        socket.onmessage = (event) => {
            setLogs(prev => {
                const newLogs = [...prev, event.data];
                // Limit to last 100 logs for performance
                return newLogs.slice(-100);
            });
        };

        socket.onerror = () => {
            // Add a small delay for error reporting to avoid flashing on normal fast reloads
            setTimeout(() => {
                if (socket.readyState !== WebSocket.OPEN) {
                    setLogs(prev => [...prev.slice(-100), "[ERROR] WebSocket connection failed. Is the backend running?"]);
                }
            }, 2000);
        };

        socket.onclose = () => {
            setLogs(prev => [...prev.slice(-100), "[INFO] Log stream disconnected."]);
        };

        return () => {
            socket.close();
        };
    }, []);

    useEffect(() => {
        // Auto-scroll to the bottom when logs update
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <section className="terminal-panel" style={panelStyle}>
            <div className="panel-tabs" style={tabsStyle}>
                <div className="tab active" style={tabStyle(true)}>TERMINAL</div>
            </div>
            <div 
                className="panel-content" 
                ref={scrollRef}
                style={contentStyle}
            >
                {logs.map((log, i) => (
                    <div 
                        key={i} 
                        className={`log-line ${log.includes('SUCCESS') ? 'success' : log.includes('ERROR') ? 'error' : ''}`}
                        style={{
                            marginBottom: '4px',
                            color: log.includes('SUCCESS') ? 'var(--vscode-logs)' : 
                                   log.includes('ERROR') ? '#f14c4c' : 
                                   'var(--vscode-text)',
                            opacity: 0.9
                        }}
                    >
                        {log}
                    </div>
                ))}
            </div>
        </section>
    );
};

// Styles
const panelStyle: React.CSSProperties = {
    height: '180px',
    background: 'var(--vscode-bg)',
    borderTop: '1px solid var(--vscode-border)',
    display: 'flex',
    flexDirection: 'column'
};

const tabsStyle: React.CSSProperties = {
    display: 'flex',
    paddingLeft: '15px',
    background: 'var(--vscode-bg)'
};

const tabStyle = (active: boolean): React.CSSProperties => ({
    padding: '8px 15px',
    fontSize: '11px',
    cursor: 'pointer',
    opacity: active ? 1 : 0.6,
    borderBottom: active ? '1px solid var(--vscode-accent)' : 'none',
    transition: 'all 0.2s ease'
});

const contentStyle: React.CSSProperties = {
    flex: 1,
    padding: '10px 20px',
    overflowY: 'auto',
    fontFamily: "'Fira Code', monospace",
    fontSize: '12px',
    lineHeight: 1.4
};

export default TerminalPanel;
