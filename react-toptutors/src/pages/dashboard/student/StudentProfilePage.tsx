import { Helmet } from 'react-helmet-async';
import { useState, useEffect } from 'react';
import { Link as RouterLink, useParams } from 'react-router-dom';
// @mui
import { Container, Tab, Tabs, Box, CircularProgress, Button } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getStudent } from '../../../redux/slices/student';
import { assignTeachers } from '../../../redux/slices/tutor';
import { getTutors } from '../../../redux/slices/tutor';
// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
// sections
import { AccountGeneral } from '../../../sections/@dashboard/student/account';
import SendEmailVerification from '../../../sections/@dashboard/components/SendEmailVerification';
import { AccountChangePassword } from '../../../sections/@dashboard/customer/account';
import { TutorList } from '../../../sections/@dashboard/tutor/list';
import { ITutor } from '../../../@types/tutor';
import { AssignNewTutors } from 'src/sections/@dashboard/student';
// ----------------------------------------------------------------------

export default function StudentAccountPage() {
  const { id } = useParams();
  const dispatch = useDispatch();

  const { user } = useAuthContext();

  const { student, isLoading } = useSelector((state) => state.student);
  const { tutors } = useSelector((state) => state.tutor);

  const [currentTab, setCurrentTab] = useState('general');
  const isEdit = user?.admin || user?.student;
  console.log(student);

  useEffect(() => {
    if (id) {
      dispatch(getStudent(id));
      if (currentTab === 'teachers') {
        dispatch(getTutors('active'));
      }
    }
  }, [dispatch, id, currentTab]);
  const handleAssignTeachers = (teacherId: number[], studentEmail: string) => {
    dispatch(assignTeachers(teacherId, studentEmail));
  };
  const filterStudentTeachers = (studentTutors: string[] | undefined) => {
    if (studentTutors) {
      console.log(studentTutors);
      console.log(tutors);
      const filteredStudents = tutors.filter((tutor: ITutor) =>
        studentTutors.find((studentTutor) => studentTutor === tutor.id.toString())
      );
      console.log(filteredStudents);
      return filteredStudents;
    }
    return [];
  };
  const [openNewStudent, setOpenNewStudent] = useState(false);
  const handleNewStudent = (value: boolean) => {
    setOpenNewStudent(value);
  };
  const TABS = [
    {
      value: 'general',
      label: 'Oplysninger',
      roles: ['admin', 'customer', 'tutor', 'student'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: isLoading ? (
        <Box
          sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <>
          <AccountGeneral
            defaultValues={{
              id: student?.id || '',
              first_name: student?.first_name || '',
              last_name: student?.last_name || '',
              email: student?.email || '',
              phone: student?.phone || '',
              status: student?.status || '',
              student_type: student?.student_type || '',
            }}
            isEdit={isEdit}
          />
          {user?.admin || (user?.teacher && student?.student_type === 'child') ? (
            <Button
              component={RouterLink}
              to={PATH_DASHBOARD.family.profile(student?.customer_id || '')}
              size="large"
              variant="contained"
              sx={{ m: 2 }}
            >
              Se kontaktpersonens profil
            </Button>
          ) : (
            <></>
          )}
        </>
      ),
    },
    // {
    //   value: 'billing',
    //   label: 'Billing',
    //   icon: <Iconify icon="ic:round-receipt" />,
    //   component: (
    //     <AccountBilling
    //       cards={_userPayment}
    //       addressBook={_userAddressBook}
    //       invoices={_userInvoices}
    //     />
    //   ),
    // },
    // {
    //   value: 'notifications',
    //   label: 'Notifikationer',
    //   icon: <Iconify icon="eva:bell-fill" />,
    //   component: <AccountNotifications />,
    // },
    {
      value: 'change_password',
      label: 'Skift adgangskode',
      roles: ['student', 'admin'],
      icon: <Iconify icon="ic:round-vpn-key" />,
      component: <AccountChangePassword />,
    },
    {
      value: 'teachers',
      roles: ['admin'],
      label: 'Tutors',
      icon: <Iconify icon="mdi:teach" />,
      component: <TutorList isAdmin tutors={filterStudentTeachers(student?.teachers)} />,
    },
  ];

  const permittedTabs = TABS.filter((tab) => tab.roles.some((role) => user?.roles.includes(role)));

  return (
    <>
      <Helmet>
        <title>Min konto</title>
      </Helmet>

      <Container maxWidth="lg">
        <CustomBreadcrumbs
          heading={isEdit ? 'Min konto' : 'Elevens Profil'}
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: isEdit ? 'Min konto' : 'Elevens Profil' },
          ]}
          action={
            <>
              {user?.admin ? (
                <>
                  {student?.student_type === 'independent' ? (
                    <SendEmailVerification email={student?.email || ''} />
                  ) : (
                    <></>
                  )}
                  {currentTab === 'teachers' ? (
                    <Button
                      onClick={() => handleNewStudent(true)}
                      variant="contained"
                      startIcon={<Iconify icon="eva:plus-fill" />}
                    >
                      Tilføj ny tutor
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
        <AssignNewTutors
          handleAssignNewTeachers={handleAssignTeachers}
          onCancel={handleNewStudent}
          open={openNewStudent}
          teachers={tutors}
          student={student}
        ></AssignNewTutors>
      </Container>
    </>
  );
}
