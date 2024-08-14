import React, { useState } from 'react';
import Pipeline from '../components/partitioningPipline';

function Partitioning() {
    //const [currentStep] = useState(0);
    const shouldShowText = true;

    // Logic to update the currentStep based on user interaction

    return (
        <div style={{ textAlign: 'center' }}>
            <Pipeline showText={shouldShowText} />
            <button className='start-button'>Start partitioning</button>
            {/* Your partitioning page content */}
        </div>
    );
}

export default Partitioning;
