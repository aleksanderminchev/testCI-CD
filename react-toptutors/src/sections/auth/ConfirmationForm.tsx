import { useState } from 'react';
import * as Yup from 'yup';
// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { useNavigate } from 'react-router-dom';

// @mui
import { Stack, Alert, IconButton, InputAdornment, Button } from '@mui/material';
// auth
import { useAuthContext } from '../../auth/useAuthContext';
// components
import { useSnackbar } from '../../components/snackbar';
import Iconify from '../../components/iconify';
import FormProvider, { RHFTextField } from '../../components/hook-form';

// ----------------------------------------------------------------------

type FormValuesProps = {
  email: string;
  password: string;
  confirmPassword: string;
  afterSubmit?: string;
};

type Props = {
  token: string;
};

export default function ConfirmationForm({ token }: Props) {
  const { confirmation } = useAuthContext();

  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const LoginSchema = Yup.object().shape({
    email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    password: Yup.string().required('Password is required'),
    confirmPassword: Yup.string().required('Confirmation password is required'),
  });

  const defaultValues = {
    email: '',
    password: '',
    confirmPassword: '',
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
    formState: { errors },
  } = methods;

  const values = watch();
  const navigate = useNavigate();

  const onSubmit = async (data: FormValuesProps) => {
    if (!isConfirmPassword().value) {
      try {
        const response = await confirmation(data.email, data.password, data.confirmPassword, token);
        if (response) {
          enqueueSnackbar('Profile confirmed!', {
            variant: 'success',
          });
          navigate('/');
        } else {
          enqueueSnackbar('Error validating profile', { variant: 'error' });
        }
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

        <RHFTextField
          name="password"
          label="Password"
          type={showPassword ? 'text' : 'password'}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowPassword(!showPassword)} edge="end">
                  <Iconify icon={showPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <RHFTextField
          name="confirmPassword"
          label="Confirm Password"
          type={showConfirmPassword ? 'text' : 'password'}
          error={!!isConfirmPassword().value}
          helperText={isConfirmPassword().value && isConfirmPassword().message}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton onClick={() => setShowConfirmPassword(!showConfirmPassword)} edge="end">
                  <Iconify icon={showConfirmPassword ? 'eva:eye-fill' : 'eva:eye-off-fill'} />
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

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
          Set password
        </Button>
      </Stack>
    </FormProvider>
  );
}
