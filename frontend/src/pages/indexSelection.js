import React, { useState } from 'react';
import Pipeline from '../components/indexingPipline';
import WorkloadAnalyzer from '../components/WorkloadAnalyzer';
import NavigationButtons from '../components/NavigationButtons';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import '../css/IndexSelection.css'; // Ensure this CSS file includes the animations

function IndexSelection() {
    const [currentStep, setCurrentStep] = useState(0);

    // Function to handle step change
    const handleStepChange = (direction) => {
        setCurrentStep((prevStep) => {
            if (direction === 'next') {
                return Math.min(prevStep + 1, 4); // 4 is the total number of steps - 1
            } else if (direction === 'prev') {
                return Math.max(prevStep - 1, 0);
            }
            return prevStep;
        });
    };

    return (
        <div style={{ textAlign: 'center' }}>
            <Pipeline showText={currentStep === 0} currentStep={currentStep} />
            
            <TransitionGroup>
                <CSSTransition
                    key={currentStep}
                    timeout={300}
                    classNames="fade"
                >
                    <div>
                        {/* Step 0: Start indexing */}
                        {currentStep === 0 && (
                            <CSSTransition
                                in={currentStep === 0}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <div className='start-button-div'>
                                    <button className='start-button' onClick={() => handleStepChange('next')}>
                                        Start indexing
                                    </button>
                                </div>
                            </CSSTransition>
                        )}
                        
                        {/* Step 1: Analyze workload */}
                        {currentStep === 1 && (
                            <CSSTransition
                                in={currentStep === 1}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <div>
                                    <WorkloadAnalyzer />
                                </div>
                            </CSSTransition>
                        )}

                        {/* Step 2: Choose initial indexes */}
                        {currentStep === 2 && (
                            <CSSTransition
                                in={currentStep === 2}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <div>
                                    {/* Your Component for this step */}
                                </div>
                            </CSSTransition>
                        )}

                        {/* Step 3: Execute queries */}
                        {currentStep === 3 && (
                            <CSSTransition
                                in={currentStep === 3}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <div>
                                    {/* Your Component for this step */}
                                </div>
                            </CSSTransition>
                        )}

                        {/* Step 4: End */}
                        {currentStep === 4 && (
                            <CSSTransition
                                in={currentStep === 4}
                                timeout={300}
                                classNames="fade"
                                unmountOnExit
                            >
                                <div>
                                    {/* Your Component for this step */}
                                </div>
                            </CSSTransition>
                        )}
                    </div>
                </CSSTransition>
            </TransitionGroup>

            {/* Common Navigation Buttons */}
            <NavigationButtons currentStep={currentStep} handleStepChange={handleStepChange} />
        </div>
    );
}

export default IndexSelection;
