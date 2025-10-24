import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

function PostDetailPage() {
  const [post, setPost] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id } = useParams(); // Gets the 'id' from the URL

  useEffect(() => {
    // Fetch the single post
    fetch(`http://127.0.0.1:8000/api/posts/${id}/`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Post not found');
        }
        return response.json();
      })
      .then(data => {
        setPost(data);
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);
        setLoading(false);
      });
  }, [id]); // Re-run this effect if the 'id' changes

  if (loading) return <div className="loading">Loading post...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!post) return null;

  // We'll add this later
  const isOwner = true; // TODO: Check if logged-in user is post.author.id

  return (
    <div className="post-detail">
      <h2>{post.title}</h2>
      <p>By {post.author.username} | {new Date(post.created_at).toLocaleDateString()}</p>
      
      {/* We use dangerouslySetInnerHTML to render HTML content from the API */}
      {/* This assumes your post.content is safe HTML. Be careful with this! */}
      <div className="post-content" dangerouslySetInnerHTML={{ __html: post.content.replace(/\n/g, '<br />') }} />
      
      {isOwner && (
        <div style={{margin: '20px 0', padding: '15px', backgroundColor: '#f0f0f0', borderRadius: '5px'}}>
          <h4>Post Actions</h4>
          <Link to={`/posts/${post.id}/edit`} style={{backgroundColor: '#007bff', color: 'white', padding: '8px 16px', textDecoration: 'none', borderRadius: '4px', marginRight: '10px'}}>✏️ Edit Post</Link>
          <Link to={`/posts/${post.id}/delete`} style={{backgroundColor: '#dc3545', color: 'white', padding: '8px 16px', textDecoration: 'none', borderRadius: '4px'}}>🗑️ Delete Post</Link>
        </div>
      )}
      
      <hr />
      <p><Link to="/posts">← Back to all posts</Link></p>
    </div>
  );
}

export default PostDetailPage;