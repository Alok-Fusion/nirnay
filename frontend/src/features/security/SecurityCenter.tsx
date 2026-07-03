import { Box, Typography, Grid, Card, CardContent, Divider, Switch, List, ListItem, ListItemText, ListItemIcon } from '@mui/material';
import { Security, DevicesOther, Block, Fingerprint, NotificationsActive } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { mockSecurityMetrics, mockRecipients } from '../../services/mockData';

const MotionCard = motion(Card);

export const SecurityCenter = () => {
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
        <Grid item xs={12} md={6}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} sx={{ height: '100%' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>AI Protection Metrics</Typography>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography color="text.secondary">Overall Security Score</Typography>
                <Typography fontWeight="bold" color="secondary.main">{mockSecurityMetrics.overallScore} / 100</Typography>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                <Typography color="text.secondary">Trusted Devices</Typography>
                <Typography fontWeight="bold">{mockSecurityMetrics.trustedDevices}</Typography>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                <Typography color="text.secondary">Blocked Fraud Attempts (30d)</Typography>
                <Typography fontWeight="bold" color="error.main">{mockSecurityMetrics.blockedAttempts}</Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Security Settings */}
        <Grid item xs={12} md={6}>
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
        <Grid item xs={12}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>Recipient Security Profiles</Typography>
              <Grid container spacing={3}>
                {mockRecipients.map(rec => (
                  <Grid item xs={12} sm={6} md={4} key={rec.id}>
                    <Box sx={{ p: 2, borderRadius: 2, border: '1px solid rgba(0,0,0,0.1)', bgcolor: rec.isTrusted ? 'transparent' : 'rgba(239, 68, 68, 0.05)' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        {rec.isTrusted ? <CheckCircle color="success" fontSize="small" /> : <Block color="error" fontSize="small" />}
                        <Typography variant="subtitle2" fontWeight="600">{rec.name}</Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">{rec.accountMasked} • {rec.bankCode}</Typography>
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
