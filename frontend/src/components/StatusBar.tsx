import React from 'react';
import { GitBranch, RefreshCw, Palette } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';

const StatusBar: React.FC = () => {
    const { theme, toggleTheme } = useTheme();

    return (
        <footer className="status-bar" style={{
            width: '100%',
            height: '25px',
            background: 'var(--vscode-status)',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '0 10px',
            fontSize: '11px',
            color: '#fff',
            cursor: 'default',
            zIndex: 110
        }}>
            <div className="left" style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
                <div className="status-item main" style={itemStyle}>
                    <GitBranch size={12} style={{ marginRight: '5px' }} />
                    <span>main</span>
                </div>
                <div className="status-item" style={{ ...itemStyle, background: 'none' }}>
                    <RefreshCw size={12} style={{ marginRight: '5px' }} />
                    <span>Index: Ready</span>
                </div>
            </div>
            
            <div className="right" style={{ display: 'flex', alignItems: 'center', height: '100%' }}>
                <div 
                    className="status-item clickable" 
                    onClick={toggleTheme}
                    style={{ ...itemStyle, background: 'none', cursor: 'pointer' }}
                >
                    <Palette size={12} style={{ marginRight: '5px' }} />
                    <span>Theme: {theme === 'cyberpunk' ? 'Cyberpunk Neon' : 'Classic Dark+'}</span>
                </div>
                <div className="status-item" style={{ ...itemStyle, background: 'none' }}>
                    <span>Mistral-7B</span>
                </div>
            </div>
        </footer>
    );
};

const itemStyle: React.CSSProperties = { 
    display: 'flex', 
    alignItems: 'center', 
    padding: '0 10px', 
    height: '100%',
    background: 'rgba(0,0,0,0.1)',
    transition: 'background 0.2s'
};

export default StatusBar;
