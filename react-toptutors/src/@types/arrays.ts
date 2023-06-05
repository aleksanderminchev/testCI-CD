export type IAutocomplete = {
  id: string;
  label: string;
};

export type ILanguage = {
  id: string;
  name: string;
};

export type ILanguageState = {
  loadingLanguage: boolean;
  error: Error | string | null;
  languages: ILanguage[];
  language: ILanguage | null;
};

export type IQualification = {
  id: string;
  name: string;
};
export type IQualificationState = {
  loadingQualification: boolean;
  error: Error | string | null;
  qualifications: IQualification[];
  qualification: IQualification | null;
};

export type IInterest = {
  id: string;
  name: string;
};
export type IInterestState = {
  loadingInterest: boolean;
  error: Error | string | null;
  interests: IInterest[];
  interest: IInterest | null;
};

export type ISubject = {
  id: string;
  name: string;
};
export type ISubjectState = {
  loadingSubject: boolean;
  error: Error | string | null;
  subjects: ISubject[];
  subject: ISubject | null;
};

export type IProgram = {
  id: string;
  name: string;
};
export type IProgramState = {
  loadingProgram: boolean;
  error: Error | string | null;
  programmes: IProgram[];
  program: IProgram | null;
};

export type IHigher_education_program = {
  id: string;
  name: string;
};
export type IHigher_education_programState = {
  loadingHigher_education_program: boolean;
  error: Error | string | null;
  higher_education_programmes: IHigher_education_program[];
  higher_education_program: IHigher_education_program | null;
};
export type IHigher_education_institution = {
  id: string;
  name: string;
};
export type IHigher_education_institutionState = {
  loadingHigher_education_institution: boolean;
  error: Error | string | null;
  higher_education_institutions: IHigher_education_institution[];
  higher_education_institution: IHigher_education_institution | null;
};

export type IHigh_school = {
  id: string;
  name: string;
};
export type IHigh_schoolState = {
  loadingHigh_school: boolean;
  error: Error | string | null;
  high_schools: IHigh_school[];
  high_school: IHigh_school | null;
};

export type IGender = {
  value: string;
  label: string;
};
