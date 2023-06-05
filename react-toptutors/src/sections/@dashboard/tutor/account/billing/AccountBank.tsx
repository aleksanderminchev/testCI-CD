import * as Yup from 'yup';

import { useState } from 'react';
// @mui
import {
  Stack,
  Button,
  Dialog,
  IconButton,
  DialogTitle,
  DialogProps,
  DialogActions,
  DialogContent,
  InputAdornment,
} from '@mui/material';
import { LoadingButton } from '@mui/lab';

// components
import Iconify from '../../../../../components/iconify';
import MenuPopover from '../../../../../components/menu-popover';
import { useSnackbar } from '../../../../../components/snackbar';
//redux
import { useDispatch, useSelector } from '../../../../../redux/store';
import { editTutor, selectTutor } from '../../../../../redux/slices/tutor';

// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import FormProvider, { RHFTextField } from '../../../../../components/hook-form';
// types
import { ITutor } from '../../../../../@types/tutor';

// ----------------------------------------------------------------------

interface Props extends DialogProps {
  onClose: VoidFunction;
}

type FormValuesProps = Partial<ITutor>;

export default function AccountBank({ onClose, ...other }: Props) {
  const [openPopover, setOpenPopover] = useState<HTMLElement | null>(null);

  const dispatch = useDispatch();

  const tutor = useSelector(selectTutor);

  const { enqueueSnackbar } = useSnackbar();

  const handleOpenPopover = (event: React.MouseEvent<HTMLElement>) => {
    setOpenPopover(event.currentTarget);
  };

  const handleClosePopover = () => {
    setOpenPopover(null);
  };

  const UpdateBankSchema = Yup.object().shape({
    reg_number: Yup.string()
      .matches(/^\d+$/, { message: 'Må kun indeholde tal.' })
      .required('Der mangler reg. nr.')
      .min(4, 'Skal være på 4 cifre.')
      .max(4, 'Skal være på 4 cifre.'),
    bank_number: Yup.string()
      .matches(/^\d+$/, { message: 'Må kun indeholde tal.' })
      .required('Der mangler kontonr.')
      .min(4, 'Skal minimum være 4 cifre.')
      .max(10, 'Kan maks være 10 cifre.'),
  });

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(UpdateBankSchema),
    defaultValues: { reg_number: tutor?.reg_number, bank_number: tutor?.bank_number },
  });

  const {
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const onSubmit = async (data: FormValuesProps) => {
    try {
      onClose();
      const tutorData = {
        id: tutor?.id,
        reg_number: data.reg_number,
        bank_number: data.bank_number,
      };

      const success = await dispatch(editTutor(tutorData));

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

  return (
    <>
      <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
        <Dialog maxWidth="xs" onClose={onClose} {...other}>
          <DialogTitle>Opdater bankoplysninger</DialogTitle>

          <DialogContent sx={{ overflow: 'unset' }}>
            <Stack spacing={3}>
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <RHFTextField
                  name="reg_number"
                  label="Reg. nr."
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton size="small" edge="end" onClick={handleOpenPopover}>
                          <Iconify icon="eva:info-fill" />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />

                <RHFTextField
                  name="bank_number"
                  label="Kontonummer"
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton size="small" edge="end" onClick={handleOpenPopover}>
                          <Iconify icon="eva:info-fill" />
                        </IconButton>
                      </InputAdornment>
                    ),
                  }}
                />
              </Stack>
            </Stack>
          </DialogContent>

          <DialogActions>
            <Button color="inherit" variant="outlined" onClick={onClose}>
              Annuller
            </Button>

            <LoadingButton
              type="submit"
              variant="contained"
              onClick={methods.handleSubmit(onSubmit)}
              loading={isSubmitting}
            >
              Opdater
            </LoadingButton>
          </DialogActions>
        </Dialog>
      </FormProvider>

      <MenuPopover
        open={openPopover}
        onClose={handleClosePopover}
        arrow="bottom-center"
        sx={{ maxWidth: 300, typography: 'body2', textAlign: 'center' }}
      >
        Reg.nr. er de første fire cifre og de resterende er kontonummeret.
        <br />
        <br />
        Eksempel: 1234-567890
      </MenuPopover>
    </>
  );
}
