import { useEffect } from 'react';
import { useParams } from 'react-router';
// auth
import { useAuthContext } from '../../../auth/useAuthContext';
// @mui
import { Container } from '@mui/material';
// components
import { useSettingsContext } from '../../../components/settings';
import ViewInvoice from '../../../sections/@dashboard/invoice/ViewInvoice';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getInvoice } from '../../../redux/slices/invoice';

export default function ViewInvoicePage() {
  const dispatch = useDispatch();
  const params = useParams();
  const { user } = useAuthContext();

  const { themeStretch } = useSettingsContext();
  const { invoice } = useSelector((state) => state.invoice);

  useEffect(() => {
    dispatch(getInvoice(parseInt(params?.id || '', 10)));
  }, [dispatch, params?.id]);

  return (
    <Container maxWidth={themeStretch ? false : 'lg'}>
      <ViewInvoice admin={user?.admin} invoice={invoice} />
    </Container>
  );
}
