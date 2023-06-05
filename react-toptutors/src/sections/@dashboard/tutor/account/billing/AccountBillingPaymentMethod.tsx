import { useState } from 'react';
// redux
import { useSelector } from 'react-redux';
import { selectTutor } from '../../../../../redux/slices/tutor';

// @mui
import { Card, Stack, Paper, Typography, IconButton } from '@mui/material';
// components
import Iconify from '../../../../../components/iconify';
import AccountBank from './AccountBank';

// ----------------------------------------------------------------------

export default function AccountBillingPaymentMethod() {
  const [open, setOpen] = useState(false);

  const tutor = useSelector(selectTutor);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Card sx={{ p: 3 }}>
        <Stack direction="row" alignItems="center" sx={{ mb: 3 }}>
          <Typography
            variant="overline"
            sx={{
              flexGrow: 1,
              color: 'text.secondary',
            }}
          >
            Bankoplysninger
          </Typography>
        </Stack>

        <Stack
          spacing={2}
          direction={{
            xs: 'column',
            md: 'row',
          }}
        >
          <Paper
            variant="outlined"
            sx={{
              p: 3,
              width: 1,
              position: 'relative',
            }}
          >
            <Iconify icon="bi:bank" />
            {tutor?.reg_number && tutor?.bank_number ? (
              <Typography variant="subtitle2">
                {tutor?.reg_number} - {tutor?.bank_number}
              </Typography>
            ) : (
              <Typography variant="subtitle2" color="error">
                Du mangler at opdatere dine bankoplysninger.
              </Typography>
            )}

            <IconButton
              onClick={handleOpen}
              sx={{
                top: 8,
                right: 8,
                position: 'absolute',
              }}
            >
              <Iconify icon="eva:more-vertical-fill" />
            </IconButton>
          </Paper>
        </Stack>
      </Card>

      <AccountBank open={open} onClose={handleClose} />
    </>
  );
}
