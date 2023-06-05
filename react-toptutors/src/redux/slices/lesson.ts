import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';

import { ILessonState, ILesson } from '../../@types/lesson';

const initialState: ILessonState = {
  isLoading: false,
  error: null,
  lessons: [],
  lesson: null,
  recording: null,
};
const slice = createSlice({
  name: 'lesson',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.isLoading = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.isLoading = false;
      state.error = action.payload; // if you only write action.payload, you do not dot-in to the actual data, where all data for lesson is
    }, // GET Lesosns
    getLessonSuccess(state, action) {
      state.isLoading = false;
      state.lesson = action.payload;
    },
    getLessonsSuccess(state, action) {
      state.isLoading = false;
      state.lessons = action.payload;
    },
    getLessonRecodingsSuccess(state, action) {
      state.isLoading = false;
      state.recording = action.payload;
    },
  },
});

export default slice.reducer;

export function getLesson(id: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8080/api/lesson/${id}`);
      console.log(response.data);
      if (response.status === 404) {
        throw new Error('Lesson not found');
      } else {
        dispatch(slice.actions.getLessonSuccess(response.data));
        console.log(slice);
      }
    } catch (error) {
      console.error(error);
      dispatch(slice.actions.hasError(error));
    }
  };
}

export function getLessons() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8080/api/lesson`);
      console.log(response);
      if (response.status === 404) {
        throw new Error('Lesson not found');
      } else {
        dispatch(slice.actions.getLessonsSuccess(response.data.data));
        console.log(slice);
      }
    } catch (error) {
      console.error(error);
      dispatch(slice.actions.hasError(error));
    }
  };
}
/**
 *
 * @param id  Id of the user account of the student
 * @param start_date Lessons between this date, this is the first date
 * @param end_date Lessons between this date, this is the last date
 * @returns array of lessons and assings them to the state
 */
export function getLessonsForStudent(
  id: string | number,
  start_date: string | undefined,
  end_date: string | undefined
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log('herer si the id for lessonsForStudent', id);
    const url =
      start_date && end_date
        ? `https://localhost:8080/api/lessons-student/${id}?start_date=${start_date}&end_date=${end_date}`
        : `https://localhost:8080/api/lessons-student/${id}`;
    try {
      const response = await axios.get(url, {
        withCredentials: true,
      });
      console.log(response);
      const configuredTimeArray = response.data.data.map((lesson: ILesson) => {
        return {
          ...lesson,
          from_time: new Date(`${lesson.from_time.toString()}Z`),
          to_time: new Date(`${lesson.to_time.toString()}Z`),
        };
      });
      dispatch(slice.actions.getLessonsSuccess(configuredTimeArray));
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
 *
 * @param id  Id of the user account of the student
 * @param start_date Lessons between this date, this is the first date
 * @param end_date Lessons between this date, this is the last date
 * @returns array of lessons and assings them to the state
 */
export function getLessonsForCustomer(
  id: string | number,
  start_date: string | undefined,
  end_date: string | undefined
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log('herer si the id for lessonsForStudent', id);
    const url =
      start_date && end_date
        ? `https://localhost:8080/api/lessons-customer/${id}?start_date=${start_date}&end_date=${end_date}`
        : `https://localhost:8080/api/lessons-customer/${id}`;
    try {
      const response = await axios.get(url, { withCredentials: true });
      console.log(response);
      const configuredTimeArray = response.data.data.map((lesson: ILesson) => {
        return {
          ...lesson,
          from_time: new Date(`${lesson.from_time.toString()}Z`),
          to_time: new Date(`${lesson.to_time.toString()}Z`),
        };
      });
      dispatch(slice.actions.getLessonsSuccess(configuredTimeArray));
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
 *
 * @param id  Id of the user account of the student
 * @param start_date Lessons between this date, this is the first date
 * @param end_date Lessons between this date, this is the last date
 * @returns array of lessons and assings them to the state
 */
export function getLessonsForTeacher(
  id: string | number,
  start_date: string | undefined,
  end_date: string | undefined
) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log('herer si the id for lessonsForStudent', id);
    const url =
      start_date && end_date
        ? `https://localhost:8080/api/lessons-teacher/${id}?start_date=${start_date}&end_date=${end_date}`
        : `https://localhost:8080/api/lessons-teacher/${id}`;
    try {
      const response = await axios.get(url, { withCredentials: true });
      console.log(response);
      const configuredTimeArray = response.data.data.map((lesson: ILesson) => {
        return {
          ...lesson,
          from_time: new Date(`${lesson.from_time.toString()}Z`),
          to_time: new Date(`${lesson.to_time.toString()}Z`),
        };
      });
      dispatch(slice.actions.getLessonsSuccess(configuredTimeArray));
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
export function getLessonRecordings(id: number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log(id);
    try {
      const response = await axios.get(`https://localhost:8080/api/lesson_replay/${id}`, { withCredentials: true });
      console.log(response.data);
      if (response.status === 404) {
        throw new Error('Lesson not found');
      } else {
        dispatch(slice.actions.getLessonRecodingsSuccess(response.data));
        console.log(slice);
      }
    } catch (error) {
      console.error(error);
      dispatch(slice.actions.hasError(error));
    }
  };
}
