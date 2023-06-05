import { Link as RouterLink } from 'react-router-dom';

// @mui
import { Alert, Tooltip, Stack, Typography, Link, Box } from '@mui/material';
// auth
import { useAuthContext } from '../../auth/useAuthContext';
// routes
import { PATH_AUTH } from '../../routes/paths';
// layouts
import LoginLayout from '../../layouts/login';
//
import AuthForgotPasswordForm from './AuthForgotPasswordForm';

// ----------------------------------------------------------------------

export default function Forgot() {
  const { method } = useAuthContext();

  return (
    <LoginLayout>
      <Stack spacing={2} sx={{ mb: 5, position: 'relative' }}>
        <Typography variant="h4">Forgot password hos TopTutors 🎓</Typography>

        {/* <Stack direction="row" spacing={0.5}>
          <Typography variant="body2">Ny bruger?</Typography>

          <Link component={RouterLink} to={PATH_AUTH.register} variant="subtitle2">
            Opret en konto
          </Link>
        </Stack> */}
      </Stack>

      <AuthForgotPasswordForm />
    </LoginLayout>
  );
}
