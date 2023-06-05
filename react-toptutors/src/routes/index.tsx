import { Navigate, useRoutes } from 'react-router-dom';
import { wrapUseRoutes } from '@sentry/react';

// auth
import RoleBasedGuard from '../auth/RoleBasedGuard';
import AuthGuard from '../auth/AuthGuard';
import GuestGuard from '../auth/GuestGuard';
// layouts
import CompactLayout from '../layouts/compact';
import DashboardLayout from '../layouts/dashboard';
// config
import { PATH_AFTER_LOGIN } from '../config-global';
//
import {
  Page404,
  PageDashboard,
  LoginPage,
  RegisterPage,
  ForgotPasswordPage,
  ConfirmationPage,
  // Tutor
  PageTutorList,
  TutorProfilePage,
  TutorCreatePage,
  TutorStudentsPage,
  // Customer
  PageCustomerList,
  CustomerProfilePage,
  CustomerCreatePage,
  CustomerTeachersPage,
  // Student
  PageStudentList,
  StudentProfilePage,
  StudentCreatePage,
  StudentTeachersPage,
  // Lessons
  PageLessonsList,
  LessonPage,
  LessonRecordingPage,

  // Invoices
  PageInvoiceList,
  PageCustomerInvoicesList,
  PageInvoice,
  PageCreateEditInvoice,
  // Transactions
  PageTransactionList,
  PageCustomerTransactionsList,
  PageViewTransaction,
  PageEditCreateTransaction,
  //Balances
  PageBalancesList,
  PageBalance,
  // Payslips
  PagePayslipsList,
  PagePayslipDetails,
} from './elements';

import Calendarpage from '../pages/dashboard/calendar/CalendarPage';

type Props = {
  setReturnForStudent: (value: boolean) => void;
  setUrlForLesson: (value: string) => void;
  urlForLesson: string;
};

const useSentryRoutes = wrapUseRoutes(useRoutes);

// ----------------------------------------------------------------------

