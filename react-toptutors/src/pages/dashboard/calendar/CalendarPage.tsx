import FullCalendar from '@fullcalendar/react'; // => request placed at the top
import allLocales from '@fullcalendar/core/locales-all';
import { DateSelectArg, EventClickArg, EventDropArg, EventInput } from '@fullcalendar/core';
import interactionPlugin, { EventResizeDoneArg } from '@fullcalendar/interaction';
import listPlugin from '@fullcalendar/list';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import timelinePlugin from '@fullcalendar/timeline';
//
import googleCalendarPlugin from '@fullcalendar/google-calendar';
//
import { useState, useRef, useEffect, useCallback } from 'react';
import { Helmet } from 'react-helmet-async';
import { useAuthContext } from 'src/auth/useAuthContext';
// @mui
import { Card, Button, Container, IconButton, DialogTitle, Dialog } from '@mui/material';

// redux
import { useDispatch, useSelector } from '../../../redux/store';

import {
  cancellationLesson,
  getStudents,
  getCustomers,
  getTeachers,
  getEventsStudents,
  getEventsTeacher,
  getEventsAdmin,
  createEvent,
  updateEvent,
  deleteEvent,
  getEventsCustomers,
} from '../../../redux/slices/calendar';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';

// utils
import { fDate, fTimestamp } from '../../../utils/formatTime';
// hooks
import useResponsive from '../../../hooks/useResponsive';
// @types
import { ICalendarEvent, ICalendarViewValue } from '../../../@types/calendar';
import { IStudent } from '../../../@types/student';
import { ITutor } from '../../../@types/tutor';
import { ICustomer } from '../../../@types/customer';
// components
import Iconify from '../../../components/iconify';
import { useSnackbar } from '../../../components/snackbar';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { useSettingsContext } from '../../../components/settings';
// sections
import {
  CalendarForm,
  ViewLessonForm,
  StyledCalendar,
  CalendarToolbar,
  CalendarFilterDrawer,
} from '../../../sections/@dashboard/calendar';

// ----------------------------------------------------------------------

const COLOR_OPTIONS = [
  '#00AB55', // theme.palette.primary.main,
  '#FFC107', // theme.palette.warning.main,
  '#FF4842', // theme.palette.error.main
];

// ----------------------------------------------------------------------

