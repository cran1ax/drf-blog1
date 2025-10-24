import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function LogoutPage() {
  const navigate = useNavigate();
  const { logout } = useAuth(); // Get the logout function from context

  useEffect(() => {
    logout(); // Clear the tokens from state and localStorage
    navigate('/'); // Redirect to homepage
  }, [logout, navigate]);

  // Nothing to render, it just redirects
  return null; 
}

export default LogoutPage;