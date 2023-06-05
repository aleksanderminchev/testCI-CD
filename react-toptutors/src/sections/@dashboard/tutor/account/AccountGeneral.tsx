import * as Yup from 'yup';

// image compression
import imageCompression from 'browser-image-compression';
import { useEffect, useCallback, useState } from 'react';
// form
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { phoneNumberValidation } from '../../../../utils/phoneValidation';
import { MuiTelInputInfo } from 'mui-tel-input';

// auth
import RoleBasedGuard from '../../../../auth/RoleBasedGuard';
// redux
import { useDispatch, useSelector } from '../../../../redux/store';
import { editTutor, uploadTutorProfileImage } from '../../../../redux/slices/tutor';
import {
  getHigh_schools,
  getHigher_education_institutions,
  getHigher_education_programs,
  getInterests,
  getLanguages,
  getPrograms,
  getQualifications,
  getSubjects,
} from '../../../../redux/slices/arrays';
// @mui
import { Box, Grid, Card, Stack, Typography } from '@mui/material';

import { LoadingButton } from '@mui/lab';

// assets
import { countries } from '../../../../assets/data';
// components
import { CustomFile } from '../../../../components/upload';
import { useSnackbar } from '../../../../components/snackbar';
import FormProvider, {
  RHFSelect,
  RHFSlider,
  RHFTextField,
  RHFUploadAvatar,
  RHFRadioGroup,
  RHFAutocomplete,
  RHFCheckbox,
  RHFTel,
} from '../../../../components/hook-form';

import { ITutor } from '../../../../@types/tutor';
import { IAutocomplete } from '../../../../@types/arrays';
import { fData } from '../../../../utils/formatNumber';
import { fDate } from '../../../../utils/formatTime';
// ----------------------------------------------------------------------

interface FormValuesProps extends Omit<Partial<ITutor>, 'isEdit'> {
  photo?: CustomFile | string;
  subjects_update?: IAutocomplete[];
  programs_update?: IAutocomplete[];
  qualifications_update?: IAutocomplete[];
  languages_update?: IAutocomplete[];
  interests_update?: IAutocomplete[];
  high_school_update?: IAutocomplete;
  higher_education_programmes_update?: IAutocomplete;
  higher_education_institutions_update?: IAutocomplete;
  isEdit: boolean;
}

const GENDER_OPTION = [
  { label: 'Mand', value: 'male' },
  { label: 'Kvinde', value: 'female' },
];

