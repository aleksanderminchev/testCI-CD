import * as Yup from 'yup';
import merge from 'lodash/merge';
import { isBefore } from 'date-fns';
import { EventInput } from '@fullcalendar/core';
// form
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { Box, Stack, Button, Tooltip, TextField, IconButton, DialogActions } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { MobileDateTimePicker } from '@mui/x-date-pickers';

// @types
import { IStudent } from '../../../@types/student';
import { ICalendarEvent } from '../../../@types/calendar';
import { ITutor } from '../../../@types/tutor';
// components
import Iconify from '../../../components/iconify';
import { useSnackbar } from '../../../components/snackbar';
import { ColorSinglePicker } from '../../../components/color-utils';
import FormProvider, {
  RHFTextField,
  RHFSwitch,
  RHFSelect,
  RHFAutocomplete,
} from '../../../components/hook-form';

// ----------------------------------------------------------------------

type FormValuesProps = ICalendarEvent;

type Props = {
  event: EventInput | null | undefined;
  admin: boolean;
  teachers: [];
  students: [];
  range: {
    start: Date;
    end: Date;
  } | null;
  onCancel: VoidFunction;
  onDeleteEvent: VoidFunction;
  onCreateUpdateEvent: (newEvent: ICalendarEvent) => void;
};
const today = new Date();
// ----------------------------------------------------------------------
/**
 * This function returns the initial values for the form based on provided event or range.
 *
 * @function getInitialValues
 * @param {EventInput | null | undefined} event - The event input data.
 * @param {{ start: Date; end: Date } | null} range - The date range for the event.
 * @returns {FormValuesProps} An object containing the initial form values.
 */
const getInitialValues = (
  event: EventInput | null | undefined,
  range: { start: Date; end: Date } | null
) => {
  const initialEvent: FormValuesProps = {
    title: '',
    title_data: '',
    description: '',
    completionNotes: '',
    color: '#1890FF',
    paid: false,
    allDay: false,
    trial_lesson: false,
    studentId: { code: '', label: '', priority: '' },
    studentName: '',
    teacherName: '',
    teacherId: { code: '', label: '', priority: '' },
    start: range
      ? new Date(range.start)
      : new Date(today.getFullYear(), today.getMonth(), today.getDate(), 16),
    end: range
      ? new Date(range.end)
      : new Date(today.getFullYear(), today.getMonth(), today.getDate(), 18),
  };

  if (event || range) {
    return merge({}, initialEvent, event);
  }

  return initialEvent;
};

// ----------------------------------------------------------------------
/**
 * This functional component renders a calendar form with various input fields to create or update events.
 *
 * @component
 * @param {Props} {
 *   event,
 *   teachers,
 *   students,
 *   range,
 *   admin,
 *   onCreateUpdateEvent,
 *   onDeleteEvent,
 *   onCancel,
 * } - Props required for the CalendarForm component.
 * @returns {JSX.Element} The rendered CalendarForm component.
 */
