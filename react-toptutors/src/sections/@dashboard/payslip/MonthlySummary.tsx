import * as Yup from 'yup';
import { useState, useEffect, useMemo } from 'react';
// form
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { Button, TextField, Grid, Divider, Stack, Box, Typography } from '@mui/material';
import { MobileDatePicker } from '@mui/x-date-pickers';
// @types
import { ITemporaryPayslip } from '../../../@types/payslip';

import FormProvider from '../../../components/hook-form';
import { fCurrency, fNumber } from '../../../utils/formatNumber';
import FinalizaPayslips from './FinalizePayslips';

// ----------------------------------------------------------------------

interface FormValuesProps {
  start_date: Date;
  end_date: Date;
}
type Props = {
  handlePayslips: (start_date: Date, end_date: Date) => void;
  createWages: (start_date: Date, end_date: Date, payment_date: Date) => void;
  temporaryPayslips: ITemporaryPayslip[];
};
export default function MonthlySummary({ handlePayslips, createWages, temporaryPayslips }: Props) {
  const NewUserSchema = Yup.object().shape({
    // password:Yup.string(),
    // email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    // avatarUrl: Yup.string().required('Avatar is required').nullable(true),
  });
  const defaultValuesIndependent = useMemo(
    () => ({
      start_date: new Date(new Date().getFullYear(), new Date().getMonth() - 1, 16),
      end_date: new Date(new Date().getFullYear(), new Date().getMonth(), 15),
    }),
    []
    // eslint-disable-next-line react-hooks/exhaustive-deps
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewUserSchema),
    defaultValues: defaultValuesIndependent,
  });
  const { reset, watch, control, setValue, handleSubmit } = methods;

  const values = watch();
  console.log(values);

  // useEffect(() => {
  //   if (currentUser) {
  //     reset(defaultValuesIndependent);
  //   }
  //   if (!isEdit) {
  //     reset(defaultValuesIndependent);
  //   }
  //   // eslint-disable-next-line react-hooks/exhaustive-deps
  // }, [ currentUser]);
  const onSubmit = async (data: FormValuesProps) => {
    try {
      handlePayslips(data.start_date, data.end_date);
      reset();
      // navigate(PATH_DASHBOARD.family.root);
    } catch (err) {
      console.error(err);
      // enqueueSnackbar(!isEdit ? 'Create success!' : 'Update success!', { variant: 'error' });
    }
  };
  const [unpaidHours, setUnpaidHours] = useState(0);
  const [unpaidWages, setUnpaidWages] = useState(0);
  const [paidWages, setPaidWages] = useState(0);
  const [paidHours, setPaidHours] = useState(0);
  const [paidReferrals, setPaidReferrals] = useState(0);
  const [paidReferralsNumber, setPaidReferralsNumber] = useState(0);
  const [unpaidReferrals, setUnpaidReferrals] = useState(0);
  const [unpaidReferralsNumber, setUnpaidReferralsNumber] = useState(0);
  useEffect(() => {
    if (temporaryPayslips) {
      let wages = 0;
      let hours = 0;
      let paidWages = 0;
      let paidHours = 0;
      let paidReferrals = 0;
      let unpaidReferrals = 0;
      let unpaidReferralsNumber = 0;
      let paidReferralsNumber = 0;
      temporaryPayslips.forEach((payslip) => {
        wages += payslip.unpaid_wage;
        paidReferrals += payslip.referrals_amount_paid;
        unpaidReferrals += payslip.referrals_amount_unpaid;
        unpaidReferralsNumber += payslip.referrals_number_unpaid;
        paidReferralsNumber += payslip.referrals_number_paid;
        hours += payslip.unpaid_hours;
        paidWages += payslip.paid_wage;
        paidHours += payslip.paid_hours;
      });
      setUnpaidWages(wages);
      setPaidWages(paidWages);
      setUnpaidHours(hours);
      setPaidHours(paidHours);
      setUnpaidReferrals(unpaidReferrals);
      setPaidReferrals(paidReferrals);
      setUnpaidReferralsNumber(unpaidReferralsNumber);
      setPaidReferralsNumber(paidReferralsNumber);
    }
  }, [temporaryPayslips]);
  return (
    <Grid container spacing={2}>
      <Grid item xs={6} md={2}>
        <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
          <Controller
            name="start_date"
            render={({ field }) => (
              <MobileDatePicker
                {...field}
                onChange={(newValue: Date | null) => field.onChange(newValue)}
                label="Sluttidspunkt"
                views={['year', 'month', 'day']}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            )}
          />
          <Controller
            name="end_date"
            render={({ field }) => (
              <MobileDatePicker
                {...field}
                onChange={(newValue: Date | null) => field.onChange(newValue)}
                label="Sluttidspunkt"
                views={['year', 'month', 'day']}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            )}
          />
          <Button type="submit" variant="contained">
            View Summary
          </Button>
        </FormProvider>
      </Grid>
      <Grid item xs={12} md={8}>
        <Box>
          <Grid container spacing={5}>
            <Grid item xs={12} md={12}>
              <Typography variant="h6">Unpaid Lesson Earnings</Typography>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Payslip Hours: </Typography>
                {unpaidHours} hours
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Payslip Wages: </Typography>
                DKK{fCurrency(unpaidWages)}
              </Stack>
              <Divider />
            </Grid>
            <Grid item xs={12} md={12}>
              <Typography variant="h6">Paid Lesson Earnings</Typography>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Payslip Hours: </Typography>
                {paidHours} hours
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Payslip Wages: </Typography>
                DKK{fCurrency(paidWages)}
              </Stack>
              <Divider />
            </Grid>
            <Grid item xs={12} md={12}>
              <Typography variant="h6">Unpaid Non-Teaching Earnings</Typography>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Event Count </Typography>0
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Non-Teaching Hours </Typography>
                0.0
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>TopTutor Count </Typography>0
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Earnings</Typography>
                0.0
              </Stack>
              <Divider />
            </Grid>

            <Grid item xs={12} md={12}>
              <Typography variant="h6">Unpaid Other Compensation</Typography>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Transaction count</Typography>
                {fNumber(unpaidReferralsNumber)}
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>TopTutor count </Typography>
                {fNumber(unpaidReferralsNumber)}
              </Stack>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>TopTutor Earnings </Typography>
                {fCurrency(unpaidReferrals)}
              </Stack>

              <Divider />
            </Grid>

            <Grid item xs={12} md={12}>
              <Typography variant="h6">Total Unpaid Earnings</Typography>
              <Divider />
              <Stack
                spacing={3}
                direction="row"
                justifyContent="space-between"
                sx={{
                  color: 'text.main',
                }}
              >
                <Typography>Total </Typography>
                DKK{fCurrency(unpaidWages + unpaidReferrals)}
              </Stack>
              <Divider />
            </Grid>
            <Grid item xs={12} md={12}>
              <FinalizaPayslips
                createWagePayments={createWages}
                start_date={values.start_date}
                end_date={values.end_date}
              />
            </Grid>
          </Grid>
        </Box>
      </Grid>
    </Grid>
  );
}