export default function AccountGeneral(defaultValues: FormValuesProps) {
  const { enqueueSnackbar } = useSnackbar();

  const dispatch = useDispatch();
  const isEdit = defaultValues.isEdit;
  const { qualifications, loadingQualification } = useSelector((state) => state.qualification);
  const { languages, loadingLanguage } = useSelector((state) => state.language);
  const { subjects, loadingSubject } = useSelector((state) => state.subject);
  const { interests, loadingInterest } = useSelector((state) => state.interest);
  const { programmes, loadingProgram } = useSelector((state) => state.program);
  const { higher_education_programmes, loadingHigher_education_program } = useSelector(
    (state) => state.higher_education_program
  );
  const { higher_education_institutions, loadingHigher_education_institution } = useSelector(
    (state) => state.higher_education_institution
  );
  const { high_schools, loadingHigh_school } = useSelector((state) => state.high_school);

  useEffect(() => {
    if (!qualifications.length) dispatch(getQualifications());
    if (!interests.length) dispatch(getInterests());
    if (!higher_education_institutions.length) dispatch(getHigher_education_institutions());
    if (!higher_education_programmes.length) dispatch(getHigher_education_programs());
    if (!high_schools.length) dispatch(getHigh_schools());
    if (!programmes.length) dispatch(getPrograms());
    if (!languages.length) dispatch(getLanguages());
    if (!subjects.length) dispatch(getSubjects());
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [dispatch]);

  const UpdateTutorSchema = Yup.object().shape({
    first_name: Yup.string().required('Fornavn er et krav'),
    last_name: Yup.string().required('Efternavn er påkrævet'),
    email: Yup.string()
      .required('E-mail er påkrævet')
      .email('E-mailen skal være en gyldig e-mailadresse'),
    phone: phoneNumberValidation.required('Telefonnummer er påkrævet'),
    open_for_new_students: Yup.boolean(),
    gender: Yup.string(),
  });

  const methods = useForm<FormValuesProps>({
    resolver: yupResolver(UpdateTutorSchema),
    defaultValues,
  });

  const {
    handleSubmit,
    watch,
    setValue,
    formState: { isSubmitting },
  } = methods;

  const [fileForUpload, setFileForUpload] = useState<File>();

  const handleDrop = useCallback(
    async (acceptedFiles: File[]) => {
      if (acceptedFiles.length === 0) {
        enqueueSnackbar('Enten er filformatet forkert, eller billedstørrelsen er for stor.', {
          variant: 'error',
        });
      }

      const file = acceptedFiles[0];

      const compressedFile = await imageCompression(file, {
        maxSizeMB: 1,
        maxWidthOrHeight: 1080,
        useWebWorker: true,
      });

      setFileForUpload(compressedFile);

      const newFile = Object.assign(compressedFile, {
        preview: URL.createObjectURL(compressedFile),
      });

      if (newFile) {
        setValue('photo', newFile.preview, { shouldValidate: true });
      }
    },
    [enqueueSnackbar, setValue]
  );

  const onSubmit = async (data: FormValuesProps) => {
    try {
      // Destructure the data object and exclude the 'hire_date' property
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      const { hire_date, isEdit, updated_on_tw_at, created_on_tw_at, ...filteredData } = data;

      // Check if 'open_for_new_students' is defined as a String and convert the value to a boolean. if the value of filteredData.open_for_new_students is equal to the string 'true'. Then the expression evaluates to true, and if it's not, the expression evaluates to false.
      const open_for_new_students =
        typeof filteredData.open_for_new_students === 'string'
          ? filteredData.open_for_new_students === 'true'
          : filteredData.open_for_new_students;

      // Map through the array to get only the integer values of the "id" property if object is defined
      const extractIds = (data: IAutocomplete[] | IAutocomplete | undefined) => {
        // Ensure data is an array
        const dataArray = Array.isArray(data) ? data : data ? [data] : [];

        // Filter out null or undefined values
        // Map the array to get the "id" property values, then filter out any null or undefined values
        const idArray = dataArray
          .map((item) => item?.id)
          .filter((id) => id !== null && id !== undefined);

        return idArray;
      };

      const subjects_update = extractIds(filteredData.subjects_update);
      const programs_update = extractIds(filteredData.programs_update);
      const higher_education_institutions_update = extractIds(
        filteredData.higher_education_institutions_update
      );
      const higher_education_programmes_update = extractIds(
        filteredData.higher_education_programmes_update
      );
      const qualifications_update = extractIds(filteredData.qualifications_update);
      const languages_update = extractIds(filteredData.languages_update);
      const interests_update = extractIds(filteredData.interests_update);
      const high_school_update = extractIds(filteredData.high_school_update);

      console.log(high_school_update, 'high_school_update');
      console.log(filteredData.high_school_update, 'filteredData.high_school_update');
      let photoUrl;
      if (fileForUpload) {
        photoUrl = await dispatch(
          uploadTutorProfileImage(
            fileForUpload,
            `${filteredData.id}_tutor_${fDate(hire_date || new Date(), 'dd-MM-yyyy HH:mm:ss')}`,
            fileForUpload.type
          )
        );
      }

      // Create the updatedData object with the new 'open_for_new_students' value that overwrites the old one.
      const updatedData = {
        ...filteredData,
        id: defaultValues.id,
        photo: photoUrl || filteredData.photo,
        ...(typeof open_for_new_students !== 'undefined' && { open_for_new_students }),
        ...(subjects_update && { subjects_update }), // Replace the old subjects_update with the new one only if subjects_update is defined
        ...(programs_update && { programs_update }),
        ...(higher_education_institutions_update && { higher_education_institutions_update }),
        ...(higher_education_programmes_update && { higher_education_programmes_update }),
        ...(qualifications_update && { qualifications_update }),
        ...(languages_update && { languages_update }),
        ...(interests_update && { interests_update }),
        ...(high_school_update && { high_school_update }),
      };
      const success = await dispatch(editTutor(updatedData));

      console.log(success);

      if (success) {
        enqueueSnackbar('Update success!');
      } else {
        enqueueSnackbar('Update failed!', { variant: 'error' });
      }
    } catch (error) {
      console.error(error);
      enqueueSnackbar('Update failed!', { variant: 'error' });
    }
  };

  const values = watch();

  const errorsCPR = () => {
    if (values.payroll_id) {
      if (values.payroll_id.match('^\\d{6}-\\d{4}$')) {
        return { value: false, message: 'Correct CPR number' };
      } else {
        return { value: true, message: 'CPR Number has to have the format XXXXXX-XXXX' };
      }
    } else {
      return { value: true, message: 'Du mangler at udfylde dit CPR-nummer' };
    }
  };

  const changeCPR = (newCPR: string) => {
    setValue('payroll_id', newCPR, { shouldValidate: true });
  };

  const handleChange = (newPhone: string, info: MuiTelInputInfo) => {
    setValue('phone', info.numberValue || '', { shouldValidate: true });
  };

  const handleOptions = (
    objects: { id: string; [key: string]: any }[],
    labelProperty: string,
    selectedObjects: { id: string }[] | { id: string } | undefined
  ) => {
    const mappedObjects = objects.map((object) => {
      return { id: object.id, label: object[labelProperty] };
    });

    let filteredObjects;

    if (Array.isArray(selectedObjects)) {
      filteredObjects = mappedObjects.filter(
        (mappedObject) => !selectedObjects.find((object) => object.id === mappedObject.id)
      );
    } else if (selectedObjects) {
      filteredObjects = mappedObjects.filter(
        (mappedObject) => selectedObjects.id !== mappedObject.id
      );
    } else {
      filteredObjects = mappedObjects;
    }

    return filteredObjects;
  };

  return (
    <FormProvider methods={methods} onSubmit={handleSubmit(onSubmit)}>
      <Grid container spacing={3}>
        <RoleBasedGuard roles={['admin', 'teacher']}>
          <Grid item xs={12} md={4}>
            <Card sx={{ py: 10, px: 3, textAlign: 'center' }}>
              <RHFUploadAvatar
                name="photo"
                maxSize={3145728}
                onDrop={handleDrop}
                helperText={
                  <Typography
                    variant="caption"
                    sx={{
                      mt: 2,
                      mx: 'auto',
                      display: 'block',
                      textAlign: 'center',
                      color: 'text.secondary',
                    }}
                  >
                    Allowed *.jpeg, *.jpg, *.png, *.gif
                    <br /> max size of {fData(3145728)}
                  </Typography>
                }
              />
              <RHFSelect
                disabled={!isEdit}
                native
                name="open_for_new_students"
                label="Ønsker du flere elever?"
                sx={{ mt: 5 }}
              >
                <option value="true">Ja</option>
                <option value="false">Nej</option>
              </RHFSelect>

              <RoleBasedGuard roles={['admin']}>
                <RHFSelect disabled native name="status" label="Status" sx={{ mt: 5 }}>
                  <option value="prosepctive">prospective</option>
                  <option value="active">Active</option>
                  <option value="inactive">inactive</option>
                </RHFSelect>

                <RHFTextField name="hire_date" label="Hired date" disabled sx={{ mt: 5 }} />

                <RHFTextField
                  name="updated_on_tw_at"
                  label="Last updated"
                  disabled
                  sx={{ mt: 5 }}
                />

                <RHFTextField
                  name="created_on_tw_at"
                  label="Created date"
                  disabled
                  sx={{ mt: 5 }}
                />

                <RHFSlider
                  name="wage_per_hour"
                  step={10}
                  min={0}
                  max={200}
                  valueLabelDisplay="on"
                  getAriaValueText={(value) => `Timeløn på ${value} kr.`}
                  valueLabelFormat={(value) => `Timeløn på ${value} kr.`}
                  disabled
                  marks
                  sx={{ mt: 5 }}
                />
              </RoleBasedGuard>
            </Card>
          </Grid>
        </RoleBasedGuard>
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
              <RHFTextField disabled={!isEdit} name="first_name" label="Fornavn" />
              <RHFTextField disabled={!isEdit} name="last_name" label="Efternavn" />

              <RHFTextField disabled={!isEdit} name="email" label="E-mail" />

              <RHFTel
                disabled={!isEdit}
                name="phone"
                label="Telefonnummer"
                onChange={handleChange}
              />

              <RHFTextField disabled={!isEdit} name="address" label="Address" />

              <RHFSelect
                disabled={!isEdit}
                native
                name="country"
                label="Country"
                placeholder="Country"
              >
                <option value="" />
                {countries.map((country) => (
                  <option key={country.code} value={country.label}>
                    {country.label}
                  </option>
                ))}
              </RHFSelect>

              <RHFTextField disabled={!isEdit} name="city" label="City" />

              <RHFTextField disabled={!isEdit} name="zip_code" label="Zip/Code" />
            </Box>

            <Stack spacing={1} sx={{ mt: 3 }}>
              <Typography variant="subtitle2" sx={{ color: 'text.secondary' }}>
                Køn
              </Typography>
              <RHFRadioGroup
                disabled={!isEdit}
                row
                spacing={4}
                name="gender"
                options={GENDER_OPTION}
              />
            </Stack>
            <RoleBasedGuard roles={['admin', 'teacher']}>
              <Stack spacing={1} sx={{ mt: 3 }}>
                <RHFTextField
                  onChange={(e) => changeCPR(e.target.value)}
                  disabled={!isEdit}
                  name="payroll_id"
                  label="CPR-nummer"
                  error={!!errorsCPR().value}
                  helperText={errorsCPR().value && errorsCPR().message}
                  color={errorsCPR().value ? 'error' : 'success'}
                />
              </Stack>
            </RoleBasedGuard>
            <Stack spacing={3} alignItems="flex-end" sx={{ mt: 3 }}>
              <RHFTextField
                disabled={!isEdit}
                name="bio"
                multiline
                rows={4}
                label="Profilbeskrivelse"
              />
            </Stack>

            <Stack spacing={1} sx={{ mt: 3 }}>
              {!loadingSubject && (
                <RHFAutocomplete
                  name="subjects_update"
                  label="Undervisningsfag"
                  multiple
                  limitTags={3}
                  options={handleOptions(subjects, 'subject', values.subjects_update)}
                  disableClearable
                  disableCloseOnSelect
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!Array.isArray(values.subjects_update)) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) => !values.subjects_update?.find((object) => object.id === option.id)
                    );

                    return filtered;
                  }}
                />
              )}
            </Stack>

            <Box
              rowGap={3}
              columnGap={2}
              display="grid"
              sx={{ mt: 3 }}
              gridTemplateColumns={{
                xs: 'repeat(1, 1fr)',
                sm: 'repeat(2, 1fr)',
              }}
            >
              {!loadingProgram && (
                <RHFAutocomplete
                  disabled={!isEdit}
                  name="programs_update"
                  label="Matematik programmer"
                  multiple
                  limitTags={3}
                  options={handleOptions(programmes, 'program', values.programs_update)}
                  disableClearable
                  disableCloseOnSelect
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!Array.isArray(values.programs_update)) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) => !values.programs_update?.find((object) => object.id === option.id)
                    );

                    return filtered;
                  }}
                />
              )}

              {!loadingQualification && (
                <RHFAutocomplete
                  disabled={!isEdit}
                  name="qualifications_update"
                  label="Særlige kvalifikationer"
                  multiple
                  limitTags={3}
                  options={handleOptions(
                    qualifications,
                    'qualification',
                    values.qualifications_update
                  )}
                  disableClearable
                  disableCloseOnSelect
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!Array.isArray(values.qualifications_update)) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) =>
                        !values.qualifications_update?.find((object) => object.id === option.id)
                    );

                    return filtered;
                  }}
                />
              )}

              {!loadingLanguage && (
                <RHFAutocomplete
                  name="languages_update"
                  limitTags={3}
                  disabled={!isEdit}
                  label="Sprog jeg snakker flydende"
                  multiple
                  options={handleOptions(languages, 'language', values.languages_update)}
                  disableClearable
                  disableCloseOnSelect
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!Array.isArray(values.languages_update)) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) =>
                        !values.languages_update?.find((object) => object.id === option.id)
                    );

                    return filtered;
                  }}
                />
              )}

              {!loadingInterest && (
                <RHFAutocomplete
                  name="interests_update"
                  disabled={!isEdit}
                  limitTags={3}
                  label="Interesser"
                  multiple
                  options={handleOptions(interests, 'interest', values.interests_update)}
                  disableClearable
                  disableCloseOnSelect
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!Array.isArray(values.interests_update)) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) =>
                        !values.interests_update?.find((object) => object.id === option.id)
                    );

                    return filtered;
                  }}
                />
              )}

              {!loadingHigh_school && (
                <RHFAutocomplete
                  name="high_school_update"
                  disabled={!isEdit}
                  limitTags={3}
                  label="Gymnasietype"
                  options={handleOptions(high_schools, 'name', values.high_school_update)}
                  disableClearable
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!values.high_school_update) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) => values.high_school_update?.id !== option.id
                    );

                    return filtered;
                  }}
                />
              )}

              <RHFCheckbox
                disabled={!isEdit}
                name="finished_highschool"
                label="Er du færdig med gymnasiet?"
              />

              {values.finished_highschool && !loadingHigher_education_program && (
                <RHFAutocomplete
                  disabled={!isEdit}
                  name="higher_education_programmes_update"
                  limitTags={3}
                  label="Videregående uddannelse"
                  options={handleOptions(
                    higher_education_programmes,
                    'name',
                    values.higher_education_programmes_update
                  )}
                  disableClearable
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!values.high_school_update) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) => values.high_school_update?.id !== option.id
                    );

                    return filtered;
                  }}
                />
              )}

              {values.finished_highschool && !loadingHigher_education_institution && (
                <RHFAutocomplete
                  disabled={!isEdit}
                  name="higher_education_institutions_update"
                  limitTags={3}
                  label="Videregående uddannelsesinstitution"
                  options={handleOptions(
                    higher_education_institutions,
                    'name',
                    values.higher_education_institutions_update
                  )}
                  disableClearable
                  filterSelectedOptions
                  ChipProps={{ size: 'small' }}
                  filterOptions={(options) => {
                    if (!values.high_school_update) {
                      return options;
                    }

                    const filtered = options.filter(
                      (option) => values.high_school_update?.id !== option.id
                    );

                    return filtered;
                  }}
                />
              )}
            </Box>

            <Stack spacing={3} alignItems="flex-end" sx={{ mt: 3 }}>
              {isEdit ? (
                <LoadingButton type="submit" variant="contained" loading={isSubmitting}>
                  Gem ændringer
                </LoadingButton>
              ) : (
                <></>
              )}
            </Stack>
          </Card>
        </Grid>
      </Grid>
    </FormProvider>
  );
}
