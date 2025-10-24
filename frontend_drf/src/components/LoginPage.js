import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(null);
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    fetch('http://127.0.0.1:8000/api/token/', { // <-- 1. URL is new
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // 2. We no longer use 'credentials: include'
      body: JSON.stringify({ username, password })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Login failed');
      }
      return response.json();
    })
    .then(data => {
      // 3. We get 'access' and 'refresh' tokens, not a 'user' object
      if (data.access && data.refresh) {
        setMessage(`<div class="success-message">✅ Login successful</div>`);
        
        login(data.access, data.refresh); // 4. Save BOTH tokens to context
        
        setTimeout(() => {
          navigate('/'); // Redirect to homepage
        }, 1000);
      } else {
        setMessage('<div class="error">❌ Login failed. Please check your credentials.</div>');
      }
    })
    .catch(error => {
      setMessage(`<div class="error">❌ ${error.message}</div>`);
    });
  };

  return (
    <>
      <h2>🔑 Login</h2>
      <p style={{textAlign: 'center', color: '#666', fontSize: '1.1rem', marginBottom: '2rem'}}>
        Welcome back! Sign in to your account
      </p>

      <div className="form-container">
        <form id="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">👤 Username:</label>
            <input 
              type="text" 
              id="username" 
              name="username" 
              required 
              value={username} 
              onChange={e => setUsername(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="password">🔒 Password:</label>
            <input 
              type="password" 
              id="password" 
              name="password" 
              required 
              value={password}
              onChange={e => setPassword(e.target.value)}
            />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn">🚀 Login</button>
          </div>
        </form>

        <div id="message" dangerouslySetInnerHTML={{ __html: message }}></div>

        <div className="form-link">
          <p>Don't have an account? <Link to="/register">📝 Register here</Link></p>
        </div>
      </div>
    </>
  );
}

export default LoginPage;