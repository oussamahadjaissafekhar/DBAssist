import React from 'react';
import '../css/Modal.css';

function Modal({ isOpen, onClose, onPrev, onNext }) {
    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <button className="close-button" onClick={onClose}>X</button>
                <div className="graph-container">
                    {/* Insert your graph components here */}
                    <h3>Your Graph</h3>
                </div>
                <div className="navigation-buttons">
                    <img
                        src={require('../icons/left-arrow.png')}
                        alt="Previous"
                        className="nav-button left"
                        onClick={onPrev}
                    />
                    <img
                        src={require('../icons/right-arrow.png')}
                        alt="Next"
                        className="nav-button right"
                        onClick={onNext}
                    />
                </div>
            </div>
        </div>
    );
}

export default Modal;
