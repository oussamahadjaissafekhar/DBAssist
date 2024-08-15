// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Connect from './pages/connect';
import Partitioning from './pages/partitioning'; // Correct spelling of 'partitioning'
import IndexSelection from './pages/indexSelection';
import Sidebar from './components/sidebar';
import './App.css'

function App() {
    const location = useLocation();

    // Hide Sidebar on the Connect page
    const shouldShowSidebar = location.pathname !== '/';

    return (
        <div style={{ display: 'flex' }}>
            {shouldShowSidebar && <Sidebar />}
            <div style={{ flex: 1, marginLeft: shouldShowSidebar ? '250px' : '0' }}>
                <Routes>
                    <Route path="/" element={<Connect onConnect={handleConnect} />} />
                    <Route path="/partition" element={<Partitioning />} />
                    <Route path="/index" element={<IndexSelection />} />
                    {/* Add more routes as needed */}
                </Routes>
            </div>
        </div>
    );
}

function handleConnect(response) {
    // Handle connection logic
    console.log('Connection response:', response);
}

export default function AppWrapper() {
    return (
        <Router>
            <App />
        </Router>
    );
}