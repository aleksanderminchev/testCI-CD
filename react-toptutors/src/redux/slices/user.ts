import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';

import { IUserState, IUserAccountChangePassword } from '../../@types/user';

const initialState: IUserState = {
  isLoading: false,
  error: null,
  users: [],
  user: null,
};

const slice = createSlice({
  name: 'customer',
  initialState,
  reducers: {
    // START LOADING
    startLoading(state) {
      state.isLoading = true;
    },

    // HAS ERROR
    hasError(state, action) {
      state.isLoading = false;
      state.error = action.payload.data; // if you only write action.payload, you do not dot-in to the actual data, where all data for customer is
    },
    // GET Users
    getUsersSuccess(state, action) {
      state.isLoading = false;
      state.users = action.payload.data;
    },
    // GET User
    getUserSuccess(state, action) {
      state.isLoading = false;
      state.user = action.payload.data;
    },
    // DELETE User
    deleteCustomerSuccess(state, action) {
      state.isLoading = false;
      state.user = null;
    },
  },
});

export default slice.reducer;

export function getUsers() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('https://localhost:8081/api/users');
      dispatch(slice.actions.getUsersSuccess(response.data));
    } catch (error) {
      dispatch(slice.actions.hasError(error));
    }
  };
}
export function getUser(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/users/${id}`);
      if (response.status === 404) {
        throw new Error('User not found');
      } else {
        dispatch(slice.actions.getUserSuccess(response));
      }
    } catch (error) {
      console.error(error);
      dispatch(slice.actions.hasError(error));
    }
  };
}

export function editUser(form: Partial<IUserAccountChangePassword>) {
  const data_to_update_user = {
    password: form.confirmNewPassword,
    old_password: form.oldPassword,
  };

  return async (dispatch: Dispatch): Promise<boolean> => {
    dispatch(slice.actions.startLoading());
    try {
      // Note that user is determined on their current Token, so only the logged in user can change their own data.
      const response = await axios.put(`https://localhost:8081/api/me`, {
        ...data_to_update_user,
      });
      dispatch(slice.actions.getUserSuccess(response));
      return true; // Return true on success
    } catch (error) {
      console.error(error);
      dispatch(slice.actions.hasError(error));
      return false; // return false on error
    }
  };
}
export function resendEmailVerification(email: string) {
  return async (dispatch: Dispatch) => {
    try {
      console.log(localStorage.getItem('accessToken'));
      const response = await axios.post(
        'https://localhost:8081/api/resendEmail',
        { email: email },
        {
          withCredentials: true,
        }
      );
      if (response.status === 200) {
        return true; //
      } else {
        return false; //
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
// ----------------------------------------------------------------------
