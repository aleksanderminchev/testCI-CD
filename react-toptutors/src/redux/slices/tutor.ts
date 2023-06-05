import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';
import { RootState } from '../../redux/store'; // import RootState from the store
import { PutObjectCommand, S3Client } from '@aws-sdk/client-s3';
import { ITutorState } from '../../@types/tutor';
import { ITutor } from '../../@types/tutor';

const initialState: ITutorState = {
  isLoading: false,
  error: null,
  tutors: [],
  tutor: null,
};

const slice = createSlice({
  name: 'tutor',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.isLoading = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.isLoading = false;
      state.error = action.payload;
    },
    // GET TutorS
    getTutorsSuccess(state, action) {
      state.isLoading = false;
      state.tutors = action.payload.data;
      state.error = null;
    },
    // GET Tutor
    getTutorSuccess(state, action) {
      state.isLoading = false;
      state.tutor = action.payload;
      state.error = null;
    },
    uploadTutorProfileImageSuccess(state) {
      state.isLoading = false;
    },
  },
});

export default slice.reducer;

export const selectTutor = (state: RootState) => state.tutor.tutor;

export function getTutors(status: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/teachers?status=${status}`);
      dispatch(slice.actions.getTutorsSuccess(response.data));
      console.log(response.data);
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
export function getTutorsCustomer(email: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/get_all_teachers/${email}`);
      dispatch(slice.actions.getTutorsSuccess(response));
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
 * This method assigns tutors to students
 * @param teacherId Array of teacher Ids to assign to student
 * @param student_email Student Email
 * @returns the newly assigned teachers
 */
export function assignTeachers(teacherId: number[], student_email: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log(teacherId);
    console.log(student_email);
    try {
      const response = await axios.post(
        'https://localhost:8081/api/take_teachers',
        {
          teacher_id: teacherId,
          student_email: student_email,
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
export function getTutor(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      console.log('from axious', id);
      const response = await axios.get(`https://localhost:8081/api/teachers/${id}`, {
        withCredentials: true,
      });
      dispatch(slice.actions.getTutorSuccess(response.data));
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
      return false;
    }
  };
}

export function editTutor(form: Partial<ITutor>) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading);
    try {
      console.log(form);
      const response = await axios.put(
        'https://localhost:8081/api/teacher',
        {
          ...form,
        },
        { withCredentials: true }
      );
      dispatch(slice.actions.getTutorSuccess(response.data));
      console.log(response);
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
export function uploadTutorProfileImage(file: File, fileName: string, fileType: string) {
  return async (dispatch: Dispatch) => {
    try {
      // Step 2: The s3Client function validates your request and directs it to your Space's specified endpoint using the AWS SDK.
      if (file) {
        const s3Client = new S3Client({
          endpoint: 'https://ams3.digitaloceanspaces.com', // Find your endpoint in the control panel, under Settings. Prepend "https://".
          forcePathStyle: false, // Configures to use subdomain/virtual calling format.
          region: 'ams3', // Must be "us-east-1" when creating new Spaces. Otherwise, use the region in your endpoint (e.g. nyc3).
          credentials: {
            accessKeyId: process.env.REACT_APP_SPACE_KEY_ID || '', // Access key pair. You can create access key pairs using the control panel or API.
            secretAccessKey: process.env.REACT_APP_SPACES_SECRET || '', // Secret access key defined through an environment variable.
          },
        });
        const command = new PutObjectCommand({
          Bucket: 'tt-portal',
          Key: `tutor-images/${fileName}`,
          Body: file,
          ContentType: fileType,
          ACL: 'public-read-write',
        });
        const response = await s3Client.send(command);
        console.log(response);
        dispatch(slice.actions.uploadTutorProfileImageSuccess());
        return `https://tt-portal.ams3.cdn.digitaloceanspaces.com/tutor-images/${fileName}`;
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
      return '';
    }
  };
}
export function createTutor(tutor: ITutor, subjects_create: string[], programs_create: string[]) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    const age =
      (new Date().getTime() - new Date(tutor?.birthday).getTime()) / (1000 * 60 * 60 * 24);
    console.log(`${new Date(tutor?.birthday).toISOString()}Z`);
    const tutorForSend = {
      ...tutor,
      subjects_create: subjects_create,
      programs_create: programs_create,
      photo: '',
      status: 'prospective',
      finished_highschool: true,
      age: Math.abs(Math.round(age / 365.25)),
      birthday: new Date(tutor?.birthday).toISOString(),
    };
    console.log(tutor);
    console.log(tutorForSend);
    try {
      const response = await axios.post(`https://localhost:8081/api/teachers`, tutorForSend, { withCredentials: true });
      if (response.status === 404) {
        throw new Error('Tutor not found');
      } else {
        dispatch(slice.actions.getTutorSuccess(response));
        console.log(response);
        return true;
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
      return false;
    }
  };
}
