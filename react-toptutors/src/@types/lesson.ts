import { ITutor } from './tutor';
import { IStudent } from './student';

export type ILesson = {
  id: string;
  title: string;
  lesson_type: string;
  created_at: Date;
  last_updated: Date;
  completed_at: Date;
  completion_notes: string;
  duration_in_minutes: number;
  wage: number;
  trial_lesson: boolean;
  description: string;
  from_time: Date;
  to_time: Date;
  space: string;
  status: string;
  paid: boolean;
  teacher: ITutor;
  student: IStudent;
  tutor: ITutor['email'];
};

export type ILessonDetails = {
  id: string;
  student: string;
  avatar: string;
  date: Date | string | number;
  startTime: Date;
  endTime: Date;
  duration: number;
  status: string;
  wage: number;
  paid: string;
};
export type ILessonForStudent = {
  id: string;
  title: string;
  space: string;
  duration_in_minutes: number;
  description: string;
  completion_notes: string;
  wage: number;
  status: string;
  paid: boolean;
  trial_lesson: boolean;
  created_at: Date;
  last_updated: Date;
  completed_at: Date;
  from_time: Date;
  to_time: Date;
  lesson_reminder_sent_at: Date;
  teacher: ITutor;
  student: IStudent;
};

export type ILessonsForStudentState = {
  isLoading: boolean;
  error: Error | string | null;
  lessons: ILessonForStudent[];
  lesson: ILessonForStudent | null;
};

export type IRecording = {
  url: string | '';
  start_time: Date;
  end_time: Date;
  name: string;
};
export type IUserLessonNotificationSettings = {
  email_lesson_reminders: boolean;
  email_lesson_notes: boolean;
};

export type ILessonListState = {
  byId: Record<string, ILesson>;
  allIds: string[];
};

export type ILessonState = {
  isLoading: boolean;
  error: Error | string | null;
  lessons: ILesson[];
  lesson: ILesson | null;
  recording: IRecording | null;
};
