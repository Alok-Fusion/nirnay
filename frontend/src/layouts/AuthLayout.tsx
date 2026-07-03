import { Box, Typography } from '@mui/material';
import { Outlet } from 'react-router-dom';

export const AuthLayout = () => {
  return (
    <Box sx={{ minHeight: '100vh', display: 'flex', bgcolor: 'background.default' }}>
      {/* Left side - Branding & Value Prop */}
      <Box 
        sx={{ 
          flex: 1, 
          display: { xs: 'none', md: 'flex' }, 
          flexDirection: 'column',
          justifyContent: 'center',
          p: 8,
          background: 'linear-gradient(135deg, #1A237E 0%, #10B981 100%)',
          color: 'white'
        }}
      >
        <Typography variant="h2" sx={{ fontWeight: 800, mb: 2 }}>NIRNAY</Typography>
        <Typography variant="h5" sx={{ fontWeight: 400, opacity: 0.9, maxWidth: 500 }}>
          The premium banking experience secured by advanced artificial intelligence.
        </Typography>
      </Box>

      {/* Right side - Forms */}
      <Box sx={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', p: 4 }}>
        <Box sx={{ width: '100%', maxWidth: 400 }}>
          <Outlet />
        </Box>
      </Box>
    </Box>
  );
};
