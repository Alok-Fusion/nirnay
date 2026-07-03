import { useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts';
import { useLogin } from '../../services/apiHooks';

export const LoginScreen = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const loginMutation = useLogin();
  const [error, setError] = useState('');

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    const data = new FormData(e.currentTarget);
    const email = data.get('email');
    const password = data.get('password');

    try {
      const { tokenData, userData } = await loginMutation.mutateAsync({ email, password });
      login(tokenData, userData);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
    }
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
        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}

        <TextField
          fullWidth
          label="Email Address"
          type="email"
          name="email"
          variant="outlined"
          sx={{ mb: 3 }}
          defaultValue="alok@example.com"
          required
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          name="password"
          variant="outlined"
          sx={{ mb: 4 }}
          defaultValue="password"
          required
        />
        <Button 
          fullWidth 
          type="submit" 
          variant="contained" 
          color="primary" 
          size="large"
          disabled={loginMutation.isPending}
          sx={{ py: 1.5, fontSize: '1.1rem' }}
        >
          {loginMutation.isPending ? 'Signing In...' : 'Sign In'}
        </Button>
      </form>
    </motion.div>
  );
};

