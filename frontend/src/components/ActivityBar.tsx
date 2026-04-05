import React from 'react';
import { Files, Search } from 'lucide-react';

interface ActivityBarProps {
    activeView: 'explorer' | 'search';
    isSidebarOpen: boolean;
    onToggle: (view: 'explorer' | 'search') => void;
}

const ActivityBar: React.FC<ActivityBarProps> = ({ activeView, isSidebarOpen, onToggle }) => {
    return (
        <aside className="activity-bar" style={{
            width: '50px',
            height: '100%',
            background: 'var(--vscode-activity-bar)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            padding: '10px 0',
            zIndex: 100
        }}>
            <div className="top-items" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%' }}>
                <div 
                    className="activity-item" 
                    title="Explorer" 
                    onClick={() => onToggle('explorer')}
                    style={itemStyle(activeView === 'explorer' && isSidebarOpen)}
                >
                    <Files size={24} />
                </div>
                <div 
                    className="activity-item" 
                    title="Search" 
                    onClick={() => onToggle('search')}
                    style={itemStyle(activeView === 'search' && isSidebarOpen)}
                >
                    <Search size={24} />
                </div>
            </div>
        </aside>
    );
};

const itemStyle = (active: boolean): React.CSSProperties => ({
    padding: '12px',
    width: '100%',
    display: 'flex',
    justifyContent: 'center',
    cursor: 'pointer',
    color: active ? 'var(--vscode-activity-active)' : 'var(--vscode-activity-inactive)',
    borderLeft: active ? '2px solid var(--vscode-accent)' : 'none',
    transition: 'all 0.2s',
    opacity: active ? 1 : 0.6
});

export default ActivityBar;
