import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';

// --- AUTH ---
export const useLogin = () => {
  return useMutation({
    mutationFn: async (credentials: any) => {
      // Backend expects form-data for OAuth2PasswordRequestForm
      const formData = new URLSearchParams();
      formData.append('username', credentials.email);
      formData.append('password', credentials.password);
      
      const { data: tokenData } = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      
      // Fetch user profile immediately after getting token
      const { data: userData } = await api.get('/users/me', {
        headers: {
          'Authorization': `Bearer ${tokenData.access_token}`
        }
      });
      
      return { tokenData, userData };
    }
  });
};

export const useUser = () => {
  return useQuery({
    queryKey: ['user'],
    queryFn: async () => {
      const { data } = await api.get('/users/me');
      return data;
    },
    retry: false
  });
};

export const useUserBehavior = () => {
  return useQuery({
    queryKey: ['user-behavior'],
    queryFn: async () => {
      const { data } = await api.get('/users/me/behavior');
      return data;
    }
  });
};

// --- ACCOUNTS ---
export const useAccounts = () => {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: async () => {
      const { data } = await api.get('/accounts/summary');
      return data;
    }
  });
};

// --- RECIPIENTS ---
export const useRecipients = () => {
  return useQuery({
    queryKey: ['recipients'],
    queryFn: async () => {
      const { data } = await api.get('/recipients');
      return data;
    }
  });
};

// --- TRANSACTIONS ---
export const useTransfer = () => {
  return useMutation({
    mutationFn: async (payload: any) => {
      const { data } = await api.post('/transactions/transfer', payload);
      return data;
    },
    onSuccess: () => {
      // Invalidation moved to useAuthenticateTransaction since /transfer only analyzes now
    }
  });
};

export const useChat = () => {
  return useMutation({
    mutationFn: async (payload: { message: string; transactionId?: string }) => {
      const { data } = await api.post('/conversation/chat', payload);
      return data;
    }
  });
};

export const useAuthenticateTransaction = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (transactionId: string) => {
      const { data } = await api.post(`/transactions/${transactionId}/authenticate`);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['risk-history'] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      queryClient.invalidateQueries({ queryKey: ['security'] });
      queryClient.invalidateQueries({ queryKey: ['analytics'] });
      queryClient.invalidateQueries({ queryKey: ['user-behavior'] });
    }
  });
};

export const useTransactions = () => {
  return useQuery({
    queryKey: ['transactions'],
    queryFn: async () => {
      const { data } = await api.get('/transactions/history');
      return data;
    }
  });
};

export const useSecurityMetrics = () => {
  return useQuery({
    queryKey: ['security'],
    queryFn: async () => {
      const { data } = await api.get('/risk/metrics');
      return data;
    }
  });
};

// --- RISK & ANALYTICS ---
export const useRiskHistory = () => {
  return useQuery({
    queryKey: ['risk-history'],
    queryFn: async () => {
      const { data } = await api.get('/risk/history');
      return data;
    }
  });
};

export const useRiskReport = (transactionId: string) => {
  return useQuery({
    queryKey: ['risk-report', transactionId],
    queryFn: async () => {
      const { data } = await api.get(`/risk/report/${transactionId}`);
      return data;
    },
    enabled: !!transactionId
  });
};

export const useAnalytics = () => {
  return useQuery({
    queryKey: ['analytics'],
    queryFn: async () => {
      const { data } = await api.get('/analytics/dashboard');
      return data;
    }
  });
};

// --- ADMIN ---
export const useAdminStats = () => {
  return useQuery({
    queryKey: ['admin-stats'],
    queryFn: async () => {
      const { data } = await api.get('/admin/system-stats');
      return data;
    }
  });
};
