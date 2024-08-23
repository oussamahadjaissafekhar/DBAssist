import React, { useContext, useState } from 'react';
import { DbContext } from '../DbContext';
import Pipeline from '../components/partitioningPipline';
import NavigationButtons from '../components/NavigationButtons';
import { CSSTransition, TransitionGroup } from 'react-transition-group';
import '../css/partitioning.css';
import CurrentDBInfo from '../components/partitioning/currentDBInfo';
import '../css/dbInfo.css'
import { showDBInfo, getDataChangeStats} from '../api';
import DataChangeIdentification from '../components/partitioning/dataChangeIdentification';
import WorkloadAnalyzer from '../components/WorkloadAnalyzer'
import LoadingOverlay from '../components/partitioning/loadingOverlay';
import KeyChoice from '../components/partitioning/keyChoice';
import Schema from '../components/partitioning/schema';
import PartitioningScript from '../components/partitioning/partitioningScript';
import DataMigration from '../components/partitioning/dataMigration';

function Partitioning() {

    const [currentStep, setCurrentStep] = useState(0);
    const [loading, setLoading] = useState(false);
    const [nodes, setNodes] = useState([]) 
    const [edges, setEdges] = useState([])
    const [isPopupVisible, setPopupVisible] = useState(false)
    const [dataChangeStats, setDataChangeStats] = useState(null)
    const { dbName } = useContext(DbContext);
    const [fileName, setFileName] = useState('');

    
    // Function to handle step change
    const handleStepChange = (direction) => {
    setCurrentStep((prevStep) => {
        if (direction === 'next') {
            return Math.min(prevStep + 1, 6);
        } else if (direction === 'prev') {
            return Math.max(prevStep - 1, 0);
        }
        return prevStep;
    });
    };

    const handleFileNameChange = (name) => {
        setFileName(name);
    };

    const handleDBinfoClick = async () => {
    setPopupVisible(true);
    try {
    const response = await showDBInfo();
    setNodes(response.nodes)
    setEdges(response.edges)
    } catch (error) {
    console.error("Error getting db info:", error);
    }
    }

    const closePopup = () => {
    setPopupVisible(false);
    }

    const handleStartButtonClick = async () => {
        setLoading(true); // Show loading indicator
        try {
        const stats = await getDataChangeStats();
        console.log(stats)
        setDataChangeStats(stats);
        handleStepChange('next');
        } catch (error) {
        console.error("Error fetching data change stats:", error);
        } finally {
        setLoading(false); // Hide loading indicator
        }
    }

    return (
        <div style={{ textAlign: 'center' }}>
            {currentStep !== 0 && <Pipeline currentStep={currentStep} />}
            <div className="components-container">
                <TransitionGroup>
                    <CSSTransition
                        key={currentStep}
                        timeout={300}
                        classNames="fade"
                    >
                        <div>
                            {/*the loading overlay is applicable for all steps*/}
                            <LoadingOverlay isLoading={loading} message={"Analyzing logs"}/>
                            {/* Step 0: DB info */}
                            {currentStep === 0 && (
                                <CSSTransition
                                    in={currentStep === 0}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <>
                                    <div className="header-container" onClick={handleDBinfoClick}>
                                        <h2>Current database: {dbName}</h2>
                                        <img src={require('../icons/info.png')} alt="info" className="box-button-icon" />
                                    </div>
                                    <CurrentDBInfo isVisible={isPopupVisible} onClose={closePopup} nodes= {nodes} edges = {edges} />
                                    <Pipeline currentStep={currentStep} />
                                    <div className='start-button-div'>
                                        <button className='start-button' onClick={handleStartButtonClick}>
                                            Start partitioning
                                        </button>
                                    </div>
                                    </>
                                </CSSTransition>
                            )}

                            {/* Step 1: Data change */}
                            {currentStep === 1 && (
                                <CSSTransition
                                    in={currentStep === 1}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <h1>Data change identification</h1>
                                        <DataChangeIdentification data = {dataChangeStats}></DataChangeIdentification>
                                    </div>
                                </CSSTransition>
                            )}
                            
                            {/* Step 2: Analyze workload*/}
                            {currentStep === 2 && (
                                <CSSTransition
                                    in={currentStep === 2}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                        <div>
                                            <WorkloadAnalyzer onFileNameChange={handleFileNameChange}/>
                                        </div>
                                </CSSTransition>
                            )}

                            {/* Step 3: key selection */}
                            {currentStep === 3 && (
                                <CSSTransition
                                    in={currentStep === 3}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <h1>Selected partitioning keys</h1>
                                        <KeyChoice></KeyChoice>
                                    </div>
                                </CSSTransition>
                            )}

                            {/* Step 4 : generate schema */}
                            {currentStep === 4 && (
                                <CSSTransition
                                    in={currentStep === 4}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <h1>Schema generation</h1>
                                        <Schema></Schema>
                                    </div>
                                </CSSTransition>
                            )}
                            
                            {/* Step 5:  deploy schema*/}
                            {currentStep === 5 && (
                                <CSSTransition
                                    in={currentStep === 5}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <h1>Schema deployment</h1>
                                        <PartitioningScript></PartitioningScript>
                                    </div>
                                </CSSTransition>
                            )}

                            {/* Step 6: End */}
                            {currentStep === 6 && (
                                <CSSTransition
                                    in={currentStep === 6}
                                    timeout={300}
                                    classNames="fade"
                                    unmountOnExit
                                >
                                    <div>
                                        <h1>Data migration</h1>
                                        <DataMigration></DataMigration>
                                    </div>
                                </CSSTransition>
                            )}
                        </div>
                    </CSSTransition>
                </TransitionGroup>
            </div>
            <NavigationButtons currentStep={currentStep} numbersteps={6} handleStepChange={handleStepChange} />
        </div>
    );
}

export default Partitioning;
