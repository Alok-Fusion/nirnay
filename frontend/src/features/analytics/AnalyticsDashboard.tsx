import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, LineChart, Line } from 'recharts';

const mockSpendingData = [
  { name: 'Jan', spending: 4000, income: 5500 },
  { name: 'Feb', spending: 3000, income: 5500 },
  { name: 'Mar', spending: 2000, income: 5500 },
  { name: 'Apr', spending: 2780, income: 5800 },
  { name: 'May', spending: 1890, income: 5800 },
  { name: 'Jun', spending: 2390, income: 6000 },
  { name: 'Jul', spending: 3490, income: 6000 },
];

const mockAiInterventionData = [
  { name: 'Week 1', blocked: 2, approved: 15 },
  { name: 'Week 2', blocked: 1, approved: 18 },
  { name: 'Week 3', blocked: 4, approved: 12 },
  { name: 'Week 4', blocked: 0, approved: 20 },
];

const MotionCard = motion(Card);

export const AnalyticsDashboard = () => {
  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" fontWeight="700">Analytics</Typography>
        <Typography variant="body1" color="text.secondary">Understand your financial health and AI protection trends.</Typography>
      </Box>

      <Grid container spacing={4}>
        {/* Spending vs Income */}
        <Grid item xs={12} lg={8}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 4 }}>Cash Flow (6 Months)</Typography>
              <Box sx={{ width: '100%', height: 350 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={mockSpendingData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.3} />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} />
                    <YAxis axisLine={false} tickLine={false} tickFormatter={(value) => `$${value}`} />
                    <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }} />
                    <Bar dataKey="spending" fill="#1A237E" radius={[4, 4, 0, 0]} name="Spending" />
                    <Bar dataKey="income" fill="#10B981" radius={[4, 4, 0, 0]} name="Income" />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* AI Interventions */}
        <Grid item xs={12} lg={4}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} sx={{ height: '100%' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 4 }}>AI Risk Interventions</Typography>
              <Box sx={{ width: '100%', height: 350 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={mockAiInterventionData}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.3} />
                    <XAxis dataKey="name" axisLine={false} tickLine={false} />
                    <YAxis axisLine={false} tickLine={false} />
                    <Tooltip contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }} />
                    <Line type="monotone" dataKey="blocked" stroke="#EF4444" strokeWidth={3} dot={{ r: 4 }} name="Blocked (Fraud)" />
                    <Line type="monotone" dataKey="approved" stroke="#10B981" strokeWidth={3} dot={{ r: 4 }} name="Safe Transfers" />
                  </LineChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>
      </Grid>
    </Box>
  );
};
