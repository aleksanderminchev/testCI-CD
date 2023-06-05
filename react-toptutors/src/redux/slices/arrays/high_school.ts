import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { IHigh_schoolState } from '../../../@types/arrays';

const initialState: IHigh_schoolState = {
  loadingHigh_school: false,
  error: null,
  high_schools: [],
  high_school: null,
};

const slice = createSlice({
  name: 'high_school',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingHigh_school = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingHigh_school = false;
      state.error = action.payload.data.data;
    },
    // GET high_schoolS
    getHigh_schoolsSuccess(state, action) {
      state.loadingHigh_school = false;
      state.high_schools = action.payload.data;
    },
    // GET Tutor
    getHigh_schoolSuccess(state, action) {
      state.loadingHigh_school = false;
      state.high_school = action.payload;
      console.log(state.high_school);
    },
  },
});

export function getHigh_schools() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/get_all_highschools');
      dispatch(slice.actions.getHigh_schoolsSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
