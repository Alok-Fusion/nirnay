import { Box, Typography, Card, Button, List, ListItem, ListItemText, Chip, IconButton } from '@mui/material';
import { motion } from 'framer-motion';
import { Delete, Edit, Security } from '@mui/icons-material';
import { useRecipients } from '../../services/apiHooks';

export const RecipientManagement = () => {
  const { data: recipients = [], isLoading } = useRecipients();

  return (
    <Box sx={{ p: 4, maxWidth: 800, mx: 'auto' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 4, alignItems: 'center' }}>
        <Typography variant="h4" sx={{ fontWeight: 700 }}>Recipient Management</Typography>
        <Button variant="contained" color="primary">Add New Recipient</Button>
      </Box>

      <Card sx={{ borderRadius: 4, overflow: 'hidden' }}>
        {isLoading ? (
          <Typography sx={{ p: 4, textAlign: 'center' }}>Loading recipients...</Typography>
        ) : (
          <List sx={{ p: 0 }}>
            {recipients.map((recipient: any, index: number) => (
              <motion.div
                key={recipient.id || index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <ListItem
                  sx={{
                    p: 3,
                    borderBottom: '1px solid',
                    borderColor: 'divider',
                    '&:last-child': { borderBottom: 'none' }
                  }}
                  secondaryAction={
                    <Box>
                      <IconButton edge="end" aria-label="edit" sx={{ mr: 1 }}>
                        <Edit />
                      </IconButton>
                      <IconButton edge="end" aria-label="delete" color="error">
                        <Delete />
                      </IconButton>
                    </Box>
                  }
                >
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="h6">{recipient.name}</Typography>
                        {recipient.is_trusted && (
                          <Chip size="small" icon={<Security fontSize="small" />} label="Trusted" color="success" />
                        )}
                      </Box>
                    }
                    secondary={
                      <Box sx={{ mt: 1 }}>
                        <Typography variant="body2" color="text.secondary">
                          Account: {recipient.account_number} | Bank: {recipient.bank_code}
                        </Typography>
                      </Box>
                    }
                  />
                </ListItem>
              </motion.div>
            ))}
            {recipients.length === 0 && (
              <Typography sx={{ p: 4, textAlign: 'center', color: 'text.secondary' }}>
                No recipients found. Add one to get started.
              </Typography>
            )}
          </List>
        )}
      </Card>
    </Box>
  );
};