export default function CalendarPage() {
  // Snackbar handling
  const { enqueueSnackbar } = useSnackbar();

  // Accessing settings context
  const { themeStretch } = useSettingsContext();

  // Dispatching actions to the Redux store
  const dispatch = useDispatch();

  // Boolean for checking if the device is a desktop
  const isDesktop = useResponsive('up', 'sm');

  // Calendar component reference
  const calendarRef = useRef<FullCalendar>(null);

  // Extracting required data from the Redux store
  const { error } = useSelector((state) => state.calendar);
  const { teachers, students, customers } = useGetStudentsAndTeachers();
  const { user } = useAuthContext();

  // State variables for managing the modals, selected event, and selected date range
  const [openForm, setOpenForm] = useState(false);
  const [openViewForm, setOpenViewForm] = useState(false);
  const [selectedEventId, setSelectedEventId] = useState<string | ''>('');
  const [selectedRange, setSelectedRange] = useState<{
    start: Date;
    end: Date;
  } | null>(null);
  // State variable for the current date
  const [date, setDate] = useState(new Date());

  const [endDate, setEndDate] = useState<Date | null>(
    new Date((date || new Date()).getFullYear(), (date || new Date()).getMonth() + 1, 1)
  );
  const [startDate, setStartDate] = useState<Date | null>(
    new Date((date || new Date()).getFullYear(), (date || new Date()).getMonth(), 1)
  );

  console.log(date);
  const events = useGetEvents(date);

  // State variables for managing filters and filter values
  const [openFilter, setOpenFilter] = useState(false);
  const [cancel, setCancel] = useState(false);
  const [filterEventColor, setFilterEventColor] = useState<string[]>([]);
  const [filterTeacher, setFilterTeacher] = useState<ITutor[]>([]);
  const [filterStudent, setFilterStudent] = useState<IStudent[]>([]);
  const [filterCustomer, setFilterCustomer] = useState<ICustomer[]>([]);
  const [filterByPaid, setFilterByPaid] = useState<boolean>(false);
  const [filterByTrial, setFilterByTrial] = useState<boolean>(false);

  // State variable for the calendar view
  const [view, setView] = useState<ICalendarViewValue>(isDesktop ? 'dayGridMonth' : 'listWeek');

  // Selecting the event by its ID
  const selectedEvent = useSelector(() => {
    if (selectedEventId) {
      return events.find((event) => event.id === selectedEventId);
    }

    return null;
  });

  // Effect to handle view change and error display
  useEffect(() => {
    const calendarEl = calendarRef.current;
    if (calendarEl) {
      const calendarApi = calendarEl.getApi();

      const newView = isDesktop ? 'dayGridMonth' : 'listWeek';
      calendarApi.changeView(newView);
      setView(newView);
    }
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
  }, [isDesktop, error, enqueueSnackbar]);

  /**
   * Opens the appropriate modal based on the selected event.
   */
  const handleOpenModal = () => {
    if (selectedEventId) {
      setOpenViewForm(true);
    } else {
      setOpenForm(true);
    }
  };

  /**
   * Conditionally renders the "Planlæg lektion" button if the user is an admin or a teacher.
   * @returns {ReactElement} The rendered button or an empty fragment.
   */
  const renderCreateLessonButton = () => {
    if (user?.admin || user?.teacher) {
      return (
        <Button
          variant="contained"
          startIcon={<Iconify icon="eva:plus-fill" />}
          onClick={handleOpenModal}
        >
          Planlæg lektion
        </Button>
      );
    }
    return <></>;
  };

  /**
   * Handles lesson cancellation based on the provided reason.
   * @param {string} reason - The reason for cancelling the lesson.
   */
  const cancelLesson = (reason: string) => {
    try {
      const event = getEventForForm();
      const today = new Date();
      const monthMiddle = new Date(today.getFullYear(), today.getMonth(), 15, 23, 59, 59);
      const checkAgeEnd = new Date(event?.end?.toString() || new Date());
      const checkAgeStart = new Date(event?.start?.toString() || new Date());
      if ((new Date().getTime() - checkAgeEnd.getTime()) / (60 * 60 * 24 * 1000) > 7) {
        throw Error('Lesson is older than 7 days');
      } else if (event?.paid) {
        throw Error('Paid lesson cannot be edited');
      } else if (checkAgeStart.getTime() <= monthMiddle.getTime() && today.getDate() > 15) {
        throw Error('Lesson cannot be edited in the previous wage month');
      }
      // const cancellationType:string=checkCancellationTime(startTime,reason)
      if (user?.admin) {
        dispatch(cancellationLesson(event?.id || '', reason));
        handleCloseModal();
      } else if (user?.teacher) {
        dispatch(cancellationLesson(event?.id || '', reason));
        handleCloseModal();
      }
    } catch (err) {
      console.log(err);
      enqueueSnackbar(err.message, { variant: 'error' });
    }
  };

  /**
   * Closes both form modals and resets the selected event and range.
   */
  const handleCloseModal = () => {
    setOpenForm(false);
    setOpenViewForm(false);
    setSelectedEventId('');
    setSelectedRange(null);
  };

  /**
   * Updates the `cancel` state variable with the provided value.
   * @param {boolean} state - The new value for the `cancel` state.
   */
  const handleCancelModal = (state: boolean) => {
    setCancel(state);
  };

  /**
   * Navigates to today's date on the calendar and updates the `date` state variable.
   */
  const handleClickToday = () => {
    const calendarEl = calendarRef.current;
    if (calendarEl) {
      const calendarApi = calendarEl.getApi();

      calendarApi.today();
      setDate(calendarApi.getDate());
    }
  };

  /**
   * Changes the calendar view to the specified view type.
   * @param {ICalendarViewValue} newView - The new calendar view type.
   */
  const handleChangeView = (newView: ICalendarViewValue) => {
    const calendarEl = calendarRef.current;
    if (calendarEl) {
      const calendarApi = calendarEl.getApi();

      calendarApi.changeView(newView);
      setView(newView);
    }
  };

  /**
   * Navigates to the previous date range in the calendar view.
   */
  const handleClickDatePrev = () => {
    const calendarEl = calendarRef.current;
    if (calendarEl) {
      const calendarApi = calendarEl.getApi();

      calendarApi.prev();
      setDate(calendarApi.getDate());
    }
  };

  /**
   * Navigates to the next date range in the calendar view.
   */
  const handleClickDateNext = () => {
    const calendarEl = calendarRef.current;
    if (calendarEl) {
      const calendarApi = calendarEl.getApi();

      calendarApi.next();
      setDate(calendarApi.getDate());
    }
  };

  /**
   * Handles date range selection in the calendar.
   * @param {DateSelectArg} arg - The selected date range.
   */
  const handleSelectRange = (arg: DateSelectArg) => {
    const calendarEl = calendarRef.current;
    if (calendarEl) {
      const calendarApi = calendarEl.getApi();

      calendarApi.unselect();
    }
    console.log(arg);
    const start_date = new Date(
      arg.start.getFullYear(),
      arg.start.getMonth(),
      arg.start.getDate(),
      16
    );
    const end_date = new Date(
      arg.start.getFullYear(),
      arg.start.getMonth(),
      arg.start.getDate(),
      18
    );
    handleOpenModal();
    setSelectedRange({
      start: start_date,
      end: end_date,
    });
  };

  /**
   * Handles event selection in the calendar.
   * @param {EventClickArg} arg - The selected event.
   */
  const handleSelectEvent = (arg: EventClickArg) => {
    setSelectedEventId(arg.event.id);
    handleOpenModal();
  };

  /**
   * Returns the selected event object for the form.
   * @returns {ICalendarEvent | undefined} The selected event object or undefined.
   */
  const getEventForForm = () => {
    const value = events.find((event) => event.id?.toString() === selectedEventId);
    return value;
  };

  /**
   * Handles resizing events in the calendar.
   * @param {EventResizeDoneArg} arg - The resized event.
   */
  const handleResizeEvent = ({ event }: EventResizeDoneArg) => {
    try {
      const startDateISO = new Date(event?.start || new Date()).toISOString();
      const endDateISO = new Date(event?.end || new Date()).toISOString();
      if ((user?.admin || user?.teacher) && event?.backgroundColor === '#FFC107') {
        dispatch(
          updateEvent(event.id, {
            start: startDateISO,
            end: endDateISO,
          })
        );
      } else {
        enqueueSnackbar('Cannot update the lesson', { variant: 'error' });
        handleClickToday();
      }
    } catch (err) {
      console.log(err);
      enqueueSnackbar('Cannot update the lesson', { variant: 'error' });
      handleClickToday();
    }
  };

  /**
   * Handles dragging and dropping events in the calendar.
   * @param {EventDropArg} arg - The dropped event.
   */
  const handleDropEvent = ({ event }: EventDropArg) => {
    try {
      const startDateISO = new Date(event?.start || new Date()).toISOString();
      const endDateISO = new Date(event?.end || new Date()).toISOString();
      console.log(event);
      if ((user?.admin || user?.teacher) && event?.backgroundColor === '#FFC107') {
        dispatch(
          updateEvent(event.id, {
            start: startDateISO,
            end: endDateISO,
          })
        );
      } else {
        enqueueSnackbar('Cannot update the lesson', { variant: 'error' });
        handleClickToday();
      }
    } catch (err) {
      console.log(err);
      enqueueSnackbar('Cannot update the lesson', { variant: 'error' });
      handleClickToday();
    }
  };

  /**
   * Handles creating or updating an event in the calendar.
   * @param {ICalendarEvent} newEvent - The new or updated event object.
   */
  const handleCreateUpdateEvent = async (newEvent: ICalendarEvent) => {
    try {
      if (selectedEventId) {
        const success = await dispatch(updateEvent(selectedEventId, newEvent));

        if (success) {
          enqueueSnackbar('Lektionen er opdateret!');
        } else {
          enqueueSnackbar('Update failed!', { variant: 'error' });
        }
      } else {
        const success = await dispatch(createEvent(newEvent));
        if (success) {
          enqueueSnackbar('Lektionen er oprettet!');
        } else {
          enqueueSnackbar('Update failed!', { variant: 'error' });
        }
      }
    } catch (error) {
      console.error(error);
      enqueueSnackbar('Update failed!', { variant: 'error' });
    }
  };

  /**
   * Handles deleting an event from the calendar.
   */
  const handleDeleteEvent = () => {
    try {
      if (selectedEventId) {
        handleCloseModal();
        dispatch(deleteEvent(selectedEventId));
        enqueueSnackbar('Delete success!');
      }
    } catch (err) {
      console.error(err);
    }
  };

  /**
   * Handles filtering events by color.
   * @param {string} eventColor - The event color to filter by.
   */
  const handleFilterEventColor = (eventColor: string) => {
    const checked = filterEventColor.includes(eventColor)
      ? filterEventColor.filter((value) => value !== eventColor)
      : [...filterEventColor, eventColor];

    setFilterEventColor(checked);
  };

  /**
   * Handles filtering events by teachers.
   * @param {Array<{ value: ITutor; priority: string }>} options - The teacher filter options.
   */
  const handleFilterEventTeacher = (options: { value: ITutor; priority: string }[]) => {
    setFilterTeacher(options.map((option) => option.value));
  };

  /**
   * Handles filtering paid lessons.
   * @param {boolean} option - The boolean value indicating whether to filter paid lessons.
   */
  const handleFilterPaidLessons = (option: boolean) => {
    setFilterByPaid(option);
  };

  /**
   * Handles filtering trial lessons.
   * @param {boolean} option - The boolean value indicating whether to filter trial lessons.
   */
  const handleFilterTrialLessons = (option: boolean) => {
    setFilterByTrial(option);
  };

  /**
   * Handles filtering events by students.
   * @param {Array<{ value: IStudent; priority: string }>} options - The student filter options.
   */
  const handleFilterEventStudent = (options: { value: IStudent; priority: string }[]) => {
    setFilterStudent(options.map((option) => option.value));
  };

  /**
   * Handles filtering events by customers.
   * @param {Array<{ value: ICustomer; priority: string }>} options - The customer filter options.
   */
  const handleFilterEventCustomer = (options: { value: ICustomer; priority: string }[]) => {
    setFilterCustomer(options.map((option) => option.value));
  };

  /**
   * Handles resetting all filters to their initial state.
   */
  const handleResetFilter = () => {
    setStartDate(new Date((date || new Date()).getFullYear(), (date || new Date()).getMonth(), 1));
    setEndDate(
      new Date((date || new Date()).getFullYear(), (date || new Date()).getMonth() + 1, 1)
    );
    setFilterByPaid(false);
    setFilterEventColor([]);
    setFilterStudent([]);
    setFilterTeacher([]);
    setFilterCustomer([]);
  };

  /**
   * Applies specified filters to the calendar events data.
   * @returns {ICalendarEvent[]} The filtered calendar events.
   */
  const dataFiltered=applyFilter({
    inputData: events,
    filterEventColor,

    filterTeacher,
    filterCustomer,
    filterStudent,
    filterByPaid,
    filterByTrial,
  })
  console.log(dataFiltered);
  return (
    <>
      <Helmet>
        <title> Kalender | TopTutors</title>
      </Helmet>
      <Container maxWidth={themeStretch ? false : 'xl'}>
        <CustomBreadcrumbs
          links={[
            {
              name: 'Oversigt',
              href: PATH_DASHBOARD.root,
            },
            {
              name: 'Kalender',
            },
          ]}
          action={renderCreateLessonButton()}
        />

        <Card>
          <StyledCalendar>
            <CalendarToolbar
              isAdmin={user?.admin}
              date={date}
              view={view}
              onNextDate={handleClickDateNext}
              onPrevDate={handleClickDatePrev}
              onToday={handleClickToday}
              onChangeView={handleChangeView}
              onOpenFilter={() => setOpenFilter(true)}
            />

            <FullCalendar
              weekends
              editable
              droppable
              selectable
              locales={allLocales}
              locale="da"
              firstDay={1}
              rerenderDelay={10}
              eventTimeFormat={{
                hour: '2-digit',
                minute: '2-digit',
                hour12: false,
              }}
              allDayMaintainDuration
              eventResizableFromStart
              ref={calendarRef}
              initialDate={date}
              initialView={view}
              dayMaxEventRows={3}
              eventDisplay="block"
              events={dataFiltered || events}
              headerToolbar={false}
              fixedWeekCount={false}
              initialEvents={events}
              select={handleSelectRange}
              eventDrop={handleDropEvent}
              eventClick={handleSelectEvent}
              eventResize={handleResizeEvent}
              height={isDesktop ? 720 : 'auto'}
              plugins={[
                listPlugin,
                dayGridPlugin,
                timelinePlugin,
                timeGridPlugin,
                interactionPlugin,
                googleCalendarPlugin,
              ]}
              googleCalendarApiKey="<YOUR API KEY>"
            />
          </StyledCalendar>
        </Card>
      </Container>

      {(user?.teacher || user?.admin) && !selectedEventId ? (
        <>
          <Dialog
            fullWidth
            maxWidth="xs"
            open={openForm && !selectedEventId}
            onClose={handleCloseModal}
          >
            <DialogTitle>{selectedEvent ? 'Rediger lektion' : 'Planlæg lektion'}</DialogTitle>
            <CalendarForm
              teachers={teachers}
              students={students}
              admin={user?.admin}
              event={selectedEvent}
              range={selectedRange}
              onCancel={handleCloseModal}
              onCreateUpdateEvent={handleCreateUpdateEvent}
              onDeleteEvent={handleDeleteEvent}
            />
          </Dialog>
        </>
      ) : (
        <></>
      )}
      <Dialog
        fullWidth
        maxWidth="xs"
        open={openViewForm || selectedEventId !== ''}
        onClose={handleCloseModal}
      >
        <DialogTitle>
          <IconButton
            sx={{ position: 'absolute', right: 8, top: 8 }}
            color="error"
            onClick={handleCloseModal}
          >
            <Iconify icon="ic:sharp-close" />
          </IconButton>
        </DialogTitle>

        <ViewLessonForm
          event={getEventForForm()}
          admin={user?.admin}
          teachers={teachers}
          students={students}
          editable={!(user?.teacher || user?.admin)}
          range={selectedRange}
          cancel={cancel}
          onClose={handleCloseModal}
          onCancel={handleCancelModal}
          cancelLesson={cancelLesson}
          onCreateUpdateEvent={handleCreateUpdateEvent}
          onDeleteEvent={handleDeleteEvent}
          colorOptions={COLOR_OPTIONS}
        />
      </Dialog>
      {user?.admin ? (
        <CalendarFilterDrawer
          teachers={teachers}
          students={students}
          customers={customers}
          admin={user?.admin}
          events={events}
          startDate={startDate}
          endDate={endDate}
          setStartDate={(value) => {
            setStartDate(value);
          }}
          setEndDate={(value) => {
            setEndDate(value);
          }}
          openFilter={openFilter}
          colorOptions={COLOR_OPTIONS}
          onResetFilter={handleResetFilter}
          filterEventColor={filterEventColor}
          filterStudents={filterStudent.map((value) => ({ value, priority: '' }))}
          filterTeachers={filterTeacher.map((value) => ({ value, priority: '' }))}
          filterCustomers={filterCustomer.map((value) => ({ value, priority: '' }))}
          onCloseFilter={() => setOpenFilter(false)}
          onFilterEventColor={handleFilterEventColor}
          onFilterEventTeacher={handleFilterEventTeacher}
          onFilterEventStudent={handleFilterEventStudent}
          onFilterEventCustomer={handleFilterEventCustomer}
          onFilterPaidLessons={handleFilterPaidLessons}
          onFilterTrialLessons={handleFilterTrialLessons}
          filterByPaid={filterByPaid}
          filterByTrial={filterByTrial}
          onSelectEvent={(eventId) => {
            if (eventId) {
              console.log(eventId);
              setSelectedEventId(eventId.toString());
              handleOpenModal();
            }
          }}
        />
      ) : (
        <></>
      )}
    </>
  );
}

