import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';

// sections
import { useAuthContext } from '../../../auth/useAuthContext';
import LessonRecordings from '../../../sections/@dashboard/lessons/LessonRecordings';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getLesson, getLessonRecordings } from '../../../redux/slices/lesson';

import { Box, CircularProgress } from '@mui/material';

/**
 * This functional component renders the LessonRecordingPage, which displays lesson recordings.
 *
 * @component
 * @returns {JSX.Element} The rendered LessonRecordingPage component.
 */
export default function LessonRecordingPage() {
  const { user } = useAuthContext();
  const { id } = useParams();
  const dispatch = useDispatch();
  const { lesson, recording, isLoading } = useSelector((state) => state.lesson);
  const [openRecording, setOpenRecording] = useState({ open: false, url: '' });

  // Fetch lesson and lesson recordings when the component mounts or updates.
  useEffect(() => {
    const idSend = id || '';
    dispatch(getLesson(idSend));
    dispatch(getLessonRecordings(parseInt(id || '', 10)));
  }, [user, id, dispatch]);

  /**
   * This function handles the opening and closing of the lesson recording.
   *
   * @function handleRecording
   * @param {string | ''} url - The URL of the lesson recording.
   * @param {boolean} open - The boolean value representing if the recording is open.
   */
  const handleRecording = (url: string | '', open: boolean) => {
    setOpenRecording({ open, url });
  };

  return (
    <>
      {isLoading ? (
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100%',
          }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <LessonRecordings
          lesson={lesson}
          recording={recording}
          handleRecording={handleRecording}
          openRecording={openRecording}
        />
      )}
    </>
  );
}
