// utils
import axios from '../utils/axios';

// ----------------------------------------------------------------------

export const setSession = (accessToken: string | null) => {
  // If access token is not null
  if (accessToken) {
    localStorage.setItem('accessToken', accessToken);

    axios.defaults.headers.common.Authorization = `Bearer ${accessToken}`;
  } else {
    localStorage.removeItem('accessToken');

    delete axios.defaults.headers.common.Authorization;
  }
};
