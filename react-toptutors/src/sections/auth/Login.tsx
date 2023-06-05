// @mui
import { Stack, Typography } from '@mui/material';
// auth
import { useAuthContext } from '../../auth/useAuthContext';
// layouts
import LoginLayout from '../../layouts/login';
import AuthLoginForm from './AuthLoginForm';

// ----------------------------------------------------------------------

export default function Login() {
  const { method } = useAuthContext();

  return (
    <LoginLayout>
      <Stack spacing={2} sx={{ mb: 5, position: 'relative' }}>
        <Typography variant="h4">Log ind hos TopTutors 🎓</Typography>

        {/* <Stack direction="row" spacing={0.5}>
          <Typography variant="body2">Ny bruger?</Typography>

          <Link component={RouterLink} to={PATH_AUTH.register} variant="subtitle2">
            Opret en konto
          </Link>
        </Stack> */}
      </Stack>

      <AuthLoginForm />
    </LoginLayout>
  );
}
