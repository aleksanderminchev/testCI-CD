import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router';

// @mui
import { Button, Box, CircularProgress, Container } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getCustomerTransactions } from '../../../redux/slices/transaction';

// components
import Iconify from '../../../components/iconify';

import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import { CustomerTransactionalList } from '../../../sections/@dashboard/transaction/list';

export default function TransactionListPage() {
  const { themeStretch } = useSettingsContext();

  const dispatch = useDispatch();
  const params = useParams();

  const { customerTransactions, isLoading } = useSelector((state) => state.transaction);

  const changePageRequestDispatch = (offset: number) => {
    dispatch(getCustomerTransactions(parseInt(params?.customer_id || '', 10), offset));
  };
  useEffect(() => {
    dispatch(getCustomerTransactions(parseInt(params?.customer_id || '', 10), 0));
  }, [dispatch, params?.customer_id]);

  useEffect(() => {
    if (customerTransactions.data.length) {
      // setTableData(customerTransactions.data);
    }
  }, [customerTransactions]);
  return (
    <>
      <Helmet>
        <title>Transaktioner for kunde</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Transaktioner for kunde"
          links={[
            {
              name: 'Dashboard',
              href: PATH_DASHBOARD.root,
            },
            {
              name: 'Transaktioner',
              href: PATH_DASHBOARD.transaction.root,
            },
          ]}
          action={
            <Button
              component={RouterLink}
              to={PATH_DASHBOARD.transaction.new}
              variant="contained"
              startIcon={<Iconify icon="eva:plus-fill" />}
            >
              New Transaction
            </Button>
          }
        />
        {isLoading ? (
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
        )}
      </Container>
    </>
  );
}
