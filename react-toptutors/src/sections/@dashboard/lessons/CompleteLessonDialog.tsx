// react
import { useEffect, useState } from 'react';
// @mui
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  Button,
  TextField,
  Typography,
  IconButton,
  DialogActions,
  Dialog,
  DialogTitle,
} from '@mui/material';

// components
import Iconify from '../../../components/iconify';
import { CalendarForm } from '../calendar';
import { ICalendarEvent } from '../../../@types/calendar';

type FinishLessonProps = {
  cancel: boolean;
  admin: boolean;
  error: string | Error | null;
  teachers: [];
  students: [];
  onCancel: (state: boolean) => void;
  finishLessson: (completionNotes: string) => void;
  handleCreateUpdateEvent: (newEvent: ICalendarEvent) => void;
};
/**
 * Dialog for lesson completion for teachers
 *
 */
export default function CompleteLessonDialong({
  finishLessson,
  error,
  handleCreateUpdateEvent,
  cancel,
  teachers,
  students,
  admin,
  onCancel,
}: FinishLessonProps) {
  const today = new Date();
  const [todayInfo, setTodayInfo] = useState('');
  const [improvement, setImpovement] = useState('');
  const [nextLesson, setNextLesson] = useState(false);
  const [selectedRange, setSelectedRange] = useState<{
    start: Date;
    end: Date;
  } | null>(null);
  const steps = [
    {
      label: 'Hvad har I arbejdet på i dag? 🔨',
      field: (
        <TextField
          value={todayInfo}
          onChange={(e) => setTodayInfo(e.target.value)}
          multiline
          rows={6}
          inputProps={{ maxLength: 40 }}
          sx={{ margin: '2%' }}
          label="Hvad har I gennemgået i dag?"
        />
      ),
    },
    {
      label: 'Hvad er eleven blevet bedre til? 💪',
      field: (
        <TextField
          value={improvement}
          onChange={(e) => setImpovement(e.target.value)}
          multiline
          rows={6}
          inputProps={{ maxLength: 40 }}
          sx={{ margin: '2%' }}
          label="What has the student improved in?"
        />
      ),
    },
    {
      label: 'Hvornår er den næste lektion? 📆',
      field: (
        <Button
          variant="contained"
          size="medium"
          color="inherit"
          onClick={() => setNextLesson(true)}
          sx={{ mr: 1 }}
        >
          Opret den næste lektion i kalenderen
        </Button>
      ),
    },
  ];
  const [activeStep, setActiveStep] = useState(0);
  const [skipped, setSkipped] = useState(new Set<number>());

  const isStepSkipped = (step: number) => skipped.has(step);
  console.log(error);
  const scheduleLesson = (newEvent: ICalendarEvent) => {
    handleCreateUpdateEvent(newEvent);
  };
  const handleNext = () => {
    let newSkipped = skipped;
    if (isStepSkipped(activeStep)) {
      newSkipped = new Set(newSkipped.values());
      newSkipped.delete(activeStep);
    }
    // if(error){
    //   enqueueSnackbar(error,{variant:error})
    // }
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
    setSkipped(newSkipped);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleSkip = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
    setSkipped((prevSkipped) => {
      const newSkipped = new Set(prevSkipped.values());
      newSkipped.add(activeStep);
      return newSkipped;
    });
  };

  const handleReset = () => {
    setActiveStep(0);
  };
  useEffect(() => {
    if (error) {
      handleBack();
    }
  }, [error]);
  console.log(error);
  return (
    <Dialog fullWidth maxWidth="lg" open={cancel} onClose={() => onCancel(false)}>
      <DialogTitle>
        <Box display="flex" alignItems="center">
          <Box flexGrow={0.95}>
            <Typography>Finish Lesson </Typography>
          </Box>
          <Box>
            <IconButton size="small" color="error" onClick={() => onCancel(false)}>
              <Iconify icon="ic:sharp-close" />
            </IconButton>
          </Box>
        </Box>
      </DialogTitle>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((step, index: number) => {
          const stepProps: { completed?: boolean } = {};
          const labelProps = { optional: <Typography variant="caption">Valgfrit</Typography> };
          if (isStepSkipped(index)) {
            stepProps.completed = false;
          }
          return (
            <Step key={step.label} {...stepProps}>
              <StepLabel {...labelProps}>{step.label}</StepLabel>
            </Step>
          );
        })}
      </Stepper>
      {nextLesson ? (
        <Dialog fullWidth maxWidth="lg" open={nextLesson} onClose={() => setNextLesson(false)}>
          <DialogTitle>Planlæg lektion</DialogTitle>
          <CalendarForm
            teachers={teachers}
            students={students}
            admin={!admin}
            event={null}
            range={selectedRange}
            onCancel={() => {
              setNextLesson(false);
              if (!error) {
                handleNext();
              }
            }}
            onCreateUpdateEvent={scheduleLesson}
            // eslint-disable-next-line @typescript-eslint/no-empty-function
            onDeleteEvent={() => {}}
          />
        </Dialog>
      ) : (
        <></>
      )}
      {activeStep === steps.length ? (
        <>
          <Box sx={{ flex: '1 1 auto' }} />
          <Typography>Are you sure you want to complete this lesson?</Typography>
          {/* <Typography color={'red'}>{error?.toString() || ''}</Typography> */}
          <DialogActions>
            <Button size="small" onClick={handleReset}>
              Reset
            </Button>
            <Button
              onClick={() => {
                finishLessson(
                  `What did you do today? \n${todayInfo}\nWhat has the student improved in? \n${improvement}\n`
                );
                onCancel(false);
              }}
              variant="contained"
            >
              Yes
            </Button>
          </DialogActions>
        </>
      ) : (
        <>
          {steps[activeStep].field}
          <Box sx={{ display: 'flex', flexDirection: 'row', pt: 2 }}>
            <Button
              size="small"
              color="inherit"
              disabled={activeStep === 0}
              onClick={handleBack}
              sx={{ mr: 1 }}
            >
              Tilbage
            </Button>
            <Box sx={{ flex: '1 1 auto' }} />
            <Button size="small" color="inherit" onClick={handleSkip} sx={{ mr: 1 }}>
              Spring over
            </Button>
            <Button size="small" onClick={handleNext}>
              {activeStep === steps.length - 1 ? 'Afslut lektionen' : 'Næste'}
            </Button>
          </Box>
        </>
      )}
    </Dialog>
  );
}
