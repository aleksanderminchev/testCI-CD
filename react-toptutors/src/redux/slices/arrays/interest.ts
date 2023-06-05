import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { IInterestState } from '../../../@types/arrays';

const initialState: IInterestState = {
  loadingInterest: false,
  error: null,
  interests: [],
  interest: null,
};

const slice = createSlice({
  name: 'language',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingInterest = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingInterest = false;
      state.error = action.payload.data;
    },
    // GET interestS
    getInterestsSuccess(state, action) {
      state.loadingInterest = false;
      state.interests = action.payload.data;
    },
    // GET Interest
    getInterestSuccess(state, action) {
      state.loadingInterest = false;
      state.interest = action.payload;
      console.log(state.interest);
    },
  },
});

export function getInterests() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/interests');
      dispatch(slice.actions.getInterestsSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
