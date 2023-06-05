import { Helmet } from 'react-helmet-async';
import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
// @mui
import { Container, Box, CircularProgress } from '@mui/material';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getPayslip } from '../../../redux/slices/payslip';
import { getTutor } from '../../..//redux/slices/tutor';

// components
import { useSettingsContext } from '../../../components/settings';
import CustomBreadcrumbs, { BreadcrumbsLinkProps } from '../../../components/custom-breadcrumbs';
// sections
import PayslipDetails from '../../../sections/@dashboard/payslip/details';

// ----------------------------------------------------------------------

export default function PayslipDetailsPage() {
  const { themeStretch } = useSettingsContext();

  // Hook to dispatch actions to the Redux store
  const dispatch = useDispatch();

  // Select payslip and isLoading from the Redux store
  const { payslip, isLoading } = useSelector((state) => state.payslip);
  const { tutor } = useSelector((state) => state.tutor);
  const { tutor_id, id } = useParams();

  useEffect(() => {
    if (id) {
      dispatch(getPayslip(id));
    }
    if (tutor_id) {
      dispatch(getTutor(tutor_id));
    }
  }, [dispatch, id, tutor_id]);

  return (
    <>
      <Helmet>
        <title> Lønseddel | TopTutors</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Lønseddel"
          links={
            [
              { name: 'Oversigt', href: PATH_DASHBOARD.root },
              tutor_id && {
                name: 'Min profil',
                href: PATH_DASHBOARD.tutor.profile(tutor_id),
              },
              { name: `Lønseddel ${id}` }, // Effect to fetch payslips when the component mounts
            ].filter(Boolean) as BreadcrumbsLinkProps[]
          }
        />
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
          <PayslipDetails payslip={payslip || undefined} tutor={tutor || undefined} />
        )}
      </Container>
    </>
  );
}
