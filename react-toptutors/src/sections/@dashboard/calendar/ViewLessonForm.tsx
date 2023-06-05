import * as Yup from 'yup';
import merge from 'lodash/merge';
import { isBefore } from 'date-fns';
import { EventInput } from '@fullcalendar/core';
// form
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { Box, Stack, Button, TextField, DialogActions, Grid } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { MobileDateTimePicker } from '@mui/x-date-pickers';
import { useNavigate } from 'react-router';

// @types
import { IStudent } from '../../../@types/student';
import { ICalendarEvent } from '../../../@types/calendar';
import { ITutor } from '../../../@types/tutor';
// components
import FormProvider, {
  RHFTextField,
  RHFSwitch,
  RHFAutocomplete,
} from '../../../components/hook-form';
import { CancelLessonDialog } from './CancelLessonDialog';
import { CompleteLessonDialog } from '../lessons';
import { useState } from 'react';
//redux
import { completeLesson, createEvent } from '../../../redux/slices/calendar';
import { useDispatch, useSelector } from '../../../redux/store';
// ----------------------------------------------------------------------

type FormValuesProps = ICalendarEvent;

type Props = {
  colorOptions: string[];
  event: EventInput | null | undefined;
  admin: boolean;
  editable: boolean;
  teachers: [];
  students: [];
  cancel: boolean;
  range: {
    start: Date;
    end: Date;
  } | null;
  onClose: VoidFunction;
  onCancel: (state: boolean) => void;
  cancelLesson: (reason: string) => void;
  onDeleteEvent: VoidFunction;
  onCreateUpdateEvent: (newEvent: ICalendarEvent) => void;
};

// ----------------------------------------------------------------------

const getInitialValues = (
  event: EventInput | null | undefined,
  range: { start: Date; end: Date } | null
) => {
  const initialEvent: FormValuesProps = {
    title: '',
    title_data: '',
    description: '',
    color: '#1890FF',
    completionNotes: '',
    studentId: { code: '', label: '', priority: '' },
    studentName: '',
    teacherId: { code: '', label: '', priority: '' },
    teacherName: '',
    paid: false,
    trial_lesson: false,
    allDay: false,
    start: range ? new Date(range.start).toString() : new Date().toString(),
    end: range ? new Date(range.end).toString() : new Date().toString(),
  };

  if (event || range) {
    return merge({}, initialEvent, event);
  }

  return initialEvent;
};

// ----------------------------------------------------------------------
/**
 * @component
 *
 * @param {Props} {
 * event,
 * range,
 * admin,
 * editable,
 * teachers,
 * students,
 * cancel,
 * colorOptions,
 * onCreateUpdateEvent,
 * onDeleteEvent,
 * onClose,
 * onCancel,
 * cancelLesson,
 *  }
 * @returns  {JSX.Element} The rendered ViewLessonForm component. This is used to view Lessons in the Calendar
 */
