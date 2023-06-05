// react
import { useState } from 'react';
// @mui
import {
  Box,
  Button,
  Typography,
  IconButton,
  DialogActions,
  Dialog,
  DialogContent,
  DialogTitle,
} from '@mui/material';

// select data
import { cancellations } from '../../../assets/data';

// components
import Iconify from '../../../components/iconify';
import { RHFSelect } from '../../../components/hook-form';

type CancellationProps = {
  cancel: boolean;
  admin: boolean;
  onCancel: (state: boolean) => void;
  cancelLesson: (reason: string) => void;
};

export function CancelLessonDialog({ cancelLesson, cancel, admin, onCancel }: CancellationProps) {
  const [reason, setReason] = useState('');
  return (
    <Dialog fullWidth maxWidth="xs" open={cancel} onClose={() => onCancel(false)}>
      <DialogTitle>
        Aflys lektionen
        <IconButton
          sx={{ position: 'absolute', right: 8, top: 8 }}
          color="error"
          onClick={() => onCancel(false)}
        >
          <Iconify icon="ic:sharp-close" />
        </IconButton>
      </DialogTitle>
      <DialogContent>
        <Typography>Hvorfor aflyses lektionen?</Typography>
      </DialogContent>
      <DialogActions>
        <Box display="flex" flexDirection="column" alignItems="stretch" width="100%">
          <RHFSelect
            onChange={(option) => {
              setReason(option.target.value);
            }}
            native
            name="reason"
          >
            <option />
            {cancellations.map((cancellation) => (
              <option
                label={cancellation.label}
                key={cancellation.code}
                id={cancellation.code}
                value={cancellation.value}
              >
                {cancellation.label}
              </option>
            ))}
          </RHFSelect>
          <Button
            onClick={() => {
              cancelLesson(reason);
              onCancel(false);
            }}
            variant="contained"
            color="error"
            sx={{ mt: 3 }}
          >
            Aflys
          </Button>
        </Box>
      </DialogActions>
    </Dialog>
  );
}
