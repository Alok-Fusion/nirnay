import { Box, Typography, Grid, Card, CardContent, Divider, Switch, List, ListItem, ListItemText, ListItemIcon, Chip } from '@mui/material';
import { Security, Block, Fingerprint, NotificationsActive, CheckCircle } from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useSecurityMetrics, useRecipients, useUserBehavior } from '../../services/apiHooks';
import { TwinTrainer } from './TwinTrainer';

const MotionCard = motion(Card);

const formatHour = (hour: number | null | undefined) => {
  if (hour == null) return 'N/A';
  const ampm = hour >= 12 ? 'PM' : 'AM';
  const displayHour = hour % 12 || 12;
  return `${displayHour}:00 ${ampm}`;
};

const getLimit = (level: string | undefined) => {
  switch (level) {
    case 'TRUSTED':
      return '$100,000';
    case 'ESTABLISHED':
      return '$50,000';
    case 'LEARNING':
      return '$25,000';
    case 'NEW':
    default:
      return '$10,000';
  }
};

export const SecurityCenter = () => {
  const { data: securityMetrics, isLoading: isLoadingSecurity } = useSecurityMetrics();
  const { data: recipients = [] } = useRecipients();
  const { data: behavior, isLoading: isLoadingBehavior } = useUserBehavior();
  
  const isLoading = isLoadingSecurity || isLoadingBehavior;
  
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
              <Typography variant="h6" sx={{ mb: 3 }}>AI Protection & Twin Metrics</Typography>
              {isLoading ? (
                <Typography>Loading metrics...</Typography>
              ) : (
                <>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                    <Typography color="text.secondary">Digital Twin Level</Typography>
                    <Chip 
                      label={behavior?.trust_level || 'NEW'} 
                      color="primary" 
                      size="small" 
                      sx={{ fontWeight: 'bold', fontSize: '0.75rem' }} 
                    />
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Behavioral Trust Score</Typography>
                    <Typography sx={{ fontWeight: 'bold' }} color="primary.main">{(behavior?.trust_score ?? 50)} / 100</Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Average Transfer Hour</Typography>
                    <Typography sx={{ fontWeight: 'bold' }}>{formatHour(behavior?.preferred_transfer_hour)}</Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Daily Transfer Limit</Typography>
                    <Typography sx={{ fontWeight: 'bold' }} color="success.main">{getLimit(behavior?.trust_level)}</Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Daily Transfer Velocity</Typography>
                    <Typography sx={{ fontWeight: 'bold' }}>{(behavior?.average_daily_transactions ?? 0).toFixed(2)} tx/day</Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Active Locations</Typography>
                    <Typography sx={{ fontWeight: 'bold', textAlign: 'right' }}>
                      {behavior?.known_locations && behavior.known_locations.length > 0 
                        ? behavior.known_locations.join(', ') 
                        : 'None'}
                    </Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Trusted Devices</Typography>
                    <Typography sx={{ fontWeight: 'bold', textAlign: 'right' }}>
                      {behavior?.known_devices && behavior.known_devices.length > 0 
                        ? behavior.known_devices.join(', ') 
                        : 'None'}
                    </Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
                    <Typography color="text.secondary">Blocked Attempts (30d)</Typography>
                    <Typography sx={{ fontWeight: 'bold' }} color="error.main">{metrics.blockedAttempts}</Typography>
                  </Box>
                  <Divider sx={{ my: 1.5 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                    <Typography color="text.secondary">Last Action Profile Update</Typography>
                    <Typography sx={{ fontWeight: 'bold' }}>
                      {behavior?.last_updated ? new Date(behavior.last_updated).toLocaleString() : 'N/A'}
                    </Typography>
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

        {/* Digital Twin training upload */}
        <Grid size={{ xs: 12 }}>
          <TwinTrainer />
        </Grid>

        {/* Trusted & Blocked Recipients */}
        <Grid size={{ xs: 12 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3 }}>Recipient Security Profiles</Typography>
              <Grid container spacing={3}>
                {recipients.map((rec: any) => (
                  <Grid size={{ xs: 12, sm: 6, md: 4 }} key={rec.id}>
                    <Box sx={{ p: 2, borderRadius: 2, border: '1px solid rgba(0,0,0,0.1)', bgcolor: rec.is_trusted ? 'transparent' : 'rgba(239, 68, 68, 0.05)' }}>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                        {rec.is_trusted ? <CheckCircle color="success" fontSize="small" /> : <Block color="error" fontSize="small" />}
                        <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>{rec.name}</Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">{rec.account_number} • {rec.bank_code}</Typography>
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

