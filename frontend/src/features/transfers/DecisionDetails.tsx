import { Box, Typography, Card, CardContent, Grid, Button, Divider, Chip, Alert } from '@mui/material';
import { Shield, ArrowBack, CheckCircle, Block, Psychology, Gavel, Memory, WarningAmber } from '@mui/icons-material';
import { useNavigate, useParams } from 'react-router-dom';
import { useTransactions, useRiskReport } from '../../services/apiHooks';
import { CircularProgress, LinearProgress } from '@mui/material';
import { motion } from 'framer-motion';

const MotionCard = motion(Card);

const SCAM_TYPE_LABELS: Record<string, { label: string; color: 'error' | 'warning'; description: string }> = {
  crypto_scam: {
    label: '🔴 Crypto Scam Detected',
    color: 'error',
    description: 'This transfer was directed to a cryptocurrency platform. Crypto-based scams are irreversible and among the fastest-growing financial frauds. This transfer was blocked to protect your funds.'
  },
  potential_investment_scam: {
    label: '⚠️ Investment Scam Risk',
    color: 'warning',
    description: 'High-return investment opportunities are the most common form of financial fraud. Legitimate investment firms do not request bank transfers from new customers. NIRNAY flagged this for your protection.'
  },
  potential_romance_scam: {
    label: '⚠️ Romance Scam Pattern',
    color: 'warning',
    description: 'Fraudsters build emotional relationships online before requesting money. This transfer matches the profile of a romance scam — first transfer to an overseas or new contact.'
  },
  potential_business_email_compromise: {
    label: '⚠️ Business Email Compromise Risk',
    color: 'warning',
    description: 'Attackers intercept business communications to redirect payments. NIRNAY detected a sudden change in payment recipient combined with a large amount. Call the vendor directly to verify.'
  },
  social_engineering_pressure: {
    label: '⚠️ Social Engineering Detected',
    color: 'warning',
    description: 'This transfer shows signs of social engineering — large amount, new recipient, unusual time. Scammers create urgency to prevent careful thinking. Take your time before proceeding.'
  },
  velocity_fraud_attack: {
    label: '🔴 Velocity Attack Blocked',
    color: 'error',
    description: 'Unusual number of transfers in a short time period. This pattern is consistent with an account takeover or automated fraud attack. Your account has been protected.'
  }
};

