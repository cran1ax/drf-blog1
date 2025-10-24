import React from 'react';
import { Outlet, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext'; // 1. Import the hook

function Layout() {
  const { isAuthenticated } = useAuth(); // 2. Get the real auth state from context

  return (
    <>
      <header>
        <div className="container">
          <div className="header-content">
            <div className="logo">
              <Link to="/"><h1>📝 Django Blog</h1></Link>
            </div>
            <nav>
              <Link to="/">🏠 Home</Link>
              <Link to="/posts">📄 All Posts</Link>
              
              {/* 3. This logic will now check your global state! */}
              {isAuthenticated ? (
                <>
                  <Link to="/profile">👤 Profile</Link>
                  <Link to="/create-post">✍️ Create Post</Link>
                  <Link to="/logout">🚪 Logout</Link>
                </>
              ) : (
                <>
                  <Link to="/login">🔑 Login</Link>
                  <Link to="/register">📝 Register</Link>
                </>
              )}
            </nav>
          </div>
        </div>
      </header>
      
      <main>
        <div className="container">
          <div className="content-wrapper">
            <Outlet />
          </div>
        </div>
      </main>
      
      <footer>
        <div className="container">
          <p>✨ Django Blog API - Beautiful Frontend ✨</p>
        </div>
      </footer>
    </>
  );
}

export default Layout;