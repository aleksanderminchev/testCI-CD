/**

PayslipListPage displays a list of payslips in a table format.
If the user is Admin then it shows all payslips. If the user is a Tutor then it shows that tutor's payslips.
Users can filter, sort, and paginate the payslips, and perform actions such as deleting a payslip.
The component uses various hooks to manage its state and interact with the Redux store.

AI Generated DOCS.
*/

import { Helmet } from 'react-helmet-async';
import { useState, useEffect } from 'react';
// @mui
import { Tab, Tabs, Container, Box } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';

// redux
import { useDispatch, useSelector } from '../../../redux/store';
import {
  getPayslips,
  getTutorPayslips,
  calculateMontlyPayslip,
  createWagePayments,
} from '../../../redux/slices/payslip';

import { useAuthContext } from '../../../auth/useAuthContext';

// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import PayslipList from '../../../sections/@dashboard/payslip/list/PayslipList';
import { MonthlySummary } from '../../../sections/@dashboard/payslip';
import { fDate } from '../../../utils/formatTime';

// ----------------------------------------------------------------------

export default function PayslipListPage() {
  // Get themeStretch from useSettingsContext custom hook
  const { themeStretch } = useSettingsContext();

  // Hook to dispatch actions to the Redux store
  const dispatch = useDispatch();

  // Select payslips and isLoading from the Redux store
  const { payslips, temporaryPayslips, isLoading } = useSelector((state) => state.payslip);

  const { user } = useAuthContext();
  const requestTemporaryPayslips = (start_date: Date, end_date: Date) => {
    try {
      dispatch(
        calculateMontlyPayslip(fDate(start_date, 'yyyy-MM-dd'), fDate(end_date, 'yyyy-MM-dd'))
      );
    } catch (err) {
      console.error(err);
    }
  };

  const createWages = (start_date: Date, end_date: Date, payment_date: Date) => {
    try {
      dispatch(
        createWagePayments(
          fDate(start_date, 'yyyy-MM-dd'),
          fDate(end_date, 'yyyy-MM-dd'),
          payment_date.toISOString()
        )
      );
    } catch (err) {
      console.error(err);
    }
  };
  // Effect to fetch payslips when the component mounts
  useEffect(() => {
    if (user?.admin) {
      dispatch(getPayslips());
    } else if (user?.teacher) {
      dispatch(getTutorPayslips(user?.uid));
    }
  }, [dispatch, user?.admin, user?.uid]);

  const [currentTab, setCurrentTab] = useState('general');

  const TABS = [
    {
      value: 'general',
      label: 'Oplysninger',
      roles: ['admin', 'tutor'],
      icon: <Iconify icon="ic:round-account-box" />,
      component: <PayslipList payslips={payslips}></PayslipList>,
    },
    {
      value: 'montly_summary',
      label: 'Monthly Summary',
      roles: ['admin'],
      icon: <Iconify icon="mdi:auto-pay" />,
      component: (
        <MonthlySummary
          temporaryPayslips={temporaryPayslips}
          handlePayslips={requestTemporaryPayslips}
          createWages={createWages}
        />
      ),
    },
  ];
  const permittedTabs = TABS.filter((tab) => tab.roles.some((role) => user?.roles.includes(role)));

  return (
    <>
      <Helmet>
        <title>Lønsedler</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Lønsedler"
          links={[
            { name: 'Oversigt', href: PATH_DASHBOARD.root },
            { name: 'Payslips', href: PATH_DASHBOARD.payslip.root },
          ]}
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

// ----------------------------------------------------------------------
