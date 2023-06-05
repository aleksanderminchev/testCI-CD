import { useState, useEffect } from 'react';
// @mui
import {
  Box,
  Grid,
  Card,
  Button,
  Typography,
  Stack,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText,
} from '@mui/material';
// redux
import { useDispatch, useSelector } from '../../../../../redux/store';
import { editTutor, selectTutor } from '../../../../../redux/slices/tutor';
import { getTutorPayslips } from '../../../../../redux/slices/payslip';

// auth
import RoleBasedGuard from '../../../../../auth/RoleBasedGuard';
// @types

// components
import { useSnackbar } from '../../../../../components/snackbar';
import Label from '../../../../../components/label';
import AccountBillingPaymentMethod from './AccountBillingPaymentMethod';
import AccountBillingInvoiceHistory from './AccountBillingPayslipsHistory';

// ----------------------------------------------------------------------

export default function AccountBilling() {
  const { enqueueSnackbar } = useSnackbar();

  const tutor = useSelector(selectTutor);

  const dispatch = useDispatch();
  const { payslips, isLoading } = useSelector((state) => state.payslip);

  useEffect(() => {
    if (tutor?.id) {
      dispatch(getTutorPayslips(tutor?.id));
    }
  }, [dispatch, tutor?.id]);
  const [open, setOpen] = useState(false);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleUpdate = async (status?: string) => {
    try {
      setOpen(false);
      const tutorData = {
        id: tutor?.id,
        status: status,
        ...(status !== 'active' ? { open_for_new_students: true } : {}),
      };

      const success = await dispatch(editTutor(tutorData));

      if (success) {
        enqueueSnackbar('Update success!');
      } else {
        enqueueSnackbar('Update failed!', { variant: 'error' });
      }
    } catch (error) {
      console.error(error);
      enqueueSnackbar('Update failed!', { variant: 'error' });
    }
  };

  return (
    <Grid container spacing={5}>
      <Grid item xs={12} md={8}>
        <Stack spacing={3}>
          <Card sx={{ p: 3 }}>
            <Typography
              variant="overline"
              sx={{ mb: 3, display: 'block', color: 'text.secondary' }}
            >
              Status
            </Typography>
            {(() => {
              switch (tutor?.status) {
                case 'active':
                  // Render the button for the 'active' status
                  return (
                    <>
                      <Label
                        color="success"
                        sx={{
                          textTransform: 'uppercase',
                          fontSize: '14px',
                        }}
                      >
                        Aktiv
                      </Label>
                      <RoleBasedGuard roles={['admin']}>
                        <Box
                          sx={{
                            mt: { xs: 2, sm: 0 },
                            position: { sm: 'absolute' },
                            top: { sm: 24 },
                            right: { sm: 24 },
                          }}
                        >
                          <Button
                            size="small"
                            color="error"
                            variant="outlined"
                            sx={{ mr: 1 }}
                            onClick={handleClickOpen}
                          >
                            Bliv inaktiv
                          </Button>
                          <Dialog open={open} onClose={handleClose}>
                            <DialogTitle>{`Vil sætte din profil til inaktiv?`}</DialogTitle>

                            <DialogContent>
                              <DialogContentText id="alert-dialog-description">
                                Du har også mulighed at sætte din profil til ønsker ikke flere
                                forløb, hvis du ønsker at være midlertidligt inaktiv. Bemærk, at du
                                altid kan blive gjort aktiv, hvis du ønsker at være tutor igen.
                              </DialogContentText>
                            </DialogContent>

                            <DialogActions>
                              <Button onClick={handleClose} autoFocus>
                                Annuller
                              </Button>
                              <Button onClick={() => handleUpdate('inactive')} color="error">
                                Bliv inaktiv
                              </Button>
                            </DialogActions>
                          </Dialog>
                        </Box>
                      </RoleBasedGuard>
                    </>
                  );
                case 'inactive':
                  // Render the button for the 'inactive' status
                  return (
                    <>
                      <Label
                        color="error"
                        sx={{
                          textTransform: 'uppercase',
                          fontSize: '14px',
                        }}
                      >
                        Inaktiv
                      </Label>
                      <RoleBasedGuard roles={['admin']}>
                        <Box
                          sx={{
                            mt: { xs: 2, sm: 0 },
                            position: { sm: 'absolute' },
                            top: { sm: 24 },
                            right: { sm: 24 },
                          }}
                        >
                          <Button
                            size="small"
                            variant="outlined"
                            color="success"
                            sx={{ mr: 1 }}
                            onClick={handleClickOpen}
                          >
                            Bliv aktiv
                          </Button>
                          <Dialog open={open} onClose={handleClose}>
                            <DialogTitle>{`Vil sætte din profil til aktiv?`}</DialogTitle>

                            <DialogContent>
                              <DialogContentText id="alert-dialog-description">
                                Du vil igen blive aktiv tutor og vil kunne tage undervisningsforløb
                                med nye elever.
                              </DialogContentText>
                            </DialogContent>

                            <DialogActions>
                              <Button onClick={handleClose}>Annuller</Button>
                              <Button
                                onClick={() => handleUpdate('active')}
                                color="success"
                                autoFocus
                              >
                                Bliv aktiv
                              </Button>
                            </DialogActions>
                          </Dialog>
                        </Box>
                      </RoleBasedGuard>
                    </>
                  );
              }
            })()}
          </Card>

          <AccountBillingPaymentMethod />
        </Stack>
      </Grid>

      <Grid item xs={12} md={4}>
        <AccountBillingInvoiceHistory payslips={payslips} isLoading={isLoading} />
      </Grid>
    </Grid>
  );
}
