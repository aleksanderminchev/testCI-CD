import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';
import { IPayslipState } from '../../@types/payslip';

const initialState: IPayslipState = {
  isLoading: false,
  error: null,
  payslips: [],
  payslip: null,
  temporaryPayslips: [],
};

const slice = createSlice({
  name: 'payslips',
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
    getPayslipsSuccess(state, action) {
      state.isLoading = false;
      state.payslips = action.payload.data;
    },
    // GET Specific Payslip by ID
    getPayslipSuccess(state, action) {
      state.isLoading = false;
      state.payslip = action.payload.data;
    },
    getTemporaryPayslipsSuccess(state, action) {
      state.isLoading = false;
      state.temporaryPayslips = action.payload.data;
    },
  },
});

export default slice.reducer;

export function getPayslips() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get('https://localhost:8083/api/wagepayments', { withCredentials: true });
      console.log(response);
      dispatch(slice.actions.getPayslipsSuccess(response.data));
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

export function getPayslip(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8083/api/wagepayment/${id}`, { withCredentials: true });
      if (response.status === 404) {
        throw new Error('Payslip not found');
      } else {
        dispatch(slice.actions.getPayslipSuccess(response));
        console.log(response);
        console.log('suceess');
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

export function getTutorPayslips(tutor_id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8083/api/tutor_wagepayments/${tutor_id}`, {
        params: { tutor_id },
        withCredentials: true,
      });
      if (response.status === 404) {
        throw new Error('Payslips not found');
      } else {
        dispatch(slice.actions.getPayslipsSuccess(response));
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

export function calculateMontlyPayslip(start_date: string, end_date: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      console.log(start_date);
      console.log(end_date);
      const response = await axios.post(
        'https://localhost:8083/api/calculate_wages_hours',
        {
          start_date: start_date,
          end_date: end_date,
        },
        { withCredentials: true }
      );
      dispatch(slice.actions.getTemporaryPayslipsSuccess(response));
      console.log(response);
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

export function createWagePayments(start_date: string, end_date: string, payment_date: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      console.log(start_date);
      console.log(end_date);
      const response = await axios.post(
        'https://localhost:8083/api/bulk_wagepayments',
        {
          payment_date: payment_date,
          start_date: start_date,
          end_date: end_date,
        },
        { withCredentials: true }
      );
      const downloadResponse = await axios
        .post(
          'https://localhost:8083/api/download',
          { start_date: start_date, end_date: end_date },
          {
            withCredentials: true,
            responseType: 'blob',
            headers: {
              Accept: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            },
          }
        )
        .then((result) => {
          const href = URL.createObjectURL(result.data);

          // create "a" HTML element with href to file & click
          const link = document.createElement('a');
          link.href = href;
          link.setAttribute('download', `wages_${start_date}_${end_date}.xlsx`); //or any other extension
          document.body.appendChild(link);
          link.click();

          // clean up "a" element & remove ObjectURL
          document.body.removeChild(link);
          URL.revokeObjectURL(href);
        });
      console.log(downloadResponse);
      dispatch(slice.actions.getPayslipsSuccess(response.data));
      console.log(response);
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
