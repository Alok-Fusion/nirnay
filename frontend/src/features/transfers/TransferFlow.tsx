import { Box, Typography, Button, TextField, MenuItem, Stepper, Step, StepLabel, CircularProgress, Card } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { useRecipients, useTransfer } from '../../services/apiHooks';
import { useAuth } from '../../contexts';
import { Lock, CheckCircle, SupportAgent } from '@mui/icons-material';

const MotionBox = motion(Box);

export const TransferFlow = () => {
  const { data: recipients = [], isLoading: loadingRecipients } = useRecipients();
  const transferMutation = useTransfer();
  const { stepUpAuth } = useAuth();

  const [activeStep, setActiveStep] = useState(0);
  const [recipientId, setRecipientId] = useState('');
  const [amount, setAmount] = useState('');
  const [transferResult, setTransferResult] = useState<any>(null);

  const steps = ['Details', 'NIRNAY Review', 'Confirm'];

  const handleNext = async () => {
    if (activeStep === 0) {
      if (!recipientId || !amount) return;
      
      setActiveStep(1); // Go to Analyzing state
      
      try {
        // Find the selected recipient to get the account number
        const selectedRecipient = recipients.find((r: any) => r.id === recipientId);
        
        // Execute real transfer which invokes the AI engine
        const result = await transferMutation.mutateAsync({
          recipient_account_number: selectedRecipient?.account_number || "0000",
          amount: parseFloat(amount),
          currency: 'USD'
        });
        
        setTransferResult(result);
        setActiveStep(2); // Analysis complete, show review
      } catch (error) {
        console.error("Transfer failed", error);
        // Fallback to error state or retry (omitted for brevity)
        setActiveStep(0);
      }
    } else {
      setActiveStep(activeStep + 1);
    }
  };

  const handleConfirm = async () => {
    // If step-up auth is required based on AI recommendation
    if (transferResult?.risk_evaluation?.recommended_action !== "Proceed") {
      const authSuccess = await stepUpAuth();
      if (!authSuccess) return;
    }
    
    // In a real system, we might have a separate /confirm endpoint.
    // For now, the MVP /transfer handles everything if we consider it "approved".
    // We navigate to dashboard on success.
    window.location.href = '/dashboard';
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', py: 4 }}>
      <Box sx={{ mb: 6 }}>
        <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>Secure Transfer</Typography>
        <Typography variant="body1" color="text.secondary">Send money with AI-backed confidence.</Typography>
      </Box>

      <Stepper activeStep={activeStep} sx={{ mb: 6 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      <Card sx={{ p: { xs: 2, md: 4 }, borderRadius: 4, minHeight: 400 }}>
        <AnimatePresence mode="wait">
          {activeStep === 0 && (
            <MotionBox
              key="step0"
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
                onClick={handleNext}
                disabled={!recipientId || !amount || transferMutation.isPending}
                sx={{ mt: 2 }}
              >
                Continue to Review
              </Button>
            </MotionBox>
          )}

          {activeStep === 1 && (
            <MotionBox
              key="step1"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, x: 20 }}
            >
              {transferMutation.isPending ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', py: 8, gap: 3 }}>
                  <CircularProgress size={60} thickness={4} />
                  <Typography variant="h6" color="primary">NIRNAY AI is analyzing this transaction...</Typography>
                  <Typography variant="body2" color="text.secondary">Evaluating risk, context, and policy rules.</Typography>
                </Box>
              ) : (
                <Box>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 4, p: 2, bgcolor: 'rgba(16, 185, 129, 0.05)', borderRadius: 2, border: '1px solid rgba(16, 185, 129, 0.2)' }}>
                    <SupportAgent sx={{ fontSize: 40, color: 'primary.main' }} />
                    <Box>
                      <Typography variant="h6" color="primary.main">Analysis Complete</Typography>
                      <Typography variant="body2" color="text.secondary">
                        Risk Score: {transferResult?.risk_evaluation?.risk_score || 0}/100 • 
                        Confidence: {transferResult?.risk_evaluation?.confidence || 0}%
                      </Typography>
                    </Box>
                  </Box>

                  <Typography variant="h6" sx={{ mb: 2 }}>Decision Timeline</Typography>
                  <Box sx={{ pl: 2, borderLeft: '2px solid rgba(0,0,0,0.1)', mb: 4 }}>
                    {(transferResult?.risk_evaluation?.evidence || []).map((ev: any, idx: number) => (
                      <MotionBox 
                        key={idx}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: idx * 0.2 }}
                        sx={{ position: 'relative', mb: 3, pl: 3 }}
                      >
                        <Box sx={{ 
                          position: 'absolute', left: -25, top: 0, 
                          bgcolor: 'background.paper', width: 16, height: 16, 
                          borderRadius: '50%', border: '2px solid',
                          borderColor: ev.type === 'POSITIVE' ? 'success.main' : 'warning.main'
                        }} />
                        <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>{ev.title || ev.action || 'AI Decision Step'}</Typography>
                        <Typography variant="body2" color="text.secondary">{ev.description || ev.details}</Typography>
                      </MotionBox>
                    ))}
                    {!(transferResult?.risk_evaluation?.evidence?.length) && (
                        <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>Analysis completed securely.</Typography>
                    )}
                  </Box>

                  <Box sx={{ bgcolor: '#F8F9FA', p: 3, borderRadius: 2, mb: 4 }}>
                    <Typography variant="subtitle2" color="text.secondary" sx={{ textTransform: 'uppercase', letterSpacing: 1, mb: 1 }}>
                      AI Recommendation
                    </Typography>
                    <Typography variant="body1" sx={{ fontWeight: 500 }}>
                      {transferResult?.risk_evaluation?.recommended_action || transferResult?.message}
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', gap: 2 }}>
                    <Button variant="outlined" size="large" onClick={() => setActiveStep(0)}>Back</Button>
                    <Button 
                      variant="contained" 
                      color="primary" 
                      size="large" 
                      startIcon={<Lock />}
                      onClick={handleConfirm}
                      sx={{ flex: 1 }}
                    >
                      Authenticate & Confirm
                    </Button>
                  </Box>
                </Box>
              )}
            </MotionBox>
          )}

          {activeStep === 2 && (
            <MotionBox
              key="step2"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              sx={{ textAlign: 'center', py: 8 }}
            >
              <CheckCircle color="success" sx={{ fontSize: 80, mb: 2 }} />
              <Typography variant="h4" sx={{ mb: 1 }}>Transfer Complete</Typography>
              <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
                ${amount} has been securely transferred.
              </Typography>
              <Button variant="outlined" onClick={() => { setActiveStep(0); setAmount(''); setRecipientId(''); }}>
                Start New Transfer
              </Button>
            </MotionBox>
          )}
        </AnimatePresence>
      </Card>
    </Box>
  );
};

