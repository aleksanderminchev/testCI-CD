// ----------------------------------------------------------------------
import { ICustomer } from './customer';

export type IInvoiceAddress = {
  id: string;
  name: string;
  address: string;
  company: string;
  email: string;
  phone: string;
};

export type IInvoiceItem = {
  id: string;
  title: string;
  description: string;
  quantity: number;
  price: number;
  total: number;
  service: string;
};

export type IInvoice = {
  id: string;
  customer_id: string;
  type_order: string;
  email: string;
  email_sent: boolean;
  name: string;
  total_price: number;
  stripe_invoice_id: string;
  total_hours: number;
  installments: number;
  discount: string | undefined;
  status: string;
  created_at: Date;
  last_updated: Date;
};
export type IInvoicePagination = {
  data: IInvoice[];
  page: number;
  offset: number;
  total: number;
};
export type IInvoiceState = {
  isLoading: boolean;
  error: Error | string | null;
  invoices: IInvoicePagination;
  customerInvoices: IInvoicePagination;
  invoice: IInvoice | null;
};
