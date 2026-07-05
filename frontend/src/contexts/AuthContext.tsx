import { createContext, useContext, useState } from 'react';
import type { ReactNode } from 'react';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (tokenData: { access_token: string, refresh_token: string }, userData: User) => void;
  logout: () => void;
  stepUpAuth: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const getInitialUser = (): User | null => {
    try {
      const stored = localStorage.getItem('user');
      return stored ? JSON.parse(stored) : null;
    } catch {
      return null;
    }
  };

  const [user, setUser] = useState<User | null>(getInitialUser);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(!!localStorage.getItem('accessToken'));

  const login = (tokenData: { access_token: string, refresh_token: string }, userData: User) => {
    localStorage.setItem('accessToken', tokenData.access_token);
    localStorage.setItem('refreshToken', tokenData.refresh_token);
    localStorage.setItem('user', JSON.stringify(userData));
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
    setUser(null);
    setIsAuthenticated(false);
  };

  const stepUpAuth = async () => {
    // In a real app, this would trigger an MPIN modal.
    return new Promise<boolean>((resolve) => {
      const pin = prompt("Enter MPIN for Step-Up Authentication (Try '1234'):");
      if (pin === '1234') {
        resolve(true);
      } else {
        alert("Incorrect PIN.");
        resolve(false);
      }
    });
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout, stepUpAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

