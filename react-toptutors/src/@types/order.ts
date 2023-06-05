// ----------------------------------------------------------------------
import { ICustomer } from './customer';

export type IOrderAddress = {
  id: string;
  name: string;
  address: string;
  company: string;
  email: string;
  phone: string;
};

export type IOrderItem = {
  id: string;
  title: string;
  description: string;
  quantity: number;
  price: number;
  total: number;
  service: string;
};

export type IOrder = {
  id: string;
  customer_id: string;
  type_order: string;
  name: string;
  total_price: number;
  stripe_order_id: string;
  total_hours: number;
  installments: number;
  discount: string;
  status: string;
  created_at: Date;
  last_updated: Date;
};
export type IOrderPagination = {
  data: IOrder[];
  page: number;
  offset: number;
  total: number;
};
export type IOrderState = {
  isLoading: boolean;
  error: Error | string | null;
  orders: IOrderPagination;
  customerOrders: IOrderPagination;
  order: IOrder | null;
};
