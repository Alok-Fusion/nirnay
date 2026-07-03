import { createContext, useContext, useState, ReactNode } from 'react';
import { api } from '../services/api';

interface User {
  id: string;
  name: string;
  email: string;
}

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  login: (token: string, userData: User) => void;
  logout: () => void;
  stepUpAuth: () => Promise<boolean>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);

  const login = (token: string, userData: User) => {
    localStorage.setItem('accessToken', token);
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
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
