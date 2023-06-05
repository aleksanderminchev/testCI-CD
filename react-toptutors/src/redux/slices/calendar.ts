import { createSlice, Dispatch } from '@reduxjs/toolkit';
// utils
import axios from '../../utils/axios';

// @types
import { ICalendarState, ICalendarEvent } from '../../@types/calendar';
import { ILesson } from '../../@types/lesson';

// ----------------------------------------------------------------------

const initialState: ICalendarState = {
  isLoading: false,
  error: null,
  events: [],
  teachers: [],
  students: [],
  customers: [],
};

const slice = createSlice({
  name: 'calendar',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.isLoading = true;
      state.error = null;
    },

    // HAS ERROR
    hasError(state, action) {
      state.isLoading = false;
      state.error = action.payload;
    },
    // GET STUDENTS
    getStudentsSuccess(state, action) {
      state.isLoading = false;
      state.students = action.payload;
    },
    // GET TEACHERS
    getTeachersSuccess(state, action) {
      state.isLoading = false;
      state.teachers = action.payload;
    },
    // GET Customers
    getCustomersSuccess(state, action) {
      state.isLoading = false;
      state.customers = action.payload;
    },
    // GET EVENTS
    getEventsSuccess(state, action) {
      state.isLoading = false;
      state.events = action.payload;
    },

    // CREATE EVENT
    createEventSuccess(state, action) {
      const newEvent = action.payload;
      state.isLoading = false;
      state.events = [...state.events, newEvent];
      state.error = null;
    },

    // UPDATE EVENT
    updateEventSuccess(state, action) {
      state.isLoading = false;
      state.error = null;
      state.events = state.events.map((event) => {
        if (event.id === action.payload.id) {
          return action.payload;
        }
        return event;
      });
    },

    // DELETE EVENT
    deleteEventSuccess(state, action) {
      state.isLoading = false;
      state.events = state.events.filter((event) => event.id !== action.payload);
    },
  },
});

// Reducer
export default slice.reducer;

// ----------------------------------------------------------------------

/**
 * Retrieves events for a specific student and dispatches the result to the store.
 * @param {number} studentId - The ID of the student whose events need to be fetched.
 * @returns {Function} An async Redux thunk action.
 *
 * This function fetches the lessons for a specific student, maps the response to a desired format,
 * and dispatches the result to the Redux store. It also handles errors and dispatches error messages.
 */
export function getEventsStudents(
  studentId: number,
  from_date: string | undefined,
  to_date: string | undefined
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(
        `https://localhost:8080/api/lessons-student/${studentId}?from_date=${from_date}&to_date=${to_date}`,
        {
          headers: { Authorization: `Bearer ${localStorage.getItem('accessToken')}` },
          withCredentials: true,
        }
      );
      const eventsForReturn = response.data.data.map((lesson: ILesson) => {
        let colorForReturn = '';
        if (lesson.status === 'attended') {
          colorForReturn = '#00AB55';
        } else if (lesson.status === 'scheduled') {
          colorForReturn = '#FFC107';
        } else {
          colorForReturn = '#FF4842';
        }
        return {
          title: lesson.title,
          id: lesson.id,
          start: new Date(`${lesson.from_time.toString()}Z`),
          end: new Date(`${lesson.to_time.toString()}Z`),
          color: colorForReturn,
          completionNotes: lesson.completion_notes,
          paid: lesson.paid,
          studentId: {
            code: lesson.student.id,
            label: `${lesson.student.first_name} ${lesson.student.last_name}`,
          },
          studentName: `${lesson.student.first_name} ${lesson.student.last_name}`,
          trial_lesson: lesson.trial_lesson,
          teacherName: `${lesson.teacher.first_name} ${lesson.teacher.last_name}`,
          teacherId: {
            code: lesson.teacher.id,
            label: `${lesson.teacher.first_name} ${lesson.teacher.last_name}`,
          },
          description: lesson.description,
          status: lesson.status,
        };
      });
      dispatch(slice.actions.getEventsSuccess(eventsForReturn));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}
