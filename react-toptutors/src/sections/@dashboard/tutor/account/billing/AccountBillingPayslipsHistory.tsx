import { Link as RouterLink } from 'react-router-dom';

// @mui
import { Stack, Link, Card, Typography, Box, CircularProgress } from '@mui/material';
// utils
import { fDate } from '../../../../../utils/formatTime';
import { fCurrency } from '../../../../../utils/formatNumber';
// components
import { PATH_DASHBOARD } from '../../../../../routes/paths';

import { IPayslip } from '../../../../../@types/payslip';

// ----------------------------------------------------------------------

type Props = {
  isLoading: boolean;
  payslips: IPayslip[];
};

export default function AccountBillingPayslipsHistory({ payslips, isLoading }: Props) {
  return isLoading ? (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
      <CircularProgress />
    </Box>
  ) : (
    <Card sx={{ p: 3 }}>
      <Stack spacing={3} alignItems="flex-end">
        <Typography variant="overline" sx={{ width: 1, color: 'text.secondary' }}>
          Lønsedler
        </Typography>
        <Stack spacing={2} sx={{ width: 1 }}>
          {payslips.length === 0 ? (
            <Typography variant="body2">Ingen lønsedler endnu</Typography>
          ) : (
            <>
              {payslips.map((payslip) => (
                <Link
                  key={payslip.id}
                  component={RouterLink}
                  to={PATH_DASHBOARD.payslip.profile(payslip.teacher_id, payslip.id)}
                >
                  <Stack
                    key={payslip.id}
                    direction="row"
                    justifyContent="space-between"
                    sx={{ width: 1 }}
                  >
                    <Typography variant="body2" sx={{ minWidth: 120 }}>
                      {fDate(payslip.payment_date)}
                    </Typography>

                    <Typography variant="body2">{fCurrency(payslip.amount)} kr.</Typography>
                  </Stack>
                </Link>
              ))}
            </>
          )}
        </Stack>
      </Stack>
    </Card>
  );
}
