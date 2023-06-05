import { Card, Typography, Grid, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { IBalance } from '../../../@types/balance';
import { ICustomer } from '../../../@types/customer';

// utils
import { fCurrency, fNumber } from '../../../utils/formatNumber';

type Props = {
  tab?: boolean;
  balance: IBalance | null;
  customer: ICustomer | null;
};

export default function ViewBalance({ tab, balance, customer }: Props) {
  const navigate = useNavigate();
  return (
    <Card sx={{ py: 10, px: 3, textAlign: 'center' }}>
      <Grid container spacing={1}>
        <Grid item xs={6}>
          <Typography>
            {customer?.first_name} {customer?.last_name}
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>Invoice balance: {fCurrency(balance?.invoice_balance || 0)}DKK</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>Hours Used: {fNumber(balance?.hours_used || 0)}</Typography>
          <Typography>Hours Free: {fNumber(balance?.hours_free || 0)}</Typography>
          <Typography>Hours Ordered: {fNumber(balance?.hours_ordered || 0)}</Typography>
          <Typography>Hours Scheduled: {fNumber(balance?.hours_scheduled || 0)}</Typography>
          <Typography>
            Hours Left:
            {fNumber(
              (balance?.hours_ordered || 0) -
                (balance?.hours_used || 0) +
                (balance?.hours_free || 0)
            )}
          </Typography>
        </Grid>
        {!tab ? (
          <Grid item xs={12}>
            <Button
              variant="contained"
              onClick={() => {
                navigate(`/family/${balance?.customer_id}`);
              }}
            >
              View Customer Profile
            </Button>
          </Grid>
        ) : (
          <></>
        )}
      </Grid>
    </Card>
  );
}
