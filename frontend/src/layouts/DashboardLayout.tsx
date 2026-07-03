import { Box, Drawer, List, ListItem, ListItemIcon, ListItemText, Typography, AppBar, Toolbar, IconButton, Avatar, ListItemButton } from '@mui/material';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Home, SwapHoriz, Shield, PieChart, Settings, Menu } from '@mui/icons-material';
import { useState } from 'react';

const drawerWidth = 260;

const menuItems = [
  { text: 'Command Center', icon: <Home />, path: '/dashboard' },
  { text: 'Transfer', icon: <SwapHoriz />, path: '/transfer' },
  { text: 'Security', icon: <Shield />, path: '/security' },
  { text: 'Transactions', icon: <SwapHoriz />, path: '/transactions' },
  { text: 'Analytics', icon: <PieChart />, path: '/analytics' },
  { text: 'Settings', icon: <Settings />, path: '/settings' },
  { text: 'Admin', icon: <Shield />, path: '/admin' },
];

export const DashboardLayout = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleDrawerToggle = () => setMobileOpen(!mobileOpen);

  const drawerContent = (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <Box sx={{ p: 3, display: 'flex', alignItems: 'center', gap: 2 }}>
        <Box sx={{ width: 32, height: 32, borderRadius: '50%', background: 'linear-gradient(135deg, #1A237E, #10B981)' }} />
        <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: '-0.02em', color: 'primary.main' }}>
          NIRNAY
        </Typography>
      </Box>
      <List sx={{ px: 2, flex: 1 }}>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding sx={{ mb: 1 }}>
            <ListItemButton
              onClick={() => navigate(item.path)}
              sx={{
                borderRadius: 2,
                backgroundColor: location.pathname.startsWith(item.path) && item.path !== '/dashboard' || location.pathname === item.path ? 'rgba(26, 35, 126, 0.08)' : 'transparent',
                color: location.pathname.startsWith(item.path) && item.path !== '/dashboard' || location.pathname === item.path ? 'primary.main' : 'text.secondary',
                '&:hover': {
                  backgroundColor: 'rgba(26, 35, 126, 0.04)',
                }
              }}
            >
            <ListItemIcon sx={{ color: 'inherit', minWidth: 40 }}>{item.icon}</ListItemIcon>
            <ListItemText primary={item.text} slotProps={{ primary: { sx: { fontWeight: 600, fontSize: '0.9rem' } } }} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Box sx={{ p: 2, borderTop: '1px solid rgba(0,0,0,0.05)' }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 1 }}>
          <Avatar sx={{ width: 36, height: 36, bgcolor: 'primary.light' }}>A</Avatar>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 600 }}>Alok Kumar</Typography>
            <Typography variant="caption" color="text.secondary">Premium Tier</Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar
        position="fixed"
        elevation={0}
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
          bgcolor: 'background.default',
          borderBottom: '1px solid rgba(0,0,0,0.05)',
        }}
      >
        <Toolbar>
          <IconButton color="inherit" edge="start" onClick={handleDrawerToggle} sx={{ mr: 2, display: { sm: 'none' }, color: 'text.primary' }}>
            <Menu />
          </IconButton>
          <Box sx={{ flexGrow: 1 }} />
        </Toolbar>
      </AppBar>

      <Box component="nav" sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}>
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{ keepMounted: true }}
          sx={{ display: { xs: 'block', sm: 'none' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: 'none' } }}
        >
          {drawerContent}
        </Drawer>
        <Drawer
          variant="permanent"
          sx={{ display: { xs: 'none', sm: 'block' }, '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth, borderRight: '1px solid rgba(0,0,0,0.05)' } }}
          open
        >
          {drawerContent}
        </Drawer>
      </Box>

      <Box component="main" sx={{ flexGrow: 1, p: { xs: 2, sm: 4 }, width: { sm: `calc(100% - ${drawerWidth}px)` }, mt: '64px' }}>
        <Outlet />
      </Box>
    </Box>
  );
};

