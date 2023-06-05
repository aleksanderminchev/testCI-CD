import { Suspense, lazy, ElementType } from 'react';
// components
import LoadingScreen from '../components/loading-screen';

// ----------------------------------------------------------------------

const Loadable = (Component: ElementType) => {
  const LoadableComponent = (props: any) => (
    <Suspense fallback={<LoadingScreen />}>
      <Component {...props} />
    </Suspense>
  );

  LoadableComponent.displayName = 'Loadable'; // Set displayName property
  return LoadableComponent;
};

// ----------------------------------------------------------------------

// AUTH
export const LoginPage = Loadable(lazy(() => import('../pages/auth/LoginPage')));
export const RegisterPage = Loadable(lazy(() => import('../pages/auth/RegisterPage')));
export const ConfirmationPage = Loadable(lazy(() => import('../pages/auth/ConfirmationPage')));
export const ForgotPasswordPage = Loadable(lazy(() => import('../pages/auth/ForgotPasswordPage')));
// Dashboard
export const PageDashboard = Loadable(lazy(() => import('../pages/DashboardPage')));

// Students
export const PageStudentList = Loadable(
  lazy(() => import('../pages/dashboard/student/StudentListPage'))
);
export const StudentProfilePage = Loadable(
  lazy(() => import('../pages/dashboard/student/StudentProfilePage'))
);
export const StudentCreatePage = Loadable(
  lazy(() => import('../pages/dashboard/student/StudentCreatePage'))
);
export const StudentTeachersPage = Loadable(
  lazy(() => import('../pages/dashboard/student/StudentTeachersPage'))
);
// Tutors
export const PageTutorList = Loadable(lazy(() => import('../pages/dashboard/tutor/TutorListPage')));
export const TutorProfilePage = Loadable(
  lazy(() => import('../pages/dashboard/tutor/TutorProfilePage'))
);
export const TutorCreatePage = Loadable(
  lazy(() => import('../pages/dashboard/tutor/TutorCreatePage'))
);
export const TutorStudentsPage = Loadable(
  lazy(() => import('../pages/dashboard/tutor/TutorStudentsPage'))
);
// Customers
export const PageCustomerList = Loadable(
  lazy(() => import('../pages/dashboard/customer/CustomerListPage'))
);
export const CustomerProfilePage = Loadable(
  lazy(() => import('../pages/dashboard/customer/CustomerProfilePage'))
);
export const CustomerCreatePage = Loadable(
  lazy(() => import('../pages/dashboard/customer/CustomerCreatePage'))
);
export const CustomerTeachersPage = Loadable(
  lazy(() => import('../pages/dashboard/customer/CustomerTeachersPage'))
);
// Transactions
export const PageCustomerTransactionsList = Loadable(
  lazy(() => import('../pages/dashboard/transactions/CustomerTransactionsListPage'))
);
export const PageTransactionList = Loadable(
  lazy(() => import('../pages/dashboard/transactions/TransactionsListPage'))
);
export const PageViewTransaction = Loadable(
  lazy(() => import('../pages/dashboard/transactions/ViewTransactionPage'))
);
export const PageEditCreateTransaction = Loadable(
  lazy(() => import('../pages/dashboard/transactions/EditCreateTransactionPage'))
);
// Invoices
export const PageInvoiceList = Loadable(
  lazy(() => import('../pages/dashboard/invoice/InvoiceListPage'))
);
export const PageInvoice = Loadable(
  lazy(() => import('../pages/dashboard/invoice/ViewInvoicePage'))
);
export const PageCreateEditInvoice = Loadable(
  lazy(() => import('../pages/dashboard/invoice/EditCreateInvoicePage'))
);
export const PageCustomerInvoicesList = Loadable(
  lazy(() => import('../pages/dashboard/invoice/CustomerInvoiceListPage'))
);
// Calendar
export const PageCalendar = Loadable(
  lazy(() => import('../pages/dashboard/calendar/CalendarPage'))
);
// Lessons
export const PageLessonsList = Loadable(
  lazy(() => import('../pages/dashboard/lessons/LessonsListPage'))
);
export const LessonPage = Loadable(lazy(() => import('../pages/dashboard/lessons/LessonPage')));
export const LessonRecordingPage = Loadable(
  lazy(() => import('../pages/dashboard/lessons/LessonRecordingPage'))
);

// Payslips
export const PagePayslipsList = Loadable(
  lazy(() => import('../pages/dashboard/payslip/PayslipListPage'))
);
export const PagePayslipDetails = Loadable(
  lazy(() => import('../pages/dashboard/payslip/PayslipDetailsPage'))
);
// Balances
export const PageBalancesList = Loadable(
  lazy(() => import('../pages/dashboard/balance/BalanceListPage'))
);
export const PageBalance = Loadable(
  lazy(() => import('../pages/dashboard/balance/ViewBalancePage'))
);
export const Page404 = Loadable(lazy(() => import('../pages/Page404')));
