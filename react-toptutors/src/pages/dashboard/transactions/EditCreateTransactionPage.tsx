import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';

// @mui
import { Container, Box, CircularProgress } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
import { useSnackbar } from '../../../components/snackbar';

// sections
import { EditCreateTransactionForm } from '../../../sections/@dashboard/transaction';

import { useDispatch, useSelector } from '../../../redux/store';
import {
  getTransaction,
  createTransaction,
  updateTransaction,
} from '../../../redux/slices/transaction';
import { getCustomers } from '../../../redux/slices/customer';

import { ITransaction } from '../../../@types/transaction';

// ----------------------------------------------------------------------

export default function EditCreateTransactionPage() {
  const { id } = useParams();

  const dispatch = useDispatch();

  const { transaction, error, isLoading } = useSelector((state) => state.transaction);
  const { customers } = useSelector((state) => state.customer);
  const isEdit = transaction ? true : false;
  console.log(customers);
  const handleCreateUpdate = (form: ITransaction) => {
    if (!isEdit) {
      dispatch(createTransaction(form));
    } else {
      dispatch(updateTransaction(form));
    }
  };
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (id) {
      dispatch(getTransaction(id));
    }
    if (customers.data.length === 0) {
      dispatch(getCustomers());
    }
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
  }, [dispatch, id, customers]);

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
            <EditCreateTransactionForm
              isEdit={isEdit}
              handleCreateUpdate={handleCreateUpdate}
              transaction={transaction}
              customers={customers}
            />
          )}
        </Box>
      </Container>
    </>
  );
}
