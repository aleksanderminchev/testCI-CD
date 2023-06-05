import * as Yup from 'yup';
import { useCallback, useEffect, useMemo, useState } from 'react';
// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { LoadingButton } from '@mui/lab';
import { Box, Card, Grid, Typography } from '@mui/material';
// utils
import { fData, fNumber } from '../../../utils/formatNumber';
// select options
import { invoice_types, discounts } from '../../../assets/data/orders';
// routes
// @types
import { IInvoice } from '../../../@types/invoice';
import { ICustomerPagination, ICustomer } from '../../../@types/customer';

// components
import Label from '../../../components/label';
import { CustomFile } from '../../../components/upload';
import { useSnackbar } from '../../../components/snackbar';

import FormProvider, {
  RHFSelect,
  RHFSwitch,
  RHFTextField,
  RHFUploadAvatar,
} from '../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps extends Omit<IInvoice, 'avatarUrl'> {
  avatarUrl: CustomFile | string | null;
  plan_selected: string;
  installments: number;
  email: string;
}

type Props = {
  isEdit?: boolean;
  invoice: IInvoice | null;
  customers: ICustomerPagination;
  handleCreateUpdate: (form: IInvoice) => void;
};

export default function EditCreateInvoiceForm({
  isEdit,
  invoice,
  customers,
  handleCreateUpdate,
}: Props) {
  const { enqueueSnackbar } = useSnackbar();
  const NewInvoiceSchema = Yup.object().shape({
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
      id: invoice?.id || '',
      status: invoice?.status || '',
      name: invoice?.name || '',
      email: '',
      customer_id: invoice?.customer_id || '',
      email_sent: invoice?.email_sent || false,
      discount: invoice?.discount || '',
      stripe_id: invoice?.stripe_invoice_id || '',
      plan_selected: invoice?.type_order?.split('-')[2] || '',
      amount: invoice?.total_price || 0,
      total_hours: invoice?.total_hours || 0,
      installments: invoice?.installments || 0,
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [invoice]
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewInvoiceSchema),
    defaultValues: defaultValuesIndependent,
  });

  const { reset, watch, control, setValue, handleSubmit } = methods;

  const values = watch();

  useEffect(() => {
    if (isEdit && invoice) {
      reset(defaultValuesIndependent);
    }
    if (!isEdit) {
      reset(defaultValuesIndependent);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEdit, invoice]);

  const onSubmit = async (data: FormValuesProps) => {
    console.log(data);
    try {
      console.log(data);
      const hours = maxHours === 0 ? data.total_hours : maxHours;
      const installments = maxMonths === 1 ? maxMonths : data.installments;
      const discount = fNumber((1 - parseFloat(data?.discount || '1')) * 100);
      console.log(discount);
      handleCreateUpdate({
        ...data,
        email: email,
        name: name,
        total_hours: hours,
        installments: installments,
        discount: discount === '0' ? undefined : discount.toString(),
        stripe_invoice_id: `${installments}-months-${data.plan_selected}`,
      });

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

  const [maxHours, setMaxHours] = useState(0);
  const [maxMonths, setMaxMonths] = useState(0);
  const [price, setPrice] = useState(0);
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');

  const isMaxError = () => {
    return { value: false, message: `Limit is ${maxHours}` };
  };

  useEffect(() => {
    if (values?.plan_selected !== '') {
      const plan = invoice_types.find((v) => v.value === values?.plan_selected);
      setMaxHours(plan?.max || 0);
      setMaxMonths(plan?.max_months || 1);
      setPrice(plan?.price || 0);
    }

    if (values?.customer_id) {
      const customer = customers.data.find((v) => v.id.toString() === values.customer_id);
      setEmail(customer?.email || '');
      setName(`${customer?.first_name} ${customer?.last_name}` || '');
    }

    if (isEdit && invoice) {
      setMaxHours(invoice?.total_hours);
      setPrice(parseInt(invoice.type_order.split('-')[2]));
      setMaxMonths(invoice?.installments);
    }
  }, [values?.plan_selected, values?.customer_id, isEdit, invoice]);

  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ pt: 10, pb: 5, px: 3 }}>
            {isEdit && (
              <Label
                color={values.status === 'paid' ? 'success' : 'error'}
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

              <RHFTextField
                value={fNumber(
                  price *
                    (maxHours === 0 ? values?.total_hours : maxHours) *
                    parseFloat(values?.discount || '1')
                )}
                disabled
                type="text"
                name="amount"
                label="Invoice Amount"
              />

              <RHFTextField
                value={fNumber(
                  (price *
                    (maxHours === 0 ? values?.total_hours : maxHours) *
                    parseFloat(values?.discount || '1')) /
                    values?.installments
                )}
                disabled
                type="text"
                name="month_price"
                label="Monthly Price"
              />

              <RHFSelect disabled={isEdit} type="number" native label="Discount" name="discount">
                <option />
                {discounts.map((value) => (
                  <option label={value.label} value={value.value} key={value.code}>
                    {value.label}
                  </option>
                ))}
              </RHFSelect>

              <RHFTextField
                disabled={maxHours !== 0 || isEdit}
                value={maxHours !== 0 ? maxHours : null}
                InputProps={{ inputProps: { min: 0, max: maxHours === 0 ? null : maxHours } }}
                type="number"
                name="total_hours"
                error={!!isMaxError().value}
                helperText={isMaxError().value && isMaxError().message}
              >
                <Label>Total hours</Label>
              </RHFTextField>

              <RHFTextField
                disabled={isEdit}
                label="Maximum months to payout"
                name="installments"
                type="number"
                InputProps={{ inputProps: { min: 0, max: maxMonths === 0 ? null : maxMonths } }}
                error={!!isMaxError().value}
                helperText={isMaxError().value && isMaxError().message}
              />

              <RHFSelect disabled={isEdit} label="Invoice type" native name="plan_selected">
                <option />
                {invoice_types.map((value) => (
                  <option label={value.label} value={value.value} key={value.code}>
                    {value.label}
                  </option>
                ))}
              </RHFSelect>

              <RHFSwitch
                disabled={isEdit && invoice?.email_sent}
                name="email_sent"
                label="Send email"
              />

              {isEdit ? (
                <RHFSelect
                  disabled={invoice?.status === 'void'}
                  native
                  label="Status"
                  name="status"
                >
                  <option />
                  <option key="void" value="void">
                    Void
                  </option>
                  <option key="paid" value="paid">
                    Accepted
                  </option>
                  <option key="pending" value="pending">
                    Pending
                  </option>
                </RHFSelect>
              ) : (
                <></>
              )}
            </Box>

            {!isEdit ? (
              <LoadingButton type="submit" variant="contained">
                Create Order
              </LoadingButton>
            ) : (
              <></>
            )}

            {invoice?.status === 'void' ? (
              <LoadingButton type="submit" variant="contained">
                Save Changes
              </LoadingButton>
            ) : (
              <></>
            )}
          </Card>
        </Grid>
      </Grid>
    </FormProvider>
  );
}
