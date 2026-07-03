import { Box, Typography, TextField, Button } from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts';

export const LoginScreen = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate login
    login('mock_jwt_token', { id: 'usr_1', name: 'Alok Kumar', email: 'alok@example.com' });
    navigate('/dashboard');
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <Box sx={{ display: { xs: 'block', md: 'none' }, mb: 4 }}>
        <Typography variant="h3" color="primary.main" sx={{ fontWeight: "bold" }}>NIRNAY</Typography>
      </Box>

      <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>Welcome Back</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Please enter your credentials to securely log in.
      </Typography>

      <form onSubmit={handleLogin}>
        <TextField
          fullWidth
          label="Email Address"
          type="email"
          variant="outlined"
          sx={{ mb: 3 }}
          defaultValue="demo@nirnay.ai"
          required
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          variant="outlined"
          sx={{ mb: 4 }}
          defaultValue="password123"
          required
        />
        <Button 
          fullWidth 
          type="submit" 
          variant="contained" 
          color="primary" 
          size="large"
          sx={{ py: 1.5, fontSize: '1.1rem' }}
        >
          Sign In
        </Button>
      </form>
    </motion.div>
  );
};

