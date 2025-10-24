import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

function RegisterPage() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState(null);
  const navigate = useNavigate(); // For redirecting

  const handleSubmit = (e) => {
    e.preventDefault();
    
    const data = {
      username: username,
      email: email,
      first_name: firstName,
      last_name: lastName,
      password: password
    };
    
    // We must use the full URL to our backend
    fetch('http://127.0.0.1:8000/api/auth/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        setMessage(`<div class="success-message">✅ ${data.message}</div>`);
        setTimeout(() => {
          navigate('/login'); // Redirect to login page
        }, 1000);
      } else {
        // Handle errors (e.g., username taken)
        const errorMsg = Object.values(data).join(' ');
        setMessage(`<div class="error">❌ Registration failed: ${errorMsg}</div>`);
      }
    })
    .catch(error => {
      setMessage('<div class="error">❌ Error during registration.</div>');
    });
  };

  return (
    <>
      <h2>📝 Register</h2>
      <p style={{textAlign: 'center', color: '#666', fontSize: '1.1rem', marginBottom: '2rem'}}>
        Join our community and start sharing your stories
      </p>

      <div className="form-container">
        <form id="register-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="username">👤 Username:</label>
            <input type="text" id="username" name="username" required 
                   value={username} onChange={e => setUsername(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="email">📧 Email:</label>
            <input type="email" id="email" name="email" required 
                   value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="first_name">👋 First Name:</label>
            <input type="text" id="first_name" name="first_name" 
                   value={firstName} onChange={e => setFirstName(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="last_name">👋 Last Name:</label>
            <input type="text" id="last_name" name="last_name" 
                   value={lastName} onChange={e => setLastName(e.target.value)} />
          </div>
          <div className="form-group">
            <label htmlFor="password">🔒 Password:</label>
            <input type="password" id="password" name="password" required 
                   value={password} onChange={e => setPassword(e.target.value)} />
          </div>
          <div className="form-actions">
            <button type="submit" className="btn">🚀 Register</button>
          </div>
        </form>

        <div id="message" dangerouslySetInnerHTML={{ __html: message }}></div>

        <div className="form-link">
          <p>Already have an account? <Link to="/login">🔑 Login here</Link></p>
        </div>
      </div>
    </>
  );
}

export default RegisterPage;