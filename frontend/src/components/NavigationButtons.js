// src/components/NavigationButtons.js
import React from 'react';
import '../css/NavigationButtons.css'; // Add any styles you need

function NavigationButtons({ currentStep, handleStepChange , numbersteps}) {
    return (
        <div className='navigation-buttons'>
            {currentStep > 0 && (
                <button className='prev-button' onClick={() => handleStepChange('prev')}>
                    Previous
                </button>
            )}
            {currentStep < numbersteps && currentStep > 0 && (
                <button className='next-button' onClick={() => handleStepChange('next')}>
                    Next
                </button>
            )}
        </div>
    );
}

export default NavigationButtons;
