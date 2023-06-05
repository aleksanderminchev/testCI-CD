// form
import { useFormContext, Controller } from 'react-hook-form';
// @mui
import { Autocomplete, AutocompleteProps, TextField } from '@mui/material';

// ----------------------------------------------------------------------

// Define Props interface with generic types for customization
interface Props<
  T,
  Multiple extends boolean | undefined,
  DisableClearable extends boolean | undefined,
  FreeSolo extends boolean | undefined
> extends AutocompleteProps<T, Multiple, DisableClearable, FreeSolo> {
  name: string;
  label?: string;
  required?: boolean;
  helperText?: React.ReactNode;
}

// RHFAutocomplete component definition
// It receives generic types for customization and extends from the Props interface
export default function RHFAutocomplete<
  T,
  Multiple extends boolean | undefined,
  DisableClearable extends boolean | undefined
>({
  name,
  label,
  required,
  helperText,
  ...other
}: Omit<Props<T, Multiple, DisableClearable, false>, 'renderInput'>) {
  // Get control and setValue from useFormContext
  const { control, setValue } = useFormContext();

  // Use the Controller component to integrate with react-hook-form
  return (
    <Controller
      name={name}
      control={control}
      render={({ field, fieldState: { error } }) => (
        <Autocomplete
          {...field}
          onChange={(event, newValue) => setValue(name, newValue, { shouldValidate: true })}
          renderInput={(params) => (
            <TextField
              required={required}
              label={label}
              error={!!error}
              helperText={error ? error?.message : helperText}
              {...params}
            />
          )}
          getOptionLabel={(option: T) => (option as any).label || ''}
          freeSolo={false}
          {...other}
        />
      )}
    />
  );
}
