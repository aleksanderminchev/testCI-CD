import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

// @mui
import { Container, Box, Button, CircularProgress } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';

// components
import Iconify from '../../../components/iconify';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
import { useSnackbar } from '../../../components/snackbar';

// sections
import { EditCreateInvoiceForm } from '../../../sections/@dashboard/invoice';

import { useDispatch, useSelector } from '../../../redux/store';
import {
  getInvoice,
  createInvoice,
  updateInvoice,
  resendEmail,
} from '../../../redux/slices/invoice';
import { getCustomers } from '../../../redux/slices/customer';

import { IInvoice } from '../../../@types/invoice';

// ----------------------------------------------------------------------

export default function EditCreateInvoicePage() {
  const { id } = useParams();

  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { invoice, error, isLoading } = useSelector((state) => state.invoice);
  const { customers } = useSelector((state) => state.customer);
  const isEdit = invoice ? true : false;

  const handleCreateUpdate = (form: IInvoice) => {
    if (!isEdit) {
      console.log(form);
      dispatch(createInvoice(form));
      navigate('/invoice');
    } else {
      dispatch(updateInvoice(form));
    }
  };

  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (id) {
      dispatch(getInvoice(id));
    }
    if (customers.data.length === 0) {
      dispatch(getCustomers());
    }
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
  }, [dispatch, id, customers]);

  const handleEmailResend = async (invoice: IInvoice | null) => {
    if (invoice) {
      const response = await dispatch(resendEmail(invoice));
      if (response) enqueueSnackbar('Email sent successfully', { variant: 'success' });
      else enqueueSnackbar('Email was rejected', { variant: 'error' });
    }
  };

  const { themeStretch } = useSettingsContext();

  return (
    <>
      <Helmet>
        <title>Min konto</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Account"
          links={[{ name: 'Oversigt', href: PATH_DASHBOARD.root }, { name: 'Min konto' }]}
          action={
            isEdit && invoice?.status !== 'void' ? (
              <Button
                onClick={() => handleEmailResend(invoice)}
                variant="contained"
                startIcon={<Iconify icon="eva:plus-fill" />}
              >
                Send Email Again
              </Button>
            ) : (
              <></>
            )
          }
        />

        <Box sx={{ mt: 5 }}>
          {isLoading ? (
            <Box
              sx={{
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100%',
              }}
            >
              <CircularProgress />
            </Box>
          ) : (
            <EditCreateInvoiceForm
              isEdit={isEdit}
              handleCreateUpdate={handleCreateUpdate}
              invoice={invoice}
              customers={customers}
            />
          )}
        </Box>
      </Container>
    </>
  );
}
