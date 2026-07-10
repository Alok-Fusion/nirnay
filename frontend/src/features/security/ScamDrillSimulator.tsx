import { Box, Typography, Card, CardContent, Button, Chip, Dialog, DialogTitle, DialogContent, Grid } from '@mui/material';
import { Security, Warning, EmojiEvents, PlayArrow, ArrowForward } from '@mui/icons-material';
import { useState } from 'react';
import { motion } from 'framer-motion';

const MotionCard = motion(Card);

interface Scenario {
  id: number;
  title: string;
  type: string;
  attackerName: string;
  description: string;
  initialMessage: string;
  scamMarkers: string[];
  stages: {
    scammerReply: string;
    responses: {
      text: string;
      isSafe: boolean;
      feedback: string;
    }[];
  }[];
}

const SCENARIOS: Scenario[] = [
  {
    id: 1,
    title: "IRS Urgent Tax Penalty Drill",
    type: "Government Impersonation",
    attackerName: "Officer Davis (IRS Legal Division)",
    description: "A simulated call/message claiming you have urgent unpaid taxes and face arrest unless you transfer money immediately.",
    initialMessage: "This is Officer Davis from the IRS Legal Division. We have filed a lawsuit against you for unpaid tax liabilities of $3,850. If you do not authorize this settlement transfer within 30 minutes, local authorities will issue a warrant. Do not discuss this with anyone.",
    scamMarkers: [
      "Threat of immediate arrest or legal action",
      "Demanding payment via wire transfer / untraceable methods",
      "Forbidding you from talking to friends, family, or bank staff (Secrecy)"
    ],
    stages: [
      {
        scammerReply: "If you hang up or contact your bank to verify, we will immediately close this settlement window and dispatch the county sheriff. Do you understand that you must make the payment now?",
        responses: [
          {
            text: "Yes, I will authorize the transfer now to clear my record. Please don't send the police.",
            isSafe: false,
            feedback: "Falling for immediate pressure. Real government agencies will never threaten immediate arrest over a phone call or chat, nor demand wire transfers."
          },
          {
            text: "This sounds highly suspicious. I am reporting this transaction, closing my app, and calling the official IRS line to check.",
            isSafe: true,
            feedback: "Excellent! You spotted the coercion. Hanging up and contacting the verified public number is the safest action."
          }
        ]
      }
    ]
  },
  {
    id: 2,
    title: "Tech Support Refund Overpayment",
    type: "Refund & Tech Support Scam",
    attackerName: "Microsoft Support Desk Help",
    description: "A simulated scenario where a technician claims to have sent too much money as a refund and begs you to return the difference.",
    initialMessage: "Oh no! We were trying to refund you $50 for your software renewal, but our team accidentally wired $5,000 to your checking account. Look at your account, it shows the pending balance. Please send the difference of $4,950 back via peer transfer immediately. Otherwise, I will lose my job and my family will suffer.",
    scamMarkers: [
      "Excessive overpayment refund story",
      "Emotional blackmail and guilt-tripping",
      "Urging quick action to 'save' their job"
    ],
    stages: [
      {
        scammerReply: "Please help me! My manager is watching. If you don't send the $4,950 back to our supervisor's recipient account now, they will fire me tonight. Can you make the transfer?",
        responses: [
          {
            text: "I understand your job is on the line, let me quickly send the money back to your supervisor.",
            isSafe: false,
            feedback: "Guilt-tripped. Scammers often use emotional manipulation. Verify pending balances with your bank, as they often use fake HTML modifications on screen to trick you."
          },
          {
            text: "No, refunds don't work this way. I will contact my bank's official support to verify this balance before taking any action.",
            isSafe: true,
            feedback: "Fantastic choice! Legitimate companies will resolve balance issues through standard accounting reconciliations, never through personal wire transfers."
          }
        ]
      }
    ]
  }
];

