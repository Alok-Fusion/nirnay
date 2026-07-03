import { Box, Typography, Button, Card, CardContent, CircularProgress, Alert, Collapse } from '@mui/material';
import { motion, AnimatePresence } from 'framer-motion';
import { useState, useRef } from 'react';
import { useUploadStatement } from '../../services/apiHooks';
import { CloudUpload, CheckCircle, InfoOutlined, FileOpen } from '@mui/icons-material';

const MotionCard = motion(Card);
const MotionBox = motion(Box);

export const TwinTrainer = () => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const uploadMutation = useUploadStatement();
  
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [showFormats, setShowFormats] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successData, setSuccessData] = useState<any>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      validateAndSetFile(file);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file: File) => {
    setErrorMsg('');
    setSuccessData(null);
    const ext = file.name.split('.').pop()?.toLowerCase();
    if (ext !== 'csv' && ext !== 'json') {
      setErrorMsg('Unsupported format. Please select a CSV or JSON file.');
      setSelectedFile(null);
      return;
    }
    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    try {
      const res = await uploadMutation.mutateAsync(selectedFile);
      setSuccessData(res);
      setSelectedFile(null);
    } catch (err: any) {
      console.error(err);
      setErrorMsg(err?.response?.data?.detail || 'An error occurred during statement processing.');
    }
  };

  const selectFile = () => {
    fileInputRef.current?.click();
  };

  const csvTemplate = `date,amount,recipient_name,recipient_account,bank_code
2026-06-01T12:00:00,1200.00,John Doe,REC-123456,BOA001
2026-06-15T15:30:00,45.50,Power & Light,UTIL-987,PGE022
2026-06-20T09:15:00,500.00,Alice Smith,REC-555666,CHASE09`;

  const jsonTemplate = `[
  {
    "date": "2026-06-01T12:00:00",
    "amount": 1200.00,
    "recipient_name": "John Doe",
    "recipient_account": "REC-123456",
    "bank_code": "BOA001"
  }
]`;

  return (
    <MotionCard
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.3 }}
      sx={{ 
        mt: 4, 
        border: '1px dashed rgba(26, 35, 126, 0.3)',
        background: 'rgba(255, 255, 255, 0.6)',
        backdropFilter: 'blur(8px)',
      }}
    >
      <CardContent sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ fontWeight: 700, mb: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
          <CloudUpload color="primary" /> Train Your Digital Twin
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Bootstrap your behavior profile immediately instead of executing transfers manually. Upload a bank statement in CSV or JSON format.
        </Typography>

        {errorMsg && (
          <Alert severity="error" sx={{ mb: 3, borderRadius: 2 }} onClose={() => setErrorMsg('')}>
            {errorMsg}
          </Alert>
        )}

        <AnimatePresence mode="wait">
          {successData ? (
            <MotionBox
              key="success"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              sx={{ textAlign: 'center', py: 2 }}
            >
              <CheckCircle color="success" sx={{ fontSize: 60, mb: 2 }} />
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 1 }}>Digital Twin Seeded Successfully!</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                Imported {successData.imported_count} transactions. Your Behavior Profile has evolved:
              </Typography>
              
              <Box sx={{ display: 'flex', flexDirection: 'row', gap: 2, justifyContent: 'center', mb: 3 }}>
                <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2, border: '1px solid rgba(0,0,0,0.06)', minWidth: 100 }}>
                  <Typography variant="caption" color="text.secondary">Trust Level</Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700, color: 'primary.main' }}>{successData.trust_level}</Typography>
                </Box>
                <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2, border: '1px solid rgba(0,0,0,0.06)', minWidth: 100 }}>
                  <Typography variant="caption" color="text.secondary">Trust Score</Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700, color: 'success.main' }}>{successData.trust_score}/100</Typography>
                </Box>
                <Box sx={{ p: 2, bgcolor: 'background.paper', borderRadius: 2, border: '1px solid rgba(0,0,0,0.06)', minWidth: 100 }}>
                  <Typography variant="caption" color="text.secondary">Total Transacts</Typography>
                  <Typography variant="body1" sx={{ fontWeight: 700 }}>{successData.transaction_count}</Typography>
                </Box>
              </Box>

              <Button variant="outlined" onClick={() => setSuccessData(null)}>
                Upload Another Statement
              </Button>
            </MotionBox>
          ) : (
            <MotionBox key="form">
              {/* Drag and Drop Zone */}
              <Box
                onDragEnter={handleDrag}
                onDragOver={handleDrag}
                onDragLeave={handleDrag}
                onDrop={handleDrop}
                onClick={selectFile}
                sx={{
                  border: `2px dashed ${dragActive ? '#3f51b5' : 'rgba(0,0,0,0.12)'}`,
                  bgcolor: dragActive ? 'rgba(63, 81, 181, 0.04)' : 'rgba(0,0,0,0.02)',
                  borderRadius: 3,
                  py: 4,
                  px: 2,
                  textAlign: 'center',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    bgcolor: 'rgba(63, 81, 181, 0.02)',
                    borderColor: '#3f51b5'
                  },
                  mb: 3
                }}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                  accept=".csv,.json"
                />
                
                {selectedFile ? (
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1.5 }}>
                    <FileOpen color="primary" sx={{ fontSize: 40 }} />
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>{selectedFile.name}</Typography>
                    <Typography variant="caption" color="text.secondary">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </Typography>
                  </Box>
                ) : (
                  <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 1.5 }}>
                    <CloudUpload color="action" sx={{ fontSize: 48 }} />
                    <Typography variant="body1" sx={{ fontWeight: 600 }}>Drag and drop your bank statement here</Typography>
                    <Typography variant="body2" color="text.secondary">or click to browse local files (CSV or JSON)</Typography>
                  </Box>
                )}
              </Box>

              {/* Upload and Template Actions */}
              <Box sx={{ display: 'flex', flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' }}>
                <Button 
                  size="small" 
                  startIcon={<InfoOutlined />} 
                  onClick={() => setShowFormats(!showFormats)}
                >
                  {showFormats ? "Hide Format Guidelines" : "Show Format Guidelines"}
                </Button>
                
                {selectedFile && (
                  <Button 
                    variant="contained" 
                    onClick={handleUpload}
                    disabled={uploadMutation.isPending}
                    sx={{ px: 3 }}
                  >
                    {uploadMutation.isPending ? <CircularProgress size={24} color="inherit" /> : "Train Digital Twin"}
                  </Button>
                )}
              </Box>

              {/* Collapsible Format Guidelines */}
              <Collapse in={showFormats} sx={{ mt: 3 }}>
                <Box sx={{ p: 2.5, bgcolor: '#fbfbfb', borderRadius: 2, border: '1px solid rgba(0,0,0,0.06)' }}>
                  <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>Required Formats</Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Your file must contain columns/fields representing: <code>date</code> (ISO 8601), <code>amount</code>, <code>recipient_name</code>, <code>recipient_account</code>, and <code>bank_code</code>.
                  </Typography>

                  <Typography variant="caption" sx={{ fontWeight: 700, display: 'block', mb: 0.5 }}>CSV Format Example:</Typography>
                  <Box component="pre" sx={{ p: 1.5, bgcolor: '#f4f4f5', borderRadius: 1.5, fontSize: '0.75rem', overflowX: 'auto', mb: 2 }}>
                    {csvTemplate}
                  </Box>

                  <Typography variant="caption" sx={{ fontWeight: 700, display: 'block', mb: 0.5 }}>JSON Format Example:</Typography>
                  <Box component="pre" sx={{ p: 1.5, bgcolor: '#f4f4f5', borderRadius: 1.5, fontSize: '0.75rem', overflowX: 'auto' }}>
                    {jsonTemplate}
                  </Box>
                </Box>
              </Collapse>
            </MotionBox>
          )}
        </AnimatePresence>
      </CardContent>
    </MotionCard>
  );
};