export default function CalendarForm({
  event,
  teachers,
  students,
  range,
  admin,
  onCreateUpdateEvent,
  onDeleteEvent,
  onCancel,
}: Props) {
  const hasEventData = !!event;

  const EventSchema = Yup.object().shape({
    title_data: Yup.string().min(2, 'Skriv en kort titel').max(255).required('Skriv en kort titel'),
    description: Yup.string().max(5000).nullable(true),
    teacherId: Yup.object().shape({
      code: Yup.string().required(),
      label: Yup.string().required(),
    }),
    studentId: Yup.object().shape({
      code: Yup.string().required(),
      label: Yup.string().required(),
    }),
    // start:Yup.date().min(new Date(),'Lesson cannot be created earlier'),
    // end:Yup.date().min(new Date(),'Lesson cannot be created earlier')
  });

  const methods = useForm({
    resolver: yupResolver(EventSchema),
    defaultValues: getInitialValues(event, range),
  });

  const {
    reset,
    watch,
    control,
    setValue,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const values = watch();

  /**
   * This function sorts an array of teachers based on priority.
   *
   * @function sortArrayTeachers
   * @param {ITutor[]} teachersArray - The array of teachers to be sorted.
   * @returns {Array<{ code: string; label: string; priority: string }>} A sorted array of teachers with priority info.
   */
  const sortArrayTeachers = (
    teachersArray: ITutor[]
  ): { code: string; label: string; priority: string }[] => {
    const arrayForSorting = teachersArray.map((value) => {
      const priority = value.students.includes(values.studentId.code);
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
  /**
   * This function sorts an array of students based on priority.
   *
   * @function sortArrayStudents
   * @param {IStudent[]} studentsArray - The array of students to be sorted.
   * @returns {Array<{ code: string; label: string; priority: string }>} A sorted array of students with priority info.
   */
  const sortArrayStudents = (
    studentsArray: IStudent[]
  ): { code: string; label: string; priority: string }[] => {
    const arrayForSorting = studentsArray.map((value) => {
      const priority = value.teachers.includes(values.teacherId.code);
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

  /**
   * This function handles form submission by creating or updating events.
   *
   * @function onSubmit
   * @param {FormValuesProps} data - The form values to be submitted.
   */
  const onSubmit = async (data: FormValuesProps) => {
    try {
      const startDateISO = new Date(data?.start || new Date()).toISOString();
      const endDateISO = new Date(data?.end || new Date()).toISOString();
      const newEvent = {
        title: data.title_data,
        title_data: data.title_data,
        description: data.description,
        trial_lesson: data.trial_lesson,
        color: data.color,
        paid: data.paid,
        studentId: data.studentId,
        studentName: data.studentName,
        teacherName: data.teacherName,
        completionNotes: data.completionNotes,
        teacherId: data.teacherId,
        start: startDateISO,
        end: endDateISO,
        space: '',
      };
      onCreateUpdateEvent(newEvent);
      onCancel();
      reset();
    } catch (error) {
      console.error(error);
      console.log('ADSADWQQW');
    }
  };

  /**
   * This function checks for date-related errors in the form.
   *
   * @function isDateError
   * @returns {{ value: boolean; message: string }} An object containing the error status and message.
   */
  const isDateError = () => {
    const today = new Date();
    const monthMiddle = new Date(today.getFullYear(), today.getMonth(), 15, 23, 59, 59);
    const checkAgeEnd = new Date(values?.end?.toString() || new Date());
    const checkAgeStart = new Date(values?.start?.toString() || new Date());
    if (values.start && values.end) {
      if ((checkAgeEnd.getTime() - checkAgeStart.getTime()) / (60 * 60 * 1000) > 10) {
        return { value: true, message: 'Lektionens længde kan maksimalt være 10 timer' };
      } else if (
        (new Date().getTime() - checkAgeEnd.getTime()) / (60 * 60 * 1000 * 24) > 7 &&
        !admin
      ) {
        return {
          value: true,
          message: 'Lektioner kan ikke ændres efter 7 dage',
        };
      } else if (checkAgeStart.getTime() <= monthMiddle.getTime() && today.getDate() > 15) {
        return {
          value: true,
          message: 'Lektioner kan ikke ændres efter 7 dage',
        };
      }
      return {
        value: isBefore(new Date(values.end), new Date(values.start)),
        message: 'Lektionens sluttidspunkt skal være efter starttidspunktet',
      };
    }
    return { value: false, message: 'No errors' };
  };

  // const time=(new Date().getTime()-new Date(values?.start?.toString() || new Date()).getTime())/(60*60*24*1000);
  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={3} sx={{ px: 3 }}>
        <RHFAutocomplete
          disableClearable
          disableCloseOnSelect={false}
          required
          groupBy={(option) => option.priority}
          name="studentId"
          label="Elev"
          options={sortArrayStudents([...students])}
          ChipProps={{ size: 'small' }}
        />

        <RHFSwitch name="trial_lesson" label="Opstartsmøde" />

        <RHFTextField name="title_data" label="Titel" />

        <RHFTextField name="description" label="Beskrivelse" multiline rows={3} />

        <RHFAutocomplete
          disableClearable
          disableCloseOnSelect={false}
          required
          groupBy={(option) => option.priority}
          label="Tutor"
          name="teacherId"
          options={sortArrayTeachers([...teachers])}
          ChipProps={{ size: 'small' }}
        />
        <Controller
          name="start"
          control={control}
          render={({ field }) => (
            <MobileDateTimePicker
              {...field}
              ampm={false}
              ampmInClock={false}
              onChange={(newValue: Date | null) => {
                field.onChange(newValue);
                const newDate = new Date();
                setValue(
                  'end',
                  new Date(
                    newValue?.getFullYear() || newDate.getFullYear(),
                    newValue?.getMonth() || newDate.getMonth(),
                    newValue?.getDate() || newDate.getDate(),
                    (newValue?.getHours() || newDate.getHours()) + 2
                  )
                );
              }}
              label="Starttidspunkt"
              openTo="day"
              views={['day', 'hours', 'minutes']}
              minutesStep={15}
              renderInput={(params) => (
                <TextField
                  onKeyDown={(e) => {
                    e.preventDefault();
                  }}
                  {...params}
                  fullWidth
                />
              )}
            />
          )}
        />

        <Controller
          name="end"
          control={control}
          render={({ field }) => (
            <MobileDateTimePicker
              {...field}
              ampm={false}
              ampmInClock={false}
              onChange={(newValue: Date | null) => field.onChange(newValue)}
              label="Sluttidspunkt"
              minutesStep={15}
              openTo="day"
              views={['day', 'hours', 'minutes']}
              renderInput={(params) => (
                <TextField
                  {...params}
                  fullWidth
                  error={!!isDateError().value}
                  helperText={isDateError().value && isDateError().message}
                />
              )}
            />
          )}
        />
      </Stack>

      <DialogActions>
        {hasEventData && (
          <Tooltip title="Delete Event">
            <IconButton onClick={onDeleteEvent}>
              <Iconify icon="eva:trash-2-outline" />
            </IconButton>
          </Tooltip>
        )}

        <Box sx={{ flexGrow: 1 }} />

        <Button variant="outlined" color="inherit" onClick={onCancel}>
          Annuller
        </Button>

        <LoadingButton type="submit" variant="contained" loading={isSubmitting}>
          {hasEventData ? 'Opdater' : 'Tilføj'}
        </LoadingButton>
      </DialogActions>
    </FormProvider>
  );
}
