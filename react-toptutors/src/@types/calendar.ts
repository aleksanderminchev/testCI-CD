import { EventInput } from '@fullcalendar/core';

// ----------------------------------------------------------------------

export type ICalendarViewValue = 'dayGridMonth' | 'timeGridWeek' | 'timeGridDay' | 'listWeek';

export type ICalendarEvent = EventInput & {
  title: string;
  title_data: string;
  description: string;
  color: string;
  studentId: { code: string; label: string; priority: string };
  studentName: string;
  teacherId: { code: string; label: string; priority: string };
  teacherName: string;
  completionNotes: string;
  paid: boolean;
  trial_lesson: boolean;
  start: Date | string;
  end: Date | string;
};
export type ILesson = {
  data: [
    {
      id: number;
      space: string;
      duration_in_minutes: number;
      wage: number;
      status: string;
      created_at: Date;
      last_updated: Date;
      completed_at: Date;
      from_time: Date;
      to_time: Date;
      lesson_reminder_sent_at: Date;
      teacher: {
        id: number;
        email: string;
        languages: [
          {
            id: number;
            language: string;
          }
        ];
        qualifications: [
          {
            id: number;
            qualification: string;
          }
        ];
        subjects: [
          {
            id: number;
            subject: string;
          }
        ];
        interests: [
          {
            id: number;
            interest: string;
          }
        ];
        hire_date: Date;
        wage_per_hour: number;
        bio: string;
        photo: string;
        phone: string;
        open_for_new_students: boolean;
        gender: string;
        status: string;
        payroll_id: string;
        higher_education_institution: string;
        higher_education_programme: string;
        high_school: string;
        finished_highschool: boolean;
        age: number;
        birthday: Date;
        updated_on_tw_at: Date;
        created_on_tw_at: Date;
      };
      student: {
        email: string;
        gender: string;
        first_name: string;
        last_name: string;
        id: number;
        phone: string;
        email_lesson_reminders: boolean;
        created_at: Date;
        last_updated_at: Date;
        email_lesson_notes: boolean;
        status: string;
        student_type: string;
      };
    }
  ];
};

export type ICalendarState = {
  isLoading: boolean;
  error: Error | string | null;
  events: ICalendarEvent[];
  teachers: [];
  students: [];
  customers: [];
};
