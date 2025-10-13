import React, { createContext, useContext, ReactNode } from 'react';
import { useUserSession } from '@/hooks/useUserSession';

interface User {
  id: string;
  email: string;
  name: string;
  isNewUser?: boolean;
}

interface UserSessionContextType {
  user: User | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (userData: User) => void;
  logout: () => void;
  updateUser: (userData: Partial<User>) => void;
}

const UserSessionContext = createContext<UserSessionContextType | undefined>(undefined);

interface UserSessionProviderProps {
  children: ReactNode;
}

export const UserSessionProvider: React.FC<UserSessionProviderProps> = ({ children }) => {
  const userSession = useUserSession();

  return (
    <UserSessionContext.Provider value={userSession}>
      {children}
    </UserSessionContext.Provider>
  );
};

export const useUserSessionContext = (): UserSessionContextType => {
  const context = useContext(UserSessionContext);
  if (context === undefined) {
    throw new Error('useUserSessionContext must be used within a UserSessionProvider');
  }
  return context;
};
