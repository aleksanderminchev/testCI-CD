import { Helmet } from 'react-helmet-async';

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';
// @mui
import { Container, Grid, Button } from '@mui/material';

// components
import { useSettingsContext } from '../components/settings';
// sections
import {
  AppWelcome,
  AppUpcomingLessons,
  AppCarouselCards,
  AppContacts,
} from '../sections/@dashboard/dashboard';

// @types
import { ILesson } from '../@types/lesson';

// redux
import { useDispatch, useSelector } from '../redux/store';
import {
  getLessonsForStudent,
  getLessonsForCustomer,
  getLessonsForTeacher,
} from '../redux/slices/lesson';
import { getTutorsCustomer } from '../redux/slices/tutor';
import { getStudentsTeacher } from '../redux/slices/student';
// routes
import { PATH_DASHBOARD } from '../routes/paths';

// auth
import { useAuthContext } from '../auth/useAuthContext';
import RoleBasedGuard from '../auth/RoleBasedGuard';

// assets
import { MotivationIllustration } from '../assets/illustrations';
// utils
import { fDate } from '../utils/formatTime';

// ----------------------------------------------------------------------
type CarouselCard = {
  id: string;
  name: string;
  description: string;
  image: string;
  label: string;
  roles: string[];
};

const carouselCards = [
  {
    id: '1',
    label: 'Henvis en ven',
    name: 'Giv 500 kr. og få 500 kr. i rabat',
    description: 'Giv en ven 500 kr. rabat og du får 500 kr. rabat på dit næste forløb.',
    image: '',
    roles: ['customer', 'student'],
  },
  {
    id: '2',
    label: 'Hjælp os',
    name: 'Skriv en anmeldelse på Trustpilot',
    description:
      'Hjælp os med at forbedre og dele din oplevelse! Giv os en anmeldelse på Trustpilot.',
    image: '',
    roles: ['student', 'customer'],
  },
  {
    id: '3',
    label: 'Flere fag',
    name: 'Brug for hjælp i flere fag?',
    description:
      'Vi tilbyder undervisning i alle skolefag. Gvis du har brug for hjælp i flere fag, kan du altid tage kontakt til os.',
    image: '',
    roles: ['student', 'customer'],
  },
  {
    id: '4',
    label: 'Del timer',
    name: 'Del dine timer med søskende',
    description:
      'Hvis din søskende også har brug for hjælp, kan du dele din pakke med dem, så de også kan få en tutor.',
    image: '',
    roles: ['student', 'customer'],
  },
];

type Contacts = {
  id: string;
  name: string;
  email: string;
  avatar: string;
  phone: string;
}[];
function filterCardsByRoles(cards: CarouselCard[], filterRoles: string[]): CarouselCard[] {
  return cards.filter((card) => {
    return card.roles.some((role) => filterRoles.includes(role));
  });
}

