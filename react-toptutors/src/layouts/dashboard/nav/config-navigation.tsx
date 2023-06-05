import Iconify from 'src/components/iconify/Iconify';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import SvgColor from '../../../components/svg-color';
// types
import { AuthUserType } from 'src/auth/types';
// ----------------------------------------------------------------------

const icon = (name: string) => (
  <SvgColor src={`/assets/icons/navbar/${name}.svg`} sx={{ width: 1, height: 1 }} />
);

const ICONS = {
  dashboard: icon('ic_dashboard'),
  calendar: icon('ic_calendar'),
  student: <Iconify icon="ph:student" sx={{ width: 1, height: 1 }} />,
  family: <Iconify icon="carbon:pedestrian-family" sx={{ width: 1, height: 1 }} />,
  tutor: <Iconify icon="mdi:teach" sx={{ width: 1, height: 1 }} />,
  lesson: <Iconify icon="material-symbols:play-lesson" sx={{ width: 1, height: 1 }} />,
  invoice: <Iconify icon="mdi:money" sx={{ width: 1, height: 1 }} />,
  payslip: <Iconify icon="majesticons:money-hand-line" sx={{ width: 1, height: 1 }} />,
  balances: <Iconify icon="mdi:account-cash-outline" sx={{ width: 1, height: 1 }} />,
  transaction: (
    <Iconify icon="material-symbols:payments-outline-rounded" sx={{ width: 1, height: 1 }} />
  ),
};

const navConfig = (user: AuthUserType) => [
  // GENERAL
  // ----------------------------------------------------------------------
  {
    subheader: '',
    items: [
      // All
      {
        title: 'Oversigt',
        path: PATH_DASHBOARD.dashboard,
        icon: ICONS.dashboard,
        roles: ['admin', 'customer', 'teacher', 'student'],
      },
      {
        title: 'Kalender',
        path: PATH_DASHBOARD.calendar,
        icon: ICONS.calendar,
        roles: ['admin', 'customer', 'teacher', 'student'],
      },

      // Admin Only
      { title: 'Kunder', path: PATH_DASHBOARD.family.root, icon: ICONS.family, roles: ['admin'] },
      { title: 'Elever', path: PATH_DASHBOARD.student.root, icon: ICONS.student, roles: ['admin'] },
      { title: 'Tutors', path: PATH_DASHBOARD.tutor.root, icon: ICONS.tutor, roles: ['admin'] },
      {
        title: 'Lektioner',
        path: PATH_DASHBOARD.lesson.root,
        icon: ICONS.lesson,
        roles: ['admin'],
      },
      {
        title: 'Faktura',
        path: PATH_DASHBOARD.invoice.root,
        icon: ICONS.invoice,
        roles: ['admin'],
      },
      {
        title: 'Lønsedler',
        path: PATH_DASHBOARD.payslip.root,
        icon: ICONS.payslip,
        roles: ['admin'],
      },
      {
        title: 'Balances',
        path: PATH_DASHBOARD.balances.root,
        icon: ICONS.balances,
        roles: ['admin'],
      },
      {
        title: 'Transaktioner',
        path: PATH_DASHBOARD.transaction.root,
        icon: ICONS.transaction,
        roles: ['admin'],
      },
      // Customer
      {
        title: 'Min Profil',
        path: PATH_DASHBOARD.family.profile(user?.customer_dict?.id),
        icon: ICONS.dashboard,
        roles: ['customer'],
      },
      {
        title: 'Mine Tutors',
        path: PATH_DASHBOARD.family.teacherList,
        icon: ICONS.tutor,
        roles: ['customer'],
      },
      // Student
      {
        title: 'Min Profil',
        path: PATH_DASHBOARD.student.profile(user?.student_dict?.id),
        icon: ICONS.dashboard,
        roles: ['student'],
      },
      {
        title: 'Mine Tutors',
        path: PATH_DASHBOARD.student.teacherList,
        icon: ICONS.tutor,
        roles: ['student'],
      },
      // Tutor
      {
        title: 'Min Profil',
        path: PATH_DASHBOARD.tutor.profile(user?.teacher_dict?.id),
        icon: ICONS.dashboard,
        roles: ['teacher'],
      },
      {
        title: 'Mine Elever',
        path: PATH_DASHBOARD.tutor.studentList,
        icon: ICONS.student,
        roles: ['teacher'],
      },
      {
        title: 'Ledige forløb',
        path: 'https://www.toptutors.dk/course/',
        icon: ICONS.dashboard,
        roles: ['teacher'],
      },
    ],
  },
];

export default navConfig;
