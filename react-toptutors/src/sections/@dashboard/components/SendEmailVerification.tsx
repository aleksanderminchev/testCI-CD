/* follow this path to get to where the code is inspired from in the Minimal_TypeScript_v4.2.0:

src/sections/@dashboard/file/FilePanel
*/
// @mui
import { Button, StackProps } from '@mui/material';
// components

import Iconify from '../../../components/iconify';
import { useSnackbar } from '../../../components/snackbar';
import { useDispatch } from '../../../redux/store';
import { resendEmailVerification } from '../../../redux/slices/user';
// ----------------------------------------------------------------------

interface Props extends StackProps {
  email: string;
  onOpen?: VoidFunction;
}

export default function SendEmailVerification({ email, sx, ...other }: Props) {
  const { enqueueSnackbar } = useSnackbar();
  const dispatch = useDispatch();

  const sendEmail = async () => {
    const response = await dispatch(resendEmailVerification(email));
    if (response) {
      enqueueSnackbar('Email sent', { variant: 'success' });
    } else {
      enqueueSnackbar('Error sending email', { variant: 'error' });
    }
  };
  return (
    <Button
      sx={{ margin: 1 }}
      onClick={() => {
        sendEmail();
      }}
      variant="contained"
      startIcon={<Iconify icon="mdi:email-arrow-right" />}
    >
      Resend Email Verification
    </Button>
  );
}
