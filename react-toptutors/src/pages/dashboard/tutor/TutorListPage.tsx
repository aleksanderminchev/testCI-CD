import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
// @mui
import { Button, Container, CircularProgress, Box } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';

// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getTutors } from '../../../redux/slices/tutor';

// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import TutorList from '../../../sections/@dashboard/tutor/list/TutorList';

// ----------------------------------------------------------------------

export default function TutorListPage() {
  const { themeStretch } = useSettingsContext();

  const dispatch = useDispatch();

  const { tutors, isLoading } = useSelector((state) => state.tutor);

  useEffect(() => {
    dispatch(getTutors(''));
  }, [dispatch]);
  return (
    <>
      <Helmet>
        <title>Tutors</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Tutors"
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: 'Tutors', href: PATH_DASHBOARD.family.root },
          ]}
          action={
            <Button
              component={RouterLink}
              to={PATH_DASHBOARD.tutor.new}
              variant="contained"
              startIcon={<Iconify icon="eva:plus-fill" />}
            >
              Ny tutor
            </Button>
          }
        />
        {isLoading ? (
          <Box
            sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <TutorList isAdmin tutors={tutors} />
        )}
      </Container>
    </>
  );
}

// ----------------------------------------------------------------------
