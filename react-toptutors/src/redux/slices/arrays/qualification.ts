import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { IQualificationState } from '../../../@types/arrays';

const initialState: IQualificationState = {
  loadingQualification: false,
  error: null,
  qualifications: [],
  qualification: null,
};

const slice = createSlice({
  name: 'qualification',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingQualification = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingQualification = false;
      state.error = action.payload.data;
    },
    // GET QualificationS
    getQualificationsSuccess(state, action) {
      state.loadingQualification = false;
      state.qualifications = action.payload.data;
    },
    // GET Tutor
    getQualificationSuccess(state, action) {
      state.loadingQualification = false;
      state.qualification = action.payload;
      console.log(state.qualification);
    },
  },
});

export function getQualifications() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/qualifications');
      dispatch(slice.actions.getQualificationsSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
