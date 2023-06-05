export type IStudent = {
  id: string;
  customer_id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  email_lesson_reminders: boolean;
  email_lesson_notes: boolean;
  status: string;
  customer_type: string;
  created_at: Date;
  last_updated_at: Date;
  gender: string;
  student_type: string;
  teachers: string[];
};

export type IStudentState = {
  isLoading: boolean;
  error: Error | string | null;
  students: IStudent[];
  student: IStudent | null;
};
