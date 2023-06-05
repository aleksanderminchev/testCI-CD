import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';
import overwriteArray from '../../utils/overwriteArray';

import { ITransaction, ITransactionState } from '../../@types/transaction';

const initialState: ITransactionState = {
  isLoading: false,
  error: null,
  transactions: { data: [], page: 0, offset: 0, total: 0 },
  customerTransactions: { data: [], page: 0, offset: 0, total: 0 },
  transaction: null,
};

const slice = createSlice({
  name: 'transactions',
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

    // GET All Transaction
    getTransactionsSuccess(state, action) {
      state.isLoading = false;
      state.transactions = {
        data: overwriteArray(state.transactions.data, action.payload.data),
        page: 25 / action.payload.pagination.offset,
        offset: action.payload.pagination.offset,
        total: action.payload.pagination.total,
      };
    },
    // GET All Transaction
    getCustomerTransactionsSuccess(state, action) {
      state.isLoading = false;
      state.customerTransactions = {
        data: action.payload.data,
        page: 25 / action.payload.pagination.offset,
        offset: action.payload.pagination.offset,
        total: action.payload.pagination.total,
      };
    },
    // GET Specific Transaction by ID
    getTransactionSuccess(state, action) {
      state.isLoading = false;
      state.transaction = action.payload.data;
      state.error = null;
    },
    refundTransactionSuccess(state, action) {
      state.isLoading = false;
      state.transaction = action.payload.data;
      state.transactions = {
        ...state.transactions,
        data: [...state.transactions.data, action.payload.data],
      };
      state.error = null;
    },
  },
});

export default slice.reducer;

export function getTransactions(offset: number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const offsetStart = offset === 0 ? 0 : offset;
      console.log(offsetStart);
      const response = await axios.get(`https://localhost:8083/api/transaction?limit=25&offset=${offset}`, {
        withCredentials: true,
      });
      console.log(response);
      dispatch(slice.actions.getTransactionsSuccess(response.data));
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

export function getCustomerTransactions(id: number, offset: number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const offsetStart = offset === 0 ? 0 : offset;
      console.log(offsetStart);
      const response = await axios.get(`https://localhost:8083/api/transactions_customer/${id}?offset=${offset}`, {
        withCredentials: true,
      });
      console.log(response);
      dispatch(slice.actions.getCustomerTransactionsSuccess(response.data));
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

export function getTransaction(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8083/api/transaction/${id}`, {
        withCredentials: true,
      });
      if (response.status === 404) {
        throw new Error('Order not found');
      } else {
        dispatch(slice.actions.getTransactionSuccess(response));
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

export function createTransaction(transaction: ITransaction) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    const objectForRequest = {
      method: transaction.method,
      customer_id: transaction.customer_id || transaction.customer.id,
      void: transaction.void || false,
      type_transaction: transaction.type_transaction,
      amount: transaction.amount,
      currency: transaction.currency,
      stripe_transaction_id: transaction.stripe_transaction_id,
    };
    try {
      const response = await axios.post(
        `https://localhost:8083/api/transactions`,
        { ...objectForRequest },
        {
          withCredentials: true,
        }
      );
      if (response.status === 404) {
        throw new Error('Order not found');
      } else {
        const responeAttachToBalanceTransaction = await axios.post(
          'https://localhost:8083/api/add_transaction_to_balance',
          {
            customer_id: objectForRequest.customer_id,
            transaction_id: response.data.id,
          },
          { withCredentials: true }
        );
        dispatch(slice.actions.getTransactionSuccess(response));
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
export function refundTransaction(transaction: ITransaction | null) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());

    try {
      const response = await axios.get(`https://localhost:8083/api/refundTransaction/${transaction?.id}`, {
        withCredentials: true,
      });
      dispatch(slice.actions.refundTransactionSuccess(response));
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
export function updateTransaction(transaction: ITransaction) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    const objectForRequest = {
      method: transaction.method,
      id: transaction.id,
      void: transaction.void || false,
      type_transaction: transaction.type_transaction,
      amount: transaction.amount,
      currency: transaction.currency,
      stripe_transaction_id: transaction.stripe_transaction_id,
    };
    try {
      const response = await axios.put(
        `https://localhost:8083/api/update_transactions`,
        { ...objectForRequest },
        {
          withCredentials: true,
        }
      );
      if (response.status === 404) {
        throw new Error('Order not found');
      } else {
        dispatch(slice.actions.getTransactionSuccess(response));
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
