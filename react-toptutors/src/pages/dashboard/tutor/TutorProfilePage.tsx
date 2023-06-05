import { Helmet } from 'react-helmet-async';
import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// @mui
import { Container, Tab, Tabs, Box, CircularProgress, Button } from '@mui/material';

// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import SendEmailVerification from '../../../sections/@dashboard/components/SendEmailVerification';
import {
  AccountGeneral,
  AccountBilling,
  AccountChangePassword,
  AssignNewStudents,
} from '../../../sections/@dashboard/tutor/account';
import StudentList from '../../../sections/@dashboard/student/list/StudentList';

// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getTutor } from '../../../redux/slices/tutor';
import { getStudents, assignStudents } from '../../../redux/slices/student';
import { IStudent } from '../../../@types/student';

// ----------------------------------------------------------------------

export default function CustomerAccountPage() {
  const { id } = useParams();

  const dispatch = useDispatch();

  const { user } = useAuthContext();

  const { tutor, isLoading } = useSelector((state) => state.tutor);
  const { students } = useSelector((state) => state.student);
  const isEdit = user?.admin || user?.teacher;
  const [currentTab, setCurrentTab] = useState('general');

  useEffect(() => {
    if (id) {
      dispatch(getTutor(id));
      if (currentTab === 'students') {
        dispatch(getStudents('active'));
      }
    }
  }, [dispatch, id, currentTab]);

  const { themeStretch } = useSettingsContext();

  const [openNewStudent, setOpenNewStudent] = useState(false);
  const handleNewStudent = (value: boolean) => {
    setOpenNewStudent(value);
  };

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

  const handleAssignStudents = (studentId: number[], teacherEmail: string) => {
    dispatch(assignStudents(studentId, teacherEmail));
    if (id) {
      dispatch(getTutor(id));
    }
  };

  const TABS = [
    {
      value: 'general',
      label: 'Oplysninger',
      roles: ['admin', 'teacher'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: isLoading ? (
        <Box
          sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <AccountGeneral
          {...{
            id: tutor?.id || '',
            isEdit: isEdit || false,
            first_name: tutor?.first_name || '',
            last_name: tutor?.last_name || '',
            email: tutor?.email || '',
            phone: tutor?.phone || '',
            address: tutor?.address || '',
            payroll_id: tutor?.payroll_id || '',
            country: tutor?.country || '',
            city: tutor?.city || '',
            zip_code: tutor?.zip_code || '',
            gender: tutor?.gender || '',
            bio: tutor?.bio || '',
            status: tutor?.status || '',
            open_for_new_students: tutor?.open_for_new_students ?? undefined,
            finished_highschool: tutor?.finished_highschool ?? undefined,
            hire_date: tutor?.created_at || new Date(),
            updated_on_tw_at: tutor?.updated_on_tw_at
              ? new Date(tutor.updated_on_tw_at)
              : undefined,
            created_on_tw_at: tutor?.created_on_tw_at
              ? new Date(tutor.created_on_tw_at)
              : undefined,
            wage_per_hour: tutor?.wage_per_hour ?? 0,
            subjects_update: tutor?.subjects
              ? tutor.subjects.map((obj) => ({
                  id: obj.id,
                  label: obj.name,
                }))
              : [],
            programs_update: tutor?.programs
              ? tutor.programs.map((obj) => ({
                  id: obj.id,
                  label: obj.name,
                }))
              : [],
            higher_education_institutions_update: tutor?.higher_education_institutions
              ? {
                  id: tutor.higher_education_institutions[0]?.id,
                  label: tutor.higher_education_institutions[0]?.name,
                }
              : undefined,
            higher_education_programmes_update: tutor?.higher_education_programmes
              ? {
                  id: tutor.higher_education_programmes[0]?.id,
                  label: tutor.higher_education_programmes[0]?.name,
                }
              : undefined,
            qualifications_update: tutor?.qualifications
              ? tutor.qualifications.map((obj) => ({
                  id: obj.id,
                  label: obj.name,
                }))
              : [],
            languages_update: tutor?.languages
              ? tutor.languages.map((obj) => ({
                  id: obj.id,
                  label: obj.name,
                }))
              : [],
            interests_update: tutor?.interests
              ? tutor.interests.map((obj) => ({
                  id: obj.id,
                  label: obj.name,
                }))
              : [],

            high_school_update: tutor?.high_school
              ? {
                  id: tutor.high_school[0]?.id,
                  label: tutor.high_school[0]?.name,
                }
              : undefined,
            photo: tutor?.photo || '',
          }}
        />
      ),
    },
    {
      value: 'billing',
      label: 'Løn',
      roles: ['admin', 'teacher'],
      icon: <Iconify icon="ic:round-receipt" />,
      component: <AccountBilling />,
    },

    {
      value: 'change_password',
      roles: ['teacher'],
      label: 'Skift Adgangskode',
      icon: <Iconify icon="ic:round-vpn-key" />,
      component: <AccountChangePassword />,
    },
    {
      value: 'students',
      roles: ['admin'],
      label: 'Elever',
      icon: <Iconify icon="ph:student" />,
      component: <StudentList isAdmin={true} students={filterTeacherStudents(tutor?.students)} />,
    },
  ];

  // Role guard om the different tabs
  const permittedTabs = TABS.filter((tab) => tab.roles.some((role) => user?.roles.includes(role)));
  return (
    <>
      <Helmet>
        <title>Min konto</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading={isEdit ? 'Min konto' : 'Tutor profil'}
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: isEdit ? 'Min konto' : 'Tutor profil' },
          ]}
          action={
            <>
              {user?.admin ? (
                <>
                  <SendEmailVerification email={tutor?.email || ''} />
                  {currentTab === 'students' ? (
                    <Button
                      onClick={() => handleNewStudent(true)}
                      variant="contained"
                      startIcon={<Iconify icon="eva:plus-fill" />}
                    >
                      Assign New Student
                    </Button>
                  ) : (
                    <></>
                  )}
                </>
              ) : (
                <></>
              )}
            </>
          }
        />

        <Tabs value={currentTab} onChange={(event, newValue) => setCurrentTab(newValue)}>
          {permittedTabs.map((tab) => (
            <Tab key={tab.value} label={tab.label} icon={tab.icon} value={tab.value} />
          ))}
        </Tabs>

        {TABS.map(
          (tab) =>
            tab.value === currentTab && (
              <Box key={tab.value} sx={{ mt: 5 }}>
                {tab.component}
              </Box>
            )
        )}
        <AssignNewStudents
          handleAssignNewStudents={handleAssignStudents}
          onCancel={handleNewStudent}
          open={openNewStudent}
          teacher={tutor}
          students={students}
        />
      </Container>
    </>
  );
}
