export interface MockTransaction {
  id: string;
  recipientName: string;
  amount: number;
  currency: string;
  date: string;
  status: 'COMPLETED' | 'PENDING' | 'BLOCKED' | 'CANCELLED';
  aiRiskScore: number;
}

export interface MockRecipient {
  id: string;
  name: string;
  accountMasked: string;
  bankCode: string;
  isTrusted: boolean;
}

export const mockRecipients: MockRecipient[] = [
  { id: 'REC-101', name: 'Alok Kumar', accountMasked: '****4598', bankCode: 'HDFC001', isTrusted: true },
  { id: 'REC-102', name: 'Binance Exchange', accountMasked: '****9901', bankCode: 'CRYP000', isTrusted: false },
  { id: 'REC-103', name: 'John Doe', accountMasked: '****1122', bankCode: 'SBIN001', isTrusted: false },
];

export const mockTransactions: MockTransaction[] = [
  { id: 'TX-1001', recipientName: 'Alok Kumar', amount: 500, currency: 'USD', date: '2026-07-02T10:00:00Z', status: 'COMPLETED', aiRiskScore: 2.5 },
  { id: 'TX-1002', recipientName: 'Binance Exchange', amount: 5000, currency: 'USD', date: '2026-07-01T14:30:00Z', status: 'BLOCKED', aiRiskScore: 94.2 },
  { id: 'TX-1003', recipientName: 'Amazon Web Services', amount: 150, currency: 'USD', date: '2026-06-28T09:15:00Z', status: 'COMPLETED', aiRiskScore: 0.5 },
];

export const mockSecurityMetrics = {
  overallScore: 85,
  trustedDevices: 2,
  blockedAttempts: 5,
  lastLogin: '2026-07-03T11:00:00Z',
  activeAlerts: 0
};

export const mockAiAnalysis = {
  transactionId: 'TX-NEW',
  riskScore: 12.5,
  confidence: 96,
  evidence: [
    { id: 'E-1', title: 'Known Device', description: 'Transaction initiated from a recognized device (iPhone 15 Pro).', type: 'POSITIVE' },
    { id: 'E-2', title: 'New Recipient', description: 'You have never sent money to this recipient before.', type: 'WARNING' }
  ],
  recommendation: 'Proceed with standard PIN verification.',
  policyAction: 'Require Customer Confirmation'
};

