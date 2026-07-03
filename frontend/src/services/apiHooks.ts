import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import * as mockData from './mockData';

const isDemoMode = () => localStorage.getItem('nirnay_demo_mode') === 'true';

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

// --- ACCOUNTS ---
export const useAccounts = () => {
  return useQuery({
    queryKey: ['accounts'],
    queryFn: async () => {
      if (isDemoMode()) return { balance: 245000, activeAccounts: 3 };
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
      if (isDemoMode()) return mockData.mockRecipients;
      const { data } = await api.get('/recipients');
      return data;
    }
  });
};

// --- TRANSACTIONS ---
export const useTransfer = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: any) => {
      if (isDemoMode()) {
        return {
          transaction: { id: "DEMO-TX", ...payload },
          risk_evaluation: { risk_score: 10, confidence: 99, recommended_action: "Proceed", evidence: [] },
          message: "Demo transfer approved."
        };
      }
      const { data } = await api.post('/transactions/transfer', payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['accounts'] });
      queryClient.invalidateQueries({ queryKey: ['risk-history'] });
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
    }
  });
};

export const useTransactions = () => {
  return useQuery({
    queryKey: ['transactions'],
    queryFn: async () => {
      if (isDemoMode()) return mockData.mockTransactions;
      const { data } = await api.get('/transactions/history');
      return data;
    }
  });
};

export const useSecurityMetrics = () => {
  return useQuery({
    queryKey: ['security'],
    queryFn: async () => {
      if (isDemoMode()) return mockData.mockSecurityMetrics;
      const { data } = await api.get('/users/security');
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
      if (isDemoMode()) return {
        risk_score: 10,
        risk_level: "LOW",
        confidence: 99,
        recommended_action: "Proceed",
        reason_codes: ["DEMO-RULE-1"]
      };
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
      const { data } = await api.get('/analytics/summary');
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
