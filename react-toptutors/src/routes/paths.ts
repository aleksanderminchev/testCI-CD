// ----------------------------------------------------------------------

function path(root: string, sublink: string) {
  return `${root}${sublink}`;
}

const ROOTS_AUTH = '/auth';
const ROOTS_DASHBOARD = '/';

// ----------------------------------------------------------------------

export const PATH_AUTH = {
  root: ROOTS_AUTH,
  login: path(ROOTS_AUTH, '/login'),
  register: path(ROOTS_AUTH, '/register'),
  confirmation: path(ROOTS_AUTH, '/confirmation'),
  forgot: path(ROOTS_AUTH, '/forgot'),
};

export const PATH_DASHBOARD = {
  root: ROOTS_DASHBOARD,
  dashboard: path(ROOTS_DASHBOARD, 'dashboard'),
  calendar: path(ROOTS_DASHBOARD, 'calendar'),
  family: {
    root: path(ROOTS_DASHBOARD, 'family'),
    profile: (id: string) => path(ROOTS_DASHBOARD, `family/${id}`),
    teacherList: path(ROOTS_DASHBOARD, 'family/teacherList'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `family/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'family/new'),
  },
  student: {
    root: path(ROOTS_DASHBOARD, 'student'),
    profile: (id: string) => path(ROOTS_DASHBOARD, `student/${id}`),
    teacherList: path(ROOTS_DASHBOARD, 'student/teacherList'),
    new: path(ROOTS_DASHBOARD, 'student/new'),
  },
  tutor: {
    root: path(ROOTS_DASHBOARD, 'tutor'),
    profile: (id: string) => path(ROOTS_DASHBOARD, `tutor/${id}`),
    studentList: path(ROOTS_DASHBOARD, `tutor/studentList`),
    edit: (id: string) => path(ROOTS_DASHBOARD, `tutor/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'tutor/new'),
  },
  lesson: {
    root: path(ROOTS_DASHBOARD, 'lesson'),
    profile: (id: string) => path(ROOTS_DASHBOARD, `lesson/${id}`),
    recording: (id: string) => path(ROOTS_DASHBOARD, `lesson/${id}/recording`),
    edit: (id: string) => path(ROOTS_DASHBOARD, `lesson/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'lesson/new'),
  },
  invoice: {
    root: path(ROOTS_DASHBOARD, 'invoice'),
    customer: (customer_id: string) => path(ROOTS_DASHBOARD, `invoice/${customer_id}`),
    view: (customer_id: string, id: string) =>
      path(ROOTS_DASHBOARD, `invoice/${customer_id}/${id}`),
    edit: (customer_id: string, id: string) =>
      path(ROOTS_DASHBOARD, `invoice/${customer_id}/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'invoice/new'),
  },
  payslip: {
    root: path(ROOTS_DASHBOARD, 'payslip'),
    profile: (tutor_id: string, id: string) => path(ROOTS_DASHBOARD, `payslip/${tutor_id}/${id}`),
  },
  balances: {
    root: path(ROOTS_DASHBOARD, 'balances'),
    customer: (customer_id: string) => path(ROOTS_DASHBOARD, `balances/${customer_id}`),
    new: path(ROOTS_DASHBOARD, 'balances/new'),
  },
  transaction: {
    root: path(ROOTS_DASHBOARD, 'transaction'),
    customer: (customer_id: string) => path(ROOTS_DASHBOARD, `transaction/${customer_id}`),
    profile: (customer_id: string, id: string) =>
      path(ROOTS_DASHBOARD, `transaction/${customer_id}/${id}`),
    edit: (customer_id: string, id: string) =>
      path(ROOTS_DASHBOARD, `transaction/${customer_id}/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'transaction/new'),
  },
  education: {
    root: path(ROOTS_DASHBOARD, 'education'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `education/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'education/new'),
  },
  school: {
    root: path(ROOTS_DASHBOARD, 'school'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `school/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'school/new'),
  },
  subjects: {
    root: path(ROOTS_DASHBOARD, 'subjects'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `subjects/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'subjects/new'),
  },
  languages: {
    root: path(ROOTS_DASHBOARD, 'languages'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `languages/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'languages/new'),
  },
  interests: {
    root: path(ROOTS_DASHBOARD, 'interests'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `interests/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'interests/new'),
  },
  qualifications: {
    root: path(ROOTS_DASHBOARD, 'qualifications'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `qualifications/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'qualifications/new'),
  },
  programs: {
    root: path(ROOTS_DASHBOARD, 'programs'),
    edit: (id: string) => path(ROOTS_DASHBOARD, `programs/${id}/edit`),
    new: path(ROOTS_DASHBOARD, 'programs/new'),
  },
};
