import * as Yup from 'yup';
import { useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
// form
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
// @mui
import { LoadingButton } from '@mui/lab';
import { Box, Card, Grid, TextField, Switch, Typography, FormControlLabel } from '@mui/material';
import { MobileDatePicker } from '@mui/x-date-pickers';
import { MuiTelInputInfo } from 'mui-tel-input';
// utils
import { fDate } from '../../../utils/formatTime';
// select options
import { gender } from '../../../assets/data/gender';
// @types
import { ITutor } from '../../../@types/tutor';
import { IStudent } from '../../../@types/student';
import {
  IQualification,
  IInterest,
  IHigher_education_institution,
  IHigher_education_program,
  IHigh_school,
  ISubject,
  ILanguage,
  IProgram,
} from '../../../@types/arrays';
// components
import Label from '../../../components/label';
import { CustomFile } from '../../../components/upload';
import { useSnackbar } from '../../../components/snackbar';

import FormProvider, {
  RHFSelect,
  RHFSwitch,
  RHFTextField,
  RHFAutocomplete,
  RHFTel,
} from '../../../components/hook-form';

// ----------------------------------------------------------------------

interface FormValuesProps extends Omit<ITutor, 'avatarUrl'> {
  avatarUrl: CustomFile | string | null;
  subjects_create: ISubject[];
  programs_create: IProgram[];
  referred_by: string | null;
  amount: number | null;
}

type Props = {
  isEdit?: boolean;
  currentUser?: ITutor;
  tutors: ITutor[];
  tutorType?: string;
  student: IStudent | null;
  interests: IInterest[];
  qualifications: IQualification[];
  higher_education_institutions: IHigher_education_institution[];
  higher_education_programmes: IHigher_education_program[];
  high_schools: IHigh_school[];
  languages: ILanguage[];
  subjects: ISubject[];
  programmes: IProgram[];
  studentList: IStudent[] | [];
  createTutor:
    | ((values: FormValuesProps, subjects_create: string[], programmes_create: string[]) => void)
    | (() => void);
};

export default function TutorNewEditForm({
  isEdit = false,
  currentUser,
  tutors,
  student,
  studentList,
  qualifications,
  interests,
  subjects,
  programmes,
  languages,
  high_schools,
  higher_education_programmes,
  higher_education_institutions,
  tutorType,
  createTutor,
}: Props) {
  const navigate = useNavigate();

  const { enqueueSnackbar } = useSnackbar();

  const NewUserSchema = Yup.object().shape({
    first_name: Yup.string().required('Name is required'),
    last_name: Yup.string().required('Name is required'),
    email: Yup.string()
      .required('Email is required')
      .email('E-mailen skal være en gyldig e-mailadresse'),
    gender: Yup.string().oneOf(['female', 'male']),
    zip_code: Yup.string(),
    city: Yup.string(),
    country: Yup.string(),
    payroll_id: Yup.string(),
    open_for_new_students: Yup.boolean(),
    grade_average: Yup.number(),
    wage_per_hour: Yup.number(),
    bio: Yup.string().max(2000, 'Maksimum 2000 tegn.'),
    how_they_found: Yup.string(),
    birthday: Yup.date(),
  });
  const isDateError = () => {
    const today = new Date();
    const oldestDate = new Date(1945, 1);
    const birthday = values?.birthday;
    if (birthday > today) {
      return { value: true, message: 'Cannot set so young' };
    } else if (birthday < oldestDate) {
      return { value: true, message: 'Too old of a date' };
    }
    return { value: false, message: 'No errors' };
  };
  const defaultValuesIndependent = useMemo(
    () => ({
      first_name: currentUser?.first_name || '',
      last_name: currentUser?.last_name || '',
      email: currentUser?.email || '',
      phone: currentUser?.phone || '',
      gender: currentUser?.gender || '',
      zip_code: currentUser?.zip_code || '',
      city: currentUser?.city || '',
      address: currentUser?.address || '',
      country: currentUser?.country || '',
      payroll_id: currentUser?.payroll_id || '',
      open_for_new_students: currentUser?.open_for_new_students || false,
      grade_average: currentUser?.grade_average || 0,
      wage_per_hour: currentUser?.wage_per_hour || 0,
      how_they_found: currentUser?.how_they_found || '',
      referred_by: currentUser?.referred || '',
      birthday: currentUser?.birthday || new Date(fDate(new Date(), 'yyyy-MM-dd')),
      bio: currentUser?.bio || '',
      referral_amount: 200,
      programs_create: currentUser?.programs || [],
      subjects_create: currentUser?.subjects || [],
      qualification: currentUser?.qualifications || [],
      interest: currentUser?.interests || [],
      language: currentUser?.languages || [],
      higher_education_institution: currentUser?.higher_education_institutions || [],
      higher_education_programme: currentUser?.higher_education_programmes || [],
      highschool: currentUser?.high_school || '',
    }),
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [currentUser]
  );

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(NewUserSchema),
    defaultValues: defaultValuesIndependent,
  });

  const { reset, watch, control, setValue, handleSubmit } = methods;

  const values = watch();
  console.log(values);
  const handleChange = (newPhone: string, info: MuiTelInputInfo) => {
    setValue('phone', info.numberValue || '', { shouldValidate: true });
  };

  useEffect(() => {
    if (isEdit && currentUser) {
      reset(defaultValuesIndependent);
    }
    if (!isEdit) {
      reset(defaultValuesIndependent);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEdit, currentUser]);

  const onSubmit = async (data: FormValuesProps) => {
    try {
      const creationData = {
        ...data,
      };
      createTutor(
        creationData,
        data.subjects_create.map((subject) => subject.id.toString()),
        data.programs_create.map((program) => program.id.toString())
      );
      reset();
      // navigate(PATH_DASHBOARD.family.root);
    } catch (err) {
      console.error(err);
      enqueueSnackbar(!isEdit ? 'Create success!' : 'Update success!', { variant: 'error' });
    }
  };

  const handleSubjectOptions = (subjects: ISubject[]) => {
    const mappedSubjects = subjects.map((subject) => {
      return { id: subject.id.toString(), label: `${subject.name}` };
    });
    return mappedSubjects.filter(
      (mappedSubject) => !values.subjects_create.find((object) => object.id === mappedSubject.id)
    );
  };
  const handleProgramOptions = (programs: IProgram[]) => {
    const mappedSubjects = programs.map((program) => {
      return { id: program.id.toString(), label: `${program.name}` };
    });
    return mappedSubjects.filter(
      (mappedSubject) => !values.programs_create.find((object) => object.id === mappedSubject.id)
    );
  };
  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card sx={{ pt: 10, pb: 5, px: 3 }}>
            {isEdit && (
              <Label
                color={values.status === 'active' ? 'success' : 'error'}
                sx={{ textTransform: 'uppercase', position: 'absolute', top: 24, right: 24 }}
              >
                {values.status}
              </Label>
            )}

            <Box sx={{ mb: 5 }}></Box>

            {isEdit && (
              <FormControlLabel
                labelPlacement="start"
                control={
                  <Controller
                    name="status"
                    control={control}
                    render={({ field }) => (
                      <Switch
                        {...field}
                        checked={field.value !== 'active'}
                        onChange={(event) =>
                          field.onChange(event.target.checked ? 'banned' : 'active')
                        }
                      />
                    )}
                  />
                }
                label={
                  <>
                    <Typography variant="subtitle2" sx={{ mb: 0.5 }}>
                      Banned
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Apply disable account
                    </Typography>
                  </>
                }
                sx={{ mx: 0, mb: 3, width: 1, justifyContent: 'space-between' }}
              />
            )}

            <RHFSwitch
              name="isVerified"
              labelPlacement="start"
              label={
                <>
                  <Typography variant="subtitle2" sx={{ mb: 0.5 }}>
                    Disable verification email
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Enabling this will not send the user a verification email
                  </Typography>
                </>
              }
              sx={{ mx: 0, width: 1, justifyContent: 'space-between' }}
            />
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card sx={{ p: 3 }}>
            <Box
              rowGap={3}
              columnGap={2}
              display="grid"
              gridTemplateColumns={{
                xs: 'repeat(1, 1fr)',
                sm: 'repeat(2, 1fr)',
              }}
            >
              <RHFTextField name="first_name" label="First Name" />
              <RHFTextField name="last_name" label="Last Name" />
              <RHFTextField type="email" name="email" label="Email Address" />
              <RHFTextField name="payroll_id" label="CPR number" />
              <RHFTel name="phone" label="Telefonnummer" required onChange={handleChange} />
              <RHFTextField name="how_they_found" label="How did you hear about Top Tutors?" />
              <RHFTextField name="country" label="Country" />
              <RHFTextField name="zip_code" label="Zip code" />
              <RHFTextField name="address" label="Address" />
              <RHFTextField name="city" label="City" />
              <RHFTextField name="bank_number" label="Bank number" />
              <RHFTextField name="reg_number" label="Reg number" />
              <RHFTextField name="wage_per_hour" label="Wage" />
              <RHFTextField type="number" name="grade_average" label="Grade Average" />
              <RHFSelect label="Referred by" native name="referred_by">
                <option />
                {tutors.map((value) => (
                  <option
                    label={`${value.first_name} ${value.last_name}`}
                    value={value.id}
                    key={value.id}
                  >
                    {value.first_name} {value.last_name}
                  </option>
                ))}
              </RHFSelect>
              <RHFTextField name="referral_amount" label="Referral Amount" type="number" />
              <RHFSwitch name="open_for_new_students" label="Open for new Students" />
              <RHFTextField name="bio" label="Bio" multiline rows={7} />
              <Controller
                name="birthday"
                control={control}
                render={({ field }) => (
                  <MobileDatePicker
                    {...field}
                    onChange={(newValue: Date | null) => field.onChange(newValue)}
                    label="Birthday"
                    views={['year', 'month', 'day']}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        fullWidth
                        error={!!isDateError().value}
                        helperText={isDateError().value && isDateError().message}
                      />
                    )}
                  />
                )}
              />
              <RHFSelect label="Qualification " native name="qualification">
                <option />
                {qualifications.map((value) => (
                  <option label={`${value.name}`} value={value.id} key={value.id}>
                    {value.name}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect label="Interest " native name="interest">
                <option />
                {interests.map((value) => (
                  <option label={`${value.name}`} value={value.id} key={value.id}>
                    {value.name}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect label="Language " native name="language">
                <option />
                {languages.map((value) => (
                  <option label={`${value.name}`} value={value.id} key={value.id}>
                    {value.name}
                  </option>
                ))}
              </RHFSelect>
              <RHFAutocomplete
                label="Subjects"
                multiple
                filterSelectedOptions
                options={handleSubjectOptions([...subjects])}
                disableClearable
                disableCloseOnSelect={false}
                name="subjects_create"
              />
              {/* <option />
                {subjects.map((value) => (
                  <option label={`${value.subject}`} value={value.id} key={value.id}>
                    {value.subject}
                  </option>
                ))} */}
              <RHFAutocomplete
                label="Programs"
                multiple
                filterSelectedOptions
                options={handleProgramOptions([...programmes])}
                disableClearable
                disableCloseOnSelect={false}
                name="programs_create"
              />
              <RHFSelect label="High School " native name="highschool">
                <option />
                {high_schools.map((value) => (
                  <option label={`${value.name}`} value={value.id} key={value.id}>
                    {value.name}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect label="Higher Education Program " native name="higher_education_programme">
                <option />
                {higher_education_programmes.map((value) => (
                  <option label={`${value.name}`} value={value.id} key={value.id}>
                    {value.name}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect
                label="Higher Education Institution "
                native
                name="higher_education_institution"
              >
                <option />
                {higher_education_institutions.map((value) => (
                  <option label={`${value.name}`} value={value.id} key={value.id}>
                    {value.name}
                  </option>
                ))}
              </RHFSelect>
              <RHFSelect label="Gender of " native name="gender">
                <option />
                {gender.map((value) => (
                  <option label={value.label} value={value.value} key={value.code}>
                    {value.label}
                  </option>
                ))}
              </RHFSelect>
            </Box>

            <LoadingButton type="submit" variant="contained" sx={{ mt: 3 }}>
              {!isEdit ? 'Opret Tutor' : 'Gem Ændringer'}
            </LoadingButton>
            {/* </Stack> */}
          </Card>
        </Grid>
      </Grid>
    </FormProvider>
  );
}