// ----------------------------------------------------------------------
/**
 * Retrieves events based on the user role (student, teacher, admin, or customer).
 * @returns {ICalendarEvent[]} An array of events with color data.
 */
const useGetEvents = (date: Date | null) => {
  const dispatch = useDispatch();
  const { user } = useAuthContext();
  const { events } = useSelector((state) => state.calendar);

  const getAllEvents = useCallback(() => {
    const start_date = new Date(
      (date || new Date()).getFullYear(),
      (date || new Date()).getMonth(),
      1
    );
    const end_date = new Date(
      (date || new Date()).getFullYear(),
      (date || new Date()).getMonth() + 1,
      1
    );
    const from_date = fDate(start_date, 'yyyy-MM-dd');
    const to_date = fDate(end_date, 'yyyy-MM-dd');
    if (user?.student) {
      dispatch(getEventsStudents(user?.uid,from_date,to_date));
    } else if (user?.teacher) {
      dispatch(getEventsTeacher(user?.uid,from_date,to_date));
    } else if (user?.admin) {
      dispatch(getEventsAdmin(from_date, to_date));
    } else {
      dispatch(getEventsCustomers(user?.uid,from_date,to_date));
    }
  }, [dispatch, user, date]);
  console.log(events);
  useEffect(() => {
    getAllEvents();
  }, [getAllEvents]);
  console.log(events);
  const colorEvents = events.map((event) => ({
    ...event,
    title: `${event.studentName}`,
    title_data: event.title,
    textColor: event.color,
  }));
  
  return colorEvents;
};

