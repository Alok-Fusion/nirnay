import { Box, Typography, Card, CardContent, Grid, Button, Divider, LinearProgress, Chip } from '@mui/material';
import { Shield, ArrowBack, VerifiedUser, Policy, Description, Gavel } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { mockAiAnalysis, mockTransactions } from '../../services/mockData';
import { motion } from 'framer-motion';

const MotionCard = motion(Card);

export const DecisionDetails = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  // Find transaction from mock data or default
  const transaction = mockTransactions.find(t => t.id === id) || mockTransactions[1]; 
  const isBlocked = transaction.status === 'BLOCKED';

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
            <Typography variant="h4" sx={{ fontWeight: 700 }}>Decision Intelligence</Typography>
            <Typography variant="body1" color="text.secondary">Analysis for Transaction {transaction.id}</Typography>
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
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <VerifiedUser color="primary" />
                <Typography variant="h6">AI Confidence</Typography>
              </Box>
              <Typography variant="h2" color="primary.main" sx={{ fontWeight: 800, mb: 1 }}>
                {mockAiAnalysis.confidence}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={mockAiAnalysis.confidence} 
                sx={{ height: 8, borderRadius: 4, mb: 2, bgcolor: 'rgba(0,0,0,0.05)' }} 
              />
              <Typography variant="body2" color="text.secondary">
                The model is highly confident in this assessment based on historical patterns and current context.
              </Typography>
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
              <Typography variant="h5" sx={{ fontWeight: 'bold', mb: 2 }}>
                {mockAiAnalysis.policyAction}
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
            {mockAiAnalysis.evidence.map((ev, idx) => (
              <Grid size={{ xs: 12, sm: 6 }} key={ev.id}>
                <MotionCard 
                  initial={{ opacity: 0, scale: 0.95 }} 
                  animate={{ opacity: 1, scale: 1 }} 
                  transition={{ delay: 0.2 + (idx * 0.1) }}
                  sx={{ borderLeft: '4px solid', borderColor: ev.type === 'WARNING' ? 'warning.main' : 'success.main' }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      {ev.type === 'WARNING' ? <Gavel color="warning" /> : <Description color="success" />}
                      <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>{ev.title}</Typography>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                      {ev.description}
                    </Typography>
                  </CardContent>
                </MotionCard>
              </Grid>
            ))}
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

