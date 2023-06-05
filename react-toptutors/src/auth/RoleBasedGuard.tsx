import { m } from 'framer-motion';
// @mui
import { Container, Typography } from '@mui/material';
// components
import { MotionContainer, varBounce } from '../components/animate';
// assets
import { ForbiddenIllustration } from '../assets/illustrations';
//
import { useAuthContext } from './useAuthContext';

// ----------------------------------------------------------------------

type RoleBasedGuardProp = {
  hasContent?: boolean;
  verifyUser?: boolean;
  roles?: string[];
  children: React.ReactNode;
};

export default function RoleBasedGuard({
  hasContent,
  verifyUser,
  roles,
  children,
}: RoleBasedGuardProp) {
  // Logic here to get current user role
  const { user, isAuthenticated } = useAuthContext();
  console.log(isAuthenticated);
  // const currentRole = 'user';
  const currentRole = user?.roles; // admin;
  const compareRoles = () => {
    const value = currentRole.every((role: string) => roles?.includes(role));
    return value;
  };
  if (typeof roles !== 'undefined' && !compareRoles() && !(isAuthenticated && verifyUser)) {
    return hasContent ? (
      <Container component={MotionContainer} sx={{ textAlign: 'center' }}>
        <m.div variants={varBounce().in}>
          <Typography variant="h3" paragraph>
            Permission Denied
          </Typography>
        </m.div>

        <m.div variants={varBounce().in}>
          <Typography sx={{ color: 'text.secondary' }}>
            You do not have permission to access this page
          </Typography>
        </m.div>

        <m.div variants={varBounce().in}>
          <ForbiddenIllustration sx={{ height: 260, my: { xs: 5, sm: 10 } }} />
        </m.div>
      </Container>
    ) : null;
  }

  return <> {children} </>;
}
