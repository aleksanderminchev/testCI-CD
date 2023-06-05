import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
// @mui
import { Container, Box, CircularProgress } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// @types
import { IStudent } from '../../../@types/student';
// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getStudents } from '../../../redux/slices/student';

// components
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import StudentList from '../../../sections/@dashboard/student/list/StudentList';

// ----------------------------------------------------------------------

export default function TutorStudentsPage() {
  const { themeStretch } = useSettingsContext();

  const dispatch = useDispatch();
  const filterTeacherStudents = (tutorStudents: string[] | undefined) => {
    if (tutorStudents) {
      const filteredStudents = students.filter((student: IStudent) =>
        tutorStudents.find((tutorStudent) => tutorStudent === student.id.toString())
      );
      console.log(filteredStudents);
      return filteredStudents;
    }
    return [];
  };
  const { students, isLoading } = useSelector((state) => state.student);
  const { user } = useAuthContext();
  console.log(user);
  useEffect(() => {
    dispatch(getStudents(''));
  }, [dispatch]);
  return (
    <>
      <Helmet>
        <title>Tutors</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Mine Elever"
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: 'Elever', href: PATH_DASHBOARD.tutor.root },
          ]}
        />
        {isLoading ? (
          <Box
            sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <StudentList
            isAdmin={false}
            students={filterTeacherStudents(user?.teacher_dict.students)}
          />
        )}
      </Container>
    </>
  );
}

// ----------------------------------------------------------------------
