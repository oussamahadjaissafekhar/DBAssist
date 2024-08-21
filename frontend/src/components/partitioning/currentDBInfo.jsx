import React from 'react';
import '../../css/dbInfo.css'
import ERDiagram from './ERDiagram';

function CurrentDBInfo({ isVisible, onClose, nodes, edges }) {
    if (!isVisible) return null; // Don't render anything if the popup is not visible
    
      
    return (
      <div className="popup-overlay-dbinfo">
        <div className="popup-content-dbinfo">
          <button className="close-button-dbinfo" onClick={onClose}>X</button>
          <h2>Current DB schema</h2>
          <ERDiagram nodes={nodes} edges={edges}/>
        </div>
      </div>
    );
  }

export default CurrentDBInfo