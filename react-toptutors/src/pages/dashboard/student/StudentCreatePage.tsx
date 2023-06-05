import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';

// @mui
import { Container, Button } from '@mui/material';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getCustomers } from '../../../redux/slices/customer';
import { createStudent } from '../../../redux/slices/student';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import { useSettingsContext } from '../../../components/settings';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import Iconify from '../../../components/iconify';
// sections
import StudentCreateForm from '../../../sections/@dashboard/student/StudentCreateForm';
import { IStudent } from '../../../@types/student';

// ----------------------------------------------------------------------

export default function StudentCreatePage() {
  const { themeStretch } = useSettingsContext();
  const dispatch = useDispatch();
  const { customer, customers } = useSelector((state) => state.customer);
  useEffect(() => {
    if (!customers.data.length) {
      dispatch(getCustomers());
    }
  }, [dispatch]);
  const handleCreateEditStudent = (form: IStudent) => {
    dispatch(createStudent(form));
  };
  console.log(customers);
  return (
    <>
      <Helmet>
        <title> Opret en ny elev og tilføj eleven til en familie </title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Opret en ny elev og tilføj eleven til en familie "
          links={[
            {
              name: 'Oversigt',
              href: PATH_DASHBOARD.root,
            },
            {
              name: 'Kunder',
              href: PATH_DASHBOARD.family.root,
            },
            { name: 'Ny studenre' },
          ]}
          action={
            <Button
              component={RouterLink}
              to={PATH_DASHBOARD.family.new}
              variant="contained"
              startIcon={<Iconify icon="eva:plus-fill" />}
            >
              Ny kunde
            </Button>
          }
        />
        <StudentCreateForm
          createStudent={handleCreateEditStudent}
          customer={customer}
          customerList={customers.data.filter((customer) => customer.customer_type === 'family')}
        />
      </Container>
    </>
  );
}
