import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { IHigher_education_programState } from '../../../@types/arrays';

const initialState: IHigher_education_programState = {
  loadingHigher_education_program: false,
  error: null,
  higher_education_programmes: [],
  higher_education_program: null,
};

const slice = createSlice({
  name: 'higher_education_program',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingHigher_education_program = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingHigher_education_program = false;
      state.error = action.payload.data;
    },
    // GET higher_education_programS
    getHigher_education_programmesSuccess(state, action) {
      state.loadingHigher_education_program = false;
      state.higher_education_programmes = action.payload.data;
    },
    // GET Tutor
    getHigher_education_programSuccess(state, action) {
      state.loadingHigher_education_program = false;
      state.higher_education_programmes = action.payload;
      console.log(state.higher_education_programmes);
    },
  },
});

export function getHigher_education_programs() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/get_all_programmes');
      dispatch(slice.actions.getHigher_education_programmesSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
