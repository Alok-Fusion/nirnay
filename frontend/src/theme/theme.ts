import { createTheme } from '@mui/material/styles';

const typography = {
  fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  h1: { fontWeight: 700, fontSize: '2.5rem', letterSpacing: '-0.02em' },
  h2: { fontWeight: 600, fontSize: '2rem', letterSpacing: '-0.01em' },
  h3: { fontWeight: 600, fontSize: '1.75rem' },
  h4: { fontWeight: 600, fontSize: '1.5rem' },
  h5: { fontWeight: 600, fontSize: '1.25rem' },
  h6: { fontWeight: 600, fontSize: '1rem' },
  body1: { fontSize: '1rem', letterSpacing: '0.01em' },
  body2: { fontSize: '0.875rem', letterSpacing: '0.01em' },
  button: { textTransform: 'none' as const, fontWeight: 600 },
};

const components = {
  MuiButton: {
    styleOverrides: {
      root: {
        borderRadius: 8,
        padding: '10px 24px',
        boxShadow: 'none',
        '&:hover': {
          boxShadow: 'none',
        },
      },
      containedPrimary: {
        '&:hover': {
          backgroundColor: '#151C66', // Darker indigo
        },
      },
    },
  },
  MuiCard: {
    styleOverrides: {
      root: {
        borderRadius: 16,
        boxShadow: '0px 4px 20px rgba(0, 0, 0, 0.05)',
      },
    },
  },
  MuiPaper: {
    styleOverrides: {
      rounded: {
        borderRadius: 12,
      },
    },
  },
  MuiOutlinedInput: {
    styleOverrides: {
      root: {
        borderRadius: 8,
      },
    },
  },
};

const lightPalette = {
  mode: 'light' as const,
  primary: { main: '#1A237E', light: '#534BAE', dark: '#000051', contrastText: '#ffffff' }, // Deep Indigo
  secondary: { main: '#10B981', light: '#5EEAD4', dark: '#047857', contrastText: '#ffffff' }, // Emerald
  warning: { main: '#D4AF37', light: '#FDE047', dark: '#A16207', contrastText: '#ffffff' }, // Premium Gold (Accent)
  background: { default: '#F8F9FA', paper: '#FFFFFF' }, // Warm White
  text: { primary: '#111827', secondary: '#6B7280' },
};

const darkPalette = {
  mode: 'dark' as const,
  primary: { main: '#534BAE', light: '#857BFF', dark: '#1A237E', contrastText: '#ffffff' },
  secondary: { main: '#10B981', light: '#5EEAD4', dark: '#047857', contrastText: '#ffffff' },
  warning: { main: '#D4AF37', light: '#FDE047', dark: '#A16207', contrastText: '#121212' },
  background: { default: '#121212', paper: '#1E1E1E' }, // Graphite
  text: { primary: '#F9FAFB', secondary: '#9CA3AF' },
};

export const lightTheme = createTheme({
  palette: lightPalette,
  typography,
  components,
});

export const darkTheme = createTheme({
  palette: darkPalette,
  typography,
  components,
});

