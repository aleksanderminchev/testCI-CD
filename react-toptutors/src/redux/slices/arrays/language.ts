import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../../utils/axios';

import { ILanguageState } from '../../../@types/arrays';

const initialState: ILanguageState = {
  loadingLanguage: false,
  error: null,
  languages: [],
  language: null,
};

const slice = createSlice({
  name: 'language',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.loadingLanguage = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.loadingLanguage = false;
      state.error = action.payload.data;
    },
    // GET languageS
    getLanguagesSuccess(state, action) {
      state.loadingLanguage = false;
      state.languages = action.payload.data;
    },
    // GET Tutor
    getLanguageSuccess(state, action) {
      state.loadingLanguage = false;
      state.language = action.payload;
      console.log(state.language);
    },
  },
});

export function getLanguages() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('/api/languages');
      dispatch(slice.actions.getLanguagesSuccess(response.data));
      console.log(response.data);
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}

export default slice.reducer;
