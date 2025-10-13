import { useState, useEffect } from 'react';

interface User {
  id: string;
  email: string;
  name: string;
  isNewUser?: boolean;
}

interface UserSession {
  user: User | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (userData: User) => void;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

export const useUserSession = (): UserSession => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on mount
    const checkSession = () => {
      try {
        const sessionActive = localStorage.getItem('voice_cbt_session');
        const userData = localStorage.getItem('voice_cbt_user');
        
        if (sessionActive === 'active' && userData) {
          const parsedUser = JSON.parse(userData);
          setUser(parsedUser);
          setIsLoggedIn(true);
        }
      } catch (error) {
        console.error('Error checking session:', error);
        // Clear invalid session data
        localStorage.removeItem('voice_cbt_session');
        localStorage.removeItem('voice_cbt_user');
      } finally {
        setIsLoading(false);
      }
    };

    checkSession();
  }, []);

  const login = (userData: User) => {
    setUser(userData);
    setIsLoggedIn(true);
    localStorage.setItem('voice_cbt_user', JSON.stringify(userData));
    localStorage.setItem('voice_cbt_session', 'active');
  };

  const logout = () => {
    setUser(null);
    setIsLoggedIn(false);
    localStorage.removeItem('voice_cbt_user');
    localStorage.removeItem('voice_cbt_session');
    // Clear conversation history
    localStorage.removeItem('voice_cbt_conversations');
  };

  const updateUser = (userData: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...userData };
      setUser(updatedUser);
      localStorage.setItem('voice_cbt_user', JSON.stringify(updatedUser));
    }
  };

  return {
    user,
    isLoggedIn,
    isLoading,
    login,
    logout,
    updateUser
  };
};