/**
 * Retrieves events for a specific teacher and dispatches the result to the store.
 * @param {number} teacherId - The ID of the teacher whose events need to be fetched.
 * @returns {Function} An async Redux thunk action.
 *
 * This function fetches the lessons for a specific teacher, maps the response to a desired format,
 * and dispatches the result to the Redux store. It also handles errors and dispatches error messages.
 */
export function getEventsTeacher(
  teacherId: number,
  from_date: string | undefined,
  to_date: string | undefined
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(
        `https://localhost:8080/api/lessons-teacher/${teacherId}?from_date=${from_date}&to_date=${to_date}`,
        {
          withCredentials: true,
        }
      );
      console.log(response);
      const eventsForReturn = response.data.data.map((lesson: ILesson) => {
        let colorForReturn = '';
        if (lesson.status === 'attended') {
          colorForReturn = '#00AB55';
        } else if (lesson.status === 'scheduled') {
          colorForReturn = '#FFC107';
        } else {
          colorForReturn = '#FF4842';
        }
        return {
          title: lesson.title,
          id: lesson.id,
          start: new Date(`${lesson.from_time.toString()}Z`),
          end: new Date(`${lesson.to_time.toString()}Z`),
          color: colorForReturn,
          completionNotes: lesson.completion_notes,
          paid: lesson.paid,
          studentId: {
            code: lesson.student.id,
            label: `${lesson.student.first_name} ${lesson.student.last_name}`,
          },
          studentName: `${lesson.student.first_name} ${lesson.student.last_name}`,
          trial_lesson: lesson.trial_lesson,
          teacherName: `${lesson.teacher.first_name} ${lesson.teacher.last_name}`,
          teacherId: {
            code: lesson.teacher.id,
            label: `${lesson.teacher.first_name} ${lesson.teacher.last_name}`,
          },
          description: lesson.description,
          status: lesson.status,
        };
      });
      dispatch(slice.actions.getEventsSuccess(eventsForReturn));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}

/**
 * Retrieves all events for admin users and dispatches the result to the store.
 * @returns {Function} An async Redux thunk action.
 *
 * This function fetches all lessons for admin users, maps the response to a desired format,
 * and dispatches the result to the Redux store. It also handles errors and dispatches error messages.
 */
export function getEventsAdmin(from_date: string | undefined, to_date: string | undefined) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(
        `https://localhost:8080/api/lessons-admin?from_date=${from_date}&to_date=${to_date}`,
        {
          withCredentials: true,
        }
      );
      const eventsForReturn = response.data.data.map((lesson: ILesson) => {
        return {
          ...lesson,
          start: new Date(`${lesson.from_time.toString()}Z`),
          end: new Date(`${lesson.to_time.toString()}Z`),
        };
      });
      dispatch(slice.actions.getEventsSuccess(eventsForReturn));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}

/**
 * Fetches events for customers with the given customerId.
 *
 * @param {number} customerId - The ID of the customer.
 * @returns {Function} A Redux Thunk action creator.
 */
export function getEventsCustomers(
  customerId: number,
  from_date: string | undefined,
  to_date: string | undefined
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(
        `https://localhost:8080/api/lessons-customer/${customerId}?from_date=${from_date}&to_date=${to_date}`,
        {
          withCredentials: true,
        }
      );
      const eventsForReturn = response.data.data.map((lesson: ILesson) => {
        let colorForReturn = '';
        if (lesson.status === 'attended') {
          colorForReturn = '#00AB55';
        } else if (lesson.status === 'scheduled') {
          colorForReturn = '#FFC107';
        } else {
          colorForReturn = '#FF4842';
        }
        return {
          title: lesson.title,
          id: lesson.id,
          start: new Date(`${lesson.from_time.toString()}Z`),
          end: new Date(`${lesson.to_time.toString()}Z`),
          color: colorForReturn,
          completionNotes: lesson.completion_notes,
          description: lesson.description,
          trial_lesson: lesson.trial_lesson,
          paid: lesson.paid,
          studentName: `${lesson.student.first_name} ${lesson.student.last_name}`,
          teacherName: `${lesson.teacher.first_name} ${lesson.teacher.last_name}`,
          studentId: {
            code: lesson.student.id,
            label: `${lesson.student.first_name} ${lesson.student.last_name}`,
          },
          teacherId: {
            code: lesson.teacher.id,
            label: `${lesson.teacher.first_name} ${lesson.teacher.last_name}`,
          },
          status: lesson.status,
        };
      });
      dispatch(slice.actions.getEventsSuccess(eventsForReturn));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}
