import { Box, Typography, Grid, Card, CardContent, Divider, Switch, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import { Security, Block, Fingerprint, NotificationsActive, CheckCircle } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { mockRecipients } from '../../services/mockData';
import { useSecurityMetrics } from '../../services/apiHooks';

const MotionCard = motion(Card);

export const SecurityCenter = () => {
  const { data: securityMetrics, isLoading } = useSecurityMetrics();
  
  const metrics = securityMetrics || {
    overallScore: 0,
    trustedDevices: 0,
    blockedAttempts: 0,
    lastLogin: new Date().toISOString(),
    activeAlerts: 0
  };
  return (
    <Box sx={{ maxWidth: 1000, mx: 'auto', py: 4 }}>
      <Box sx={{ mb: 6, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Security sx={{ fontSize: 40, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>Security Center</Typography>
          <Typography variant="body1" color="text.secondary">Manage your AI protection and account security.</Typography>
        </Box>
      </Box>

      <Grid container spacing={4}>
        {/* Protection Metrics */}
        <Grid size={{ xs: 12, md: 6 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} sx={{ height: '100%' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>AI Protection Metrics</Typography>
              {isLoading ? (
                <Typography>Loading metrics...</Typography>
              ) : (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Overall Security Score</Typography>
                    <Typography sx={{ fontWeight: 'bold' }} color="secondary.main">{metrics.overallScore} / 100</Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Trusted Devices</Typography>
                    <Typography sx={{ fontWeight: 'bold' }}>{metrics.trustedDevices} active</Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Blocked Attempts (30d)</Typography>
                    <Typography sx={{ fontWeight: 'bold' }} color="error.main">{metrics.blockedAttempts}</Typography>
                  </Box>
                  <Divider sx={{ my: 2 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Last Login</Typography>
                    <Typography sx={{ fontWeight: 'bold' }}>{new Date(metrics.lastLogin).toLocaleString()}</Typography>
                  </Box>
                </>
              )}
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Security Settings */}
        <Grid size={{ xs: 12, md: 6 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} sx={{ height: '100%' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>Active Controls</Typography>
              <List disablePadding>
                <ListItem sx={{ px: 0 }}>
                  <ListItemIcon><Fingerprint color="primary" /></ListItemIcon>
                  <ListItemText primary="Biometric Authentication" secondary="Required for transfers over $1,000" />
                  <Switch defaultChecked color="primary" />
                </ListItem>
                <ListItem sx={{ px: 0 }}>
                  <ListItemIcon><NotificationsActive color="primary" /></ListItemIcon>
                  <ListItemText primary="AI Anomaly Alerts" secondary="Push notifications for unusual behavior" />
                  <Switch defaultChecked color="primary" />
                </ListItem>
              </List>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Trusted & Blocked Recipients */}
        <Grid size={{ xs: 12 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>Recipient Security Profiles</Typography>
              <Grid container spacing={3}>
                {mockRecipients.map(rec => (
                  <Grid size={{ xs: 12, sm: 6, md: 4 }} key={rec.id}>
                    <Box sx={{ p: 2, borderRadius: 2, border: '1px solid rgba(0,0,0,0.1)', bgcolor: rec.isTrusted ? 'transparent' : 'rgba(239, 68, 68, 0.05)' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        {rec.isTrusted ? <CheckCircle color="success" fontSize="small" /> : <Block color="error" fontSize="small" />}
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>{rec.name}</Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">{rec.accountMasked} â€¢ {rec.bankCode}</Typography>
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </MotionCard>
        </Grid>
      </Grid>
    </Box>
  );
};

