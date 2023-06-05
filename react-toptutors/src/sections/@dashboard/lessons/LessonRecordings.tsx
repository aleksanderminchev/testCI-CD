import { Helmet } from 'react-helmet-async';
import { Link as RouterLink } from 'react-router-dom';

import {
  Typography,
  Grid,
  Card,
  Tooltip,
  Divider,
  CardContent,
  Stack,
  Chip,
  IconButton,
  Button,
} from '@mui/material';

// types
import { ILesson, IRecording } from '../../../@types/lesson';
// mui
import { PATH_DASHBOARD } from '../../../routes/paths';

import { fDate } from '../../../utils/formatTime';
// components
import { CustomAvatar } from 'src/components/custom-avatar';
import Iconify from '../../../components/iconify';

type RecordingProps = {
  recording: IRecording | null;
  handleRecording: (url: string | '', open: boolean) => void;
  openRecording: { open: boolean; url: string };
  lesson: ILesson | null;
};

export default function LessonRecordings({
  lesson,
  recording,
  handleRecording,
  openRecording,
}: RecordingProps) {
  const start_time = new Date(recording?.start_time || new Date());
  const end_time = new Date(recording?.end_time || new Date());
  const lesson_type = lesson?.status;

  const colorType = () => {
    if (lesson?.status === 'attended') {
      return 'success';
    } else if (lesson?.status === 'scheduled') {
      return 'default';
    } else {
      return 'error';
    }
  };
  return (
    <>
      <Helmet>
        <title> Lesson: Recording </title>
      </Helmet>
      <Grid container lg={12} xs={12} md={12}>
        {openRecording.open ? (
          <Grid item xs={12} md={12} lg={12}>
            <iframe height="1000px" width="100%" title="Recording" src={openRecording.url || ''} />

            <Grid item xs={12} md={12} lg={12}>
              <Button onClick={() => handleRecording('', false)} variant="contained">
                Close Recoding
              </Button>
            </Grid>
          </Grid>
        ) : (
          <Grid item xs={12} md={12} lg={12}>
            <Grid item xs={12} lg={12} md={12} sx={{ margin: '5%' }}>
              <Card>
                <CardContent>
                  <div>
                    <Stack direction={'row'} spacing={1} justifyContent="space-between">
                      <Typography variant="h3" margin="1%">
                        Title: {lesson?.title}
                      </Typography>
                      <Stack direction={'row'} spacing={1} justifyContent="space-between">
                        <Chip
                          size="medium"
                          label={lesson_type?.toUpperCase()}
                          color={colorType()}
                        />
                        {lesson?.trial_lesson ? (
                          <Chip size="medium" label="Trial Lesson" color="warning" />
                        ) : (
                          <></>
                        )}
                      </Stack>
                    </Stack>
                    <Stack margin="2%" direction={'row'} spacing={1} justifyContent="space-between">
                      <div>
                        <CustomAvatar
                          variant="rounded"
                          sx={{ width: '100px', height: '100px' }}
                          src={
                            typeof lesson?.teacher?.photo === 'string'
                              ? lesson?.teacher?.photo
                              : lesson?.teacher?.photo?.preview || ''
                          }
                          alt={lesson?.teacher?.first_name || ''}
                          name={lesson?.teacher?.first_name || ''}
                        />
                        <Typography variant="h6">
                          {lesson?.teacher?.first_name} {lesson?.teacher?.last_name}
                        </Typography>
                      </div>
                      <Stack spacing={1} direction="column">
                        <Typography>
                          Studied at:{' '}
                          {lesson?.teacher?.higher_education_institutions?.map(
                            (institution) => institution.name
                          ) || ''}
                        </Typography>
                        <Typography>
                          Studied:{' '}
                          {lesson?.teacher?.higher_education_programmes?.map(
                            (programmes) => programmes.name
                          ) || ''}
                        </Typography>
                      </Stack>
                      <Typography>
                        Specilizes in:{' '}
                        {lesson?.teacher?.subjects?.map((subject) => subject.name) || ''}
                      </Typography>

                      <Tooltip title="Se profil">
                        <IconButton
                          component={RouterLink}
                          to={PATH_DASHBOARD.tutor.profile(lesson?.teacher.id || '')}
                        >
                          <Iconify width="70px" height="70px" icon="material-symbols:play-arrow" />
                        </IconButton>
                      </Tooltip>
                    </Stack>
                    <Stack margin="2%" direction={'row'} spacing={1} justifyContent="space-between">
                      <div>
                        <CustomAvatar
                          variant="rounded"
                          src={''}
                          sx={{ width: '100px', height: '100px' }}
                          alt={lesson?.student?.first_name || ''}
                          name={lesson?.student?.first_name || ''}
                        />
                        <Typography variant="h6">
                          {lesson?.student?.first_name} {lesson?.student?.last_name}
                        </Typography>
                      </div>

                      <Tooltip title="Se profil">
                        <IconButton
                          component={RouterLink}
                          to={PATH_DASHBOARD.student.profile(lesson?.student?.id || '')}
                        >
                          <Iconify width="70px" height="70px" icon="material-symbols:play-arrow" />
                        </IconButton>
                      </Tooltip>
                    </Stack>
                    <Divider sx={{ borderBottomWidth: 5 }} flexItem />
                    <Grid sx={{ marginBottom: '1%' }} item xs={12}>
                      <Typography variant="h4">Description</Typography>
                      <Typography component="p">{lesson?.description}</Typography>
                    </Grid>
                    <Grid sx={{ marginBottom: '1%' }} item xs={12}>
                      <Typography variant="h4">Completion Notes</Typography>
                      <Typography component="p">{lesson?.completion_notes}</Typography>
                    </Grid>
                    <Grid item xs={12}>
                      <Stack direction={'row'} spacing={1} justifyContent="space-between">
                        <Typography variant="h4">Start Time</Typography>
                        <Iconify width="70px" height="70px" icon="mdi:calendar-clock" />
                        <Typography>{fDate(start_time, 'dd MMM yyyy hh:mm')}</Typography>
                        <Typography variant="h4">End Time</Typography>
                        <Iconify width="70px" height="70px" icon="mdi:calendar-clock" />
                        <Typography>{fDate(end_time, 'dd MMM yyyy hh:mm')}</Typography>
                      </Stack>
                    </Grid>
                    {recording?.url !== '' ? (
                      <Button
                        onClick={() => handleRecording(recording?.url || '', true)}
                        variant="contained"
                      >
                        View Recording
                      </Button>
                    ) : (
                      <></>
                    )}
                  </div>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Grid>
    </>
  );
}
