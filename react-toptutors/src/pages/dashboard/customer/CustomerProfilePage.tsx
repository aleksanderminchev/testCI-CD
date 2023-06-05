import { Helmet } from 'react-helmet-async';
import { useState, useEffect } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';

// @mui
import { Container, Tab, Tabs, Box, CircularProgress, Button } from '@mui/material';
// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getCustomer } from '../../../redux/slices/customer';
import { getBalance } from '../../../redux/slices/balance';
import { getStudents } from '../../../redux/slices/student';
import { getCustomerTransactions } from '../../../redux/slices/transaction';
import { getCustomerInvoices } from '../../../redux/slices/invoice';
import { IStudent } from '../../../@types/student';

// sections
import {
  AccountGeneral,
  AccountChangePassword,
} from '../../../sections/@dashboard/customer/account';
import SendEmailVerification from '../../../sections/@dashboard/components/SendEmailVerification';
import { CustomerTransactionalList } from '../../../sections/@dashboard/transaction/list/';
import { CustomerInvoiceList } from '../../../sections/@dashboard/invoice/list';
import { ViewBalance } from '../../../sections/@dashboard/balance';
import StudentList from '../../../sections/@dashboard/student/list/StudentList';

// ----------------------------------------------------------------------

export default function CustomerAccountPage() {
  const { id } = useParams();
  const dispatch = useDispatch();
  const { user } = useAuthContext();
  const { customer, isLoading } = useSelector((state) => state.customer);
  const { students } = useSelector((state) => state.student);
  const { invoice, customerInvoices } = useSelector((state) => state.invoice);
  const { customerTransactions } = useSelector((state) => state.transaction);
  const { balance } = useSelector((state) => state.balance);
  const [currentTab, setCurrentTab] = useState('general');
  const changePageRequestDispatch = (offset: number) => {
    dispatch(getCustomerTransactions(parseInt(id || '', 10), offset));
  };
  const changePageRequestDispatchInvoice = (offset: number) => {
    dispatch(getCustomerInvoices(parseInt(id || '', 10), offset));
  };
  useEffect(() => {
    if (id) {
      dispatch(getCustomer(id));
      if (currentTab === 'transaction') {
        dispatch(getCustomerTransactions(parseInt(id, 10), 0));
      } else if (currentTab === 'balance') {
        dispatch(getBalance(parseInt(id, 10)));
      } else if (currentTab === 'invoice') {
        dispatch(getCustomerInvoices(parseInt(id, 10), 0));
      } else if (currentTab === 'students') {
        dispatch(getStudents(''));
      }
    }
  }, [dispatch, currentTab, id]);
  console.log(customerTransactions);
  const filterCustomerStudents = (customerStudents: string[] | undefined) => {
    if (customerStudents) {
      const filteredStudents = students.filter((student: IStudent) =>
        customerStudents.find((tutorStudent) => tutorStudent === student.id.toString())
      );
      console.log(filteredStudents);
      return filteredStudents;
    }
    return [];
  };
  const TABS = [
    {
      value: 'general',
      label: 'Oplysninger',
      roles: ['admin', 'customer'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: isLoading ? (
        <Box
          sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <AccountGeneral
          defaultValues={{
            id: customer?.id || '',
            first_name: customer?.first_name || '',
            last_name: customer?.last_name || '',
            email: customer?.email || '',
            phone: customer?.phone || '',
            status: customer?.status || '',
            customer_type: customer?.customer_type || '',
          }}
          isEdit={user?.admin || user?.customer}
        />
      ),
    },
    {
      value: 'transaction',
      label: 'Transaktioner',
      roles: ['admin'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: isLoading ? (
        <Box
          sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <CustomerTransactionalList
          customerTransactions={customerTransactions}
          changePageRequestDispatch={changePageRequestDispatch}
        />
      ),
    },
    {
      value: 'invoice',
      label: 'Faktura',
      roles: ['admin'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: isLoading ? (
        <Box
          sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <CustomerInvoiceList
          admin={user?.admin}
          customerInvoices={customerInvoices}
          changePageRequestDispatch={changePageRequestDispatchInvoice}
        />
      ),
    },
    {
      value: 'balance',
      label: 'Balance',
      roles: ['admin'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: isLoading ? (
        <Box
          sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <ViewBalance tab={true} balance={balance} customer={customer} />
      ),
    },
    {
      value: 'students',
      roles: ['admin'],
      label: 'Elever',
      icon: <Iconify icon="ph:student" />,
      component: (
        <StudentList isAdmin={true} students={filterCustomerStudents(customer?.students)} />
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
    //   label: 'Notifications',
    //   icon: <Iconify icon="eva:bell-fill" />,
    //   component: <AccountNotifications />,
    // },
    {
      value: 'change_password',
      label: 'Skift Adgangskode',
      roles: ['customer'],
      icon: <Iconify icon="ic:round-vpn-key" />,
      component: <AccountChangePassword />,
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
          heading="Min konto"
          links={[{ name: 'Oversigt', href: PATH_DASHBOARD.root }, { name: 'Min konto' }]}
          action={
            user?.admin ? (
              <>
                <Button
                  sx={{ margin: 1 }}
                  component={RouterLink}
                  to={PATH_DASHBOARD.student.new}
                  variant="contained"
                  startIcon={<Iconify icon="eva:plus-fill" />}
                >
                  Ny Studerende
                </Button>
                <SendEmailVerification email={customer?.email || ''} />
              </>
            ) : (
              <></>
            )
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
      </Container>
    </>
  );
}
