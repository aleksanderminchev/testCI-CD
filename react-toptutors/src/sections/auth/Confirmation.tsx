import { useSearchParams, useNavigate } from 'react-router-dom';

// @mui
import { Stack, Typography } from '@mui/material';
// auth
import { useAuthContext } from '../../auth/useAuthContext';
// layouts
import LoginLayout from '../../layouts/login';
//
import ConfirmationForm from './ConfirmationForm';
// ----------------------------------------------------------------------

export default function Confirmation() {
  const { method, confirmation } = useAuthContext();
  const [params] = useSearchParams();
  console.log(params.get('token'));
  const token = params.get('token');

  if (!token) window.location.replace('/404');
  return (
    <LoginLayout>
      <Stack spacing={2} sx={{ mb: 5, position: 'relative' }}>
        <Typography variant="h4">Confirm account for TopTutors</Typography>
      </Stack>

      <ConfirmationForm token={token || ''} />
    </LoginLayout>
  );
}
