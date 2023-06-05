// ----------------------------------------------------------------------
import { ICustomer } from './customer';

export type ITransactionAddress = {
  id: string;
  name: string;
  address: string;
  company: string;
  email: string;
  phone: string;
};

export type ITransactionItem = {
  id: string;
  title: string;
  description: string;
  quantity: number;
  price: number;
  total: number;
  service: string;
};

export type ITransaction = {
  id: string;
  customer_id: string;
  type_transaction: string;
  customer: ICustomer;
  amount: number;
  stripe_transaction_id: string;
  currency: string;
  void: boolean;
  method: string;
  created_at: Date;
  last_updated: Date;
};
export type ITransactionPagination = {
  data: ITransaction[];
  page: number;
  offset: number;
  total: number;
};
export type ITransactionState = {
  isLoading: boolean;
  error: Error | string | null;
  transactions: ITransactionPagination;
  customerTransactions: ITransactionPagination;
  transaction: ITransaction | null;
};
