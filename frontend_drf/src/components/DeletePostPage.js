import React, { useState, useEffect } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // 1. Import useAuth

function DeletePostPage() {
  const [post, setPost] = useState(null);
  const [error, setError] = useState(null);
  const { id } = useParams();
  const navigate = useNavigate();
  const { accessToken } = useAuth(); // 2. Get the access token

  // 1. Fetch current post data for confirmation (public)
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/api/posts/${id}/`)
      .then(response => {
        if (!response.ok) throw new Error('Post not found.');
        return response.json();
      })
      .then(data => {
        setPost(data);
      })
      .catch(error => setError(error.message));
  }, [id]);

  // 2. Handle the delete button click
  const handleDelete = () => {
    fetch(`http://127.0.0.1:8000/api/posts/${id}/delete/`, {
      method: 'DELETE',
      headers: {
        // 3. Add the Authorization header
        'Authorization': `Bearer ${accessToken}`
      }
      // 4. 'credentials: include' is GONE
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Delete failed. You may not be the author.');
      }
      // 204 No Content is a successful delete
      if (response.status === 204) {
        navigate('/'); // Navigate to homepage
      } else {
        return response.json();
      }
    })
    .catch(error => {
      setError(error.message);
    });
  };

  if (error) return <div className="error">{error}</div>
  if (!post) return <div className="loading">Loading post...</div>

  return (
    <>
      <h2>🗑️ Delete Post</h2>
      <div style={{backgroundColor: '#ffe6e6', border: '1px solid #ff9999', padding: '20px', borderRadius: '5px', marginBottom: '20px'}}>
        <h3>⚠️ Are you sure you want to delete this post?</h3>
        <p><strong>Title:</strong> {post.title}</p>
        <p><strong>Author:</strong> {post.author.username}</p>
        <p><strong>Created:</strong> {new Date(post.created_at).toLocaleDateString()}</p>
        <p style={{color: '#cc0000'}}><strong>This action cannot be undone!</strong></p>
      </div>
      
      <div>
        <button 
          onClick={handleDelete} 
          className="btn" 
          style={{backgroundColor: '#cc0000'}}>
          Yes, Delete Post
        </button>
        <Link 
          to={`/posts/${post.id}`} 
          className="btn" 
          style={{marginLeft: '10px', backgroundColor: '#666'}}>
          Cancel
        </Link>
      </div>
    </>
  );
}

export default DeletePostPage;