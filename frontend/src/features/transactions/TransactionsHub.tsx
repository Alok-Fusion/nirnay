import { useState, useMemo } from 'react';
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Chip, TextField, InputAdornment, IconButton, Paper } from '@mui/material';
import { Person, Search, FilterList, Download, CheckCircle, Warning, Block } from '@mui/icons-material';
import { useTransactions } from '../../services/apiHooks';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

const MotionTableRow = motion(TableRow);

export const TransactionsHub = () => {
  const { data: transactions = [], isLoading } = useTransactions();
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const filteredTransactions = useMemo(() => {
    return transactions.filter((tx: any) => 
      tx.recipientName.toLowerCase().includes(searchTerm.toLowerCase()) || 
      tx.id.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }, [transactions, searchTerm]);

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
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
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
              <TableCell sx={{ fontWeight: 600 }}>Recipient</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Amount</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Date</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>AI Risk Score</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={6} align="center">Loading transactions...</TableCell></TableRow>
            ) : filteredTransactions.length === 0 ? (
              <TableRow><TableCell colSpan={6} align="center">No transactions found.</TableCell></TableRow>
            ) : filteredTransactions.map((tx: any) => (
              <MotionTableRow 
                key={tx.id} 
                hover 
                onClick={() => navigate(`/decision/${tx.id}`)}
                sx={{ cursor: 'pointer' }}
              >
                <TableCell sx={{ fontFamily: 'monospace' }}>{tx.id}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Person fontSize="small" color="action" />
                    <Typography variant="body2">{tx.recipientName}</Typography>
                  </Box>
                </TableCell>
                <TableCell>${tx.amount.toLocaleString()}</TableCell>
                <TableCell>{new Date(tx.created_at).toLocaleString()}</TableCell>
                <TableCell>
                  <Chip 
                    label={tx.aiRiskScore} 
                    size="small" 
                    color={tx.aiRiskScore > 50 ? "error" : "success"}
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Chip 
                    label={tx.status} 
                    size="small" 
                    icon={tx.status === 'COMPLETED' ? <CheckCircle /> : tx.status === 'REJECTED' ? <Block /> : <Warning />}
                    color={tx.status === 'COMPLETED' ? "success" : tx.status === 'REJECTED' ? "error" : "warning"}
                  />
                </TableCell>
              </MotionTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