// ----------------------------------------------------------------------
/**
 * Creates a new calendar event with the given details.
 *
 * @param {ICalendarEvent} newEvent - The details of the new event to create.
 * @returns {Function} A Redux Thunk action creator.
 */
export function createEvent(newEvent: ICalendarEvent) {
  return async (dispatch: Dispatch) => {
    try {
      dispatch(slice.actions.startLoading());

      const idTeacher = newEvent.teacherId.code;
      const idStudent = newEvent.studentId.code;

      // Boolean if Trial Lesson or not
      const trial = newEvent.trial_lesson;

      // Payload to create the Lesson
      const objectForRequest = {
        title: newEvent.title_data,
        description: newEvent.description,
        to_time: newEvent.end,
        from_time: newEvent.start,
        trial_lesson: trial,
        teacher_id: parseInt(idTeacher, 10),
        student_id: parseInt(idStudent, 10),
      };

      // Error validation before making the request.
      const today = new Date();
      const monthMiddle = new Date(today.getFullYear(), today.getMonth(), 15, 23, 59, 59);
      const checkAgeStart = new Date(newEvent?.start?.toString() || new Date());
      const checkAgeEnd = new Date(newEvent?.end?.toString() || new Date());

      // If the lesson is older than 7 days or in previous wage period then throw error.
      if ((new Date().getTime() - checkAgeEnd.getTime()) / (60 * 60 * 24 * 1000) > 7) {
        throw Error('Lesson is older than 7 days');
      } else if (checkAgeStart.getTime() <= monthMiddle.getTime() && today.getDate() > 15) {
        throw Error('Lesson cannot be in the previous wage month');
      }
      // Throw error if lesson is longer than 10 hours.
      if ((checkAgeEnd.getTime() - checkAgeStart.getTime()) / (60 * 60 * 1000) > 10) {
        throw Error('Lesson is 10 hours or more');
      }

      // Making the request to create the Lesson
      const response = await axios.post('https://localhost:8080/api/lesson', objectForRequest, { withCredentials: true });

      // dispatching the response.
      dispatch(
        slice.actions.createEventSuccess({
          title: response.data.title,
          id: response.data.id,
          start: new Date(`${response.data.from_time.toString()}Z`),
          end: new Date(`${response.data.to_time.toString()}Z`),
          description: response.data.description,
          paid: false,
          studentName: `${response.data.student.first_name} ${response.data.student.last_name}`,
          teacherName: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          completionNotes: response.data.completion_notes,
          status: response.data.status,
          trial_lesson: response.data.trial_lesson,
          teacherId: {
            code: response.data.teacher.id,
            label: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          },
          studentId: {
            code: response.data.student.id,
            label: `${response.data.student.first_name} ${response.data.student.last_name}`,
          },
          color: '#FFC107',
        })
      );
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}

/**
 * Fetches all students based on the user type and email.
 *
 * @param {string} email - The email of the user requesting the data.
 * @param {string} userType - The type of the user requesting the data ('teacher', 'admin', 'student', or 'customer').
 * @returns {Function} A Redux Thunk action creator.
 */
export function getStudents(email: string, userType: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      if (userType === 'teacher') {
        const response = await axios.get(`https://localhost:8081/api/get_all_students/${email}`, {
          withCredentials: true,
        });
        dispatch(slice.actions.getStudentsSuccess(response.data));
      } else if (userType === 'admin') {
        const response = await axios.get(`https://localhost:8081/api/students?status=active`, { withCredentials: true });
        dispatch(slice.actions.getStudentsSuccess(response.data.data));
      } else if (userType === 'student' || userType === 'customer') {
        const response = await axios.get(`https://localhost:8081/api/students/${email}`, { withCredentials: true });
        dispatch(slice.actions.getStudentsSuccess(response.data));
      }
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
    }
  };
}

