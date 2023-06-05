import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { IProgramState } from '../../../@types/arrays';

const initialState: IProgramState = {
  loadingProgram: false,
  error: null,
  programmes: [],
  program: null,
};

const slice = createSlice({
  name: 'program',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingProgram = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingProgram = false;
      state.error = action.payload.data;
    },
    // GET ProgramS
    getProgrammesSuccess(state, action) {
      state.loadingProgram = false;
      state.programmes = action.payload.data;
    },
    // GET Program
    getProgramSuccess(state, action) {
      state.loadingProgram = false;
      state.program = action.payload;
      console.log(state.program);
    },
  },
});

export function getPrograms() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/programs');
      dispatch(slice.actions.getProgrammesSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
