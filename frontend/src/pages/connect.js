// src/pages/connect.js
import React, { useState, useContext } from 'react';
import { connectToDatabase } from '../api';
import { useNavigate } from 'react-router-dom';
import { DbContext } from '../DbContext';

function Connect({ onConnect }) {
    const [dbname, setDbname] = useState('');
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [notification, setNotification] = useState('');
    const navigate = useNavigate(); // Hook for navigation
    const { setDbName } = useContext(DbContext);

    const handleConnect = async () => {
        const credentials = { dbname, user, password };
        try {
            console.log("credentials : ", credentials);
            const response = await connectToDatabase(credentials);
            setNotification('Connected successfully!');
            setDbName(dbname);

            // Show the notification for a short time, then navigate
            setTimeout(() => {
                navigate('/partition', {replace: true });
            }, 3000);

            onConnect(response);
        } catch (error) {
            setNotification('Failed to connect. Please check your credentials.');
            console.log(error)
        }

        // Hide the notification after 3 seconds if it's not successful
        if (!notification.startsWith('Connected')) {
            setTimeout(() => setNotification(''), 3000); // Hide after 3 seconds
        }
    };

    return (
        <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100vh',
        }}>
            <h1 style={{ color: '#00113D', fontFamily: 'Trispace' }}>Enter your DB credentials</h1>
            <div style={{ margin: '10px 0', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <label style={{ marginBottom: '5px' }}>DB name</label>
                <input
                    style={{ margin: '0', padding: '10px', width: '300px', height: '30px', border: '1px solid #000000', background: '#EFEFEF', borderRadius: '10px' }}
                    type="text"
                    placeholder="DB Name"
                    value={dbname}
                    onChange={(e) => setDbname(e.target.value)}
                />
            </div>
            <div style={{ margin: '10px 0', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <label style={{ marginBottom: '5px' }}>User</label>
                <input
                    style={{ margin: '0', padding: '10px', width: '300px', height: '30px', border: '1px solid #000000', background: '#EFEFEF', borderRadius: '10px' }}
                    type="text"
                    placeholder="User"
                    value={user}
                    onChange={(e) => setUser(e.target.value)}
                />
            </div>
            <div style={{ margin: '10px 0', display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <label style={{ marginBottom: '5px' }}>Password</label>
                <input
                    style={{ margin: '0', padding: '10px', width: '300px', height: '30px', border: '1px solid #000000', background: '#EFEFEF', borderRadius: '10px' }}
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>
            <button
                style={{
                    marginTop: '40px',
                    padding: '10px 20px',
                    width: '150px',
                    backgroundColor: '#00113D',
                    color: 'white',
                    border: 'none',
                    borderRadius: '5px',
                    cursor: 'pointer',
                }}
                onClick={handleConnect}
            >
                Connect
            </button>

            {notification && (
                <div style={{
                    marginTop: '20px',
                    padding: '10px 20px',
                    backgroundColor: notification.startsWith('Connected') ? '#d4edda' : '#f8d7da',
                    color: notification.startsWith('Connected') ? '#155724' : '#721c24',
                    border: `1px solid ${notification.startsWith('Connected') ? '#c3e6cb' : '#f5c6cb'}`,
                    borderRadius: '5px',
                    width: '300px',
                    textAlign: 'center',
                }}>
                    {notification}
                </div>
            )}
        </div>
    );
}

export default Connect;
