// form
import { ComponentPropsWithoutRef } from 'react';
import { useFormContext, Controller } from 'react-hook-form';
// @mui
import { MuiTelInput } from 'mui-tel-input';

// ----------------------------------------------------------------------

type Props = {
  name: string;
  helperText?: string;
} & ComponentPropsWithoutRef<typeof MuiTelInput>;

export default function RHFTel({ name, helperText, ...other }: Props) {
  const { control } = useFormContext();

  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <MuiTelInput
          {...field}
          defaultCountry="DK"
          value={typeof field.value === 'number' && field.value === 0 ? '' : field.value}
          error={!!error}
          helperText={error ? error?.message : helperText}
          forceCallingCode
          {...other}
        />
      )}
    />
  );
}
