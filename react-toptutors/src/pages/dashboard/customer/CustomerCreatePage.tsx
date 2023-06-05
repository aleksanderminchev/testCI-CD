import { Helmet } from 'react-helmet-async';
import { useEffect, useState } from 'react';
import { Link as RouterLink } from 'react-router-dom';

// @mui
import { Container, Select, FormControl, MenuItem, Button } from '@mui/material';
import { SelectChangeEvent } from '@mui/material/Select';
// select options
import { customerType } from '../../../assets/data/customerType';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import { useSettingsContext } from '../../../components/settings';
import { useSnackbar } from '../../../components/snackbar';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import Iconify from '../../../components/iconify';

// sections
import { ICustomer } from '../../../@types/customer';
import CustomerCreateForm from '../../../sections/@dashboard/customer/CustomerCreateForm';

// redux
import { createCustomer } from '../../../redux/slices/customer';
import { useDispatch, useSelector } from '../../../redux/store';

// ----------------------------------------------------------------------

export default function CustomerCreatePage() {
  const { themeStretch } = useSettingsContext();

  const { enqueueSnackbar } = useSnackbar();

  const [customerCreationType, setCustomerCreationType] = useState<string>('');

  const { error } = useSelector((state) => state.customer);
  const handleChange = (event: SelectChangeEvent<typeof customerCreationType>) => {
    setCustomerCreationType(event.target.value);
  };
  const dispatch = useDispatch();

  const sendCustomerCreation = (customerData: ICustomer) => {
    console.log(customerData);

    dispatch(createCustomer(customerData, customerCreationType));
    // if(!error){
    //   enqueueSnackbar('Create success!',{variant:"success"});
    // }
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
  };
  useEffect(() => {
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
  }, [error, enqueueSnackbar]);
  console.log(customerCreationType);
  return (
    <>
      <Helmet>
        <title> Opret ny kunde (Familie eller Independent)</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Opret ny kunde (Familie eller Independent)"
          links={[
            {
              name: 'Oversigt',
              href: PATH_DASHBOARD.root,
            },
            {
              name: 'Kunder',
              href: PATH_DASHBOARD.family.root,
            },
            { name: 'Ny kunde' },
          ]}
          action={
            <Button
              component={RouterLink}
              to={PATH_DASHBOARD.student.new}
              variant="contained"
              startIcon={<Iconify icon="eva:plus-fill" />}
            >
              Opret ny elev
            </Button>
          }
        />
        <FormControl fullWidth>
          <Select
            sx={{ mb: 2 }}
            onChange={handleChange}
            label="Select type"
            defaultValue=""
            value={customerCreationType}
          >
            {customerType.map((type) => (
              <MenuItem key={type.code} value={type.value}>
                {type.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        {customerCreationType === '' ? (
          <></>
        ) : (
          <CustomerCreateForm
            customerType={customerCreationType}
            createCustomer={sendCustomerCreation}
          />
        )}
      </Container>
    </>
  );
}
