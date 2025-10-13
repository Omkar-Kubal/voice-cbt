import { useState, useEffect } from 'react';
import { 
  signInWithPopup, 
  signOut, 
  onAuthStateChanged, 
  User,
  GoogleAuthProvider
} from 'firebase/auth';
import { auth, googleProvider } from '@/lib/firebase';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
}

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    loading: true,
    error: null
  });

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setAuthState({
        user,
        loading: false,
        error: null
      });
    });

    return () => unsubscribe();
  }, []);

  const signInWithGoogle = async () => {
    try {
      setAuthState(prev => ({ ...prev, loading: true, error: null }));
      const result = await signInWithPopup(auth, googleProvider);
      
      // Send user data to backend
      if (result.user) {
        await syncUserWithBackend(result.user);
        
        // Create user session for our app
        const userData = {
          id: result.user.uid,
          email: result.user.email || '',
          name: result.user.displayName || result.user.email?.split('@')[0] || 'User',
          isNewUser: result.user.metadata.creationTime === result.user.metadata.lastSignInTime
        };
        
        // Store in our session system
        localStorage.setItem('voice_cbt_user', JSON.stringify(userData));
        localStorage.setItem('voice_cbt_session', 'active');
      }
      
      setAuthState(prev => ({ ...prev, loading: false }));
      return result.user;
    } catch (error: any) {
      console.error('Google sign-in error:', error);
      
      // Handle specific Firebase errors
      let errorMessage = 'Failed to sign in with Google';
      if (error.code === 'auth/popup-closed-by-user') {
        errorMessage = 'Sign-in cancelled. Please try again.';
      } else if (error.code === 'auth/popup-blocked') {
        errorMessage = 'Popup blocked. Please allow popups and try again.';
      } else if (error.code === 'auth/cancelled-popup-request') {
        errorMessage = 'Sign-in cancelled. Please try again.';
      } else if (error.code === 'auth/account-exists-with-different-credential') {
        errorMessage = 'An account already exists with this email using a different sign-in method.';
      } else if (error.message) {
        errorMessage = error.message;
      }
      
      setAuthState(prev => ({ 
        ...prev, 
        loading: false, 
        error: errorMessage 
      }));
      throw error;
    }
  };

  const logout = async () => {
    try {
      setAuthState(prev => ({ ...prev, loading: true, error: null }));
      await signOut(auth);
      
      // Clear our app session
      localStorage.removeItem('voice_cbt_user');
      localStorage.removeItem('voice_cbt_session');
      localStorage.removeItem('voice_cbt_conversations');
      
      setAuthState(prev => ({ ...prev, loading: false }));
    } catch (error: any) {
      const errorMessage = error.message || 'Failed to sign out';
      setAuthState(prev => ({ 
        ...prev, 
        loading: false, 
        error: errorMessage 
      }));
      throw error;
    }
  };

  return {
    ...authState,
    signInWithGoogle,
    logout
  };
};

// Sync user data with backend
const syncUserWithBackend = async (user: User) => {
  try {
    const response = await fetch('/api/v1/auth/sync', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
        provider: 'google'
      })
    });

    if (!response.ok) {
      throw new Error('Failed to sync user with backend');
    }

    return await response.json();
  } catch (error) {
    console.error('Error syncing user with backend:', error);
    // Don't throw here - authentication should still work even if sync fails
  }
};
