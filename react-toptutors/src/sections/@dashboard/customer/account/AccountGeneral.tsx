import * as Yup from 'yup';
// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { phoneNumberValidation } from '../../../../utils/phoneValidation';
import { MuiTelInputInfo } from 'mui-tel-input';

// @mui
import { Box, Grid, Card, Stack } from '@mui/material';
import { LoadingButton } from '@mui/lab';
// auth
import RoleBasedGuard from '../../../../auth/RoleBasedGuard';
// redux
import { useDispatch } from '../../../../redux/store';
import { editCustomer } from '../../../../redux/slices/customer';
// types
import { ICustomer } from '../../../../@types/customer';
// import { CustomFile } from '../../../../components/upload';
import { useSnackbar } from '../../../../components/snackbar';
import FormProvider, {
  RHFSelect,
  RHFTextField,
  RHFTel,
  // RHFUploadAvatar,
} from '../../../../components/hook-form';

// ----------------------------------------------------------------------

type FormValuesProps = {
  defaultValues: Partial<ICustomer>;
  isEdit: boolean;
};

export default function AccountGeneral({ defaultValues, isEdit }: FormValuesProps) {
  const { enqueueSnackbar } = useSnackbar();

  const dispatch = useDispatch();
  console.log(isEdit);
  const UpdateUserSchema = Yup.object().shape({
    first_name: Yup.string().required('Fornavn er påkrævet'),
    last_name: Yup.string().required('Efternavn er påkrævet'),
    email: Yup.string()
      .required('E-mail er påkrævet')
      .email('E-mailen skal være en gyldig e-mailadresse'),
    // photoURL: Yup.string().required('Avatar is required').nullable(true),
    phone: phoneNumberValidation.required('Telefonnummer er påkrævet'),
  });

  const methods = useForm<Partial<ICustomer>>({
    resolver: yupResolver(UpdateUserSchema),
    defaultValues,
  });

  const {
    setValue,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const handleChange = (newPhone: string, info: MuiTelInputInfo) => {
    setValue('phone', info.numberValue || '', { shouldValidate: true });
  };
  const onSubmit = async (data: Partial<ICustomer>) => {
    try {
      const success = await dispatch(editCustomer(data));

      if (success) {
        enqueueSnackbar('Update success!');
      } else {
        enqueueSnackbar('Update failed!', { variant: 'error' });
      }
    } catch (error) {
      console.error(error);
      enqueueSnackbar('Update failed!', { variant: 'error' });
    }
  };

  // const handleDrop = useCallback(
  //   (acceptedFiles: File[]) => {
  //     const file = acceptedFiles[0];

  //     const newFile = Object.assign(file, {
  //       preview: URL.createObjectURL(file),
  //     });

  //     if (file) {
  //       setValue('photoURL', newFile, { shouldValidate: true });
  //     }
  //   },
  //   [setValue]
  // );

  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Grid container spacing={3}>
        <RoleBasedGuard roles={['admin']}>
          <Grid item xs={12} md={4}>
            <Card sx={{ p: 3, textAlign: 'center' }}>
              {/* <RHFUploadAvatar
              name="photoURL"
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
            /> */}
              <RHFSelect disabled native name="status" label="Status" sx={{ mt: 5 }}>
                <option label="Aktiv" value="active">
                  Aktiv
                </option>
                <option label="Inaktiv" value="inactive">
                  Inaktiv
                </option>
              </RHFSelect>

              <RHFSelect disabled native name="customer_type" label="Type" sx={{ mt: 5 }}>
                <option label="Familie" value="family">
                  Family
                </option>
                <option label="Child" value="child">
                  Child
                </option>
                <option label="Independent" value="independent">
                  Independent student
                </option>
              </RHFSelect>

              <RHFTextField disabled name="id" label="Kunde ID" sx={{ mt: 5 }} />
            </Card>
          </Grid>
        </RoleBasedGuard>

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
              <RHFTextField disabled={!isEdit} name="first_name" label="Fornavn" />
              <RHFTextField disabled={!isEdit} name="last_name" label="Efternavn" />

              <RHFTextField disabled={!isEdit} name="email" label="E-mail" />

              <RHFTel
                disabled={!isEdit}
                name="phone"
                label="Telefonnummer"
                onChange={handleChange}
              />
            </Box>

            <Stack spacing={3} alignItems="flex-end" sx={{ mt: 3 }}>
              {isEdit ? (
                <LoadingButton type="submit" variant="contained" loading={isSubmitting}>
                  Gem ændringer
                </LoadingButton>
              ) : (
                <></>
              )}
            </Stack>
          </Card>
        </Grid>
      </Grid>
    </FormProvider>
  );
}