// ----------------------------------------------------------------------
/**
 * Retrieves students and teachers based on the user role (student, teacher, or admin).
 * For admin users, it also retrieves customer data.
 * @returns {Object} An object containing teachers, students, and customers arrays.
 */
const useGetStudentsAndTeachers = () => {
  const dispatch = useDispatch();
  const { user } = useAuthContext();
  const { teachers, students, customers } = useSelector((state) => state.calendar);
  const getAllTeachersAndStudents = useCallback(() => {
    if (user?.teacher) {
      dispatch(getStudents(user?.email, 'teacher'));
      dispatch(getTeachers(user?.email, 'teacher'));
    } else if (user?.admin) {
      dispatch(getStudents(user?.email, 'admin'));
      dispatch(getTeachers(user?.email, 'admin'));
      dispatch(getCustomers());
    } else if (user?.customer || user?.student) {
      dispatch(getStudents(user?.email, 'student'));
      dispatch(getTeachers(user?.email, 'student'));
    }
  }, [user, dispatch]);

  useEffect(() => {
    getAllTeachersAndStudents();
  }, [getAllTeachersAndStudents]);
  return { teachers, students, customers };
};
// ----------------------------------------------------------------------
/**
 * Filters the input events based on the provided filter criteria.
 * @param {Object} params - The filter parameters.
 * @param {ICalendarEvent[]} params.inputData - The input events array.
 * @param {string[]} params.filterEventColor - The event color filter.

 * @param {ITutor[]|null} params.filterTeacher - The teacher filter.
 * @param {boolean|null} params.filterByPaid - The paid lessons filter.
 * @param {boolean|null} params.filterByTrial - The trial lessons filter.
 * @param {IStudent[]|null} params.filterStudent - The student filter.
 * @param {ICustomer[]|null} params.filterCustomer - The customer filter.
 * @param {boolean} params.isError - The error flag for invalid date range.
 * @returns {ICalendarEvent[]} The filtered events array.
 */