export default function ViewLessonForm({
  event,
  range,
  admin,
  editable,
  teachers,
  students,
  cancel,
  colorOptions,
  onCreateUpdateEvent,
  onDeleteEvent,
  onClose,
  onCancel,
  cancelLesson,
}: Props) {
  const hasEventData = !!event;

  const navigate = useNavigate();
  const dispatch = useDispatch();
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
    // end:Yup.date().min(new Date(),'Lesson cannot be created earlier'),
  });

  const methods = useForm({
    resolver: yupResolver(EventSchema),
    defaultValues: getInitialValues(event, range),
  });
  const { error } = useSelector((state) => state.calendar);
  const {
    reset,
    watch,
    control,
    setValue,
    handleSubmit,
    formState: { isSubmitting },
  } = methods;

  const values = watch();
  const onSubmit = async (data: FormValuesProps) => {
    try {
      const startDateISO = new Date(data?.start || new Date()).toISOString();
      const endDateISO = new Date(data?.end || new Date()).toISOString();
      const newEvent = {
        title: data.title_data,
        title_data: data.title_data,
        description: data.description,
        color: data.color,
        allDay: data.allDay,
        paid: data.paid,
        completionNotes: data.completionNotes,
        studentId: data.studentId,
        studentName: data.studentName,
        teacherName: data.teacherName,
        teacherId: data.teacherId,
        trial_lesson: data.trial_lesson,
        start: startDateISO,
        end: endDateISO,
      };
      onCreateUpdateEvent(newEvent);
      onClose();
      reset();
    } catch (error) {
      console.error(error);
    }
  };
  console.log(values);
  /**
   * Sorts and allows the RHFSelect element to accept the data
   * @param studentsArray Initial teacher array
   * @returns a sorted list of the teachers, the array has been mapped to fit the RHFSelect elemetn
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
   * Sorts and allows the RHFSelect element to accept the data
   * @param studentsArray Initial Student array
   * @returns a sorted list of the students, the array has been mapped to fit the RHFSelect elemetn
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
  // Handles everything related to completing the lesson.
  const sendLessonCompletion = (completionNotes: string) => {
    dispatch(completeLesson(parseInt(event?.id || '', 10), completionNotes));
    navigate('/calendar');
    setTimeout(() => {
      window.location.replace('/calendar');
    }, 800);
  };

  // Creates a new lesson if they choose to plan it right away.
  const handleCreateUpdateEvent = (newEvent: ICalendarEvent) => {
    dispatch(createEvent(newEvent));
  };
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
  const time =
    (new Date().getTime() - new Date(values?.start?.toString() || new Date()).getTime()) /
    (60 * 60 * 24 * 1000);
  const stateEdit = editable && event?.status !== 'scheduled';

  const [openCompleteLessonDialog, setOpenCompleteLessonDialog] = useState(false);
  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Stack spacing={3} sx={{ px: 3 }}>
        <RHFTextField disabled={stateEdit || time > 7} name="title_data" label="Titel" />

        <RHFTextField
          disabled={stateEdit || time > 7}
          name="description"
          label="Beskrivelse"
          multiline
          rows={3}
        />

        {/* If lesson has been completed then show completion notes. */}
        {event?.status !== 'scheduled' && (
          <RHFTextField
            disabled={stateEdit || time > 7}
            name="completionNotes"
            label="Evalueringsrapport"
            multiline
            rows={10}
          />
        )}
        <RHFSwitch
          disabled={stateEdit || time > 7 || event?.status !== 'scheduled'}
          name="trial_lesson"
          label="Opstartsmøde"
        />
        {/* <RHFTextField disabled name="status" label="Status" /> */}
        <RHFAutocomplete
          disableClearable
          disableCloseOnSelect={false}
          required
          groupBy={(option) => option.priority}
          disabled
          label="Elev"
          name="studentId"
          options={sortArrayStudents([...students])}
          ChipProps={{ size: 'small' }}
        />
        <RHFAutocomplete
          disableClearable
          disableCloseOnSelect={false}
          required
          groupBy={(option) => option.priority}
          disabled
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
              ampm={false}
              ampmInClock={false}
              disabled={stateEdit || time > 7 || event?.status !== 'scheduled'}
              {...field}
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
              minutesStep={15}
              openTo="day"
              views={['day', 'hours', 'minutes']}
              renderInput={(params) => <TextField disabled {...params} fullWidth />}
            />
          )}
        />

        <Controller
          name="end"
          control={control}
          render={({ field }) => (
            <MobileDateTimePicker
              {...field}
              disabled={stateEdit || time > 7 || event?.status !== 'scheduled'}
              ampm={false}
              ampmInClock={false}
              onChange={(newValue: Date | null) => field.onChange(newValue)}
              label="Sluttidspunkt"
              minutesStep={15}
              openTo="day"
              views={['day', 'hours', 'minutes']}
              renderInput={(params) => (
                <TextField
                  disabled={editable}
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

      <Box sx={{ flexGrow: 1 }} />
      <DialogActions>
        <Grid container direction="column" spacing={2}>
          <Grid item xs={12}>
            <Button
              variant="contained"
              fullWidth
              onClick={() => {
                if (event?.status === 'scheduled') {
                  navigate(`/lesson/${event?.id}`);
                } else {
                  navigate(`/lesson/${event?.id}/recording`);
                }
              }}
            >
              {event?.status === 'scheduled' ? 'Tilslut Lektion' : 'Se lektionen'}
            </Button>
          </Grid>
          <Grid item container xs={12} spacing={1}>
            {stateEdit || time > 7 ? (
              <></>
            ) : (
              <>
                <Grid item xs={4}>
                  <LoadingButton
                    disabled={editable || time > 7}
                    type="submit"
                    variant="outlined"
                    loading={isSubmitting}
                  >
                    Gem ændringer
                  </LoadingButton>
                </Grid>
                {event?.status !== 'scheduled' ? (
                  <></>
                ) : (
                  <>
                    <Grid item xs={4}>
                      <Button
                        variant="contained"
                        color="success"
                        onClick={() => setOpenCompleteLessonDialog(true)}
                      >
                        Complete Lesson
                      </Button>
                    </Grid>
                    <Grid item xs={4}>
                      <Button variant="outlined" color="error" onClick={() => onCancel(true)}>
                        Aflys lektionen
                      </Button>
                    </Grid>
                  </>
                )}
              </>
            )}
          </Grid>
        </Grid>
      </DialogActions>

      <CancelLessonDialog
        admin={admin}
        cancel={cancel}
        onCancel={onCancel}
        cancelLesson={cancelLesson}
      />
      <CompleteLessonDialog
        teachers={teachers}
        students={students}
        error={error}
        finishLessson={sendLessonCompletion}
        handleCreateUpdateEvent={handleCreateUpdateEvent}
        cancel={openCompleteLessonDialog}
        admin={admin}
        onCancel={setOpenCompleteLessonDialog}
      />
    </FormProvider>
  );
}
