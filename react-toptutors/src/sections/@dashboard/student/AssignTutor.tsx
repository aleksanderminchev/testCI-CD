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
import Iconify from '../../../components/iconify';

// @types
import { IStudent } from '../../../@types/student';
import { ITutor } from '../../../@types/tutor';
import FormProvider, { RHFAutocomplete } from '../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps {
  teachers: { code: string; label: string; priority: string }[];
}
type Props = {
  open: boolean;
  teachers: ITutor[];
  student: IStudent | null;
  handleAssignNewTeachers: (teacherId: number[], studentEmail: string) => void;
  onCancel: (value: boolean) => void;
};
export default function AssignTutors({
  open,
  teachers,
  student,
  onCancel,
  handleAssignNewTeachers,
}: Props) {
  const NewUserSchema = Yup.object().shape({
    // password:Yup.string(),
    // email: Yup.string().required('Email is required').email('Email must be a valid email address'),
    // avatarUrl: Yup.string().required('Avatar is required').nullable(true),
  });
  const sortArrayStudents = (
    teachersArray: ITutor[]
  ): { code: string; label: string; priority: string }[] => {
    const arrayForSorting = teachersArray.map((value) => {
      const priority = value.students.includes(student?.id.toString() || '');
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
      const foundTeacher = teachers.find((value) => value.id.toString() === student);
      if (foundTeacher) {
        return {
          code: foundTeacher.id.toString(),
          label: `${foundTeacher.first_name} ${foundTeacher.last_name}`,
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
    if (student?.teachers && teachers) {
      const initialArray = filterInitialValues(student?.teachers);
      if (initialArray) {
        setValue('teachers', initialArray, { shouldValidate: true });
      }
    }
  }, [student?.teachers, teachers]);
  const defaultValuesIndependent = useMemo(
    () => ({
      teachers: [],
    }),
    []
    // eslint-disable-next-line react-hooks/exhaustive-deps
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewUserSchema),
    defaultValues: defaultValuesIndependent,
  });
  const { reset, watch, control, setValue, handleSubmit } = methods;

  const values = watch();
  const onSubmit = async (data: FormValuesProps) => {
    try {
      handleAssignNewTeachers(
        data.teachers.map((teacher) => parseInt(teacher.code)),
        student?.email || ''
      );
      onCancel(false);
      //navigate(PATH_DASHBOARD.dashboard);
    } catch (err) {
      console.error(err);
      // enqueueSnackbar(!isEdit ? 'Create success!' : 'Update success!', { variant: 'error' });
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
              name="teachers"
              label="Elev"
              options={sortArrayStudents([...teachers])}
              ChipProps={{ size: 'small' }}
              filterOptions={(options) => {
                const filtered = options.filter(
                  (option) => !values.teachers?.find((object) => object.code === option.code)
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
