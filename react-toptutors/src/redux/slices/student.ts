import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';

import { IStudentState, IStudent } from '../../@types/student';

const initialState: IStudentState = {
  isLoading: false,
  error: null,
  students: [],
  student: null,
};

const slice = createSlice({
  name: 'student',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.isLoading = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.isLoading = false;

      state.error = action.payload; // if you only write action.payload, you do not dot-in to the actual data, where all data for student is
    },
    // GET Students
    getStudentsSuccess(state, action) {
      state.isLoading = false;
      state.students = action.payload.data;
    },
    // GET Student
    getStudentSuccess(state, action) {
      state.isLoading = false;
      state.student = action.payload.data;
    },
    // DELETE Student
    deleteStudentSuccess(state, action) {
      state.isLoading = false;
      state.student = null;
    },
  },
});

export default slice.reducer;

export function getStudents(status: string | undefined) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/students?status=${status}`);
      dispatch(slice.actions.getStudentsSuccess(response.data));
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
export function getStudentsTeacher(email: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/get_all_students/${email}`);
      dispatch(slice.actions.getStudentsSuccess(response));
      console.log(response);
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
 * This method assigns students to tutors
 * @param studentId Array of student Ids to assign to student
 * @param student_email Teacher Email
 * @returns the newly assigned students
 */
export function assignStudents(studentId: number[], teacher_email: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log(studentId);
    console.log(teacher_email);
    try {
      const response = await axios.post(
        'https://localhost:8081/api/take_students',
        {
          student_id: studentId,
          teacher_email: teacher_email,
        },
        { withCredentials: true }
      );
      console.log(response);
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

export function getStudent(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/students/${id}`);
      if (response.status === 404) {
        throw new Error('Student not found');
      } else {
        dispatch(slice.actions.getStudentSuccess(response));
        console.log(response.data);
      }
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

export function createStudent(student: IStudent) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      if (student?.phone) {
        const response = await axios.post(
          `https://localhost:8081/api/student_with_user`,
          {
            ...student,
          },
          { withCredentials: true }
        );
        if (response.status === 404) {
          throw new Error('Student not found');
        } else {
          dispatch(slice.actions.getStudentSuccess(response));
          console.log(response.data);
        }
      } else {
        const objectForRequest = {
          id: student.id,
          first_name: student.first_name,
          last_name: student.last_name,
          gender: student.gender,
          email: student.email,
        };
        const response = await axios.post(
          'https://localhost:8081/api/student',
          {
            ...objectForRequest,
          },
          { withCredentials: true }
        );
      }
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
export function deleteStudent(id: string | undefined) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.delete(`https://localhost:8081/api/student/${id}`);

      if (response.status === 404) {
        throw new Error('Student not found');
      } else {
        dispatch(slice.actions.deleteStudentSuccess({}));
      }
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

export function editStudent(form: Partial<IStudent>) {
  const data_to_update_user = {
    id: form.id,
    email: form.email,
    first_name: form.first_name,
    last_name: form.last_name,
    phone: form.phone,
    email_lesson_reminder: form.email_lesson_reminders,
    email_lesson_notes: form.email_lesson_notes,
  };

  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.put(`https://localhost:8081/api/student`, {
        ...data_to_update_user,
      });
      console.log(response);
      dispatch(slice.actions.getStudentSuccess(response));
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
