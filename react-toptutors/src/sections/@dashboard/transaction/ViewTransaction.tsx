import { Card, Typography, Grid, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { ITransaction } from '../../../@types/transaction';
// utils
import { fDate } from '../../../utils/formatTime';
import { fCurrency } from '../../../utils/formatNumber';

type Props = {
  transaction: ITransaction | null;
  refund: (transaction: ITransaction | null) => void;
};

export default function ViewTransaction({ transaction, refund }: Props) {
  const navigate = useNavigate();
  return (
    <Card sx={{ py: 10, px: 3, textAlign: 'center' }}>
      <Grid container spacing={1}>
        <Grid item xs={6}>
          <Typography>
            {transaction?.customer.first_name} {transaction?.customer.last_name}
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography style={{ backgroundColor: transaction?.void ? 'yellow' : 'lightblue' }}>
            {transaction?.void ? 'Voided payment' : 'Regular Payment'}
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>
            {fCurrency(transaction?.amount || 0)} {transaction?.currency}
          </Typography>
          <Typography>{fDate(transaction?.created_at || new Date(), 'dd MMM yyyy')}</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>{transaction?.method}</Typography>
          <Typography>{transaction?.type_transaction}</Typography>
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            onClick={() => {
              navigate(`/family/${transaction?.customer.id}`);
            }}
          >
            View Customer Profile
          </Button>
          <Button
            variant="contained"
            color="warning"
            onClick={() => {
              navigate(`/transaction/${transaction?.id}/edit`);
            }}
          >
            Edit Transaction
          </Button>
          {/* <Button
            variant="contained"
            color="error"
            onClick={() => {
              refund(transaction);
            }}
          >
            Refund the transaction
          </Button> */}
        </Grid>
      </Grid>
    </Card>
  );
}