export default function Router({ urlForLesson, setReturnForStudent, setUrlForLesson }: Props) {
  return useSentryRoutes([
    {
      path: 'auth',
      children: [
        {
          path: 'login',
          element: (
            <GuestGuard>
              <LoginPage />
            </GuestGuard>
          ),
        },
        {
          path: 'register',
          element: (
            <GuestGuard>
              <RegisterPage />
            </GuestGuard>
          ),
        },
        {
          path: 'confirmation',
          element: (
            <GuestGuard>
              <ConfirmationPage />
            </GuestGuard>
          ),
        },
        {
          path: 'forgot',
          element: (
            <GuestGuard>
              <ForgotPasswordPage />
            </GuestGuard>
          ),
        },
      ],
    },
    // ALL APP ROUTES
    {
      path: '/',
      element: (
        <AuthGuard>
          <DashboardLayout />
        </AuthGuard>
      ),
      children: [
        { element: <Navigate to={PATH_AFTER_LOGIN} replace />, index: true },
        { path: 'dashboard', element: <PageDashboard /> },
        { path: 'calendar', element: <Calendarpage /> },
        {
          path: 'student',
          children: [
            { element: <PageStudentList />, index: true },
            { path: ':id', element: <StudentProfilePage /> },
            {
              path: 'new',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <StudentCreatePage />
                </RoleBasedGuard>
              ),
            },
            {
              path: 'teacherList',
              element: (
                <RoleBasedGuard hasContent roles={['student']}>
                  <StudentTeachersPage />
                </RoleBasedGuard>
              ),
            },
          ],
        },
        {
          path: 'family', // Aka Customers. They can either be family or independent.
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageCustomerList />
                </RoleBasedGuard>
              ),
              index: true,
            },
            { path: ':id', element: <CustomerProfilePage /> },
            {
              path: ':id/edit',
              element: (
                <RoleBasedGuard hasContent roles={['admin', 'customer']}>
                  <CustomerProfilePage />
                </RoleBasedGuard>
              ),
            },
            {
              path: 'new',
              element: (
                <RoleBasedGuard roles={['admin']}>
                  <CustomerCreatePage />
                </RoleBasedGuard>
              ),
            },
            {
              path: 'teacherList',
              element: (
                <RoleBasedGuard roles={['customer']}>
                  <CustomerTeachersPage />
                </RoleBasedGuard>
              ),
            },
          ],
        },
        {
          path: 'tutor',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageTutorList />
                </RoleBasedGuard>
              ),
              index: true,
            },
            { path: ':id', element: <TutorProfilePage /> },
            { path: ':id/edit', element: <Page404 /> },
            {
              path: 'new',
              element: (
                <RoleBasedGuard roles={['admin']}>
                  <TutorCreatePage />
                </RoleBasedGuard>
              ),
            },
            {
              path: 'studentList',
              element: (
                <RoleBasedGuard roles={['teacher']}>
                  <TutorStudentsPage />
                </RoleBasedGuard>
              ),
            },
          ],
        },
        {
          path: 'lesson',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin', 'teacher', 'student', 'customer']}>
                  <PageLessonsList />
                </RoleBasedGuard>
              ),
              index: true,
            },
            {
              path: ':id',
              element: (
                <RoleBasedGuard hasContent roles={['admin', 'customer', 'student', 'teacher']}>
                  <LessonPage
                    goBackStudent={setReturnForStudent}
                    urlForLesson={urlForLesson}
                    setUrlForLesson={setUrlForLesson}
                    setRedirectionUrl={(value: string) => {
                      console.log(value);
                    }}
                  />
                </RoleBasedGuard>
              ),
            }, // route to connect to lesson space
            {
              path: ':id/recording',
              element: (
                <RoleBasedGuard hasContent roles={['admin', 'customer', 'teacher', 'student']}>
                  <LessonRecordingPage />
                </RoleBasedGuard>
              ),
            }, // route for the lesson recording
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'invoice',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            },
            {
              path: ':customer_id',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageCustomerInvoicesList />
                </RoleBasedGuard>
              ),
            },
            {
              path: ':customer_id/:id',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoice />
                </RoleBasedGuard>
              ),
            },
            {
              path: ':customer_id/:id/edit',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageCreateEditInvoice />
                </RoleBasedGuard>
              ),
            },
            {
              path: 'new',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageCreateEditInvoice />
                </RoleBasedGuard>
              ),
            },
          ],
        },
        {
          path: 'payslip',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PagePayslipsList />
                </RoleBasedGuard>
              ),
              index: true,
            },
            {
              path: ':tutor_id/:id',
              element: (
                <RoleBasedGuard hasContent roles={['admin', 'teacher']}>
                  <PagePayslipDetails />
                </RoleBasedGuard>
              ),
            }, // This is the page to see the individual payslip.
          ],
        },
        {
          path: 'balances',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageBalancesList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // See a list of all customers' balances.
            {
              path: ':customer_id',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageBalance />
                </RoleBasedGuard>
              ),
            }, // this page to see the customer's balance
          ],
        },
        {
          path: 'transaction',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageTransactionList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // all transactions
            {
              path: ':customer_id',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageCustomerTransactionsList />
                </RoleBasedGuard>
              ),
            }, // this page to see the specific customer's transactions
            {
              path: ':customer_id/:id',
              element: (
                <RoleBasedGuard hasContent roles={['admin', 'customer']}>
                  <PageViewTransaction />
                </RoleBasedGuard>
              ),
            }, // this page to see the specific transaction
            {
              path: 'new',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageEditCreateTransaction />
                </RoleBasedGuard>
              ),
            },
            {
              path: ':id/edit',
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageEditCreateTransaction />
                </RoleBasedGuard>
              ),
            },
          ],
        },

        {
          path: 'education',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'school',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'subjects',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'languages',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'interests',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'qualifications',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
        {
          path: 'programs',
          children: [
            {
              element: (
                <RoleBasedGuard hasContent roles={['admin']}>
                  <PageInvoiceList />
                </RoleBasedGuard>
              ),
              index: true,
            }, // List of all
            { path: ':id/edit', element: <Page404 /> },
            { path: 'new', element: <Page404 /> },
          ],
        },
      ],
    },
    {
      element: <CompactLayout />,
      children: [{ path: '404', element: <Page404 /> }],
    },
    { path: '*', element: <Navigate to="/404" replace /> },
  ]);
}
