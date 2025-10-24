import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function PostsPage() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch ALL posts from your API
    fetch('http://127.0.0.1:8000/api/posts/')
      .then(response => response.json())
      .then(data => {
        // The data might be paginated (e.g., data.results)
        // Adjust if your API returns { count, next, previous, results }
        setPosts(data.results ? data.results : data); 
        setLoading(false);
      })
      .catch(error => {
        setError('Error fetching posts.');
        setLoading(false);
      });
  }, []);

  return (
    <>
      <h2>📄 All Posts</h2>
      <p style={{textAlign: 'center', color: '#666', fontSize: '1.1rem', marginBottom: '2rem'}}>
        Explore all the amazing content from our community
      </p>

      <div id="posts">
        {loading && <div className="loading">Loading...</div>}
        {error && <div className="error">📭 {error}</div>}
        
        {posts.length > 0 ? (
          posts.map(post => (
            <div className="post-card" key={post.id}>
              <h4><Link to={`/posts/${post.id}`}>{post.title}</Link></h4>
              <div className="post-meta">
                👤 By {post.author.username} | 📅 {new Date(post.created_at).toLocaleDateString()}
              </div>
            </div>
          ))
        ) : (
          !loading && <div className="error">📭 No posts found.</div>
        )}
      </div>
    </>
  );
}

export default PostsPage;