import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { IHigher_education_institutionState } from '../../../@types/arrays';

const initialState: IHigher_education_institutionState = {
  loadingHigher_education_institution: false,
  error: null,
  higher_education_institutions: [],
  higher_education_institution: null,
};

const slice = createSlice({
  name: 'higher_education_institution',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingHigher_education_institution = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingHigher_education_institution = false;
      state.error = action.payload.data;
    },
    // GET higher_education_institutionS
    getHigher_education_institutionsSuccess(state, action) {
      state.loadingHigher_education_institution = false;
      state.higher_education_institutions = action.payload.data;
    },
    // GET higher_education_institution
    getHigher_education_institutionSuccess(state, action) {
      state.loadingHigher_education_institution = false;
      state.higher_education_institutions = action.payload;
      console.log(state.higher_education_institutions);
    },
  },
});

export function getHigher_education_institutions() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/get_all_institutions');
      dispatch(slice.actions.getHigher_education_institutionsSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