export const ScamDrillSimulator = () => {
  const [openDrill, setOpenDrill] = useState(false);
  const [activeScenario, setActiveScenario] = useState<Scenario | null>(null);
  const [drillStage, setDrillStage] = useState<0 | 1 | 2>(0); // 0: Scammer Initial, 1: Stage 1 Scammer Response, 2: Completed
  const [drillMessages, setDrillMessages] = useState<Array<{ sender: string; text: string; isBot: boolean }>>([]);
  const [score, setScore] = useState<number>(100);
  const [resultsExplanation, setResultsExplanation] = useState<string>('');

  const startDrill = (scenario: Scenario) => {
    setActiveScenario(scenario);
    setDrillStage(0);
    setScore(100);
    setDrillMessages([
      { sender: scenario.attackerName, text: scenario.initialMessage, isBot: true }
    ]);
    setOpenDrill(true);
  };

  const handleChooseResponse = (resp: any) => {
    // Log user message
    setDrillMessages(prev => [...prev, { sender: "You", text: resp.text, isBot: false }]);

    // Move to next step or complete
    setTimeout(() => {
      if (resp.isSafe) {
        setResultsExplanation(`Drill Completed: SUCCESS! ${resp.feedback}`);
        setDrillStage(2); // Complete
      } else {
        setScore(0);
        setResultsExplanation(`Drill Completed: WARNING! ${resp.feedback}`);
        setDrillStage(2); // Complete
      }
    }, 800);
  };

  const handleReportScam = () => {
    setResultsExplanation("Drill Completed: SUCCESS! You proactively reported this transaction as suspicious. This is the optimal security procedure.");
    setDrillStage(2);
  };

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h6" sx={{ mb: 2, fontWeight: 700, display: 'flex', alignItems: 'center', gap: 1.5 }}>
        <Security color="primary" /> NIRNAY Interactive Security Drills
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
        Test your resilience against advanced AI social engineering, impersonation, and pressure tactics. Run simulated sandbox drills to build fraud-spotting instincts.
      </Typography>

      <Grid container spacing={3}>
        {SCENARIOS.map((scen) => (
          <Grid size={{ xs: 12, md: 6 }} key={scen.id}>
            <MotionCard 
              whileHover={{ scale: 1.01 }} 
              sx={{ border: '1px solid rgba(0,0,0,0.06)', borderRadius: 3 }}
            >
              <CardContent sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1.5 }}>
                  <Chip label={scen.type} size="small" color="secondary" variant="outlined" sx={{ fontWeight: 600 }} />
                </Box>
                <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 1 }}>{scen.title}</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3.5 }}>
                  {scen.description}
                </Typography>
                <Button 
                  variant="outlined" 
                  startIcon={<PlayArrow />}
                  onClick={() => startDrill(scen)}
                  fullWidth
                >
                  Launch Drill
                </Button>
              </CardContent>
            </MotionCard>
          </Grid>
        ))}
      </Grid>

      {/* Drill Play Dialog */}
      <Dialog open={openDrill} onClose={() => setOpenDrill(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid rgba(0,0,0,0.06)' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Warning color="warning" />
            <Typography variant="subtitle1" sx={{ fontWeight: 700 }}>Scam Simulation Sandbox</Typography>
          </Box>
          <Chip label={`Safety Score: ${score}%`} color={score > 50 ? "success" : "error"} />
        </DialogTitle>
        <DialogContent sx={{ py: 3, display: 'flex', flexDirection: 'column', height: 420 }}>
          {/* Chat area */}
          <Box sx={{ flexGrow: 1, overflowY: 'auto', mb: 2, display: 'flex', flexDirection: 'column', gap: 1.5, pr: 1 }}>
            {drillMessages.map((msg, index) => (
              <Box 
                key={index}
                sx={{
                  maxWidth: '85%',
                  alignSelf: msg.isBot ? 'flex-start' : 'flex-end',
                  bgcolor: msg.isBot ? 'grey.100' : 'primary.main',
                  color: msg.isBot ? 'text.primary' : 'white',
                  p: 2,
                  borderRadius: msg.isBot ? '16px 16px 16px 2px' : '16px 16px 2px 16px',
                  fontSize: '0.9rem',
                  lineHeight: 1.45
                }}
              >
                <Typography variant="caption" sx={{ fontWeight: 600, display: 'block', mb: 0.5, color: msg.isBot ? 'text.secondary' : 'rgba(255,255,255,0.8)' }}>
                  {msg.sender}
                </Typography>
                {msg.text}
              </Box>
            ))}
          </Box>

          {/* Interactive controls */}
          <Box sx={{ pt: 2, borderTop: '1px solid rgba(0,0,0,0.06)' }}>
            {drillStage === 0 && activeScenario && (
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                <Button 
                  variant="outlined" 
                  color="error" 
                  fullWidth
                  onClick={handleReportScam}
                >
                  🚨 Report Scam Immediately
                </Button>
                <Button 
                  variant="contained" 
                  endIcon={<ArrowForward />}
                  fullWidth
                  onClick={() => {
                    setDrillMessages(prev => [
                      ...prev,
                      { sender: activeScenario.attackerName, text: activeScenario.stages[0].scammerReply, isBot: true }
                    ]);
                    setDrillStage(1);
                  }}
                >
                  Reply to Scammer
                </Button>
              </Box>
            )}

            {drillStage === 1 && activeScenario && (
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1.5 }}>
                {activeScenario.stages[0].responses.map((resp, idx) => (
                  <Button 
                    key={idx}
                    variant="outlined" 
                    sx={{ textAlign: 'left', textTransform: 'none', justifyContent: 'flex-start', p: 1.5 }}
                    onClick={() => handleChooseResponse(resp)}
                  >
                    {resp.text}
                  </Button>
                ))}
              </Box>
            )}

            {drillStage === 2 && (
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', py: 2 }}>
                {score === 100 ? (
                  <EmojiEvents color="success" sx={{ fontSize: 60, mb: 1.5 }} />
                ) : (
                  <Warning color="error" sx={{ fontSize: 60, mb: 1.5 }} />
                )}
                <Typography variant="subtitle1" sx={{ fontWeight: 700, mb: 1 }}>
                  {score === 100 ? "You Passed the Drill!" : "Security Drill Warning"}
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                  {resultsExplanation}
                </Typography>

                <Box sx={{ width: '100%', mb: 2 }}>
                  <Typography variant="caption" sx={{ fontWeight: 600, display: 'block', textAlign: 'left', mb: 0.5 }}>
                    Coercion Markers to Look Out For:
                  </Typography>
                  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, textAlign: 'left' }}>
                    {activeScenario?.scamMarkers.map((marker, i) => (
                      <Box key={i} sx={{ display: 'flex', gap: 1, alignItems: 'flex-start' }}>
                        <Warning color="warning" sx={{ fontSize: 16, mt: 0.2 }} />
                        <Typography variant="caption" color="text.secondary">{marker}</Typography>
                      </Box>
                    ))}
                  </Box>
                </Box>

                <Button variant="contained" onClick={() => setOpenDrill(false)}>
                  Finish Drill
                </Button>
              </Box>
            )}
          </Box>
        </DialogContent>
      </Dialog>
    </Box>
  );
};
