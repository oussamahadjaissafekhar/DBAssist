// src/components/Sidebar.js
import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { disconnectFromDatabase } from '../api'; // Import the API function

function Sidebar() {
    const location = useLocation();
    const navigate = useNavigate();

    const handleDisconnect = async () => {
        try {
            await disconnectFromDatabase(); // Call the API to disconnect
            
            // Replace the current entry with the home route and set up history
            navigate('/', { replace: true });
            
            // Additionally, you might want to force a refresh to clear potential state
            window.location.reload(); // Optional: Only if you need to reset application state
        } catch (error) {
            console.error('Error disconnecting:', error);
            // Handle error if needed (e.g., show an error message)
        }
    };

    return (
        <div style={sidebarStyle}>
            <div style={logoContainerStyle}>
                <img src={require('../icons/Logo.png')} alt="DBAssist Logo" style={logoStyle} />
            </div>
            <div style={linksContainerStyle}>
                <Link 
                    to="/partition" 
                    style={{
                        ...linkStyle, 
                        ...(location.pathname === '/partition' && activeLinkStyle)
                    }}
                >
                    <img 
                        src={
                            location.pathname === '/partition' 
                            ? require('../icons/seperated lists blue.png') 
                            : require('../icons/seperated lists white.png')
                        } 
                        alt="" 
                        style={iconPlaceholder} 
                    />
                    Partitioning tool
                </Link>
                <Link 
                    to="/index" 
                    style={{
                        ...linkStyle, 
                        ...(location.pathname === '/index' && activeLinkStyle)
                    }}
                >
                    <img 
                        src={
                            location.pathname === '/index' 
                            ? require('../icons/list-start blue.png') 
                            : require('../icons/list-start white.png')
                        } 
                        alt="" 
                        style={iconPlaceholder} 
                    />
                    Indexing tool
                </Link>
            </div>
            <div style={buttonsContainerStyle}>
                <button style={aboutButtonStyle}>
                    <img 
                        src={require('../icons/about.png')} 
                        alt="" 
                        style={iconPlaceholder} 
                    />
                    About DBAssist
                </button>
                <button 
                    style={disconnectButtonStyle}
                    onClick={handleDisconnect} // Handle disconnect on button click
                >
                    Disconnect
                </button>
            </div>
        </div>
    );
}

const sidebarStyle = {
    position: 'fixed',
    left: 0,
    top: 0,
    width: '200px',
    height: '100vh',
    backgroundColor: '#00113D',
    color: 'white',
    display: 'flex',
    flexDirection: 'column',
    padding: '20px',
    boxShadow: '-2px 0 5px rgba(0,0,0,0.3)',
};

const logoContainerStyle = {
    marginBottom: '20px',
    textAlign: 'center',
};

const logoStyle = {
    width: '150px',
    height: 'auto',
};

const linksContainerStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'start',
    marginTop: '200px',
};

const linkStyle = {
    color: 'white',
    textDecoration: 'none',
    fontSize: '15px',
    marginBottom: '15px',
    textAlign: 'center',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '10px 5px',
    borderRadius: '5px',
    transition: 'all 0.3s ease', // Smooth transition for hover effect
};

const activeLinkStyle = {
    backgroundColor: 'white',
    color: '#00113D',
};

const buttonsContainerStyle = {
    marginTop: 'auto',
    paddingBottom: '50px',
};

const aboutButtonStyle = {
    backgroundColor: '#00113D',
    color: 'white',
    border: '1px solid white',
    padding: '10px',
    borderRadius: '5px',
    cursor: 'pointer',
    width: '100%',
    marginBottom: '10px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.3s ease', // Smooth transition for hover effect
    fontFamily: "'Trispace', sans-serif"
};

const disconnectButtonStyle = {
    backgroundColor: 'red',
    color: 'white',
    border: '1px solid white',
    padding: '10px',
    borderRadius: '5px',
    cursor: 'pointer',
    width: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.3s ease', // Smooth transition for hover effect
    fontFamily: "'Trispace', sans-serif"
};

const iconPlaceholder = {
    width: '20px',
    height: '20px',
    marginRight: '10px',
};

export default Sidebar;
