import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext'; // 1. Import useAuth

function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState(null);
  const { accessToken } = useAuth(); // 2. Get the access token

  // 1. Fetch current profile data on load
  useEffect(() => {
    // Only fetch if we have a token
    if (accessToken) {
      fetch('http://127.0.0.1:8000/api/auth/profile/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // 3. Add Authorization header
          'Authorization': `Bearer ${accessToken}`
        }
      })
      .then(response => {
        if (!response.ok) {
          throw new Error('Error loading profile.');
        }
        return response.json();
      })
      .then(data => {
        setProfile(data);
        setFirstName(data.first_name || '');
        setLastName(data.last_name || '');
        setEmail(data.email || '');
      })
      .catch(error => {
        setMessage(`<div class="error">❌ ${error.message}</div>`);
      });
    }
  }, [accessToken]); // 4. Re-run if accessToken changes

  // 2. Handle the form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const data = {
      first_name: firstName,
      last_name: lastName,
      email: email
    };
    
    fetch('http://127.0.0.1:8000/api/auth/profile/update/', {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        // 5. Add Authorization header
        'Authorization': `Bearer ${accessToken}`
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.message) {
        setMessage(`<div class="success-message">✅ ${data.message}</div>`);
        setProfile(data.user); // Update profile with new data
      } else {
        setMessage('<div class="error">❌ Error updating profile.</div>');
      }
    })
    .catch(error => {
      setMessage('<div class="error">❌ Error updating profile.</div>');
    });
  };

  return (
    <>
      <h2>User Profile</h2>
      <div id="profile-info">
        {profile ? (
          <>
            <p><strong>Username:</strong> {profile.username}</p>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>Name:</strong> {profile.first_name} {profile.last_name}</p>
          </>
        ) : (
          <p>Loading profile...</p>
        )}
      </div>

      <h3>Update Profile</h3>
      <form id="update-profile-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="first_name">First Name:</label><br />
          <input type="text" id="first_name" name="first_name" 
                 value={firstName} onChange={e => setFirstName(e.target.value)} />
        </div>
        <div className="form-group">
          <label htmlFor="last_name">Last Name:</label><br />
          <input type="text" id="last_name" name="last_name" 
                 value={lastName} onChange={e => setLastName(e.target.value)} />
        </div>
        <div className="form-group">
          <label htmlFor="email">Email:</label><br />
          <input type="email" id="email" name="email" 
                 value={email} onChange={e => setEmail(e.target.value)} />
        </div>
        <div className="form-actions">
          <button type="submit" className="btn">Update Profile</button>
        </div>
      </form>

      <div id="message" dangerouslySetInnerHTML={{ __html: message }}></div>
    </>
  );
}

export default ProfilePage;