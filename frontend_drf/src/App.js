import React from 'react';
import { Routes, Route } from 'react-router-dom';

// 1. Import all your components
import Layout from './components/Layout';
import LoginPage from './components/LoginPage';
import RegisterPage from './components/RegisterPage';
import HomePage from './components/HomePage';
import PostsPage from './components/PostsPage';
import PostDetailPage from './components/PostDetailPage';
import ProfilePage from './components/ProfilePage';
import CreatePostPage from './components/CreatePostPage';
import UpdatePostPage from './components/UpdatePostPage';
import DeletePostPage from './components/DeletePostPage';
import LogoutPage from './components/LogoutPage';


function App() {
  return (
    // 2. This <Routes> component handles all the routing
    <Routes>
      {/* 3. This is the "parent" route. It shows the Layout (header/footer) */}
      <Route path="/" element={<Layout />}>
        
        {/* 4. These are your "child" pages */}
        <Route index element={<HomePage />} />
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="posts" element={<PostsPage />} />
        <Route path="posts/:id" element={<PostDetailPage />} />
        <Route path="profile" element={<ProfilePage />} />
        <Route path="create-post" element={<CreatePostPage />} />
        <Route path="posts/:id/edit" element={<UpdatePostPage />} />
        <Route path="posts/:id/delete" element={<DeletePostPage />} />
        <Route path="logout" element={<LogoutPage />} /> 

      </Route>
    </Routes>
  );
}

export default App;