/**
 * Fetches all teachers based on the user type and email.
 *
 * @param {string} email - The email of the user requesting the data.
 * @param {string} userType - The type of the user requesting the data ('teacher', 'admin', 'student', or 'customer').
 * @returns {Function} A Redux Thunk action creator.
 */
export function getTeachers(email: string, userType: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      if (userType === 'teacher') {
        const response = await axios.get(`https://localhost:8081/api/teachers/${email}`, { withCredentials: true });
        dispatch(slice.actions.getTeachersSuccess([response.data]));
      } else if (userType === 'admin') {
        const response = await axios.get('https://localhost:8081/api/teachers-calendar?filter_status=active', {
          withCredentials: true,
        });
        dispatch(slice.actions.getTeachersSuccess(response.data.data));
      } else if (userType === 'student' || userType === 'customer') {
        const response = await axios.get(`https://localhost:8081/api/get_all_teachers/${email}`, {
          withCredentials: true,
        });
        dispatch(slice.actions.getTeachersSuccess(response.data));
      }
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
    }
  };
}
// ----------------------------------------------------------------------

/**
 * Fetches all customers.
 *
 * @returns {Function} A Redux Thunk action creator.
 */
export function getCustomers() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/customers`, { withCredentials: true });
      dispatch(slice.actions.getCustomersSuccess(response.data.data));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
    }
  };
}
// ----------------------------------------------------------------------
/**
 * This function updates the event object with the given parameters.
 *
 * @function updateEvent
 * @param {string} eventId - The ID of the event to be updated.
 * @param {Partial<{
 *    description: string | null;
 *    completionNotes: string | null;
 *    title: string | null;
 *    title_data: string | null;
 *    paid: boolean | null;
 *    trial_lesson: boolean | null;
 *    start: Date | string | number | null;
 *    end: Date | string | number | null;
 *  }>} event - The event object with properties to be updated.
 * @returns {Function} An async function to be dispatched.
 */
export function updateEvent(
  eventId: string,
  event: Partial<{
    description: string | null;
    completionNotes: string | null;
    title: string | null;
    title_data: string | null;
    paid: boolean | null;
    trial_lesson: boolean | null;
    start: Date | string | number | null;
    end: Date | string | number | null;
  }>
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const today = new Date();
      const monthMiddle = new Date(today.getFullYear(), today.getMonth(), 15, 23, 59, 59);
      const checkAgeEnd = new Date(event?.end?.toString() || new Date());
      const checkAgeStart = new Date(event?.start?.toString() || new Date());
      if ((new Date().getTime() - checkAgeEnd.getTime()) / (60 * 60 * 24 * 1000) > 7) {
        throw Error('Lesson is older than 7 days');
      } else if (event.paid) {
        throw Error('Paid lesson cannot be edited');
      } else if (checkAgeStart.getTime() <= monthMiddle.getTime() && today.getDate() > 15) {
        throw Error('Lesson cannot be in the previous wage month');
      } else if ((checkAgeEnd.getTime() - checkAgeStart.getTime()) / (60 * 60 * 1000) > 10) {
        throw Error('Lesson cannot be more than 10 hours');
      }
      console.log((checkAgeEnd.getTime() - checkAgeStart.getTime()) / (60 * 1000));
      console.log(event);
      const updateObject = {
        from_time: event.start,
        to_time: event.end,
        completion_notes: event.completionNotes || '',
        description: event.description,
        title: event.title_data,
        trial_lesson: event.trial_lesson,
      };
      console.log(updateObject);
      const response = await axios.put(
        'https://localhost:8080/api/update_lessons',
        {
          id: parseInt(eventId, 10),
          ...updateObject,
        },
        { withCredentials: true }
      );
      console.log(updateObject);
      console.log(event.start);
      console.log(event.end);
      if (response.data.status === 'scheduled') {
        const rescheduleResponse = await axios.put(
          'https://localhost:8080/api/reschedule_lesson',
          {
            id: parseInt(eventId, 10),
            from_time: event.start,
            to_time: event.end,
          },
          { withCredentials: true }
        );
      }
      console.log(response);
      let colorForReturn = '';
      if (response.data.status === 'attended') {
        colorForReturn = '#00AB55';
      } else if (response.data.status === 'scheduled') {
        colorForReturn = '#FFC107';
      } else {
        colorForReturn = '#FF4842';
      }
      dispatch(
        slice.actions.updateEventSuccess({
          title: response.data.title,
          id: response.data.id,
          start: new Date(`${response.data.from_time.toString()}Z`),
          end: new Date(`${response.data.to_time.toString()}Z`),
          description: response.data.description,
          completionNotes: response.data.completion_notes,
          trial_lesson: response.data.trial_lesson,
          status: response.data.status,
          paid: response.data.paid,
          studentName: `${response.data.student.first_name} ${response.data.student.last_name}`,
          teacherName: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          teacherId: {
            code: response.data.teacher.id,
            label: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          },
          studentId: {
            code: response.data.student.id,
            label: `${response.data.student.first_name} ${response.data.student.last_name}`,
          },
          color: colorForReturn,
        })
      );
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}

// ----------------------------------------------------------------------
/**
 * This function deletes an event with the given eventId.
 *
 * @function deleteEvent
 * @param {string} eventId - The ID of the event to be deleted.
 * @returns {Function} An async function to be dispatched.
 */
export function deleteEvent(eventId: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.delete(`https://localhost:8080/api/lesson/${eventId}`, { withCredentials: true });
      console.log(response.data);
      dispatch(slice.actions.deleteEventSuccess(parseInt(eventId, 10)));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}

