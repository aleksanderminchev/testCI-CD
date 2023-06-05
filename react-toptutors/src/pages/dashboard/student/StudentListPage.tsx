import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
// @mui
import { Button, Container, Box, CircularProgress } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';

// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getStudents } from '../../../redux/slices/student';

// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import StudentList from '../../../sections/@dashboard/student/list/StudentList';

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function StudentListPage() {
  const { themeStretch } = useSettingsContext();

  const dispatch = useDispatch();

  const { students, isLoading } = useSelector((state) => state.student);

  useEffect(() => {
    dispatch(getStudents(''));
  }, [dispatch]);

  return (
    <>
      <Helmet>
        <title>Elever</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Elever"
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: 'Elever', href: PATH_DASHBOARD.student.root },
          ]}
          action={
            <Button
              component={RouterLink}
              to={PATH_DASHBOARD.student.new}
              variant="contained"
              startIcon={<Iconify icon="eva:plus-fill" />}
            >
              Ny elev
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
          <StudentList isAdmin students={students} />
        )}
      </Container>
    </>
  );
}

// ----------------------------------------------------------------------
