import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  const [recentPosts, setRecentPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch recent posts from your API
    fetch('http://127.0.0.1:8000/api/recent-posts/')
      .then(response => response.json())
      .then(data => {
        setRecentPosts(data);
        setLoading(false);
      })
      .catch(error => {
        setError('Error fetching recent posts.');
        setLoading(false);
      });
  }, []); // The empty array [] means this runs only once when the component mounts

  return (
    <>
      <h2>🌟 Welcome to Django Blog</h2>
      <p style={{textAlign: 'center', color: '#666', fontSize: '1.1rem', marginBottom: '2rem'}}>
        Discover amazing stories, share your thoughts, and connect with our community
      </p>

      <h3>📰 Recent Posts</h3>
      <div id="recent-posts">
        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error">📭 {error}</div>}
        
        {recentPosts.length > 0 ? (
          recentPosts.map(post => (
            <div className="post-card" key={post.id}>
              {/* Use Link for navigation */}
              <h4><Link to={`/posts/${post.id}`}>{post.title}</Link></h4>
              <div className="post-meta">
                {/* Note: 'post.author.username' works because your serializer nests the UserSerializer */}
                👤 By {post.author.username} | 📅 {new Date(post.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        ) : (
          !loading && <div className="error">📭 No recent posts found.</div>
        )}
      </div>
    </>
  );
}

export default HomePage;