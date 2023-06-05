import * as Yup from 'yup';
import { useEffect, useMemo } from 'react';

// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import {
  Button,
  Dialog,
  Stack,
  IconButton,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';

// components
import Iconify from '../../../../components/iconify';
import { useSnackbar } from '../../../../components/snackbar';

// @types
import { IStudent } from '../../../../@types/student';
import { ITutor } from '../../../../@types/tutor';
import FormProvider, { RHFAutocomplete } from '../../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps {
  students: { code: string; label: string; priority: string }[];
}
type Props = {
  open: boolean;
  teacher: ITutor | null;
  students: IStudent[];
  handleAssignNewStudents: (studentId: number[], teacherEmail: string) => void;
  onCancel: (value: boolean) => void;
};

export default function AssignStudents({
  open,
  teacher,
  students,
  onCancel,
  handleAssignNewStudents,
}: Props) {
  const NewUserSchema = Yup.object().shape({
    // password:Yup.string(),
    // email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    // avatarUrl: Yup.string().required('Avatar is required').nullable(true),
  });

  const sortArrayStudents = (
    studentsArray: IStudent[]
  ): { code: string; label: string; priority: string }[] => {
    const arrayForSorting = studentsArray.map((value) => {
      const priority = value.teachers.includes(teacher?.id.toString() || '');
      return {
        code: value.id.toString(),
        label: `${value.first_name} ${value.last_name}`,
        priority: priority ? 'Priority' : 'All',
      };
    });
    return arrayForSorting.sort((a, b) => {
      if (a.priority === 'Priority') {
        return -1;
      }
      return 1;
    });
  };

  const filterInitialValues = (teacherStudents: string[]) => {
    const filtedred = teacherStudents.map((student) => {
      const foundStudent = students.find((value) => value.id.toString() === student);
      if (foundStudent) {
        return {
          code: foundStudent.id.toString(),
          label: `${foundStudent.first_name} ${foundStudent.last_name}`,
          priority: 'All',
        };
      } else {
        return {
          code: '',
          label: '',
          priority: 'All',
        };
      }
    });
    if (filtedred) return filtedred;
    else return [];
  };

  useEffect(() => {
    if (students && teacher?.students) {
      const initialArray = filterInitialValues(teacher?.students);
      if (initialArray) {
        setValue('students', initialArray, { shouldValidate: true });
      }
    }
  }, [students, teacher?.students]);

  const defaultValuesIndependent = useMemo(
    () => ({
      students: [],
    }),
    []
    // eslint-disable-next-line react-hooks/exhaustive-deps
  );

  const { enqueueSnackbar } = useSnackbar();

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewUserSchema),
    defaultValues: defaultValuesIndependent,
  });
  const { watch, setValue, handleSubmit } = methods;

  const values = watch();
  const onSubmit = async (data: FormValuesProps) => {
    try {
      handleAssignNewStudents(
        data.students.map((student) => parseInt(student.code)),
        teacher?.email || ''
      );
      onCancel(false);
      //navigate(PATH_DASHBOARD.dashboard);
    } catch (err) {
      console.error(err);
      enqueueSnackbar('Fejl. Kontakt os.', { variant: 'error' });
    }
  };
  return (
    <Stack
      spacing={3}
      direction="row"
      justifyContent="space-between"
      sx={{
        color: 'text.main',
      }}
    >
      <Dialog fullWidth maxWidth="xs" open={open} onClose={() => onCancel(false)}>
        <DialogTitle>
          Assign Students
          <IconButton
            sx={{ position: 'absolute', right: 8, top: 8 }}
            color="error"
            onClick={() => onCancel(false)}
          >
            <Iconify icon="ic:sharp-close" />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
            <RHFAutocomplete
              filterSelectedOptions
              disableClearable
              disableCloseOnSelect={false}
              multiple
              defaultChecked
              groupBy={(option) => option.priority}
              name="students"
              label="Elev"
              options={sortArrayStudents([...students])}
              ChipProps={{ size: 'small' }}
              filterOptions={(options) => {
                const filtered = options.filter(
                  (option) => !values.students?.find((object) => object.code === option.code)
                );
                console.log(filtered);
                return filtered;
              }}
            ></RHFAutocomplete>
            <Button type="submit" variant="contained">
              Assign Students
            </Button>
          </FormProvider>
        </DialogContent>
        <DialogActions></DialogActions>
      </Dialog>
    </Stack>
  );
}
