import * as Yup from 'yup';
import { useMemo } from 'react';
// form
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { Button, TextField, Stack } from '@mui/material';
import { MobileDateTimePicker } from '@mui/x-date-pickers';

import FormProvider from '../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps {
  payment_date: Date;
}
type Props = {
  //handlePayslips: (start_date: Date, end_date: Date, payment_date: Date) => void;
  start_date: Date;
  end_date: Date;
  createWagePayments: (start_date: Date, end_date: Date, payment_date: Date) => void;
};
export default function FinalizaPayslips({ start_date, end_date, createWagePayments }: Props) {
  const NewUserSchema = Yup.object().shape({
    // password:Yup.string(),
    // email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    // avatarUrl: Yup.string().required('Avatar is required').nullable(true),
  });
  const defaultValuesIndependent = useMemo(
    () => ({
      payment_date: new Date(new Date().getFullYear(), new Date().getMonth(), 28),
    }),
    []
    // eslint-disable-next-line react-hooks/exhaustive-deps
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewUserSchema),
    defaultValues: defaultValuesIndependent,
  });
  const { reset, handleSubmit } = methods;

  const onSubmit = async (data: FormValuesProps) => {
    try {
      createWagePayments(start_date, end_date, data.payment_date);
      reset();
      //navigate(PATH_DASHBOARD.dashboard);
    } catch (err) {
      console.error(err);
      // enqueueSnackbar(!isEdit ? 'Create success!' : 'Update success!', { variant: 'error' });
    }
  };
  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Stack
        spacing={3}
        direction="row"
        justifyContent="space-between"
        sx={{
          color: 'text.main',
        }}
      >
        <Controller
          name="payment_date"
          render={({ field }) => (
            <MobileDateTimePicker
              {...field}
              ampm={false}
              ampmInClock={false}
              onChange={(newValue: Date | null) => field.onChange(newValue)}
              minutesStep={15}
              label="Sluttidspunkt"
              openTo="day"
              views={['day', 'hours', 'minutes']}
              renderInput={(params) => <TextField {...params} fullWidth />}
            />
          )}
        />
        <Button type="submit" variant="contained">
          Send Payslips
        </Button>
      </Stack>
    </FormProvider>
  );
}
