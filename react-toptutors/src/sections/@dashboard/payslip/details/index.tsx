// @mui
import { styled } from '@mui/material/styles';
import {
  Box,
  Card,
  Grid,
  Table,
  Divider,
  TableRow,
  TableBody,
  TableHead,
  TableCell,
  Typography,
  TableContainer,
} from '@mui/material';
// utils
import { fDate } from '../../../../utils/formatTime';
import { fCurrency, fNumber } from '../../../../utils/formatNumber';

import { IPayslip } from '../../../../@types/payslip';
import { ITutor } from '../../../../@types/tutor';
// components
import Label from '../../../../components/label';
import Image from '../../../../components/image';
import Scrollbar from '../../../../components/scrollbar';
//
import PayslipToolbar from './PayslipToolbar';

// ----------------------------------------------------------------------

const StyledRowResult = styled(TableRow)(({ theme }) => ({
  '& td': {
    paddingTop: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
}));

// ----------------------------------------------------------------------

type Props = {
  payslip?: IPayslip;
  tutor?: ITutor;
};

export default function PayslipDetails({ payslip, tutor }: Props) {
  if (!payslip) {
    return null;
  }
  if (!tutor) {
    return null;
  }
  const { start_date, end_date, amount, referrals_amount, referrals_number, hours, id } = payslip;
  const { first_name, last_name, address, city } = tutor;
  return (
    <>
      <PayslipToolbar payslip={payslip} tutor={tutor} />

      <Card sx={{ pt: 5, px: 5 }}>
        <Grid container>
          <Grid item xs={12} sm={6} sx={{ mb: 5 }}>
            <Image disabledEffect alt="logo" src="/logo/logo_full.svg" sx={{ maxWidth: 120 }} />
          </Grid>

          <Grid item xs={12} sm={6} sx={{ mb: 5 }}>
            <Box sx={{ textAlign: { sm: 'right' } }}>
              <Label variant="soft" color="success" sx={{ textTransform: 'uppercase', mb: 1 }}>
                Udbetalt
              </Label>

              <Typography variant="h6">{`Ref. nr.-${id}`}</Typography>
            </Box>
          </Grid>

          <Grid item xs={12} sm={6} sx={{ mb: 5 }}>
            <Typography paragraph variant="overline" sx={{ color: 'text.disabled' }}>
              Honorarlønseddel fra
            </Typography>

            <Typography variant="body2">TopTutors ApS</Typography>

            <Typography variant="body2">Porcelænshaven 26, 3</Typography>
          </Grid>

          <Grid item xs={12} sm={6} sx={{ mb: 5 }}>
            <Typography paragraph variant="overline" sx={{ color: 'text.disabled' }}>
              Honorarlønseddel til
            </Typography>

            <Typography sx={{ textTransform: 'capitalize' }} variant="body2">
              {first_name} {last_name}
            </Typography>

            <Typography sx={{ textTransform: 'capitalize' }} variant="body2">
              {address}, {city}
            </Typography>
          </Grid>

          <Grid item xs={12} sm={6} sx={{ mb: 5 }}>
            <Typography paragraph variant="overline" sx={{ color: 'text.disabled' }}>
              Periode start
            </Typography>

            <Typography variant="body2">{fDate(start_date)}</Typography>
          </Grid>

          <Grid item xs={12} sm={6} sx={{ mb: 5 }}>
            <Typography paragraph variant="overline" sx={{ color: 'text.disabled' }}>
              Periode slut
            </Typography>

            <Typography variant="body2">{fDate(end_date)}</Typography>
          </Grid>
        </Grid>

        <TableContainer sx={{ overflow: 'unset' }}>
          <Scrollbar>
            <Table sx={{ minWidth: 960 }}>
              <TableHead
                sx={{
                  borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
                  '& th': { backgroundColor: 'transparent' },
                }}
              >
                <TableRow>
                  <TableCell align="left">Beskrivelse</TableCell>

                  <TableCell align="left">Antal</TableCell>

                  <TableCell align="left">Beløb</TableCell>

                  <TableCell align="right">I alt</TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                <TableRow
                  sx={{
                    borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
                  }}
                >
                  <TableCell align="left">
                    <Box sx={{ maxWidth: 560 }}>
                      <Typography variant="subtitle2">Undervisningslektioner</Typography>
                    </Box>
                  </TableCell>

                  <TableCell align="left">{hours} timer</TableCell>

                  <TableCell align="left">
                    {fCurrency((amount - referrals_amount) / hours)} kr.
                  </TableCell>
                  <TableCell align="right">{fCurrency(amount - referrals_amount)}</TableCell>
                </TableRow>

                <TableRow
                  sx={{
                    borderBottom: (theme) => `solid 1px ${theme.palette.divider}`,
                  }}
                >
                  <TableCell align="left">
                    <Box sx={{ maxWidth: 560 }}>
                      <Typography variant="subtitle2">Henvisningshonorar</Typography>
                    </Box>
                  </TableCell>

                  <TableCell align="left">{fCurrency(referrals_amount)}</TableCell>
                  <TableCell align="left">{fNumber(referrals_number)}</TableCell>
                  <TableCell align="right">
                    {fCurrency(referrals_amount / referrals_number)}
                  </TableCell>
                </TableRow>

                <StyledRowResult>
                  <TableCell colSpan={2} />

                  <TableCell align="right" sx={{ typography: 'h6' }}>
                    Total
                  </TableCell>

                  <TableCell align="right" width={140} sx={{ typography: 'h6' }}>
                    {fCurrency(amount)}
                  </TableCell>
                </StyledRowResult>
              </TableBody>
            </Table>
          </Scrollbar>
        </TableContainer>

        <Divider sx={{ mt: 5 }} />

        {/* <Grid container>
          <Grid item xs={12} md={9} sx={{ py: 3 }}>
            <Typography variant="subtitle2">NOTES</Typography>

            <Typography variant="body2">
              We appreciate your business. Should you need us to add VAT or extra notes let us know!
            </Typography>
          </Grid>

          <Grid item xs={12} md={3} sx={{ py: 3, textAlign: 'right' }}>
            <Typography variant="subtitle2">Have a Question?</Typography>

            <Typography variant="body2">support@minimals.cc</Typography>
          </Grid>
        </Grid> */}
      </Card>
    </>
  );
}
