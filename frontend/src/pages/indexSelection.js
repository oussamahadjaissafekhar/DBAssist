import React, { useState } from 'react';
import Pipeline from '../components/indexingPipline';

function IndexSelection() {
    //const [currentStep] = useState(0);
    const shouldShowText = true;

    // Logic to update the currentStep based on user interaction

    return (
        <div style={{ textAlign: 'center' }}>
            <Pipeline showText={shouldShowText} />
            <button className='start-button'>Start indexing</button>
            {/* Your IndexSelection page content */}
        </div>
    );
}

export default IndexSelection;
