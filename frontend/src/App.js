import logo from './logo.svg';
import './App.css';
import LoginForm from './Components/LoginForm/LoginForm';
import SignUpForm from './Components/SignUpForm/SignUpForm'
import React, { useEffect } from 'react';
import { Route, Routes } from 'react-router-dom';
import EmailForm from './Components/EmailV/emailForm';

function App() {
  

  return (
    
    <div>
      <Routes>
        <Route path='/' element={<LoginForm/>} />
        <Route path='/login' element={<LoginForm/>} />
        <Route path='/signup' element={<SignUpForm/>} />
        <Route path='/mail' element={<EmailForm/>} />
      </Routes>
    </div>
  );
}

export default App;
