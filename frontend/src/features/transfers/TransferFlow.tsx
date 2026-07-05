import { Box, Typography, Button, TextField, MenuItem, CircularProgress, Card, Tabs, Tab } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';
import { useRecipients, useTransfer, useAuthenticateTransaction, useCreateRecipient, useChat } from '../../services/apiHooks';
import { useAuth } from '../../contexts';
import { CheckCircle, ErrorOutlined, Security, Lock } from '@mui/icons-material';

const MotionBox = motion(Box);

export const TransferFlow = () => {
  const { data: recipients = [], isLoading: loadingRecipients } = useRecipients();
  const transferMutation = useTransfer();
  const authenticateMutation = useAuthenticateTransaction();
  const createRecipientMutation = useCreateRecipient();
  const chatMutation = useChat();
  const { stepUpAuth } = useAuth();

  const [recipientType, setRecipientType] = useState<'saved' | 'new'>('saved');
  const [recipientId, setRecipientId] = useState('');
  
  // New recipient fields
  const [newRecipientName, setNewRecipientName] = useState('');
  const [newRecipientAccount, setNewRecipientAccount] = useState('');
  const [newRecipientBankCode, setNewRecipientBankCode] = useState('');

  const [amount, setAmount] = useState('');
  const [transferResult, setTransferResult] = useState<any>(null);
  
  // 0: Form, 1: Loading, 2: Success, 3: Verification/Blocked/Chat
  const [activeState, setActiveState] = useState<0 | 1 | 2 | 3>(0);
  const [loadingStep, setLoadingStep] = useState<string>('Validating');
  
  // Chat state
  const [chatMessages, setChatMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([]);
  const [userMsg, setUserMsg] = useState('');
  const [isChatActive, setIsChatActive] = useState(false);

  const loadingSteps = [
    'Understanding your transaction...',
    'Building your behavioural profile...',
    'Running ML risk intelligence...',
    'Applying banking policies...',
    'AI reasoning in progress...',
    'Evaluating safest action...',
    'Decision ready'
  ];

  const handleSubmit = async () => {
    if (recipientType === 'saved' && (!recipientId || !amount)) return;
    if (recipientType === 'new' && (!newRecipientName || !newRecipientAccount || !newRecipientBankCode || !amount)) return;
    
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
      let selectedAccountNum = '';
      if (recipientType === 'saved') {
        const selectedRecipient = recipients.find((r: any) => r.id === recipientId);
        selectedAccountNum = selectedRecipient?.account_number || "0000";
      } else {
        // Create the new recipient first
        const newRec = await createRecipientMutation.mutateAsync({
          name: newRecipientName,
          account_number: newRecipientAccount,
          bank_code: newRecipientBankCode,
          is_trusted: false
        });
        selectedAccountNum = newRec.account_number;
      }
      
      // Execute real transfer which invokes the AI orchestrator in the background
      const result = await transferMutation.mutateAsync({
        recipient_account_number: selectedAccountNum,
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
        } else if (action === "REQUEST_MORE_INFORMATION" || action === "ESCALATE_TO_HUMAN") {
          setIsChatActive(true);
          setChatMessages([{ role: 'assistant', content: result.message }]);
          setActiveState(3);
        } else {
          setIsChatActive(false);
          setActiveState(3); // Direct Approve -> step-up authentication
        }
      }, 500);
      
    } catch (error) {
      clearInterval(interval);
      console.error("Transfer failed", error);
      setTransferResult({ message: "Transaction Failed due to a system error.", risk_evaluation: { recommended_action: "BLOCK" } });
      setActiveState(3);
    }
  };

  const handleSendChat = async () => {
    if (!userMsg.trim()) return;
    const currentMsg = userMsg;
    setUserMsg('');
    
    // Append user message to log
    setChatMessages((prev) => [...prev, { role: 'user', content: currentMsg }]);
    
    try {
      const response = await chatMutation.mutateAsync({
        message: currentMsg,
        transactionId: String(transferResult.transaction.id)
      });
      
      // Append AI response to log
      setChatMessages((prev) => [...prev, { role: 'assistant', content: response.message }]);
      
      if (response.status === 'COMPLETED') {
        const finalDecision = response.decision;
        setIsChatActive(false); // Close chat
        
        // Update transfer result message and decision action
        setTransferResult((prev: any) => ({
          ...prev,
          message: response.message,
          risk_evaluation: {
            ...prev?.risk_evaluation,
            recommended_action: finalDecision === 'APPROVE_TRANSACTION' ? 'APPROVE_TRANSACTION' : 'BLOCK'
          }
        }));
      }
    } catch (error) {
      console.error("Chat message failed", error);
      setChatMessages((prev) => [...prev, { role: 'assistant', content: "An error occurred. I couldn't reach the security engine. Please try again." }]);
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
    setNewRecipientName('');
    setNewRecipientAccount('');
    setNewRecipientBankCode('');
    setTransferResult(null);
    setChatMessages([]);
    setIsChatActive(false);
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
              sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}
            >
              <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 1 }}>
                <Tabs value={recipientType} onChange={(_, val) => setRecipientType(val)} variant="fullWidth">
                  <Tab label="Saved Recipient" value="saved" />
                  <Tab label="New Recipient" value="new" />
                </Tabs>
              </Box>

              {recipientType === 'saved' ? (
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
              ) : (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
                  <TextField
                    label="Recipient Full Name"
                    fullWidth
                    value={newRecipientName}
                    onChange={(e) => setNewRecipientName(e.target.value)}
                    placeholder="e.g. Jane Smith"
                  />
                  <TextField
                    label="Account Number"
                    fullWidth
                    value={newRecipientAccount}
                    onChange={(e) => setNewRecipientAccount(e.target.value)}
                    placeholder="e.g. 1234567890"
                  />
                  <TextField
                    label="Bank Code / Routing Number"
                    fullWidth
                    value={newRecipientBankCode}
                    onChange={(e) => setNewRecipientBankCode(e.target.value)}
                    placeholder="e.g. BOA001"
                  />
                </Box>
              )}

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
                disabled={
                  transferMutation.isPending || 
                  createRecipientMutation.isPending ||
                  !amount || 
                  (recipientType === 'saved' ? !recipientId : (!newRecipientName || !newRecipientAccount || !newRecipientBankCode))
                }
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
              sx={{ textAlign: 'center', width: '100%' }}
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
              ) : isChatActive ? (
                /* AI Coercion Conversation Guard */
                <Box sx={{ textAlign: 'left', display: 'flex', flexDirection: 'column', height: 400 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, pb: 1.5, borderBottom: '1px solid rgba(0,0,0,0.06)' }}>
                    <Security color="warning" />
                    <Box>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>NIRNAY Fraud Coercion Guard</Typography>
                      <Typography variant="caption" color="text.secondary">AI Contextual Assessment session</Typography>
                    </Box>
                  </Box>
                  
                  {/* Messages log */}
                  <Box sx={{ flexGrow: 1, overflowY: 'auto', my: 2, display: 'flex', flexDirection: 'column', gap: 1.5, pr: 1 }}>
                    {chatMessages.map((msg, index) => (
                      <Box 
                        key={index}
                        sx={{
                          maxWidth: '85%',
                          alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
                          bgcolor: msg.role === 'user' ? 'primary.main' : 'grey.100',
                          color: msg.role === 'user' ? 'white' : 'text.primary',
                          p: 1.5,
                          borderRadius: msg.role === 'user' ? '16px 16px 2px 16px' : '16px 16px 16px 2px',
                          fontSize: '0.9rem',
                          lineHeight: 1.4
                        }}
                      >
                        {msg.content}
                      </Box>
                    ))}
                    {chatMutation.isPending && (
                      <Box sx={{ alignSelf: 'flex-start', bgcolor: 'grey.100', p: 1.5, borderRadius: '16px 16px 16px 2px', display: 'flex', gap: 0.5, alignItems: 'center' }}>
                        <CircularProgress size={16} color="inherit" />
                        <Typography variant="caption" color="text.secondary">AI is analyzing...</Typography>
                      </Box>
                    )}
                  </Box>

                  {/* Input field */}
                  <Box sx={{ display: 'flex', gap: 1, pt: 1.5, borderTop: '1px solid rgba(0,0,0,0.06)' }}>
                    <TextField 
                      placeholder="Type your response..."
                      fullWidth
                      size="small"
                      value={userMsg}
                      onChange={(e) => setUserMsg(e.target.value)}
                      disabled={chatMutation.isPending}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') handleSendChat();
                      }}
                    />
                    <Button 
                      variant="contained" 
                      onClick={handleSendChat}
                      disabled={chatMutation.isPending || !userMsg.trim()}
                    >
                      Send
                    </Button>
                  </Box>
                </Box>
              ) : (
                /* Step-up password authentication */
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
