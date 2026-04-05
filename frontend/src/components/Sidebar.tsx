import React, { useState, useEffect } from 'react';
import { FileText, Folder, Trash2, Upload, Search, X } from 'lucide-react';
import axios from 'axios';

interface SidebarProps {
    activeView: 'explorer' | 'search';
}

const Sidebar: React.FC<SidebarProps> = ({ activeView }) => {
    const [files, setFiles] = useState<string[]>([]);
    const [searchQuery, setSearchQuery] = useState('');

    const fetchFiles = async () => {
        try {
            const response = await axios.get('http://localhost:8080/files');
            setFiles(response.data.files);
        } catch (error) {
            console.error("Failed to fetch files", error);
        }
    };

    useEffect(() => {
        fetchFiles();
        const interval = setInterval(fetchFiles, 5000);
        return () => clearInterval(interval);
    }, []);

    const handleDelete = async (filename: string) => {
        if (!window.confirm(`Delete ${filename}?`)) return;
        try {
            await axios.delete(`http://localhost:8080/files/${filename}`);
            fetchFiles();
        } catch (error) {
            alert("Failed to delete file.");
        }
    };

    const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        try {
            await axios.post('http://localhost:8080/upload', formData);
            fetchFiles();
        } catch (error) {
            alert("Upload failed.");
        }
    };

    return (
        <aside style={{ height: '100%', display: 'flex', flexDirection: 'column', width: '260px' }}>
            <div className="sidebar-header" style={headerStyle}>
                <span style={{ fontWeight: 'bold', fontSize: '11px', textTransform: 'uppercase' }}>
                    {activeView === 'explorer' ? 'Explorer' : 'Global Search'}
                </span>
                {activeView === 'explorer' && (
                    <label style={{ cursor: 'pointer', opacity: 0.7 }}>
                        <Upload size={14} />
                        <input type="file" style={{ display: 'none' }} onChange={handleUpload} />
                    </label>
                )}
            </div>

            <div className="sidebar-content" style={{ flex: 1, overflowY: 'auto' }}>
                {activeView === 'explorer' ? (
                    <div className="explorer-view">
                        <div className="node-item" style={labelStyle}>
                            <Folder size={16} style={{ marginRight: '5px' }} />
                            <span>raw_documents</span>
                        </div>
                        {files.map(file => (
                            <div key={file} className="node-item sub" style={{ ...itemStyle, paddingLeft: '40px', justifyContent: 'space-between' }}>
                                <div style={{ display: 'flex', alignItems: 'center' }}>
                                    <FileText size={16} style={{ marginRight: '10px' }} />
                                    <span>{file}</span>
                                </div>
                                <Trash2 
                                    size={14} 
                                    className="delete-icon" 
                                    onClick={() => handleDelete(file)}
                                    style={{ opacity: 0.5, cursor: 'pointer' }} 
                                />
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="search-view" style={{ padding: '0 20px' }}>
                        <div style={searchInputWrapper}>
                            <Search size={14} style={{ marginRight: '8px', opacity: 0.6 }} />
                            <input 
                                placeholder="Search in all documents..." 
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                                style={searchInput} 
                            />
                            {searchQuery && <X size={14} style={{ cursor: 'pointer' }} onClick={() => setSearchQuery('')} />}
                        </div>
                        <div style={{ fontSize: '12px', marginTop: '20px', opacity: 0.6, fontStyle: 'italic' }}>
                            {searchQuery ? "Search not implemented yet in backend." : "Enter a term to search..."}
                        </div>
                    </div>
                )}
            </div>
        </aside>
    );
};

// Styles
const headerStyle: React.CSSProperties = { 
    display: 'flex', 
    justifyContent: 'space-between', 
    alignItems: 'center', 
    padding: '10px 20px', 
    background: 'var(--vscode-sidebar)' 
};
const labelStyle: React.CSSProperties = { display: 'flex', alignItems: 'center', padding: '4px 20px', fontSize: '13px', cursor: 'pointer' };
const itemStyle: React.CSSProperties = { display: 'flex', alignItems: 'center', padding: '4px 20px', fontSize: '13px', cursor: 'pointer', transition: 'background 0.2s' };
const searchInputWrapper: React.CSSProperties = { 
    display: 'flex', 
    alignItems: 'center', 
    background: 'var(--vscode-bg)', 
    border: '1px solid var(--vscode-border)', 
    borderRadius: '4px', 
    padding: '5px 10px',
    marginTop: '10px'
};
const searchInput: React.CSSProperties = { flex: 1, background: 'transparent', border: 'none', color: 'var(--vscode-text)', outline: 'none', fontSize: '12px' };

export default Sidebar;
