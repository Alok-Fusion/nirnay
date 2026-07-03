import { Box, Typography, Grid, Card, CardContent, Table, TableBody, TableCell, TableHead, TableRow, Chip } from '@mui/material';
import { Shield, Warning, Gavel } from '@mui/icons-material';
import { mockTransactions } from '../../services/mockData';

export const AdminDashboard = () => {
  const highRiskTxs = mockTransactions.filter(t => t.aiRiskScore > 75);

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', py: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 4 }}>
        <Shield sx={{ fontSize: 40, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" fontWeight="700">Admin Command Center</Typography>
          <Typography variant="body1" color="text.secondary">Global AI risk monitoring and system metrics.</Typography>
        </Box>
      </Box>

      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>Active High-Risk Cases</Typography>
              <Typography variant="h3" color="error.main" fontWeight="700">{highRiskTxs.length}</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>Global AI Confidence</Typography>
              <Typography variant="h3" color="success.main" fontWeight="700">96.4%</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="text.secondary" gutterBottom>System Uptime</Typography>
              <Typography variant="h3" color="primary.main" fontWeight="700">99.99%</Typography>
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
              <TableCell sx={{ fontWeight: 600 }}>Risk Score</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
              <TableCell sx={{ fontWeight: 600 }}>Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {highRiskTxs.map(tx => (
              <TableRow key={tx.id}>
                <TableCell>{tx.id}</TableCell>
                <TableCell>{tx.recipientName}</TableCell>
                <TableCell>
                  <Typography fontWeight="700" color="error.main">{tx.aiRiskScore}/100</Typography>
                </TableCell>
                <TableCell>
                  <Chip label="Awaiting Review" color="warning" size="small" />
                </TableCell>
                <TableCell>
                  <Chip icon={<Gavel />} label="Review Case" variant="outlined" clickable />
                </TableCell>
              </TableRow>
            ))}
            {highRiskTxs.length === 0 && (
              <TableRow>
                <TableCell colSpan={5} align="center">No active cases.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </Card>
    </Box>
  );
};