export const DecisionDetails = () => {
  const navigate = useNavigate();
  const { id } = useParams();

  const { data: transactions = [], isLoading: txLoading } = useTransactions();
  const { data: riskReport, isLoading: riskLoading } = useRiskReport(id || '');

  if (txLoading || riskLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '60vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  const transaction = transactions.find((t: any) => String(t.id) === id);

  if (!transaction) {
    return <Box sx={{ py: 4, textAlign: 'center' }}><Typography>Transaction not found.</Typography></Box>;
  }

  const isBlocked = transaction.status === 'Blocked' || transaction.status === 'Failed' || transaction.status === 'Cancelled';
  const isCompleted = transaction.status === 'Completed';
  const riskScore = riskReport?.risk_score ?? transaction.aiRiskScore ?? 0;
  const riskPct = Math.round(riskScore * 100);
  const confidence = riskReport?.confidence ? Math.round(riskReport.confidence * 100) : 0;
  const scamType = riskReport?.scam_type;
  const reasoning: string[] = riskReport?.reasoning ?? [];
  const scamInfo = scamType ? SCAM_TYPE_LABELS[scamType] : null;

  const decisionLabel = isBlocked
    ? 'BLOCKED BY NIRNAY'
    : isCompleted
    ? 'APPROVED & COMPLETED'
    : 'AWAITING AUTHENTICATION';

  const decisionColor = isBlocked ? 'error' : isCompleted ? 'success' : 'warning';

  return (
    <Box sx={{ maxWidth: 1000, mx: 'auto', py: 4 }}>
      <Button startIcon={<ArrowBack />} onClick={() => navigate(-1)} sx={{ mb: 4 }}>
        Back to Overview
      </Button>

      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 4 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Box sx={{ p: 2, bgcolor: isBlocked ? 'error.light' : 'success.light', borderRadius: 2 }}>
            {isBlocked ? (
              <Block sx={{ fontSize: 32, color: 'error.dark' }} />
            ) : (
              <Shield sx={{ fontSize: 32, color: 'success.dark' }} />
            )}
          </Box>
          <Box>
            <Typography variant="h5" sx={{ fontWeight: 700 }}>
              {transaction.recipientName || 'Unknown Recipient'}
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Transaction #{transaction.id} • {new Date(transaction.created_at).toLocaleString()}
            </Typography>
          </Box>
        </Box>
        <Chip
          label={decisionLabel}
          color={decisionColor}
          icon={isBlocked ? <Block /> : <CheckCircle />}
          sx={{ fontWeight: 'bold', fontSize: '0.9rem', py: 2.5, px: 1 }}
        />
      </Box>

      {/* Scam Warning Banner */}
      {scamInfo && (
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <Alert
            severity={scamInfo.color}
            icon={<WarningAmber />}
            sx={{ mb: 3, borderRadius: 3, '& .MuiAlert-message': { width: '100%' } }}
          >
            <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 0.5 }}>
              {scamInfo.label}
            </Typography>
            <Typography variant="body2">{scamInfo.description}</Typography>
          </Alert>
        </motion.div>
      )}

      <Grid container spacing={3}>
        {/* Risk Intelligence */}
        <Grid size={{ xs: 12, md: 4 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} sx={{ height: '100%' }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Psychology color="primary" />
                <Typography variant="h6">ML Risk Intelligence</Typography>
              </Box>
              <Box sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="body2" color="text.secondary">Risk Score</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 'bold' }} color={isBlocked ? 'error.main' : 'success.main'}>
                    {riskPct} / 100
                  </Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={riskPct}
                  color={isBlocked ? 'error' : riskPct > 50 ? 'warning' : 'success'}
                  sx={{ height: 8, borderRadius: 4 }}
                />
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography color="text.secondary" variant="body2">AI Confidence</Typography>
                <Typography sx={{ fontWeight: 'bold' }} variant="body2">{confidence}%</Typography>
              </Box>
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography color="text.secondary" variant="body2">Final Status</Typography>
                <Typography sx={{ fontWeight: 'bold', textTransform: 'capitalize' }} variant="body2">
                  {transaction.status}
                </Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* NIRNAY's Decision Reasoning */}
        <Grid size={{ xs: 12, md: 8 }}>
          <MotionCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            sx={{ height: '100%', background: 'linear-gradient(135deg, #1A237E, #283593)', color: 'white' }}
          >
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Gavel sx={{ color: 'rgba(255,255,255,0.8)' }} />
                <Typography variant="h6">Why NIRNAY Made This Decision</Typography>
              </Box>
              <Typography variant="body2" sx={{ opacity: 0.7, mb: 2 }}>
                Instead of a risk number, here is the reasoning behind this decision in plain language:
              </Typography>
              <Divider sx={{ borderColor: 'rgba(255,255,255,0.15)', mb: 2 }} />
              {reasoning.filter(Boolean).length > 0 ? (
                reasoning.filter(Boolean).map((reason: string, idx: number) => (
                  <Box key={idx} sx={{ display: 'flex', gap: 1.5, mb: 1.5 }}>
                    <Box sx={{ mt: 0.5, minWidth: 8, height: 8, borderRadius: '50%', bgcolor: isBlocked ? '#ff5252' : '#69f0ae', flexShrink: 0 }} />
                    <Typography variant="body2" sx={{ opacity: 0.9, lineHeight: 1.6 }}>{reason}</Typography>
                  </Box>
                ))
              ) : (
                <Typography variant="body2" sx={{ opacity: 0.7 }}>
                  {isBlocked
                    ? 'This transaction was blocked due to policy violations and high-risk indicators.'
                    : 'This transaction complies with your historical behaviour and banking policies.'}
                </Typography>
              )}
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Evidence Trail */}
        <Grid size={{ xs: 12 }}>
          <MotionCard initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.2 }}>
            <CardContent sx={{ p: 4 }}>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
                <Memory color="secondary" />
                <Typography variant="h6">Decision Intelligence Evidence Trail</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                NIRNAY combines Machine Learning, Rule Engine analysis, and AI reasoning to form every decision.
                Each layer contributes evidence — here is what each found:
              </Typography>

              {riskReport?.reason_codes && riskReport.reason_codes.length > 0 ? (
                <Box sx={{ borderLeft: '3px solid', borderColor: 'primary.main', pl: 3 }}>
                  {riskReport.reason_codes.map((code: string, idx: number) => (
                    <Box key={idx} sx={{ position: 'relative', mb: 2.5 }}>
                      <Box sx={{
                        position: 'absolute', left: -23, top: 4,
                        bgcolor: 'primary.main', width: 10, height: 10,
                        borderRadius: '50%'
                      }} />
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{code}</Typography>
                    </Box>
                  ))}
                </Box>
              ) : (
                <Box sx={{ p: 3, bgcolor: 'action.hover', borderRadius: 2 }}>
                  <Typography variant="body2" color="text.secondary">
                    {isBlocked
                      ? 'This transaction was evaluated against NIRNAY\'s banking policies and blocked at the Rule Engine level before AI analysis was required.'
                      : 'Transaction passed all checks cleanly. No suspicious signals were found in your behavioural profile or transaction patterns.'}
                  </Typography>
                </Box>
              )}
            </CardContent>
          </MotionCard>
        </Grid>
      </Grid>
    </Box>
  );
};
