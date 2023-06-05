import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';
import overwriteArray from '../../utils/overwriteArray';

import { IBalanceState } from '../../@types/balance';

const initialState: IBalanceState = {
  isLoading: false,
  error: null,
  balances: { data: [], page: 0, offset: 0, total: 0 },
  balance: null,
};

const slice = createSlice({
  name: 'balances',
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

    // GET All Balances
    getBalancesSuccess(state, action) {
      state.isLoading = false;
      state.balances = {
        data: overwriteArray(state.balances.data, action.payload.data),
        page: 25 / action.payload.pagination.offset,
        offset: action.payload.pagination.offset,
        total: action.payload.pagination.total,
      };
    },
    // GET Specific Balance by ID
    getBalanceSuccess(state, action) {
      state.isLoading = false;
      state.balance = action.payload.data;
      state.error = null;
    },
  },
});

export default slice.reducer;

export function getBalances(offset: number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const offsetStart = offset === 0 ? 0 : offset;
      console.log(offsetStart);
      const response = await axios.get(`https://localhost:8083/api/balance?limit=25&offset=${offset}`, {
        withCredentials: true,
      });
      console.log(response);
      dispatch(slice.actions.getBalancesSuccess(response.data));
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

export function getBalance(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8083/api/get_balance/${id}`, {
        withCredentials: true,
      });
      if (response.status === 404) {
        throw new Error('Order not found');
      } else {
        dispatch(slice.actions.getBalanceSuccess(response));
        console.log(response.data);
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
    }
  };
}
