import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
// @mui
import { Container, CircularProgress, Box } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getTutorsCustomer } from '../../../redux/slices/tutor';

// components
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import TutorList from '../../../sections/@dashboard/tutor/list/TutorList';

// ----------------------------------------------------------------------

export default function CustomerTeachersPage() {
  const { themeStretch } = useSettingsContext();

  const dispatch = useDispatch();

  const { tutors, isLoading } = useSelector((state) => state.tutor);
  const { user } = useAuthContext();
  useEffect(() => {
    if (user) {
      dispatch(getTutorsCustomer(user?.email || ''));
    }
  }, [dispatch, user]);
  return (
    <>
      <Helmet>
        <title>Mine Tutors</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Mine Tutors"
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: 'Tutors', href: PATH_DASHBOARD.family.root },
          ]}
        />
        {isLoading ? (
          <Box
            sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <TutorList isAdmin={false} tutors={tutors} />
        )}
      </Container>
    </>
  );
}

// ----------------------------------------------------------------------
