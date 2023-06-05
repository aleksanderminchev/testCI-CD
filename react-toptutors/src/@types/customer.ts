export type ICustomer = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  phone: string;
  email_lesson_reminders: boolean;
  email_lesson_notes: boolean;
  status: string;
  customer_type: string;
  created_at: Date;
  last_updated: Date;
  students: string[];
};

export type ICustomerAccountGeneral = {
  id: string;
  // avatarUrl: string;
  first_name: string;
  last_name: string;
  email: string;
  phone: string;
  customer_type: string;
  status: string;
};

export type ICustomerNotificationSettings = {
  email_lesson_reminders: boolean;
  email_lesson_notes: boolean;
};

export type ICustomerListState = {
  byId: Record<string, ICustomer>;
  allIds: string[];
};

/* export type ICustomerState ={
      isLoading:boolean;
      error: Error|string|null;
      customers: ICustomerListState;
      // customer: ICustomer| null;
    } */
export type ICustomerPagination = {
  data: ICustomer[];
  offset: number;
  total: number;
};
export type ICustomerState = {
  isLoading: boolean;
  error: Error | string | null;
  customers: ICustomerPagination;
  customer: ICustomer | null;
};
