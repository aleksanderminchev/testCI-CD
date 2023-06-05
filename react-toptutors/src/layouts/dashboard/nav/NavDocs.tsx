// @mui
import { Stack, Button, Typography } from '@mui/material';
// auth
import { useAuthContext } from '../../../auth/useAuthContext';
import RoleBasedGuard from '../../../auth/RoleBasedGuard';

// ----------------------------------------------------------------------

export default function NavDocs() {
  const { user } = useAuthContext();

  return (
    <RoleBasedGuard roles={['teacher']}>
      <Stack
        spacing={3}
        sx={{
          px: 5,
          pb: 5,
          mt: 10,
          width: 1,
          display: 'block',
          textAlign: 'center',
        }}
      >
        {/* <Box component="img" src="/assets/illustrations/illustration_docs.svg" /> */}

        <div>
          <Typography gutterBottom variant="subtitle1">
            {`Hej,${user?.first_name ? ` ${user.first_name}` : ''}`}
          </Typography>

          <Typography variant="body2" sx={{ color: 'text.secondary', whiteSpace: 'pre-line' }}>
            Har du brug for hjælp? <br />
            Se TopTutors Wiki
          </Typography>
        </div>

        <Button
          variant="contained"
          target="_blank"
          rel="noopener noreferrer"
          href="https://toptutors.notion.site/toptutors/TopTutors-Wiki-8b14e3a42c624207ac3aa8f0dac81c08"
        >
          TT Wiki
        </Button>
      </Stack>
    </RoleBasedGuard>
  );
}