function applyFilter({
  inputData,
  filterEventColor,
  filterTeacher,
  filterByPaid,
  filterByTrial,
  filterStudent,
  filterCustomer,
}: {
  inputData: ICalendarEvent[];
  filterEventColor: string[];
  filterTeacher: ITutor[] | null;
  filterStudent: IStudent[] | null;
  filterCustomer: ICustomer[] | null;
  filterByPaid: boolean | null;
  filterByTrial: boolean | null;
}) {
  const stabilizedThis = inputData.map((el, index) => [el, index] as const);

  inputData = stabilizedThis.map((el) => el[0]);

  if (filterEventColor.length) {
    inputData = inputData.filter((event: EventInput) =>
      filterEventColor.includes(event.color as string)
    );
  }

  if (filterTeacher?.length) {
    inputData = inputData.filter((event: ICalendarEvent) => {
      const foundTeacher = filterTeacher.find(
        (teacher) => teacher.id.toString() === event.teacherId.code.toString()
      );
      if (foundTeacher) {
        return true;
      }
      return false;
    });
  }
  if (filterStudent?.length) {
    inputData = inputData.filter((event: ICalendarEvent) => {
      const foundStudent = filterStudent.find(
        (student) => student.id.toString() === event.studentId.code.toString()
      );
      if (foundStudent) {
        return true;
      }
      return false;
    });
  }
  if (filterCustomer?.length) {
    inputData = inputData.filter((event: ICalendarEvent) => {
      const foundCustomers = filterCustomer.find((customer) =>
        customer.students.includes(event.studentId.code.toString())
      );
      if (foundCustomers) {
        return true;
      }
      return false;
    });
  }
  if (filterByPaid) {
    inputData = inputData.filter((event: ICalendarEvent) => event.paid);
  }
  if (filterByTrial) {
    inputData = inputData.filter((event: ICalendarEvent) => event.trial_lesson);
  }

  console.log(inputData);
  return inputData;
}
