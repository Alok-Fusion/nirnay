import { Box, Typography, Card, CardContent, Grid, TextField, Button, Switch, Divider } from '@mui/material';
import { motion } from 'framer-motion';

const MotionCard = motion(Card);

export const ProfileSettings = () => {
  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', py: 4 }}>
      <Typography variant="h4" sx={{ fontWeight: 700, mb: 4 }}>Settings & Profile</Typography>

      <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} sx={{ mb: 4 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h6" sx={{ mb: 3 }}>Personal Information</Typography>
          <Grid container spacing={3}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth label="Full Name" defaultValue="Alok Kumar" />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth label="Email Address" defaultValue="alok@example.com" />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <TextField fullWidth label="Phone Number" defaultValue="+1 (555) 123-4567" />
            </Grid>
          </Grid>
          <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
            <Button variant="contained">Save Changes</Button>
          </Box>
        </CardContent>
      </MotionCard>

      <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
        <CardContent sx={{ p: 4 }}>
          <Typography variant="h6" sx={{ mb: 3 }}>Preferences</Typography>
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Box>
              <Typography sx={{ fontWeight: 500 }}>Dark Mode</Typography>
              <Typography variant="body2" color="text.secondary">Switch between light and dark themes.</Typography>
            </Box>
            <Switch color="primary" />
          </Box>
          <Divider sx={{ my: 2 }} />
          
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Box>
              <Typography sx={{ fontWeight: 500 }}>Push Notifications</Typography>
              <Typography variant="body2" color="text.secondary">Receive real-time alerts for transactions.</Typography>
            </Box>
            <Switch color="primary" defaultChecked />
          </Box>
          <Divider sx={{ my: 2 }} />

          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box>
              <Typography sx={{ fontWeight: 500 }}>Reduced Motion</Typography>
              <Typography variant="body2" color="text.secondary">Disable animations across the platform.</Typography>
            </Box>
            <Switch color="primary" />
          </Box>
        </CardContent>
      </MotionCard>
    </Box>
  );
};

