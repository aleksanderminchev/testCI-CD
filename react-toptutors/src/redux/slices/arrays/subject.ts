import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { ISubjectState } from '../../../@types/arrays';

const initialState: ISubjectState = {
  loadingSubject: false,
  error: null,
  subjects: [],
  subject: null,
};

const slice = createSlice({
  name: 'subject',
  initialState,
  reducers: {
    // START loadingG
    startLoading(state) {
      state.loadingSubject = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingSubject = false;
      state.error = action.payload.data;
    },
    // GET subjectS
    getSubjectsSuccess(state, action) {
      state.loadingSubject = false;
      state.subjects = action.payload.data;
    },
    // GET Tutor
    getSubjectSuccess(state, action) {
      state.loadingSubject = false;
      state.subject = action.payload;
      console.log(state.subject);
    },
  },
});

export function getSubjects() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/subjectss');
      dispatch(slice.actions.getSubjectsSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
