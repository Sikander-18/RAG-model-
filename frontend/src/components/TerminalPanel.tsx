import React, { useState, useEffect, useRef } from 'react';

const TerminalPanel: React.FC = () => {
    const [logs, setLogs] = useState<string[]>([
        "[INFO] Initializing system interface...",
        "[INFO] Waiting for live websocket connection..."
    ]);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        let socket: WebSocket | null = null;
        let reconnectTimeout: ReturnType<typeof setTimeout> | null = null;

        const connect = () => {
            // Using 127.0.0.1 instead of localhost for better compatibility
            socket = new WebSocket('ws://127.0.0.1:8080/ws/logs');

            socket.onopen = () => {
                setLogs(prev => [...prev, "[SUCCESS] Real-time log connection established."]);
            };

            socket.onmessage = (event) => {
                setLogs(prev => {
                    const newLogs = [...prev, event.data];
                    return newLogs.slice(-100);
                });
            };

            socket.onerror = () => {
                // Silently handle error here, the onclose will trigger the reconnect
            };

            socket.onclose = () => {
                setLogs(prev => [...prev.slice(-100), "[INFO] Connection lost. Retrying in 5s..."]);
                // Attempt to reconnect after 5 seconds
                reconnectTimeout = setTimeout(connect, 5000);
            };
        };

        connect();

        return () => {
            if (socket) socket.close();
            if (reconnectTimeout) clearTimeout(reconnectTimeout);
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
