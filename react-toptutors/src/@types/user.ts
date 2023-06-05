// ----------------------------------------------------------------------

export type IUser = {
  id: string;
  name: string;
  follower: number;
  following: number;
  totalPosts: number;
  role: string;
};

export type IUserState = {
  isLoading: boolean;
  error: Error | string | null;
  users: IUser[];
  user: IUser | null;
};

// ----------------------------------------------------------------------

export type IUserAccountBillingInvoice = {
  id: string;
  createdAt: Date | string | number;
  price: number;
};

export type IUserAccountChangePassword = {
  oldPassword: string;
  newPassword: string;
  confirmNewPassword: string;
};

// ----------------------------------------------------------------------
