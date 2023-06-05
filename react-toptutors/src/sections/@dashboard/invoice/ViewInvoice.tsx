import { Card, Typography, Grid, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

import { IInvoice } from '../../../@types/invoice';
// utils
import { fDate } from '../../../utils/formatTime';
import { fCurrency, fNumber, fPercent } from '../../../utils/formatNumber';

type Props = {
  admin: boolean;
  invoice: IInvoice | null;
};

export default function ViewInvoice({ admin, invoice }: Props) {
  const navigate = useNavigate();
  return (
    <Card sx={{ py: 10, px: 3, textAlign: 'center' }}>
      <Grid container spacing={1}>
        <Grid item xs={6}>
          <Typography>Customer Name: {invoice?.name}</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>Discount: {fPercent(invoice?.discount || 0)}</Typography>
          <Typography>Total hours: {fNumber(invoice?.total_hours || 0)}</Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>Total: {fCurrency(invoice?.total_price || 0)} DKK </Typography>
          <Typography>
            Ordered on: {fDate(invoice?.created_at || new Date(), 'dd MMM yyyy')}
          </Typography>
        </Grid>
        <Grid item xs={6}>
          <Typography>Status: {invoice?.status}</Typography>
          <Typography>Type of package: {invoice?.type_order}</Typography>
        </Grid>
        <Grid item xs={12}>
          <Button
            variant="contained"
            onClick={() => {
              navigate(`/family/${invoice?.customer_id}`);
            }}
          >
            View Customer Profile
          </Button>
          <Button
            variant="contained"
            color="warning"
            onClick={() => {
              navigate(`/invoice/${invoice?.customer_id}/${invoice?.id}/edit`);
            }}
          >
            Edit Invoice
          </Button>
        </Grid>
      </Grid>
    </Card>
  );
}