export default function DashboardPage() {
  const { themeStretch } = useSettingsContext();

  const dispatch = useDispatch();

  const { lessons, isLoading } = useSelector((state) => state.lesson);
  const { tutors } = useSelector((state) => state.tutor);
  const { students } = useSelector((state) => state.student);
  const navigate = useNavigate();
  const { user } = useAuthContext();
  const [contactList, setContactList] = useState<Contacts>([]);
  useEffect(() => {
    const today = new Date();
    const tomorrow = new Date(today.getFullYear(), today.getMonth(), today.getDate() + 7);
    // today.setDate(today.getDate() - 1);
    console.log(fDate(today, 'yyyy-MM-dd'), fDate(tomorrow, 'yyyy-MM-dd'));
    if (user?.student) {
      dispatch(
        getLessonsForStudent(user?.uid, fDate(today, 'yyyy-MM-dd'), fDate(tomorrow, 'yyyy-MM-dd'))
      );
      dispatch(getTutorsCustomer(user?.email));
    } else if (user?.teacher) {
      dispatch(
        getLessonsForTeacher(user?.uid, fDate(today, 'yyyy-MM-dd'), fDate(tomorrow, 'yyyy-MM-dd'))
      );
      dispatch(getStudentsTeacher(user?.email));
    } else if (user?.customer) {
      dispatch(
        getLessonsForCustomer(user?.uid, fDate(today, 'yyyy-MM-dd'), fDate(tomorrow, 'yyyy-MM-dd'))
      );
      dispatch(getTutorsCustomer(user?.email));
    }
  }, [dispatch, user]);
  useEffect(() => {
    if (tutors) {
      setContactList(
        tutors.map((item) => {
          return {
            id: item?.id || '',
            name: `${item?.first_name} ${item?.last_name}` || '',
            email: item?.email || '',
            avatar: typeof item.photo === 'string' ? item?.photo : item?.photo?.preview || '',
            phone: item?.phone || '',
          };
        })
      );
    }
  }, [dispatch, tutors, students, user]);
  useEffect(() => {
    if (students) {
      const mappedList = students.map((item) => {
        return {
          id: item?.id || '',
          name: `${item?.first_name} ${item?.last_name}` || '',
          email: item?.email || '',
          avatar: '',
          phone: item?.phone || '',
        };
      });
      setContactList(mappedList.slice(0, 4));
    }
  }, [dispatch, students]);
  console.log(contactList);
  const [lessonNext, setLessonNext] = useState<ILesson | undefined>();
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  useEffect(() => {
    if (lessons.length) {
      for (let i = 0; i < lessons.length; i++) {
        if (lessons[i].status === 'scheduled') {
          setLessonNext(lessons[i]);
          if (user?.teacher) {
            setFirstName(lessons[i].student.first_name);
            setLastName(lessons[i].student.last_name);
          } else {
            setFirstName(lessons[i].teacher.first_name);
            setLastName(lessons[i].teacher.last_name);
          }

          break;
        }
      }
    }
  });

  return (
    <>
      <Helmet>
        <title> Oversigt | TopTutors</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'xl'}>
        <Grid container spacing={3}>
          <RoleBasedGuard roles={['student', 'teacher', 'customer']}>
            <Grid item xs={12} md={8}>
              <AppWelcome
                title={`Velkommen tilbage, ${user?.first_name}!`}
                description={
                  lessonNext
                    ? `Du har din næste lektion d. ${fDate(
                        lessonNext?.from_time || new Date(),
                        'dd/MM'
                      )} kl. ${fDate(
                        lessonNext?.from_time.toString() || new Date(),
                        'HH:mm'
                      )} til ${fDate(lessonNext?.to_time.toString() || new Date(), 'HH:mm')} med ${
                        firstName || ''
                      } ${lastName || ''}. `
                    : 'Du har ingen planlagte lektioner, men kontakt din tutor for at planlægge en ny lektion.'
                }
                img={
                  <MotivationIllustration
                    sx={{
                      p: 3,
                      width: 360,
                      margin: { xs: 'auto', md: 'inherit' },
                    }}
                  />
                }
                action={
                  lessonNext ? (
                    <Button
                      variant="contained"
                      size="large"
                      fullWidth
                      onClick={() => {
                        navigate(`/lesson/${lessonNext?.id}`);
                      }}
                    >
                      Tilslut nu
                    </Button>
                  ) : (
                    <></>
                  )
                }
              />
            </Grid>

            <Grid item xs={12} md={4}>
              <AppCarouselCards list={filterCardsByRoles(carouselCards, user?.roles)} />
            </Grid>
            <Grid item xs={12} md={8}>
              <AppUpcomingLessons heading="Kommende lektioner" link={PATH_DASHBOARD.calendar} />
            </Grid>
            <Grid item xs={12} md={4}>
              <AppContacts
                isTeacher={user?.teacher}
                title={user?.customer || user?.student ? 'Mine tutor(s)' : 'Mine elever'}
                subheader="Kontaktoplysninger"
                list={contactList}
              />
            </Grid>
          </RoleBasedGuard>
        </Grid>
      </Container>
    </>
  );
}
