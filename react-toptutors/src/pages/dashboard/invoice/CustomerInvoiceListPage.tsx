import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import { useParams } from 'react-router';
//auth
import { useAuthContext } from '../../../auth/useAuthContext';

// @mui
import { Button, Container, Box, CircularProgress } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getCustomerInvoices } from '../../../redux/slices/invoice';

// components
import Iconify from '../../../components/iconify';

import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import { CustomerInvoiceList } from '../../../sections/@dashboard/invoice/list';

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------

export default function InvoiceListPage() {
  const { themeStretch } = useSettingsContext();
  const { user } = useAuthContext();

  const dispatch = useDispatch();
  const params = useParams();
  console.log(params);
  const { customerInvoices, isLoading } = useSelector((state) => state.invoice);

  const changePageRequestDispatch = (offset: number) => {
    dispatch(getCustomerInvoices(parseInt(params?.customer_id || '', 10), offset));
  };
  useEffect(() => {
    dispatch(getCustomerInvoices(parseInt(params?.customer_id || '', 10), 0));
  }, [dispatch, params?.customer_id]);

  return (
    <>
      <Helmet>
        <title> Customer Invoices: List | Minimal UI</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Customer Invoices List"
          links={[
            {
              name: 'Dashboard',
              href: PATH_DASHBOARD.root,
            },
            {
              name: 'Invoices',
              href: PATH_DASHBOARD.invoice.root,
            },
          ]}
          action={
            user?.admin ? (
              <Button
                component={RouterLink}
                to={PATH_DASHBOARD.invoice.new}
                variant="contained"
                startIcon={<Iconify icon="eva:plus-fill" />}
              >
                New Invoice
              </Button>
            ) : (
              <></>
            )
          }
        />
        {isLoading ? (
          <Box
            sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}
          >
            <CircularProgress />
          </Box>
        ) : (
          <CustomerInvoiceList
            admin={user?.admin}
            customerInvoices={customerInvoices}
            changePageRequestDispatch={changePageRequestDispatch}
          />
        )}
      </Container>
    </>
  );
}
