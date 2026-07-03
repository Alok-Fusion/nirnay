import { Box, Typography, Grid, Card, CardContent, CircularProgress } from '@mui/material';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, LineChart, Line, PieChart, Pie, Cell, Legend, AreaChart, Area } from 'recharts';
import { useAnalytics, useUserBehavior } from '../../services/apiHooks';
import { TrendingUp, Block, Shield, Security } from '@mui/icons-material';

const MotionCard = motion(Card);

const COLORS = ['#1A237E', '#10B981', '#F59E0B', '#EF4444'];

export const AnalyticsDashboard = () => {
  const { data: analytics, isLoading: loadingAnalytics } = useAnalytics();
  const { data: behavior, isLoading: loadingBehavior } = useUserBehavior();

  const isLoading = loadingAnalytics || loadingBehavior;

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  const cashFlowData = analytics?.cash_flow || [];
  const interventionsData = analytics?.ai_interventions || [];
  const categoryData = analytics?.category_spending || [];
  const hourlyData = analytics?.hourly_distribution || [];
  const summary = analytics?.summary || {
    total_transactions: 0,
    total_spent: 0,
    total_blocked: 0,
    active_rules_triggered: 0
  };

  const trustScore = behavior?.trust_score ?? 50;
  const trustLevel = behavior?.trust_level ?? 'NEW';

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', py: 4 }}>
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" sx={{ fontWeight: "700", mb: 1 }}>Analytics & Digital Twin Insights</Typography>
        <Typography variant="body1" color="text.secondary">
          Understand your financial patterns and monitor the behavioral heuristics powering your Digital Twin.
        </Typography>
      </Box>

      {/* KPI Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }}>
            <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 3 }}>
              <Box sx={{ width: 48, height: 48, borderRadius: 2, bgcolor: 'rgba(26, 35, 126, 0.1)', color: '#1A237E', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <TrendingUp />
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>Total Spent</Typography>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>${summary.total_spent.toLocaleString()}</Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.05 }}>
            <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 3 }}>
              <Box sx={{ width: 48, height: 48, borderRadius: 2, bgcolor: 'rgba(239, 68, 68, 0.1)', color: '#EF4444', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Block />
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>Blocked Fraud</Typography>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>${summary.total_blocked.toLocaleString()}</Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }}>
            <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 3 }}>
              <Box sx={{ width: 48, height: 48, borderRadius: 2, bgcolor: 'rgba(245, 158, 11, 0.1)', color: '#F59E0B', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Shield />
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>Policy Interventions</Typography>
                <Typography variant="h6" sx={{ fontWeight: 700 }}>{summary.active_rules_triggered} triggers</Typography>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        <Grid size={{ xs: 12, sm: 6, md: 3 }}>
          <MotionCard initial={{ opacity: 0, y: 15 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.15 }}>
            <CardContent sx={{ display: 'flex', alignItems: 'center', gap: 2, p: 3 }}>
              <Box sx={{ width: 48, height: 48, borderRadius: 2, bgcolor: 'rgba(16, 185, 129, 0.1)', color: '#10B981', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Security />
              </Box>
              <Box>
                <Typography variant="caption" color="text.secondary" sx={{ fontWeight: 600 }}>Twin Score</Typography>
                <Box sx={{ display: 'flex', alignItems: 'baseline', gap: 0.5 }}>
                  <Typography variant="h6" sx={{ fontWeight: 700 }}>{trustScore}</Typography>
                  <Typography variant="caption" color="text.secondary">/100 ({trustLevel})</Typography>
                </Box>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>
      </Grid>

      {/* Main Charts Grid */}
      <Grid container spacing={3}>
        {/* Spending vs Income */}
        <Grid size={{ xs: 12, md: 8 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 4, fontWeight: 700 }}>Cash Flow Overview (Last 6 Months)</Typography>
              <Box sx={{ width: '100%', height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={cashFlowData}>
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
        <Grid size={{ xs: 12, md: 4 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} sx={{ height: '100%' }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 4, fontWeight: 700 }}>AI Risk Interventions</Typography>
              <Box sx={{ width: '100%', height: 320 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={interventionsData}>
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

        {/* Category spending distribution */}
        <Grid size={{ xs: 12, md: 6 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Spending Category Breakdown</Typography>
              <Box sx={{ width: '100%', height: 280, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={categoryData}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={90}
                      paddingAngle={4}
                      dataKey="value"
                    >
                      {categoryData.map((_: any, index: number) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => `$${value}`} contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }} />
                    <Legend verticalAlign="bottom" height={36} />
                  </PieChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>

        {/* Temporal active distribution */}
        <Grid size={{ xs: 12, md: 6 }}>
          <MotionCard initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.25 }}>
            <CardContent sx={{ p: 4 }}>
              <Typography variant="h6" sx={{ mb: 3, fontWeight: 700 }}>Digital Twin Temporal Heuristics</Typography>
              <Box sx={{ width: '100%', height: 280 }}>
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={hourlyData}>
                    <defs>
                      <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#1A237E" stopOpacity={0.4}/>
                        <stop offset="95%" stopColor="#1A237E" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} opacity={0.2} />
                    <XAxis dataKey="hour" axisLine={false} tickLine={false} interval={3} />
                    <YAxis axisLine={false} tickLine={false} />
                    <Tooltip contentStyle={{ borderRadius: 8, border: 'none', boxShadow: '0 4px 20px rgba(0,0,0,0.1)' }} />
                    <Area type="monotone" dataKey="count" stroke="#1A237E" strokeWidth={2} fillOpacity={1} fill="url(#colorCount)" name="Transfers Count" />
                  </AreaChart>
                </ResponsiveContainer>
              </Box>
            </CardContent>
          </MotionCard>
        </Grid>
      </Grid>
    </Box>
  );
};

