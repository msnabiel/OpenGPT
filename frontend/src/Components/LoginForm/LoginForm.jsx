import React, { useState, useEffect } from "react";
import './LoginForm.css';
import { FaLock, FaUser } from "react-icons/fa";
import { Link } from 'react-router-dom';
import { auth } from './firebaseConfig'; // Import your Firebase config
import { signInWithEmailAndPassword } from 'firebase/auth';

const LoginForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [countdown, setCountdown] = useState(null); // State for countdown timer
    const [redirectUrl, setRedirectUrl] = useState(''); // State for redirect URL

    useEffect(() => {
        document.title = 'Login | Nabiel';
    }, []);

    useEffect(() => {
        let timer;
        if (countdown !== null && countdown > 0) {
            timer = setInterval(() => {
                setCountdown((prev) => prev - 1);
            }, 1000); // Update countdown every second
        } else if (countdown === 0) {
            window.location.href = redirectUrl; // Redirect when countdown reaches 0
        }
        return () => clearInterval(timer); // Cleanup interval on component unmount or when countdown changes
    }, [countdown, redirectUrl]);

    const handleLogin = async (e) => {
        e.preventDefault();
        setError(''); // Clear any previous errors
        setCountdown(null); // Clear any previous countdown
        setRedirectUrl(''); // Clear any previous redirect URL

        try {
            // Sign in with Firebase
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const userId = userCredential.user.uid; // Get the user ID from Firebase

            // Send user ID to Flask server
            const response = await fetch('http://127.0.0.1:7000', {
                method: 'POST', // Use POST method
                headers: {
                    'Content-Type': 'application/json' // Set content type to JSON
                },
                body: JSON.stringify({ user_id: userId }) // Send user_id in the request body
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Parse JSON response
            const data = await response.json();
            console.log('Success:', data); // Handle the response data

            if (data.redirect_url) {
                // Set redirect URL and start countdown
                setRedirectUrl(data.redirect_url);
                setCountdown(5); // Start countdown from 5 seconds
            } else {
                console.error('Redirect URL not found in response');
            }
        } catch (err) {
            console.error('Login error:', err);
            setError('Invalid email or password');
        }
    };

    return (
        <div className="wrapper">
            <form onSubmit={handleLogin}>
                <h1>Login</h1>
                {error && <p className="error-message">{error}</p>}
                <div className="input-box">
                    <input
                        type="text"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <FaUser className='icon' />
                </div>
                <div className="input-box">
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <FaLock className='icon' />
                </div>
                <div className="remember-forgot">
                    <label>
                        <input type="checkbox" /> Remember me
                    </label>
                    <a href="#">Forgot Password?</a>
                </div>
                <button type="submit">Login</button>
                {countdown !== null && (
                    <div className="countdown-message">
                        Redirecting in {countdown} seconds...
                    </div>
                )}
                <div className="register-link">
                    <p>Don't have an account? <Link to="/signup">Sign Up</Link></p>
                </div>
            </form>
        </div>
    );
};

export default LoginForm;