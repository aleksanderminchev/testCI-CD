import { createSlice, Dispatch } from '@reduxjs/toolkit';

import axios from '../../utils/axios';
import overwriteArray from '../../utils/overwriteArray';

import { ICustomerState, ICustomer } from '../../@types/customer';

const initialState: ICustomerState = {
  isLoading: false,
  error: null,
  customers: { data: [], total: 0, offset: 0 },
  customer: null,
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
      state.error = action.payload; // if you only write action.payload, you do not dot-in to the actual data, where all data for customer is
    },
    // GET Customer
    getCustomersSuccess(state, action) {
      state.error = null;
      state.isLoading = false;
      state.customers = {
        data: overwriteArray(state.customers.data, action.payload.data),
        total: action.payload.pagination.total,
        offset: action.payload.pagination.offset,
      };
    },
    // GET Customer
    getCustomerSuccess(state, action) {
      state.error = null;
      state.isLoading = false;
      state.customer = action.payload.data;
    },
    // DELETE CUSTOMER
    deleteCustomerSuccess(state, action) {
      state.isLoading = false;
      state.error = null;
      state.customer = null;
    },
  },
});

export default slice.reducer;

export function getCustomers() {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/customers`, { withCredentials: true });
      console.log(response);
      dispatch(slice.actions.getCustomersSuccess(response.data));
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      console.log(errorMessage);
      dispatch(slice.actions.hasError(errorMessage));
    }
  };
}
export function getCustomer(id: string | number) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.get(`https://localhost:8081/api/customer/${id}`);
      if (response.status === 404) {
        throw new Error('Customer not found');
      } else {
        dispatch(slice.actions.getCustomerSuccess(response));
        console.log(response.data);
        console.log('success GetCustomer');
      }
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      console.log(errorMessage);
      dispatch(slice.actions.hasError(errorMessage));
    }
  };
}

export function deleteCustomer(id: string | undefined) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.delete(`https://localhost:8081/api/customer/${id}`);

      if (response.status === 404) {
        throw new Error('Customer not found');
      } else {
        dispatch(slice.actions.deleteCustomerSuccess({}));
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
/**
 * Method that creates a new customer and a student attached depending if it is family type
 * @param form ICustomer object with both customer and student data depending on the type
 * @param customerCreationType type of customer independent or family
 * @returns returns true or false depending on the success or failure of the operation
 */
export function createCustomer(form: ICustomer | any, customerCreationType: string) {
  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());

    try {
      console.log(form);
      if (customerCreationType === 'independent') {
        const submitForm = {
          email: form.email,
          first_name: form.first_name,
          last_name: form.last_name,
          phone: form.phone,
        };
        const response = await axios.post(
          `https://localhost:8081/api/independent`,
          {
            ...submitForm,
          },
          { withCredentials: true }
        );
        dispatch(slice.actions.getCustomerSuccess(response));
        console.log(response);
      } else if (customerCreationType === 'family' && form?.student_email === '') {
        const submitForm = {
          email: form.email,
          first_name: form.first_name,
          last_name: form.last_name,
          student_first_name: form.student_first_name,
          student_last_name: form.student_last_name,
          gender: 'male',
          phone: form.phone,
        };
        const response = await axios.post(
          `https://localhost:8081/api/family_with_student`,
          {
            ...submitForm,
          },
          { withCredentials: true }
        );
        dispatch(slice.actions.getCustomerSuccess(response));
        console.log(response);
      } else {
        const customerForm = {
          email: form.email,
          first_name: form.first_name,
          last_name: form.last_name,
          phone: form.phone,
        };
        const studentForm = {
          email: form.student_email,
          first_name: form.student_first_name,
          last_name: form.student_last_name,
          gender: 'male',
          phone: form.student_phone,
        };
        const responseCustomer = await axios.post(
          `https://localhost:8081/api/family`,
          {
            ...customerForm,
          },
          { withCredentials: true }
        );
        const responseStudent = await axios.post(
          `https://localhost:8081/api/student_with_user`,
          {
            ...studentForm,
            id: responseCustomer.data.id,
          },
          { withCredentials: true }
        );
        dispatch(slice.actions.getCustomerSuccess(responseCustomer));
        console.log(responseCustomer);
      }
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      console.log(errorMessage);
      dispatch(slice.actions.hasError(errorMessage));
    }
  };
}

export function editCustomer(form: Partial<ICustomer>) {
  const data_to_update_user = {
    id: form.id,
    email: form.email,
    first_name: form.first_name,
    last_name: form.last_name,
    phone: form.phone,
    email_lesson_reminder: form.email_lesson_reminders,
    email_lesson_notes: form.email_lesson_notes,
  };

  return async (dispatch: Dispatch) => {
    dispatch(slice.actions.startLoading());
    try {
      const response = await axios.put(`https://localhost:8081/api/customer`, {
        ...data_to_update_user,
      });
      dispatch(slice.actions.getCustomerSuccess(response));
      return true; // Return true on success
    } catch (error) {
      console.log(error);
      let errorMessage = '';
      if (error?.errors?.json._schema) {
        errorMessage = error?.errors?.json._schema[0];
      } else {
        errorMessage = error?.message;
      }
      console.log(errorMessage);
      dispatch(slice.actions.hasError(errorMessage));
      return false; // return false on error
    }
  };
}

// ----------------------------------------------------------------------
