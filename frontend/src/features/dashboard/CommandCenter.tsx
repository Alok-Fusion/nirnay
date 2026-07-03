import { Box, Typography, Grid, Card, CardContent, Button, Stack, Chip, Divider } from '@mui/material';
import { Shield, ArrowForward, CheckCircle, Warning, FiberNew, TrendingUp, VerifiedUser } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useTransactions, useSecurityMetrics, useUserBehavior } from '../../services/apiHooks';

const MotionCard = motion(Card);

export const CommandCenter = () => {
  const navigate = useNavigate();
  const { data: transactions = [], isLoading } = useTransactions();
  const { data: securityMetrics } = useSecurityMetrics();
  const { data: behavior } = useUserBehavior();

  // Fallback to defaults while loading
  const metrics = securityMetrics || {
    overallScore: 0,
    trustedDevices: 0,
    blockedAttempts: 0
  };

  const trustScore = behavior?.trust_score ?? 50;
  const trustLevel = behavior?.trust_level ?? 'NEW';
  const txCount = behavior?.transaction_count ?? 0;

  const getStageInfo = (level: string) => {
    switch (level) {
      case 'NEW':
        return {
          index: 0,
          percent: 0,
          description: 'Your account is in the initial phase. All transaction rules and risk checks are strictly enforced. To increase your Trust Score, perform regular and safe transaction activity.',
        };
      case 'LEARNING':
        return {
          index: 1,
          percent: 33,
          description: 'NIRNAY is currently learning your transaction habits, such as preferred transfer hours, frequencies, and recipients, to build your Digital Twin profile.',
        };
      case 'ESTABLISHED':
        return {
          index: 2,
          percent: 66,
          description: 'Your financial behavior patterns have been established. Transacting with common amounts or to regular recipients will have reduced verification friction.',
        };
      case 'TRUSTED':
        return {
          index: 3,
          percent: 100,
          description: 'Highly trusted digital twin profile. Typical transactions are approved instantly, and complex AI guardrails operate completely in the background with zero user friction.',
        };
      default:
        return {
          index: 0,
          percent: 0,
          description: 'Your account is in the initial phase.',
        };
    }
  };

  const { index: activeStageIndex, percent: activePercent, description: stageDescription } = getStageInfo(trustLevel);

  const stages = [
    { label: 'NEW', sub: '0-5 Transfers', icon: <FiberNew /> },
    { label: 'LEARNING', sub: '6-20 Transfers', icon: <TrendingUp /> },
    { label: 'ESTABLISHED', sub: '21-100 Transfers', icon: <VerifiedUser /> },
    { label: 'TRUSTED', sub: '100+ Transfers', icon: <Shield /> },
  ];

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h3" sx={{ mb: 1 }}>Good morning, Alok.</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        NIRNAY is actively protecting your account — monitoring every transaction with ML, Rules, and AI before a single rupee moves.
      </Typography>

      <Grid container spacing={3}>
        {/* AI Trust Timeline */}
        <Grid size={{ xs: 12 }}>
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            sx={{ 
              mb: 1, 
              background: 'rgba(255, 255, 255, 0.8)', 
              backdropFilter: 'blur(8px)',
              border: '1px solid rgba(0, 0, 0, 0.08)',
              boxShadow: '0 4px 30px rgba(0, 0, 0, 0.05)'
            }}
          >
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', alignItems: { xs: 'flex-start', sm: 'center' }, gap: 2, mb: 3 }}>
                <Box>
                  <Typography variant="h5" sx={{ fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Shield color="primary" /> AI Trust Timeline
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Your Digital Twin trust state based on transaction frequency and behavioral consistency.
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, alignSelf: { xs: 'flex-end', sm: 'auto' } }}>
                  <Typography variant="h3" sx={{ fontWeight: 800, color: 'primary.main' }}>
                    {trustScore}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ fontWeight: 600, lineHeight: 1.2 }}>
                    / 100<br />Trust Score
                  </Typography>
                </Box>
              </Box>

              {/* Progress bar and timeline nodes */}
              <Box sx={{ position: 'relative', py: 4, px: 2, mb: 2 }}>
                {/* Background line */}
                <Box sx={{ 
                  position: 'absolute', 
                  top: '50%', 
                  left: '12%', 
                  right: '12%', 
                  height: 4, 
                  bgcolor: 'rgba(0,0,0,0.06)',
                  transform: 'translateY(-50%)',
                  zIndex: 0
                }} />
                {/* Active progress line */}
                <Box sx={{ 
                  position: 'absolute', 
                  top: '50%', 
                  left: '12%', 
                  width: `${activePercent * 0.76}%`, // Adjusted to align with centers
                  height: 4, 
                  bgcolor: 'primary.main',
                  transform: 'translateY(-50%)',
                  transition: 'width 0.8s cubic-bezier(0.4, 0, 0.2, 1)',
                  zIndex: 0
                }} />

                <Grid container sx={{ position: 'relative', zIndex: 1, justifyContent: 'space-between' }}>
                  {stages.map((stage, idx) => {
                    const isCompleted = idx <= activeStageIndex;
                    const isActive = idx === activeStageIndex;
                    return (
                      <Grid 
                        key={stage.label} 
                        size={{ xs: 3 }}
                        sx={{ 
                          textAlign: 'center', 
                          display: 'flex', 
                          flexDirection: 'column', 
                          alignItems: 'center'
                        }}
                      >
                        <Box sx={{ 
                          width: 48, 
                          height: 48, 
                          borderRadius: '50%', 
                          display: 'flex', 
                          alignItems: 'center', 
                          justifyContent: 'center',
                          bgcolor: isActive ? 'primary.main' : (isCompleted ? 'primary.light' : 'background.paper'),
                          color: isActive ? 'white' : (isCompleted ? 'primary.main' : 'text.disabled'),
                          border: `2px solid ${isCompleted ? 'primary.main' : 'rgba(0,0,0,0.12)'}`,
                          boxShadow: isActive ? '0 0 16px rgba(63, 81, 181, 0.4)' : 'none',
                          transition: 'all 0.5s ease',
                          mb: 1
                        }}>
                          {stage.icon}
                        </Box>
                        <Typography variant="subtitle2" sx={{ fontWeight: isActive ? 700 : 600, color: isActive ? 'text.primary' : 'text.secondary', fontSize: '0.875rem' }}>
                          {stage.label}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" sx={{ display: { xs: 'none', md: 'block' } }}>
                          {stage.sub}
                        </Typography>
                      </Grid>
                    );
                  })}
                </Grid>
              </Box>

              <Box sx={{ mt: 3, p: 2, borderRadius: 2, bgcolor: 'rgba(63, 81, 181, 0.04)', borderLeft: '4px solid', borderLeftColor: 'primary.main' }}>
                <Typography variant="body2" sx={{ fontWeight: 700, mb: 0.5 }}>
                  Current Phase: {trustLevel} ({txCount} transaction{txCount !== 1 ? 's' : ''} completed)
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {stageDescription}
                </Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>
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

