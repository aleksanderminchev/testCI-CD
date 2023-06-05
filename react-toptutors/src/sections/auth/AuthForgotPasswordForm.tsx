import * as Yup from 'yup';
// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { useNavigate } from 'react-router-dom';

// @mui
import { Stack, Alert, Button } from '@mui/material';
// components
import { useSnackbar } from '../../components/snackbar';
import FormProvider, { RHFTextField } from '../../components/hook-form';

// ----------------------------------------------------------------------

type FormValuesProps = {
  email: string;
  password: string;
  confirmPassword: string;
  afterSubmit?: string;
};

export default function AuthForgotPasswordForm() {
  const LoginSchema = Yup.object().shape({
    email: Yup.string().required('Email is required').email('Email must be a valid email address'),
  });

  const defaultValues = {
    email: '',
  };

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(LoginSchema),
    defaultValues,
  });
  const { enqueueSnackbar } = useSnackbar();

  const {
    reset,
    watch,
    setError,
    handleSubmit,
    formState: { errors, isSubmitting, isSubmitSuccessful },
  } = methods;
  const values = watch();
  const navigate = useNavigate();
  const onSubmit = async (data: FormValuesProps) => {
    if (!isConfirmPassword().value) {
      try {
        navigate('/');
      } catch (error) {
        console.error(error);

        reset();

        setError('afterSubmit', {
          ...error,
          message: error.message || error,
        });
      }
    } else {
      enqueueSnackbar('Password and confirm password have to be the same', { variant: 'error' });
    }
  };
  const isConfirmPassword = () => {
    if (values.password !== values.confirmPassword) {
      return {
        value: true,
        message: 'Password and confirm password have to be the same',
      };
    } else {
      return {
        value: false,
        message: 'No errors',
      };
    }
  };
  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={3}>
        {!!errors.afterSubmit && <Alert severity="error">{errors.afterSubmit.message}</Alert>}

        <RHFTextField name="email" label="Email address" />

        <Button
          fullWidth
          color="inherit"
          size="large"
          type="submit"
          variant="contained"
          sx={{
            bgcolor: 'text.primary',
            color: (theme) => (theme.palette.mode === 'light' ? 'common.white' : 'grey.800'),
            '&:hover': {
              bgcolor: 'text.primary',
              color: (theme) => (theme.palette.mode === 'light' ? 'common.white' : 'grey.800'),
            },
          }}
        >
          Request new password
        </Button>
      </Stack>
    </FormProvider>
  );
}
