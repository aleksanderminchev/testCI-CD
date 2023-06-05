import { useEffect } from 'react';
import { useParams } from 'react-router';
// @mui
import { Container } from '@mui/material';
// components
import { useSettingsContext } from '../../../components/settings';
import ViewTransaction from '../../../sections/@dashboard/transaction/ViewTransaction';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getTransaction, refundTransaction } from '../../../redux/slices/transaction';
import { ITransaction } from '../../../@types/transaction';

export default function ViewTransactionPage() {
  const dispatch = useDispatch();
  const params = useParams();
  const { themeStretch } = useSettingsContext();
  const { transaction } = useSelector((state) => state.transaction);
  const refund = (transaction: ITransaction | null) => {
    dispatch(refundTransaction(transaction));
  };
  console.log(transaction);
  useEffect(() => {
    dispatch(getTransaction(parseInt(params?.id || '', 10)));
  }, [dispatch, params?.id]);
  return (
    <Container maxWidth={themeStretch ? false : 'lg'}>
      <ViewTransaction transaction={transaction} refund={refund} />
    </Container>
  );
}
