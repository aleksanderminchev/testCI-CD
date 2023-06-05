import { combineReducers } from 'redux';

import storage from 'redux-persist/lib/storage';
// slices

import calendarReducer from './slices/calendar';
import tutorReducer from './slices/tutor';
import customerReducer from './slices/customer';
import lessonReducer from './slices/lesson';
import studentReducer from './slices/student';
import payslipReducer from './slices/payslip';
import invoiceReducer from './slices/invoice';
import transactionReducer from './slices/transaction';
import balanceReducer from './slices/balance';
// arrays
import languageReducer from './slices/arrays/language';
import interestReducer from './slices/arrays/interest';
import high_schoolReducer from './slices/arrays/high_school';
import higher_education_institutionReducer from './slices/arrays/higher_education_institution';
import higher_education_programReducer from './slices/arrays/higher_education_program';
import programReducer from './slices/arrays/program';
import qualificationReducer from './slices/arrays/qualification';
import subjectReducer from './slices/arrays/subject';

// ----------------------------------------------------------------------

export const rootPersistConfig = {
  key: 'root',
  storage,
  keyPrefix: 'redux-',
  whitelist: [],
};

const rootReducer = combineReducers({
  calendar: calendarReducer,
  customer: customerReducer,
  student: studentReducer,
  tutor: tutorReducer,
  lesson: lessonReducer,
  payslip: payslipReducer,
  transaction: transactionReducer,
  balance: balanceReducer,
  invoice: invoiceReducer,
  high_school: high_schoolReducer,
  language: languageReducer,
  interest: interestReducer,
  higher_education_institution: higher_education_institutionReducer,
  higher_education_program: higher_education_programReducer,
  program: programReducer,
  qualification: qualificationReducer,
  subject: subjectReducer,
});

export default rootReducer;
