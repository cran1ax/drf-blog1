import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function CreatePostPage() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const { accessToken } = useAuth();

  const handleSubmit = (e) => {
    e.preventDefault();
    
    fetch('http://127.0.0.1:8000/api/posts/create/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
        // 'X-CSRFToken': ... // We use session auth, so CSRF might be needed.
        // For now, Django session auth on a different port is tricky.
        // Your `authentication_classes = []` in the view might bypass this.
        // If not, we may need to switch to Token Authentication (JWT).
      },
      // This is VITAL for sending your login cookie
      body: JSON.stringify({ title, content })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('You must be logged in to create a post.');
      }
      return response.json();
    })
    .then(data => {
      // Creation was successful, navigate to the new post's detail page
      navigate(`/posts/${data.id}`);
    })
    .catch(error => {
      setError(error.message);
    });
  };

  return (
    <>
      <h2>✍️ Create New Post</h2>
      
      {error && (
        <div className="error">{error}</div>
      )}

      <div className="form-container" style={{maxWidth: '800px'}}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title:</label>
            <input 
              type="text" 
              id="title" 
              name="title" 
              required 
              value={title}
              onChange={e => setTitle(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="content">Content:</label>
            <textarea 
              id="content" 
              name="content" 
              rows="10" 
              required
              value={content}
              onChange={e => setContent(e.target.value)}
            ></textarea>
          </div>
          <div className="form-actions">
            <button type="submit" className="btn">Create Post</button>
          </div>
        </form>
      </div>
    </>
  );
}

export default CreatePostPage;