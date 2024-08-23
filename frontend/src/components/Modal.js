import React, { useState } from 'react';
import BarChart from './workloadAnalyzerCharts/BarChart';
import StackedBarChart from './workloadAnalyzerCharts/StackedBarChart';
import '../css/Modal.css';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';

// Register all necessary components
ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

function Modal({ data, onClose }) {
    const [currentChart, setCurrentChart] = useState(0);

    const charts = [
        <BarChart data={data} key="bar" />,
        <StackedBarChart data={data} key="stacked-bar" />
    ];

    if (!data || data.length === 0) {
        return (
            <div className="modal-overlay">
                <div className="modal-content">
                    <button className="close-button" onClick={onClose}>X</button>
                    <div>No data available to display.</div>
                </div>
            </div>
        );
    }

    const handleNext = () => {
        setCurrentChart((prev) => (prev + 1) % charts.length);
    };

    const handlePrevious = () => {
        setCurrentChart((prev) => (prev - 1 + charts.length) % charts.length);
    };

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button className="close-button" onClick={onClose}>X</button>
                <div className="chart-container">
                <img 
                    src={require('../icons/left-arrow.png')} 
                    alt="Previous" 
                    className="nav-button prev" 
                    onClick={handlePrevious}
                />
                    <div className="chart">
                        {charts[currentChart]}
                    </div>
                    <img 
                    src={require('../icons/right-arrow.png')} 
                    alt="Next" 
                    className="nav-button next" 
                    onClick={handleNext}
                />
                </div>
                
                
            </div>
        </div>
    );
}

export default Modal;
