import { Box, Typography, Grid, Card, CardContent, Button, Stack, Chip, Divider } from '@mui/material';
import { Shield, ArrowForward, CheckCircle, Warning } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useTransactions, useSecurityMetrics } from '../../services/apiHooks';

const MotionCard = motion(Card);

export const CommandCenter = () => {
  const navigate = useNavigate();
  const { data: transactions = [], isLoading } = useTransactions();
  const { data: securityMetrics } = useSecurityMetrics();

  // Fallback to defaults while loading
  const metrics = securityMetrics || {
    overallScore: 0,
    trustedDevices: 0,
    blockedAttempts: 0
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" sx={{ mb: 1 }}>Good morning, Alok.</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        NIRNAY is actively protecting your account — monitoring every transaction with ML, Rules, and AI before a single rupee moves.
      </Typography>

      <Grid container spacing={3}>
        {/* Quick Transfer Action */}
        <Grid size={{ xs: 12, md: 8 }}>
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            sx={{ height: '100%', background: 'linear-gradient(135deg, #1A237E, #3949AB)', color: 'white' }}
          >
            <CardContent sx={{ p: 4, display: 'flex', flexDirection: 'column', height: '100%', justifyContent: 'space-between' }}>
              <Box>
                <Typography variant="h5" sx={{ mb: 1, fontWeight: 700 }}>Ready to transfer?</Typography>
                <Typography variant="body1" sx={{ opacity: 0.9, maxWidth: 400 }}>
                  Every transfer is evaluated through Context Intelligence, ML Risk Analysis, Banking Rules, and AI Reasoning — before a single rupee moves.
                </Typography>
              </Box>
              <Box sx={{ mt: 4 }}>
                <Button 
                  variant="contained" 
                  color="secondary" 
                  size="large" 
                  endIcon={<ArrowForward />}
                  onClick={() => navigate('/transfer')}
                  sx={{ borderRadius: 8, px: 4, py: 1.5, fontWeight: 700 }}
                >
                  New Transfer
                </Button>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* AI Security Pulse */}
        <Grid size={{ xs: 12, md: 4 }}>
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.1 }}
            sx={{ height: '100%', border: '1px solid rgba(16, 185, 129, 0.2)' }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Shield color="secondary" />
                <Typography variant="h6">Security Pulse</Typography>
              </Box>
              
              <Stack spacing={2}>
                <Box sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="body2" color="text.secondary">Overall Security Score</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{metrics.overallScore} / 100</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Active Alerts</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }} color="success.main">None</Typography>
                </Box>
                <Divider />
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Trusted Devices</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{metrics.trustedDevices}</Typography>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="body2" color="text.secondary">Blocked Attempts</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }}>{metrics.blockedAttempts}</Typography>
                </Box>
              </Stack>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Recent Activity */}
        <Grid size={{ xs: 12 }}>
          <Typography variant="h5" sx={{ mt: 2, mb: 3 }}>Recent AI Decisions</Typography>
          <Stack spacing={2}>
            {isLoading ? (
              <Typography>Loading transactions...</Typography>
            ) : transactions.slice(0, 5).map((tx: any, idx: number) => (
              <MotionCard 
                key={tx.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: 0.2 + (idx * 0.1) }}
                sx={{ overflow: 'visible', cursor: 'pointer', '&:hover': { bgcolor: 'rgba(0,0,0,0.02)' } }}
                onClick={() => navigate(`/decision/${tx.id}`)}
              >
                <CardContent sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', p: '24px !important' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                    <Box sx={{ 
                      width: 48, height: 48, borderRadius: 2, 
                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                      bgcolor: tx.status === 'COMPLETED' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
                      color: tx.status === 'COMPLETED' ? '#10B981' : '#EF4444'
                    }}>
                      {tx.status === 'COMPLETED' ? <CheckCircle /> : <Warning />}
                    </Box>
                    <Box>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{tx.recipientName}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(tx.created_at).toLocaleDateString()} • ID: {tx.id}
                      </Typography>
                    </Box>
                  </Box>
                  
                  <Box sx={{ textAlign: 'right', display: 'flex', alignItems: 'center', gap: 3 }}>
                    <Box>
                      <Typography variant="body1" sx={{ fontWeight: 700 }}>
                        ${tx.amount.toLocaleString()}
                      </Typography>
                      <Chip 
                        label={`Risk Score: ${tx.aiRiskScore}`} 
                        size="small" 
                        sx={{ 
                          mt: 0.5, height: 20, fontSize: '0.7rem',
                          bgcolor: tx.aiRiskScore > 50 ? 'error.light' : 'success.light',
                          color: tx.aiRiskScore > 50 ? 'error.dark' : 'success.dark',
                          fontWeight: 600
                        }} 
                      />
                    </Box>
                  </Box>
                </CardContent>
              </MotionCard>
            ))}
          </Stack>
        </Grid>
      </Grid>
    </Box>
  );
};

