import React, { useState, useEffect } from "react";
import './SignUpForm.css';
import { FaLock, FaUser } from "react-icons/fa";
import { Link, useNavigate } from 'react-router-dom';
import { auth } from '../../firebaseConfig'; // Import Firebase config
import { createUserWithEmailAndPassword } from 'firebase/auth';

const SignUpForm = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        document.title = 'Sign-Up | Nabiel';
    }, []);

    const handleSignup = async (e) => {
        e.preventDefault();
        setError('');
        try {
            await createUserWithEmailAndPassword(auth, email, password);
            navigate('/login');
        } catch (err) {
            if (err.code === 'auth/email-already-in-use') {
                setError('User already exists');
            } else {
                setError('An error occurred: ' + err.message);
            }
        }
    };

    return (
        <div className="wrapper">
            <form onSubmit={handleSignup}>
                <h1>Sign Up</h1>
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
                <button type="submit">Register</button>
                <div className="register-link">
                    <p>Have an account? <Link to="/login">Login</Link></p>
                </div>
            </form>
        </div>
    );
};

export default SignUpForm;