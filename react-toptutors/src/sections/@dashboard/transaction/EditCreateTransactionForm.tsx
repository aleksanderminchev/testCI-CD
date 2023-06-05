import * as Yup from 'yup';
import { useCallback, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { LoadingButton } from '@mui/lab';
import { Box, Card, Grid, Typography } from '@mui/material';
// utils
import { fData } from '../../../utils/formatNumber';
// select options
import { currency } from '../../../assets/data/currency';
import { transaction_methods, transaction_types } from '../../../assets/data/transaction_method';
// @types
import { ITransaction } from '../../../@types/transaction';
import { ICustomerPagination, ICustomer } from '../../../@types/customer';

// components
import Label from '../../../components/label';
import { CustomFile } from '../../../components/upload';
import { useSnackbar } from '../../../components/snackbar';

import FormProvider, {
  RHFSelect,
  RHFTextField,
  RHFUploadAvatar,
} from '../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps extends Omit<ITransaction, 'avatarUrl'> {
  avatarUrl: CustomFile | string | null;
}

type Props = {
  isEdit?: boolean;
  transaction: ITransaction | null;
  customers: ICustomerPagination;
  handleCreateUpdate: (form: ITransaction) => void;
};

export default function EditCreateTransactionForm({
  isEdit,
  transaction,
  customers,
  handleCreateUpdate,
}: Props) {
  const navigate = useNavigate();

  const { enqueueSnackbar } = useSnackbar();
  const NewTransactionSchema = Yup.object().shape({
    // first_name: Yup.string().required('Name is required'),
    // last_name: Yup.string().required('Name is required'),
    // password:Yup.string(),
    // email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    // phone: Yup.string().required('Phone number is required'),
    // status: Yup.string().required('Status is required'),
    // customer_type: Yup.string().required('Customer Type is required'),
    // avatarUrl: Yup.string().required('Avatar is required').nullable(true),
  });
  const defaultValuesIndependent = useMemo(
    () => ({
      id: transaction?.id || '',
      method: transaction?.method || '',
      customer_id: transaction?.customer_id || transaction?.customer.id || '',
      void: transaction?.void || false,
      type_transaction: transaction?.type_transaction || '',
      amount: transaction?.amount || 0,
      currency: transaction?.currency || '',
      stripe_transaction_id: transaction?.stripe_transaction_id || '',
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [transaction]
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewTransactionSchema),
    defaultValues: defaultValuesIndependent,
  });

  const { reset, watch, control, setValue, handleSubmit } = methods;

  const values = watch();
  console.log(values);
  useEffect(() => {
    if (isEdit && transaction) {
      reset(defaultValuesIndependent);
    }
    if (!isEdit) {
      reset(defaultValuesIndependent);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEdit, transaction]);

  const onSubmit = async (data: FormValuesProps) => {
    console.log(data);
    try {
      console.log(data);
      // createCustomer(data)
      handleCreateUpdate(data);

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
                color={values.method === 'active' ? 'success' : 'error'}
                sx={{ textTransform: 'uppercase', position: 'absolute', top: 24, right: 24 }}
              >
                {values.method}
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
              <RHFSelect disabled={isEdit} label="Customer" native name="customer_id">
                <option />
                {customers.data.map((value: ICustomer) => (
                  <option
                    label={`${value.first_name} ${value.last_name}`}
                    value={value.id}
                    key={value.id}
                  >
                    {value.first_name} {value.last_name}
                  </option>
                ))}
              </RHFSelect>
              <RHFTextField type="number" name="amount" label="Beløb" />
              <RHFTextField name="stripe_transaction_id" label="Stripe ID" />
              <RHFSelect label="Metode" native name="method">
                <option />
                {transaction_methods.map(
                  (value: { label: string; value: string; code: string }) => (
                    <option label={value.label} value={value.value} key={value.code}>
                      {value.label}
                    </option>
                  )
                )}
              </RHFSelect>
              <RHFSelect label="Valuta" native name="currency">
                <option />
                {currency.map((value: { label: string; value: string; code: string }) => (
                  <option label={value.label} value={value.value} key={value.code}>
                    {value.label}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect disabled={isEdit} label="Transaktions Type" native name="type_transaction">
                <option />
                {transaction_types.map((value: { label: string; value: string; code: string }) => (
                  <option label={value.label} value={value.value} key={value.code}>
                    {value.label}
                  </option>
                ))}
              </RHFSelect>
            </Box>

            <LoadingButton type="submit" variant="contained" sx={{ mt: 2 }}>
              {!isEdit ? 'Opret transaktion' : 'Gem ændringer'}
            </LoadingButton>
            {/* </Stack> */}
          </Card>
        </Grid>
      </Grid>
    </FormProvider>
  );
}
