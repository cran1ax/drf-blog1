import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(localStorage.getItem('accessToken'));
  const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken'));
  const [user, setUser] = useState(null);

  useEffect(() => {
    if (accessToken) {
      localStorage.setItem('accessToken', accessToken);
      
      // Fetch the user's profile so we know who is logged in
      fetch('http://127.0.0.1:8000/api/auth/profile/', {
        headers: {
          'Authorization': `Bearer ${accessToken}`
        }
      })
      .then(res => {
        if (!res.ok) throw new Error("Invalid token");
        return res.json();
      })
      .then(data => setUser(data)) // Set the user data
      .catch(() => logout()); // If token is bad, log out
    } else {
      localStorage.removeItem('accessToken');
      setUser(null); // Clear user data
    }
  }, [accessToken]); // Re-run this effect when accessToken changes

  useEffect(() => {
    if (refreshToken) {
      localStorage.setItem('refreshToken', refreshToken);
    } else {
      localStorage.removeItem('refreshToken');
    }
  }, [refreshToken]);

  const login = (access, refresh) => {
    setAccessToken(access);
    setRefreshToken(refresh);
  };

  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
  };

  // Your app now knows you're logged in if you have a token
  const isAuthenticated = !!accessToken; 

  const value = {
    user,
    isAuthenticated,
    accessToken,
    login,
    logout
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  return useContext(AuthContext);
};