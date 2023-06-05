import { useEffect } from 'react';
import { useParams } from 'react-router-dom';

// @mui
import { Container } from '@mui/material';
// components
import { useSettingsContext } from '../../../components/settings';
import ViewBalance from '../../../sections/@dashboard/balance/ViewBalance';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getBalance } from '../../../redux/slices/balance';
import { getCustomer } from '../../../redux/slices/customer';

export default function ViewBalancePage() {
  const dispatch = useDispatch();
  const params = useParams();
  const { themeStretch } = useSettingsContext();
  const { balance } = useSelector((state) => state.balance);
  const { customer } = useSelector((state) => state.customer);

  useEffect(() => {
    dispatch(getBalance(parseInt(params?.customer_id || '', 10)));
    dispatch(getCustomer(parseInt(params?.customer_id || '', 10)));
  }, [dispatch, params?.customer_id]);

  return (
    <Container maxWidth={themeStretch ? false : 'lg'}>
      <ViewBalance balance={balance} customer={customer} />
    </Container>
  );
}
