import { Helmet } from 'react-helmet-async';
import { useEffect, useState } from 'react';

// @mui
import { Container } from '@mui/material';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getStudents } from '../../../redux/slices/student';
import { getQualifications } from '../../../redux/slices/arrays/qualification';
import { getInterests } from '../../../redux/slices/arrays/interest';
import { getLanguages } from '../../../redux/slices/arrays/language';
import { getSubjects } from '../../../redux/slices/arrays/subject';
import { getPrograms } from '../../../redux/slices/arrays/program';
import { getHigh_schools } from '../../../redux/slices/arrays/high_school';
import { getHigher_education_programs } from '../../../redux/slices/arrays/higher_education_program';
import { getHigher_education_institutions } from '../../../redux/slices/arrays/higher_education_institution';
import { createTutor, getTutors } from '../../../redux/slices/tutor';
// routes
import { PATH_DASHBOARD } from '../../../routes/paths';
// components
import { useSettingsContext } from '../../../components/settings';
import CustomBreadcrumbs from '../../../components/custom-breadcrumbs';
import { TutorCreateForm } from '../../../sections/@dashboard/tutor';
import { useSnackbar } from '../../../components/snackbar';
// sections
import { ITutor } from '../../../@types/tutor';

// ----------------------------------------------------------------------

export default function TutorCreatePage() {
  const { themeStretch } = useSettingsContext();

  const { enqueueSnackbar } = useSnackbar();
  const [failCreateTutor, setFailCreateTutor] = useState<ITutor>();
  const dispatch = useDispatch();
  const { error } = useSelector((state) => state.tutor);
  const { tutors } = useSelector((state) => state.tutor);
  const { student, students } = useSelector((state) => state.student);

  const { qualifications } = useSelector((state) => state.qualification);

  const { interests } = useSelector((state) => state.interest);

  const { high_schools } = useSelector((state) => state.high_school);

  const { subjects } = useSelector((state) => state.subject);

  const { programmes } = useSelector((state) => state.program);

  const { languages } = useSelector((state) => state.language);

  const { higher_education_institutions } = useSelector(
    (state) => state.higher_education_institution
  );
  const { higher_education_programmes } = useSelector((state) => state.higher_education_program);
  useEffect(() => {
    if (!students.length) dispatch(getStudents('active'));
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
    if (!qualifications.length) dispatch(getQualifications());
    dispatch(getTutors('active'));
    if (!interests.length) dispatch(getInterests());
    if (!higher_education_institutions.length) dispatch(getHigher_education_institutions());
    if (!higher_education_programmes.length) dispatch(getHigher_education_programs());
    if (!high_schools.length) dispatch(getHigh_schools());
    if (!programmes.length) dispatch(getPrograms());
    if (!languages.length) dispatch(getLanguages());
    if (!subjects.length) dispatch(getSubjects());
  }, [dispatch, error]);
  const handleCreateEditTutor = async (
    form: ITutor,
    subjects_create: string[],
    programs_create: string[]
  ) => {
    console.log(form);
    const failValueCheck = await dispatch(createTutor(form, subjects_create, programs_create));
    console.log(failValueCheck);
    if (!failValueCheck) {
      setFailCreateTutor({ ...form });
    } else {
      enqueueSnackbar('Successfully created a new tutor', { variant: 'success' });
      setFailCreateTutor(undefined);
    }
  };
  return (
    <>
      <Helmet>
        <title> Opret ny tutor </title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : 'lg'}>
        <CustomBreadcrumbs
          heading="Opret ny tutor"
          links={[
            {
              name: 'Oversigt',
              href: PATH_DASHBOARD.root,
            },
            {
              name: 'Tutor',
              href: PATH_DASHBOARD.tutor.new,
            },
            { name: 'Ny tutor' },
          ]}
        />
        <TutorCreateForm
          tutors={tutors}
          currentUser={failCreateTutor}
          higher_education_institutions={higher_education_institutions}
          qualifications={qualifications}
          languages={languages}
          programmes={programmes}
          subjects={subjects}
          high_schools={high_schools}
          higher_education_programmes={higher_education_programmes}
          interests={interests}
          createTutor={handleCreateEditTutor}
          student={student}
          studentList={students}
        />
      </Container>
    </>
  );
}
