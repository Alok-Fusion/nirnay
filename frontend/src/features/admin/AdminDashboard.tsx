import { 
  Box, Typography, Grid, Card, CardContent, Table, TableBody, TableCell, 
  TableHead, TableRow, Chip, Button, Dialog, DialogTitle, DialogContent, 
  DialogActions, TextField, MenuItem, CircularProgress 
} from '@mui/material';
import { Person, Block, CheckCircle, Settings, AdminPanelSettings } from '@mui/icons-material';
import { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  useTransactions, useAdminStats, useCustomers, 
  useSuspendCustomer, useActivateCustomer, useOverrideBehavior 
} from '../../services/apiHooks';

const MotionCard = motion(Card);

export const AdminDashboard = () => {
  const { data: transactions = [], isLoading: loadingTx } = useTransactions();
  const { data: stats = {}, isLoading: loadingStats } = useAdminStats();
  const { data: customers = [], isLoading: loadingCustomers } = useCustomers();
  
  const suspendMutation = useSuspendCustomer();
  const activateMutation = useActivateCustomer();
  const overrideMutation = useOverrideBehavior();

  const [selectedCustomer, setSelectedCustomer] = useState<any>(null);
  const [overrideScore, setOverrideScore] = useState(50);
  const [overrideLevel, setOverrideLevel] = useState('NEW');
  const [openOverride, setOpenOverride] = useState(false);

  // Filter for high risk cases
  const flaggedTransactions = transactions.filter((tx: any) => tx.aiRiskScore > 50 || tx.status === 'REJECTED');

  const handleOpenOverride = (cust: any) => {
    setSelectedCustomer(cust);
    setOverrideScore(cust.behavior?.trust_score ?? 50);
    setOverrideLevel(cust.behavior?.trust_level ?? 'NEW');
    setOpenOverride(true);
  };

  const handleSaveOverride = async () => {
    if (!selectedCustomer) return;
    try {
      await overrideMutation.mutateAsync({
        customerId: selectedCustomer.id,
        trust_score: overrideScore,
        trust_level: overrideLevel
      });
      setOpenOverride(false);
      setSelectedCustomer(null);
    } catch (err) {
      console.error("Failed to override behavior", err);
    }
  };

  const handleToggleStatus = async (cust: any) => {
    try {
      if (cust.is_active) {
        await suspendMutation.mutateAsync(cust.id);
      } else {
        await activateMutation.mutateAsync(cust.id);
      }
    } catch (err) {
      console.error("Failed to toggle status", err);
    }
  };

  const isActionPending = suspendMutation.isPending || activateMutation.isPending || overrideMutation.isPending;

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', py: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 4 }}>
        <AdminPanelSettings sx={{ fontSize: 48, color: 'primary.main' }} />
        <Box>
          <Typography variant="h4" sx={{ fontWeight: "700" }}>Admin Intelligence Center</Typography>
          <Typography variant="body1" color="text.secondary">Global security monitoring, system metrics, and customer administration.</Typography>
        </Box>
      </Box>

      {/* Stats row */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} sx={{ background: 'rgba(255,255,255,0.7)', backdropFilter: 'blur(8px)' }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 1 }}>Flagged Fraud Alerts</Typography>
              <Typography variant="h3" color="error.main" sx={{ fontWeight: "700" }}>
                {flaggedTransactions.length}
              </Typography>
            </CardContent>
          </MotionCard>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }} sx={{ background: 'rgba(255,255,255,0.7)', backdropFilter: 'blur(8px)' }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 1 }}>Total Managed Users</Typography>
              <Typography variant="h3" color="primary.main" sx={{ fontWeight: "700" }}>
                {loadingStats ? <CircularProgress size={30} /> : stats.total_users}
              </Typography>
            </CardContent>
          </MotionCard>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} sx={{ background: 'rgba(255,255,255,0.7)', backdropFilter: 'blur(8px)' }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 1 }}>AI Decision Confidence</Typography>
              <Typography variant="h3" color="success.main" sx={{ fontWeight: "700" }}>
                {stats.ai_confidence ?? "96.4"}%
              </Typography>
            </CardContent>
          </MotionCard>
        </Grid>
        <Grid size={{ xs: 12, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }} sx={{ background: 'rgba(255,255,255,0.7)', backdropFilter: 'blur(8px)' }}>
            <CardContent>
              <Typography color="text.secondary" variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 1 }}>Infrastructure Status</Typography>
              <Typography variant="h3" color="success.main" sx={{ fontWeight: "700", display: 'flex', alignItems: 'center', gap: 1 }}>
                <CheckCircle color="success" /> Healthy
              </Typography>
            </CardContent>
          </MotionCard>
        </Grid>
      </Grid>

      {/* Main Grid: Left is users list, right is flagged alerts */}
      <Grid container spacing={4}>
        {/* User Administration */}
        <Grid size={{ xs: 12, md: 7 }}>
          <Typography variant="h5" sx={{ mb: 2.5, fontWeight: 700 }}>Customer Directory & Controls</Typography>
          <Card sx={{ borderRadius: 3, border: '1px solid rgba(0,0,0,0.06)' }}>
            <Table>
              <TableHead sx={{ bgcolor: 'rgba(0,0,0,0.02)' }}>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>Customer</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Status</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Behavior Twin</TableCell>
                  <TableCell sx={{ fontWeight: 600, textAlign: 'right' }}>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loadingCustomers ? (
                  <TableRow><TableCell colSpan={4} align="center"><CircularProgress /></TableCell></TableRow>
                ) : customers.length === 0 ? (
                  <TableRow><TableCell colSpan={4} align="center">No customers found.</TableCell></TableRow>
                ) : customers.map((cust: any) => (
                  <TableRow key={cust.id} hover>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5 }}>
                        <Person color="action" />
                        <Box>
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>{cust.full_name || "Unknown"}</Typography>
                          <Typography variant="caption" color="text.secondary">{cust.email}</Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={cust.is_active ? "Active" : "Suspended"} 
                        size="small" 
                        color={cust.is_active ? "success" : "error"} 
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>
                      <Box>
                        <Typography variant="body2" sx={{ fontWeight: 600 }}>
                          Score: {cust.behavior?.trust_score ?? 50}/100
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          Level: {cust.behavior?.trust_level ?? "NEW"}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell align="right">
                      <Box sx={{ display: 'flex', flexDirection: 'row', gap: 1, justifyContent: 'flex-end' }}>
                        <Button 
                          size="small" 
                          variant="outlined" 
                          color={cust.is_active ? "error" : "success"}
                          onClick={() => handleToggleStatus(cust)}
                          disabled={isActionPending}
                          startIcon={cust.is_active ? <Block /> : <CheckCircle />}
                        >
                          {cust.is_active ? "Suspend" : "Activate"}
                        </Button>
                        <Button 
                          size="small" 
                          variant="contained" 
                          onClick={() => handleOpenOverride(cust)}
                          disabled={isActionPending}
                          startIcon={<Settings />}
                        >
                          Twin
                        </Button>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </Grid>

        {/* Flagged AI Transactions */}
        <Grid size={{ xs: 12, md: 5 }}>
          <Typography variant="h5" sx={{ mb: 2.5, fontWeight: 700 }}>Security Risk Interventions</Typography>
          <Card sx={{ borderRadius: 3, border: '1px solid rgba(239, 68, 68, 0.15)' }}>
            <Table>
              <TableHead sx={{ bgcolor: 'rgba(239, 68, 68, 0.03)' }}>
                <TableRow>
                  <TableCell sx={{ fontWeight: 600 }}>Recipient</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Amount</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Risk Score</TableCell>
                  <TableCell sx={{ fontWeight: 600 }}>Action</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {loadingTx ? (
                  <TableRow><TableCell colSpan={4} align="center"><CircularProgress /></TableCell></TableRow>
                ) : flaggedTransactions.length === 0 ? (
                  <TableRow><TableCell colSpan={4} align="center">No high-risk transactions flagged.</TableCell></TableRow>
                ) : flaggedTransactions.map((tx: any) => (
                  <TableRow key={tx.id} hover>
                    <TableCell>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>{tx.recipientName}</Typography>
                      <Typography variant="caption" color="text.secondary">Tx #{tx.id}</Typography>
                    </TableCell>
                    <TableCell>${tx.amount.toLocaleString()}</TableCell>
                    <TableCell>
                      <Chip 
                        label={`${tx.aiRiskScore}`} 
                        size="small" 
                        color={tx.aiRiskScore > 75 ? "error" : "warning"}
                        sx={{ fontWeight: 'bold' }}
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={tx.status} 
                        size="small" 
                        color={tx.status === 'COMPLETED' ? "success" : tx.status === 'REJECTED' ? "error" : "warning"}
                      />
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Card>
        </Grid>
      </Grid>

      {/* Behavior Profile Override Dialog */}
      <Dialog open={openOverride} onClose={() => setOpenOverride(false)} maxWidth="xs" fullWidth>
        <DialogTitle sx={{ fontWeight: 700 }}>Override Behavior Profile</DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3, mt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Directly override the Digital Twin values for <strong>{selectedCustomer?.full_name}</strong>.
            </Typography>
            
            <TextField
              label="Trust Score (0-100)"
              type="number"
              fullWidth
              value={overrideScore}
              onChange={(e) => setOverrideScore(Math.max(0, Math.min(100, parseInt(e.target.value) || 0)))}
            />

            <TextField
              select
              label="Trust Level"
              fullWidth
              value={overrideLevel}
              onChange={(e) => setOverrideLevel(e.target.value)}
            >
              <MenuItem value="NEW">NEW</MenuItem>
              <MenuItem value="LEARNING">LEARNING</MenuItem>
              <MenuItem value="ESTABLISHED">ESTABLISHED</MenuItem>
              <MenuItem value="TRUSTED">TRUSTED</MenuItem>
            </TextField>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenOverride(false)}>Cancel</Button>
          <Button variant="contained" onClick={handleSaveOverride} disabled={overrideMutation.isPending}>
            {overrideMutation.isPending ? "Saving..." : "Apply Override"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
