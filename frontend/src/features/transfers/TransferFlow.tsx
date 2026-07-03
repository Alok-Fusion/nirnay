import { Box, Typography, Button, TextField, MenuItem, CircularProgress, Card } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { useRecipients, useTransfer, useAuthenticateTransaction } from '../../services/apiHooks';
import { useAuth } from '../../contexts';
import { CheckCircle, ErrorOutlined, Security, Lock } from '@mui/icons-material';

const MotionBox = motion(Box);

export const TransferFlow = () => {
  const { data: recipients = [], isLoading: loadingRecipients } = useRecipients();
  const transferMutation = useTransfer();
  const authenticateMutation = useAuthenticateTransaction();
  const { stepUpAuth } = useAuth();

  const [recipientId, setRecipientId] = useState('');
  const [amount, setAmount] = useState('');
  const [transferResult, setTransferResult] = useState<any>(null);
  
  // 0: Form, 1: Loading, 2: Success, 3: Verification/Blocked
  const [activeState, setActiveState] = useState<0 | 1 | 2 | 3>(0);
  const [loadingStep, setLoadingStep] = useState<string>('Validating');

  const loadingSteps = [
    'Transaction Received',
    'Validating',
    'Checking Behaviour',
    'Running ML',
    'Applying Rules',
    'AI Analysis',
    'Decision Ready'
  ];

  const handleSubmit = async () => {
    if (!recipientId || !amount) return;
    
    setActiveState(1); // Loading state
    let stepIndex = 0;
    
    // Visually step through backend workflow
    const interval = setInterval(() => {
      if (stepIndex < loadingSteps.length - 1) {
        stepIndex++;
        setLoadingStep(loadingSteps[stepIndex]);
      }
    }, 600);
    
    try {
      const selectedRecipient = recipients.find((r: any) => r.id === recipientId);
      
      // Execute real transfer which invokes the AI orchestrator in the background
      const result = await transferMutation.mutateAsync({
        recipient_account_number: selectedRecipient?.account_number || "0000",
        amount: parseFloat(amount),
        currency: 'USD'
      });
      
      setTransferResult(result);
      
      const action = result?.risk_evaluation?.recommended_action;
      
      clearInterval(interval);
      setLoadingStep('Decision Ready');
      
      // Delay slightly for effect
      setTimeout(() => {
        if (action === "BLOCK") {
          setActiveState(3); // Blocked
        } else {
          setActiveState(3); // Both APPROVED and REQUEST_MORE_INFORMATION require auth
        }
      }, 500);
      
    } catch (error) {
      clearInterval(interval);
      console.error("Transfer failed", error);
      setTransferResult({ message: "Transaction Failed due to a system error.", risk_evaluation: { recommended_action: "BLOCK" } });
      setActiveState(3);
    }
  };

  const handleVerify = async () => {
    const authSuccess = await stepUpAuth();
    if (!authSuccess) return;
    
    try {
      await authenticateMutation.mutateAsync(transferResult.transaction.id);
      setActiveState(2); // Success
    } catch (error) {
      console.error("Authentication or execution failed", error);
      setTransferResult({ message: "Execution failed during authentication check.", risk_evaluation: { recommended_action: "BLOCK" } });
      setActiveState(3); // Back to error view
    }
  };

  const reset = () => {
    setAmount('');
    setRecipientId('');
    setTransferResult(null);
    setActiveState(0);
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>Transfer Funds</Typography>
        <Typography variant="body1" color="text.secondary">Securely send money to your recipients.</Typography>
      </Box>

      <Card sx={{ p: { xs: 3, md: 4 }, borderRadius: 4, minHeight: 350, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <AnimatePresence mode="wait">
          {activeState === 0 && (
            <MotionBox
              key="form"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}
            >
              <TextField
                select
                label="Select Recipient"
                fullWidth
                value={recipientId}
                onChange={(e) => setRecipientId(e.target.value)}
                disabled={loadingRecipients}
              >
                {recipients.map((rec: any) => (
                  <MenuItem key={rec.id} value={rec.id}>
                    {rec.name} ({rec.bank_code})
                  </MenuItem>
                ))}
              </TextField>

              <TextField
                label="Amount (USD)"
                type="number"
                fullWidth
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />

              <Button 
                variant="contained" 
                size="large" 
                onClick={handleSubmit}
                disabled={!recipientId || !amount || transferMutation.isPending}
                sx={{ py: 1.5, fontSize: '1.1rem' }}
              >
                Transfer Now
              </Button>
            </MotionBox>
          )}

          {activeState === 1 && (
            <MotionBox
              key="loading"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 4 }}
            >
              <CircularProgress size={60} thickness={4} sx={{ mb: 4 }} />
              <Typography variant="h6" sx={{ mb: 1, fontWeight: 600 }}>NIRNAY is securing your transaction...</Typography>
              <Typography variant="body1" color="primary.main" sx={{ fontWeight: 500 }}>
                {loadingStep}
              </Typography>
            </MotionBox>
          )}

          {activeState === 2 && (
            <MotionBox
              key="success"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              sx={{ textAlign: 'center' }}
            >
              <CheckCircle color="success" sx={{ fontSize: 80, mb: 2 }} />
              <Typography variant="h4" sx={{ mb: 1 }}>Transfer Complete</Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                ${amount} has been securely transferred.
              </Typography>
              <Button variant="outlined" onClick={reset}>
                Start New Transfer
              </Button>
            </MotionBox>
          )}

          {activeState === 3 && (
            <MotionBox
              key="verification"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              sx={{ textAlign: 'center' }}
            >
              {transferResult?.risk_evaluation?.recommended_action === "BLOCK" ? (
                <>
                  <ErrorOutlined color="error" sx={{ fontSize: 80, mb: 2 }} />
                  <Typography variant="h5" color="error" sx={{ mb: 2, fontWeight: 600 }}>Transaction Blocked</Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                    {transferResult?.message || "This transaction was blocked due to security policies."}
                  </Typography>
                  <Button variant="outlined" onClick={reset}>
                    Return
                  </Button>
                </>
              ) : (
                <>
                  <Security color="warning" sx={{ fontSize: 80, mb: 2 }} />
                  <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>Verification Required</Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                    {transferResult?.message || "Please authenticate to confirm this transfer."}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center' }}>
                    <Button variant="outlined" onClick={reset}>Cancel</Button>
                    <Button 
                      variant="contained" 
                      color="primary" 
                      onClick={handleVerify}
                      startIcon={<Lock />}
                      disabled={authenticateMutation.isPending}
                    >
                      {authenticateMutation.isPending ? 'Executing...' : 'Authenticate & Transfer'}
                    </Button>
                  </Box>
                </>
              )}
            </MotionBox>
          )}
        </AnimatePresence>
      </Card>
    </Box>
  );
};
