import * as Yup from 'yup';
import { useCallback, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
// form
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { MuiTelInputInfo } from 'mui-tel-input';

// @mui
import { LoadingButton } from '@mui/lab';
import { Box, Card, Grid, Switch, Typography, FormControlLabel } from '@mui/material';
// utils
import { fData } from '../../../utils/formatNumber';
// select options
import { gender } from '../../../assets/data/gender';
// @types
import { IStudent } from '../../../@types/student';
import { ICustomer } from '../../../@types/customer';

// components
import Label from '../../../components/label';
import { CustomFile } from '../../../components/upload';
import { useSnackbar } from '../../../components/snackbar';

import FormProvider, {
  RHFSelect,
  RHFSwitch,
  RHFTel,
  RHFTextField,
  RHFUploadAvatar,
} from '../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps extends Omit<IStudent, 'avatarUrl'> {
  avatarUrl: CustomFile | string | null;
}

type Props = {
  isEdit?: boolean;
  currentUser?: IStudent;
  studentType?: string;
  customer: ICustomer | null;
  customerList: ICustomer[] | [];
  createStudent: ((values: FormValuesProps) => void) | (() => void);
};

export default function StudentNewEditForm({
  isEdit = false,
  currentUser,
  customer,
  customerList,
  studentType,
  createStudent,
}: Props) {
  const navigate = useNavigate();

  const { enqueueSnackbar } = useSnackbar();

  const NewUserSchema = Yup.object().shape({
    first_name: Yup.string().required('Name is required'),
    last_name: Yup.string().required('Name is required'),
    // password:Yup.string(),
    // email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    // phone: Yup.string().required('Phone number is required'),
    // status: Yup.string().required('Status is required'),
    // student_type: Yup.string().required('Student Type is required'),
    // avatarUrl: Yup.string().required('Avatar is required').nullable(true),
  });
  const defaultValuesIndependent = useMemo(
    () => ({
      id: customer?.id || '',
      first_name: currentUser?.first_name || '',
      last_name: currentUser?.last_name || '',
      email: currentUser?.email || '',
      phone: currentUser?.phone || '',
      // avatarUrl: currentUser?.avatarUrl || null,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [currentUser]
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewUserSchema),
    defaultValues: defaultValuesIndependent,
  });

  const { reset, watch, control, setValue, handleSubmit } = methods;

  const values = watch();
  console.log(values);
  useEffect(() => {
    if (isEdit && currentUser) {
      reset(defaultValuesIndependent);
    }
    if (!isEdit) {
      reset(defaultValuesIndependent);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEdit, currentUser]);
  const handleChange = (newPhone: string, info: MuiTelInputInfo) => {
    setValue('phone', info.numberValue || '', { shouldValidate: true });
  };
  const onSubmit = async (data: FormValuesProps) => {
    console.log(data);
    try {
      console.log(data);
      createStudent(data);
      reset();
      // navigate(PATH_DASHBOARD.family.root);
    } catch (err) {
      console.error(err);
      enqueueSnackbar(!isEdit ? 'Create success!' : 'Update success!', { variant: 'error' });
    }
  };

  const handleDrop = useCallback(
    (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];

      const newFile = Object.assign(file, {
        preview: URL.createObjectURL(file),
      });

      if (file) {
        setValue('avatarUrl', newFile, { shouldValidate: true });
      }
    },
    [setValue]
  );

  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ pt: 10, pb: 5, px: 3 }}>
            {isEdit && (
              <Label
                color={values.status === 'active' ? 'success' : 'error'}
                sx={{ textTransform: 'uppercase', position: 'absolute', top: 24, right: 24 }}
              >
                {values.status}
              </Label>
            )}

            <Box sx={{ mb: 5 }}>
              <RHFUploadAvatar
                name="avatarUrl"
                maxSize={3145728}
                onDrop={handleDrop}
                helperText={
                  <Typography
                    variant="caption"
                    sx={{
                      mt: 2,
                      mx: 'auto',
                      display: 'block',
                      textAlign: 'center',
                      color: 'text.secondary',
                    }}
                  >
                    Allowed *.jpeg, *.jpg, *.png, *.gif
                    <br /> max size of {fData(3145728)}
                  </Typography>
                }
              />
            </Box>

            {isEdit && (
              <FormControlLabel
                labelPlacement="start"
                control={
                  <Controller
                    name="status"
                    control={control}
                    render={({ field }) => (
                      <Switch
                        {...field}
                        checked={field.value !== 'active'}
                        onChange={(event) =>
                          field.onChange(event.target.checked ? 'banned' : 'active')
                        }
                      />
                    )}
                  />
                }
                label={
                  <>
                    <Typography variant="subtitle2" sx={{ mb: 0.5 }}>
                      Banned
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Apply disable account
                    </Typography>
                  </>
                }
                sx={{ mx: 0, mb: 3, width: 1, justifyContent: 'space-between' }}
              />
            )}

            <RHFSwitch
              name="isVerified"
              labelPlacement="start"
              label={
                <>
                  <Typography variant="subtitle2" sx={{ mb: 0.5 }}>
                    Email Verified
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Enabling this will not send the user a verification email.
                  </Typography>
                </>
              }
              sx={{ mx: 0, width: 1, justifyContent: 'space-between' }}
            />
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card sx={{ p: 3 }}>
            <Box
              rowGap={3}
              columnGap={2}
              display="grid"
              gridTemplateColumns={{
                xs: 'repeat(1, 1fr)',
                sm: 'repeat(2, 1fr)',
              }}
            >
              <RHFTextField name="first_name" label="First Name" />
              <RHFTextField name="last_name" label="Last Name" />
              <RHFTextField name="email" label="Email Address" />
              <RHFTel name="phone" label="Telefonnummer" onChange={handleChange} />
              <RHFSelect label="Familie " native name="id">
                <option />
                {customerList.map((value) => (
                  <option
                    label={`${value.first_name} ${value.last_name}`}
                    value={value.id}
                    key={value.id}
                  >
                    {value.first_name} {value.last_name}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect label="Gender of " native name="gender">
                <option />
                {gender.map((value) => (
                  <option label={value.label} value={value.value} key={value.code}>
                    {value.label}
                  </option>
                ))}
              </RHFSelect>
            </Box>

            <LoadingButton type="submit" variant="contained" sx={{ m: 2 }} size="large">
              {!isEdit ? 'Opret elev' : 'Gem ændringer'}
            </LoadingButton>
            {/* </Stack> */}
          </Card>
        </Grid>
      </Grid>
    </FormProvider>
  );
}
