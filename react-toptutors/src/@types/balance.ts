// ----------------------------------------------------------------------
import { ICustomer } from './customer';

export type IBalanceAddress = {
  id: string;
  name: string;
  address: string;
  company: string;
  email: string;
  phone: string;
};

export type IBalanceItem = {
  id: string;
  title: string;
  description: string;
  quantity: number;
  price: number;
  total: number;
  service: string;
};

export type IBalance = {
  id: string;
  customer_id: string;
  customer: ICustomer;
  hours_used: number;
  hours_scheduled: number;
  hours_ordered: number;
  hours_free: number;
  invoice_balance: string;
};
export type IBalancePagination = {
  data: IBalance[];
  page: number;
  offset: number;
  total: number;
};
export type IBalanceState = {
  isLoading: boolean;
  error: Error | string | null;
  balances: IBalancePagination;
  balance: IBalance | null;
};
