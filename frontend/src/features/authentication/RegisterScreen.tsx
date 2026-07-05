import { useState } from 'react';
import { Box, Typography, TextField, Button, Alert } from '@mui/material';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useRegister } from '../../services/apiHooks';

export const RegisterScreen = () => {
  const navigate = useNavigate();
  const registerMutation = useRegister();
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleRegister = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError('');
    setSuccess(false);
    
    const data = new FormData(e.currentTarget);
    const email = data.get('email');
    const fullName = data.get('fullName');
    const password = data.get('password');

    try {
      await registerMutation.mutateAsync({
        email,
        full_name: fullName,
        password
      });
      setSuccess(true);
      setTimeout(() => {
        navigate('/auth/login');
      }, 2000);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Email may already be registered.');
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }}>
      <Box sx={{ display: { xs: 'block', md: 'none' }, mb: 4 }}>
        <Typography variant="h3" color="primary.main" sx={{ fontWeight: "bold" }}>NIRNAY</Typography>
      </Box>

      <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>Create Account</Typography>
      <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
        Join NIRNAY's decision intelligence platform.
      </Typography>

      <form onSubmit={handleRegister}>
        {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
        {success && <Alert severity="success" sx={{ mb: 3 }}>Registration successful! Redirecting to login...</Alert>}

        <TextField
          fullWidth
          label="Full Name"
          name="fullName"
          variant="outlined"
          sx={{ mb: 3 }}
          required
        />
        <TextField
          fullWidth
          label="Email Address"
          type="email"
          name="email"
          variant="outlined"
          sx={{ mb: 3 }}
          required
        />
        <TextField
          fullWidth
          label="Password"
          type="password"
          name="password"
          variant="outlined"
          sx={{ mb: 4 }}
          required
        />
        <Button 
          fullWidth 
          type="submit" 
          variant="contained" 
          color="primary" 
          size="large"
          disabled={registerMutation.isPending || success}
          sx={{ py: 1.5, fontSize: '1.1rem', mb: 2 }}
        >
          {registerMutation.isPending ? 'Registering...' : 'Sign Up'}
        </Button>

        <Box sx={{ textAlign: 'center', mt: 2 }}>
          <Typography variant="body2" color="text.secondary">
            Already have an account?{' '}
            <Button 
              variant="text" 
              onClick={() => navigate('/auth/login')}
              sx={{ textTransform: 'none', fontWeight: 600, p: 0, minWidth: 0, verticalAlign: 'baseline' }}
            >
              Sign In
            </Button>
          </Typography>
        </Box>
      </form>
    </motion.div>
  );
};
