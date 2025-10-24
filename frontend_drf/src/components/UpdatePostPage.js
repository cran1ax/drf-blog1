import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // 1. Import useAuth

function UpdatePostPage() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();
  const navigate = useNavigate();
  const { accessToken } = useAuth(); // 2. Get the access token

  // 1. Fetch the current post data to populate the form
  // This fetch doesn't need auth, since anyone can read a post
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/posts/${id}/`)
      .then(response => {
        if (!response.ok) throw new Error('Post not found.');
        return response.json();
      })
      .then(data => {
        setTitle(data.title);
        setContent(data.content);
        setLoading(false);
      })
      .catch(error => setError(error.message));
  }, [id]);

  // 2. Handle the form submission to update the post
  const handleSubmit = (e) => {
    e.preventDefault();
    
    fetch(`http://127.0.0.1:8000/api/posts/${id}/update/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        // 3. Add the Authorization header
        'Authorization': `Bearer ${accessToken}` 
      },
      // 4. 'credentials: include' is GONE
      body: JSON.stringify({ title, content })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Update failed. You may not be the author.');
      }
      return response.json();
    })
    .then(data => {
      // Update was successful, navigate to the post's detail page
      navigate(`/posts/${data.id}`);
    })
    .catch(error => {
      setError(error.message);
    });
  };

  if (loading) return <div className="loading">Loading post to edit...</div>

  return (
    <>
      <h2>✏️ Edit Post</h2>
      
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
            <button type="submit" className="btn">Update Post</button>
            <Link to={`/posts/${id}`} style={{marginLeft: '10px'}}>Cancel</Link>
          </div>
        </form>
      </div>
    </>
  );
}

export default UpdatePostPage;