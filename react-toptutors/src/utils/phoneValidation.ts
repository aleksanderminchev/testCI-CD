import * as Yup from 'yup';
import { parsePhoneNumber } from 'libphonenumber-js';

export const phoneNumberValidation = Yup.string().test(
  'phone',
  'Telefonnummeret er ikke gyldigt',
  (value) => {
    if (!value) return false;

    try {
      const phoneNumber = parsePhoneNumber(value);
      return phoneNumber.isValid();
    } catch (error) {
      return false;
    }
  }
);
