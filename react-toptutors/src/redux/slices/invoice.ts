import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';
import overwriteArray from '../../utils/overwriteArray';

import { IInvoice, IInvoiceState } from '../../@types/invoice';

const initialState: IInvoiceState = {
  isLoading: false,
  error: null,
  invoices: { data: [], page: 0, offset: 0, total: 0 },
  customerInvoices: { data: [], page: 0, offset: 0, total: 0 },
  invoice: null,
};

const slice = createSlice({
  name: 'invoices',
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

    // GET All Payslips
    getInvoicesSuccess(state, action) {
      state.isLoading = false;
      state.invoice = null;
      state.invoices = {
        data: overwriteArray(state.invoices.data, action.payload.data),
        page: 25 / action.payload.pagination.offset,
        offset: action.payload.pagination.offset,
        total: action.payload.pagination.total,
      };
    },
    // GET All Payslips
    getCustomerInvoicesSuccess(state, action) {
      state.isLoading = false;
      state.invoice = null;
      state.customerInvoices = {
        data: action.payload.data,
        page: 25 / action.payload.pagination.offset,
        offset: action.payload.pagination.offset,
        total: action.payload.pagination.total,
      };
    },
    // GET Specific Payslip by ID
    getInvoiceSuccess(state, action) {
      state.isLoading = false;
      state.invoice = action.payload.data;
      state.error = null;
    },
  },
});

export default slice.reducer;

export function getInvoices(offset: number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const offsetStart = offset === 0 ? 0 : offset;
      console.log(offsetStart);
      const response = await axios.get(`https://localhost:8083/api/order?limit=25&offset=${offset}`, {
        withCredentials: true,
      });
      console.log(response);
      dispatch(slice.actions.getInvoicesSuccess(response.data));
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

export function getCustomerInvoices(id: number, offset: number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const offsetStart = offset === 0 ? 0 : offset;
      console.log(offsetStart);
      const response = await axios.get(`https://localhost:8083/api/orders_customer/${id}?offset=${offset}`, {
        withCredentials: true,
      });
      console.log(response);
      dispatch(slice.actions.getCustomerInvoicesSuccess(response.data));
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

export function getInvoice(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8083/api/order/${id}`, {
        withCredentials: true,
      });
      if (response.status === 404) {
        throw new Error('Invoice not found');
      } else {
        dispatch(slice.actions.getInvoiceSuccess(response));
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
export function resendEmail(invoice: IInvoice) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.post(
        'https://localhost:8083/api/send_order_email',
        { id: invoice.id },
        {
          withCredentials: true,
        }
      );
      console.log(response);
      if (response.status === 201) {
        return true;
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
export function createInvoice(invoice: IInvoice) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    console.log(invoice);
    const objectForRequest = {
      total_hours: invoice.total_hours,
      package: invoice.stripe_invoice_id,
      installments: invoice.installments,
      email_sent: invoice.email_sent,
      crm_deal_id: '',
      email: invoice.email,
      name: invoice.name,
      discount: invoice?.discount,
    };
    try {
      const response = await axios.post(
        `https://localhost:8083/api/add_order`,
        { ...objectForRequest },
        {
          withCredentials: true,
        }
      );
      console.log(response);
      if (response.status === 404) {
        throw new Error('Invoice not found');
      } else {
        const order_id = response.data.order_id;
        const attachToBalance = {
          customer_id: invoice?.customer_id,
          order_id: order_id,
        };
        const responeAttachToBalanceInvoice = await axios.post(
          'https://localhost:8083/api/add_order_to_balance',
          {
            ...attachToBalance,
          },
          { withCredentials: true }
        );
        dispatch(slice.actions.getInvoiceSuccess(responeAttachToBalanceInvoice));
        console.log(responeAttachToBalanceInvoice);
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

export function updateInvoice(invoice: IInvoice) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    const objectForRequest = {
      uid: invoice.id,
      status: invoice.status,
      email_sent: invoice.email_sent,
    };
    try {
      if (invoice.status === 'void') {
        const response = await axios.put(
          `https://localhost:8083/api/void_order`,
          { id: invoice.id },
          {
            withCredentials: true,
          }
        );
        console.log(response);
      }
      const response = await axios.put(
        `https://localhost:8083/api/update_orders`,
        { ...objectForRequest },
        {
          withCredentials: true,
        }
      );
      if (response.status === 404) {
        throw new Error('Invoice not found');
      } else {
        dispatch(slice.actions.getInvoiceSuccess(response));
        console.log(response);
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
