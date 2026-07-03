import { Box, Typography, Grid, Card, CardContent, Table, TableBody, TableCell, TableHead, TableRow, Chip, Button } from '@mui/material';
import { Shield, Person } from '@mui/icons-material';
import { useTransactions } from '../../services/apiHooks';

export const AdminDashboard = () => {
  const { data: transactions = [], isLoading } = useTransactions();
  // Filter for high risk (simulated threshold or real status)
  const flaggedTransactions = transactions.filter((tx: any) => tx.aiRiskScore > 50 || tx.status === 'REJECTED');

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', py: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 4 }}>
        <Shield sx={{ fontSize: 40, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" sx={{ fontWeight: "700" }}>Admin Command Center</Typography>
          <Typography variant="body1" color="text.secondary">Global AI risk monitoring and system metrics.</Typography>
        </Box>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>Active High-Risk Cases</Typography>
              <Typography variant="h3" color="error.main" sx={{ fontWeight: "700" }}>{flaggedTransactions.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>Global AI Confidence</Typography>
              <Typography variant="h3" color="success.main" sx={{ fontWeight: "700" }}>96.4%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid size={{ xs: 12, md: 4 }}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>System Uptime</Typography>
              <Typography variant="h3" color="primary.main" sx={{ fontWeight: "700" }}>99.99%</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Typography variant="h5" sx={{ mb: 2, fontWeight: 600 }}>Flagged Cases</Typography>
      <Card sx={{ border: '1px solid rgba(239, 68, 68, 0.2)' }}>
        <Table>
          <TableHead sx={{ bgcolor: 'rgba(239, 68, 68, 0.05)' }}>
            <TableRow>
              <TableCell sx={{ fontWeight: 600 }}>Case ID</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>User</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Amount</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Risk Score</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {isLoading ? (
              <TableRow><TableCell colSpan={6}>Loading...</TableCell></TableRow>
            ) : transactions.map((tx: any) => (
              <TableRow key={tx.id} hover>
                <TableCell sx={{ fontFamily: 'monospace' }}>{tx.id}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Person fontSize="small" color="action" />
                    <Typography variant="body2">{tx.recipientName}</Typography>
                  </Box>
                </TableCell>
                <TableCell>${tx.amount.toLocaleString()}</TableCell>
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
                    color={tx.status === 'COMPLETED' ? "success" : tx.status === 'REJECTED' ? "error" : "warning"}
                  />
                </TableCell>
                <TableCell>
                  <Button size="small" variant="outlined">Review</Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Card>
    </Box>
  );
};
