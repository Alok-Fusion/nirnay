import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip, TextField, InputAdornment, IconButton, Paper } from '@mui/material';
import { Search, FilterList, Download, CheckCircle, Warning } from '@mui/icons-material';
import { mockTransactions } from '../../services/mockData';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const MotionTableRow = motion(TableRow);

export const TransactionsHub = () => {
  const navigate = useNavigate();

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', py: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h4" sx={{ fontWeight: 700 }}>Transactions</Typography>
          <Typography variant="body1" color="text.secondary">View and search your complete transaction history.</Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <TextField 
            size="small" 
            placeholder="Search transactions..." 
            slotProps={{
              input: {
                startAdornment: <InputAdornment position="start"><Search /></InputAdornment>,
              }
            }}
            sx={{ bgcolor: 'white', borderRadius: 1 }}
          />
          <IconButton sx={{ bgcolor: 'white' }}><FilterList /></IconButton>
          <IconButton sx={{ bgcolor: 'white' }}><Download /></IconButton>
        </Box>
      </Box>

      <TableContainer component={Paper} elevation={0} sx={{ borderRadius: 4, border: '1px solid rgba(0,0,0,0.05)' }}>
        <Table>
          <TableHead sx={{ bgcolor: 'rgba(0,0,0,0.02)' }}>
            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>ID</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Date</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Recipient</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Amount</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>AI Decision</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {mockTransactions.map((tx, idx) => {
              const isBlocked = tx.status === 'BLOCKED';
              return (
                <MotionTableRow 
                  key={tx.id}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  hover
                  sx={{ cursor: 'pointer', '&:last-child td, &:last-child th': { border: 0 } }}
                  onClick={() => navigate(`/decision/${tx.id}`)}
                >
                  <TableCell>{tx.id}</TableCell>
                  <TableCell>{new Date(tx.date).toLocaleDateString()}</TableCell>
                  <TableCell sx={{ fontWeight: 500 }}>{tx.recipientName}</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>${tx.amount.toLocaleString()}</TableCell>
                  <TableCell>
                    <Chip 
                      icon={isBlocked ? <Warning fontSize="small" /> : <CheckCircle fontSize="small" />}
                      label={isBlocked ? "High Risk" : "Approved"} 
                      size="small"
                      sx={{ 
                        bgcolor: isBlocked ? 'error.light' : 'success.light',
                        color: isBlocked ? 'error.dark' : 'success.dark',
                        fontWeight: 600
                      }}
                    />
                  </TableCell>
                  <TableCell>
                    <Typography variant="body2" sx={{ color: isBlocked ? 'error.main' : 'success.main', fontWeight: 600 }}>
                      {tx.status}
                    </Typography>
                  </TableCell>
                </MotionTableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

