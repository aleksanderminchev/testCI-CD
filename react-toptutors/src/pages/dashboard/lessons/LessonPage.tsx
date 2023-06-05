import { useEffect } from 'react';
import { useParams } from 'react-router-dom';
// components
import CompleteLessonDialong from '../../../sections/@dashboard/lessons/CompleteLessonDialog';
import { useSnackbar } from '../../../components/snackbar';

// sections
import { useAuthContext } from '../../../auth/useAuthContext';
// redux
import { useDispatch, useSelector } from '../../../redux/store';
import { getLesson } from '../../../redux/slices/lesson';
import { completeLesson, createEvent } from '../../../redux/slices/calendar';
import { getLessonUrlStudent, getLessonUrlTeacher } from '../../../utils/services';
import { ICalendarEvent } from '../../../@types/calendar';

type Props = {
  setUrlForLesson: (value: string) => void;
  goBackStudent: (value: boolean) => void;
  urlForLesson: string;
  setRedirectionUrl: (value: string) => void;
  finishLesson: boolean;
  setFinishLesson: (value: boolean) => void;
};

/**
 * This functional component renders the LessonPage, which displays the lesson content
 * in an iframe and allows teachers to complete the lesson.
 *
 * @component
 * @param {Props} {
 *   setUrlForLesson,
 *   urlForLesson,
 *   setRedirectionUrl,
 *   finishLesson,
 *   setFinishLesson,
 * } The component's props.
 * @returns {JSX.Element} The rendered LessonPage component.
 */
export default function LessonPage({
  setUrlForLesson,
  urlForLesson,
  setRedirectionUrl,
  finishLesson,
  goBackStudent,
  setFinishLesson,
}: Props) {
  const { user } = useAuthContext();

  const { id } = useParams();

  const { enqueueSnackbar } = useSnackbar();

  const dispatch = useDispatch();

  const { lesson } = useSelector((state) => state.lesson);
  const { teachers, students, error } = useSelector((state) => state.calendar);

  // Handles everything related to completing the lesson.
  const sendLessonCompletion = (completionNotes: string) => {
    dispatch(completeLesson(parseInt(lesson?.id || '', 10), completionNotes));
  };

  // Creates a new lesson if they choose to plan it right away.
  const handleCreateUpdateEvent = (newEvent: ICalendarEvent) => {
    dispatch(createEvent(newEvent));
  };

  // Fetch lesson information, set the lesson URL, and handle errors when the component mounts or updates.
  useEffect(() => {
    if (user && id !== undefined) {
      dispatch(getLesson(id));
    }
    if (user?.teacher) {
      getLessonUrlTeacher(parseInt(id || '', 10), setUrlForLesson);
      goBackStudent(false);
      setRedirectionUrl('/calendar');
    } else if (user?.customer || user?.student) {
      goBackStudent(true);
      getLessonUrlStudent(parseInt(id || '', 10), setUrlForLesson);
      setRedirectionUrl('/dashboard');
    }
    if (error) {
      enqueueSnackbar(error.toString(), { variant: 'error' });
    }
  }, [user, id, dispatch, error, enqueueSnackbar]);

  if (lesson?.status === 'scheduled') {
    return (
      <>
        {user?.teacher ? (
          <CompleteLessonDialong
            error={error}
            handleCreateUpdateEvent={handleCreateUpdateEvent}
            teachers={teachers}
            students={students}
            finishLessson={sendLessonCompletion}
            cancel={finishLesson}
            admin={false}
            onCancel={setFinishLesson}
          />
        ) : (
          <></>
        )}
        <iframe
          id="iframe"
          width="100%"
          height="100%"
          title="Lesson"
          src={urlForLesson}
          allow="camera; microphone; display-capture;fullscreen;"
        />
      </>
    );
  }
  return <></>;
}
