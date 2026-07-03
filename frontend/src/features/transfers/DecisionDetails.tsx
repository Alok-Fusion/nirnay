import { Box, Typography, Card, CardContent, Grid, Button, Divider, LinearProgress, Chip } from '@mui/material';
import { Shield, ArrowBack, Policy } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { useTransactions, useRiskReport } from '../../services/apiHooks';
import { CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';

const MotionCard = motion(Card);

export const DecisionDetails = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  
  const { data: transactions = [], isLoading: txLoading } = useTransactions();
  // Using explicit string or ignoring if not ready
  const { data: riskReport, isLoading: riskLoading } = useRiskReport(id || '');

  if (txLoading || riskLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  // Find transaction
  const transaction = transactions.find((t: any) => String(t.id) === id); 
  
  if (!transaction) {
    return <Box sx={{ py: 4, textAlign: 'center' }}><Typography>Transaction not found.</Typography></Box>;
  }

  const isBlocked = transaction.status === 'REJECTED' || transaction.status === 'BLOCKED';
  const riskScore = riskReport?.risk_score || transaction.aiRiskScore || 0;
  const confidence = riskReport?.confidence || 0;

  return (
    <Box sx={{ maxWidth: 1000, mx: 'auto', py: 4 }}>
      <Button 
        startIcon={<ArrowBack />} 
        onClick={() => navigate(-1)}
        sx={{ mb: 4 }}
      >
        Back to Overview
      </Button>

      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box sx={{ p: 2, bgcolor: isBlocked ? 'error.light' : 'success.light', borderRadius: 2 }}>
            <Shield sx={{ fontSize: 32, color: isBlocked ? 'error.dark' : 'success.dark' }} />
          </Box>
          <Box>
              <Typography variant="h5" sx={{ fontWeight: 700 }}>{transaction.recipientName || 'Unknown Recipient'}</Typography>
              <Typography variant="body1" color="text.secondary">ID: {transaction.id} • {new Date(transaction.created_at).toLocaleString()}</Typography>
          </Box>
        </Box>
        <Chip 
          label={isBlocked ? "BLOCKED BY AI" : "APPROVED BY AI"} 
          color={isBlocked ? "error" : "success"}
          sx={{ fontWeight: 'bold', fontSize: '1rem', py: 2.5, px: 1 }}
        />
      </Box>

      <Grid container spacing={3}>
        {/* Confidence Meter */}
        <Grid size={{ xs: 12, md: 4 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} sx={{ height: '100%' }}>
            <CardContent>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2" color="text.secondary">AI Risk Assessment</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }} color={isBlocked ? 'error.main' : 'success.main'}>
                    {riskScore}/100
                  </Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={riskScore} 
                  color={isBlocked ? "error" : "success"}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>

              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography color="text.secondary">Confidence Level</Typography>
                <Typography sx={{ fontWeight: 'bold' }}>{confidence}%</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography color="text.secondary">Status</Typography>
                <Typography sx={{ fontWeight: 'bold' }} color={isBlocked ? 'error.main' : 'success.main'}>{transaction.status}</Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Policy Result */}
        <Grid size={{ xs: 12, md: 8 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} sx={{ height: '100%', bgcolor: 'primary.dark', color: 'white' }}>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Policy />
                <Typography variant="h6">Policy & Compliance</Typography>
              </Box>
                <Typography variant="body1" sx={{ fontWeight: 500 }}>
                  {riskReport?.recommended_action || "Standard processing rules applied."}
                </Typography>
              <Divider sx={{ borderColor: 'rgba(255,255,255,0.2)', my: 2 }} />
              <Typography variant="body1" sx={{ opacity: 0.9 }}>
                {isBlocked 
                  ? "Transaction violates Anti-Money Laundering (AML) Rule 402a regarding high-risk unregulated exchanges."
                  : "Transaction complies with standard limits and recognized historical behaviour."}
              </Typography>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Evidence Cards */}
        <Grid size={{ xs: 12 }}>
          <Typography variant="h5" sx={{ mt: 4, mb: 2, fontWeight: 700 }}>Evidence & Reasoning</Typography>
          <Grid container spacing={3}>
            <Grid size={{ xs: 12 }}>
              <MotionCard 
                initial={{ opacity: 0, scale: 0.95 }} 
                animate={{ opacity: 1, scale: 1 }} 
                transition={{ delay: 0.2 }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h6" sx={{ mb: 3 }}>Decision Evidence</Typography>
                  
                  <Box sx={{ borderLeft: '2px solid rgba(0,0,0,0.1)', pl: 3, mb: 4 }}>
                    {riskReport?.reason_codes ? riskReport.reason_codes.map((code: string, idx: number) => (
                      <Box key={idx} sx={{ position: 'relative', mb: 3 }}>
                        <Box sx={{ position: 'absolute', left: -33, top: 2, bgcolor: 'background.paper', width: 14, height: 14, borderRadius: '50%', border: '2px solid', borderColor: 'warning.main' }} />
                        <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>Reason Code</Typography>
                        <Typography variant="body2" color="text.secondary">{code}</Typography>
                      </Box>
                    )) : (
                      <Typography variant="body2" color="text.secondary">No detailed evidence recorded.</Typography>
                    )}
                  </Box>

                  <Divider sx={{ my: 3 }} />
                </CardContent>
              </MotionCard>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

