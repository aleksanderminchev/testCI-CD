// form
import { useForm } from 'react-hook-form';
// @mui
import { Card, Stack, Typography } from '@mui/material';
import { LoadingButton } from '@mui/lab';
// @types
import { ICustomerNotificationSettings } from '../../../../@types/customer';
// components
import { useSnackbar } from '../../../../components/snackbar';
import FormProvider, { RHFSwitch } from '../../../../components/hook-form';

// ----------------------------------------------------------------------

const ACTIVITY_OPTIONS = [
  {
    value: 'email_lesson_reminders',
    label: 'Påmindelser på kommende lektioner',
  },
  {
    value: 'email_lesson_notes',
    label: 'Lektionsrapport fra tutor',
  },
] as const;

const NOTIFICATION_SETTINGS = {
  email_lesson_reminders: true,
  email_lesson_notes: true,
};

// ----------------------------------------------------------------------

type FormValuesProps = ICustomerNotificationSettings;

export default function AccountNotifications() {
  const { enqueueSnackbar } = useSnackbar();

  const defaultValues = {
    email_lesson_reminders: NOTIFICATION_SETTINGS.email_lesson_reminders,
    email_lesson_notes: NOTIFICATION_SETTINGS.email_lesson_notes,
  };

  const methods = useForm({
    defaultValues,
  });

  const {
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const onSubmit = async (data: FormValuesProps) => {
    try {
      await new Promise((resolve) => setTimeout(resolve, 500));
      enqueueSnackbar('Update success!');
      console.log('DATA', data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Card sx={{ p: 3 }}>
        <Typography variant="overline" component="div" sx={{ color: 'text.secondary' }}>
          Activity
        </Typography>

        <Stack alignItems="flex-start" spacing={1} sx={{ mt: 2 }}>
          {ACTIVITY_OPTIONS.map((activity) => (
            <RHFSwitch
              key={activity.value}
              name={activity.value}
              label={activity.label}
              sx={{ m: 0 }}
            />
          ))}
        </Stack>

        {/* <Typography variant="overline" component="div" sx={{ color: 'text.secondary', mt: 5 }}>
          Application
        </Typography>

        <Stack alignItems="flex-start" spacing={1} sx={{ mt: 2, mb: 5 }}>
          {APPLICATION_OPTIONS.map((application) => (
            <RHFSwitch
              key={application.value}
              name={application.value}
              label={application.label}
              sx={{ m: 0 }}
            />
          ))}
        </Stack> */}

        <Stack>
          <LoadingButton
            type="submit"
            variant="contained"
            loading={isSubmitting}
            sx={{ ml: 'auto' }}
          >
            Save Changes
          </LoadingButton>
        </Stack>
      </Card>
    </FormProvider>
  );
}
