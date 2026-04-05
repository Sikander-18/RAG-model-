import React, { useState } from 'react';
import { ThemeProvider } from './context/ThemeContext';
import ActivityBar from './components/ActivityBar';
import Sidebar from './components/Sidebar';
import ChatArea from './components/ChatArea';
import TerminalPanel from './components/TerminalPanel';
import StatusBar from './components/StatusBar';
import './index.css';

const App: React.FC = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const [activeSideView, setActiveSideView] = useState<'explorer' | 'search'>('explorer');

    const toggleSidebar = (view: 'explorer' | 'search') => {
        if (activeSideView === view && isSidebarOpen) {
            setIsSidebarOpen(false);
        } else {
            setActiveSideView(view);
            setIsSidebarOpen(true);
        }
    };

    return (
        <ThemeProvider>
            <div id="app" style={{
                display: 'flex',
                height: '100vh',
                width: '100vw',
                background: 'var(--vscode-bg)',
                color: 'var(--vscode-text)',
                overflow: 'hidden'
            }}>
                {/* Far Left Activity Bar */}
                <ActivityBar 
                    activeView={activeSideView} 
                    isSidebarOpen={isSidebarOpen}
                    onToggle={toggleSidebar} 
                />

                {/* Animated Sidebar */}
                <div style={{
                    width: isSidebarOpen ? '260px' : '0px',
                    transition: 'width 0.3s ease',
                    overflow: 'hidden',
                    background: 'var(--vscode-sidebar)',
                    borderRight: isSidebarOpen ? '1px solid var(--vscode-border)' : 'none',
                    display: 'flex',
                    flexDirection: 'column'
                }}>
                    <Sidebar activeView={activeSideView} />
                </div>

                {/* Main Content Area */}
                <main style={{
                    flex: 1,
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    minWidth: 0
                }}>
                    <div style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
                        <ChatArea />
                        <TerminalPanel />
                    </div>
                    <StatusBar />
                </main>
            </div>
        </ThemeProvider>
    );
};

export default App;
