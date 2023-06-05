import { CustomFile } from '../components/upload/types';
import {
  ISubject,
  IProgram,
  IInterest,
  IQualification,
  ILanguage,
  IHigher_education_program,
  IHigher_education_institution,
  IHigh_school,
} from './arrays';

export type ITutor = {
  id: string;
  email: string | undefined;
  first_name: string;
  last_name: string;
  students: string[];
  languages: ILanguage[] | undefined;
  qualifications: IQualification[] | undefined;
  subjects: ISubject[] | undefined;
  interests: IInterest[] | undefined;
  programs: IProgram[] | undefined;
  higher_education_programmes: IHigher_education_program[] | undefined;
  higher_education_institutions: IHigher_education_institution[] | undefined;
  high_school: IHigh_school[] | undefined;
  referred: string;
  referrals: [];
  hire_date: Date;
  wage_per_hour: number | undefined;
  bank_number: number | undefined;
  reg_number: number | undefined;
  how_they_found: string | undefined;
  country: string | undefined;
  address: string | undefined;
  city: string | undefined;
  zip_code: string | undefined;
  bio: string | undefined;
  photo: CustomFile | string;
  phone: string | undefined;
  open_for_new_students: boolean | undefined;
  gender: string | undefined;
  status: string | undefined;
  grade_average: number | undefined;
  payroll_id: string | undefined;
  finished_highschool: boolean | undefined;
  age: number | undefined;
  birthday: Date;
  created_at: Date;
  last_updated: Date;
  updated_on_tw_at: Date;
  created_on_tw_at: Date;
};

export type ITutorNotificationSettings = {
  activityComments: boolean;
  activityAnswers: boolean;
  activityFollows: boolean;
  applicationNews: boolean;
  applicationProduct: boolean;
  applicationBlog: boolean;
};

export type ITutorListState = {
  byId: Record<string, ITutor>;
  allIds: string[];
};

export type ITutorState = {
  isLoading: boolean;
  error: Error | string | null;
  tutors: ITutor[];
  tutor: ITutor | null;
};
