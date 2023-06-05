// react
import { useNavigate } from 'react-router';
import { EventInput } from '@fullcalendar/core';
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

// components
import Iconify from '../../../components/iconify';

type CancellationProps = {
  open: boolean;
  onCancel: (state: boolean) => void;
  event: EventInput | null | undefined;
};

export default function JoinLessonDialog({ open, onCancel, event }: CancellationProps) {
  const navigate = useNavigate();
  return (
    <Dialog fullWidth maxWidth="xs" open={open} onClose={() => onCancel(false)}>
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
        <Typography>Join?</Typography>
      </DialogContent>
      <DialogActions>
        <Box display="flex" flexDirection="row" alignItems="stretch" width="100%">
          <Button
            variant="contained"
            color="error"
            size="medium"
            fullWidth
            onClick={() => {
              onCancel(false);
            }}
          >
            No
          </Button>
          <Button
            variant="contained"
            size="medium"
            fullWidth
            onClick={() => {
              if (
                event?.status === 'scheduled' &&
                new Date(event?.start?.toString() || new Date()).getDate() === new Date().getDate()
              ) {
                navigate(`/lesson/${event?.id}`);
              } else {
                navigate(`/lesson/${event?.id}/recording`);
              }
            }}
          >
            Yes
          </Button>
        </Box>
      </DialogActions>
    </Dialog>
  );
}
