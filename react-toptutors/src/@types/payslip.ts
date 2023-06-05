import { ITutor } from './tutor';

export type IPayslip = {
  id: string;
  created_at: Date;
  last_updated: Date;
  start_date: Date;
  payment_date: Date;
  end_date: Date;
  teacher_id: string;
  amount: number;
  hours: number;
  referrals_amount: number;
  referrals_number: number;
};
export type ITemporaryPayslip = {
  id: string;
  teacher_id: string;
  unpaid_hours: number;
  unpaid_wage: number;
  paid_wage: number;
  referrals_amount_paid: number;
  referrals_number_paid: number;
  referrals_amount_unpaid: number;
  referrals_number_unpaid: number;
  paid_hours: number;
  start_date: Date;
  end_date: Date;
};
export type IPayslipState = {
  isLoading: boolean;
  error: Error | string | null;
  temporaryPayslips: ITemporaryPayslip[];
  payslips: IPayslip[];
  payslip: IPayslip | null;
};