/**
 * This function completes a lesson with the given eventId and completion notes.
 *
 * @function completeLesson
 * @param {number} eventId - The ID of the lesson to be completed.
 * @param {string} completionNotes - The notes for the completed lesson.
 * @returns {Function} An async function to be dispatched.
 */
export function completeLesson(eventId: number, completionNotes: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.put(
        `https://localhost:8080/api/complete_lessons`,
        {
          id: eventId,
          status: 'attended',
          completion_notes: completionNotes,
        },
        { withCredentials: true }
      );
      dispatch(
        slice.actions.updateEventSuccess({
          title: response.data.title,
          id: response.data.id,
          start: new Date(`${response.data.from_time.toString()}Z`),
          end: new Date(`${response.data.to_time.toString()}Z`),
          description: response.data.description,
          paid: response.data.paid,
          completionNotes: response.data.completion_notes,
          status: response.data.status,
          trial_lesson: response.data.trial_lesson,
          studentName: `${response.data.student.first_name} ${response.data.student.last_name}`,
          teacherName: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          teacherId: {
            code: response.data.teacher.id,
            label: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          },
          studentId: {
            code: response.data.student.id,
            label: `${response.data.student.first_name} ${response.data.student.last_name}`,
          },
          color: '#00AB55',
        })
      );
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}

/**
 * This function cancels a lesson with the given eventId and reason.
 *
 * @function cancellationLesson
 * @param {string} eventId - The ID of the lesson to be cancelled.
 * @param {string} reason - The reason for the cancellation of the lesson.
 * @returns {Function} An async function to be dispatched.
 */
export function cancellationLesson(eventId: string, reason: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.put(
        `https://localhost:8080/api/cancel_lesson`,
        {
          lesson_id: eventId,
          cancellation_reason: reason,
        },
        { withCredentials: true }
      );

      dispatch(
        slice.actions.updateEventSuccess({
          title: response.data.title,
          id: response.data.id,
          start: new Date(`${response.data.from_time.toString()}Z`),
          end: new Date(`${response.data.to_time.toString()}Z`),
          description: response.data.description,
          completionNotes: response.data.completion_notes,
          studentName: `${response.data.student.first_name} ${response.data.student.last_name}`,
          teacherName: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          paid: response.data.paid,
          status: response.data.status,
          trial_lesson: response.data.trial_lesson,
          teacherId: {
            code: response.data.teacher.id,
            label: `${response.data.teacher.first_name} ${response.data.teacher.last_name}`,
          },
          studentId: {
            code: response.data.student.id,
            label: `${response.data.student.first_name} ${response.data.student.last_name}`,
          },
          color: '#FF4842',
        })
      );
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      dispatch(slice.actions.hasError(errorMessage));
      return false;
    }
  };
}
