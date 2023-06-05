import axios from 'axios';
import { HOST_API_KEY } from '../config-global';
// config

// ----------------------------------------------------------------------

/** creates a new instance of the Axios library with a specified configuration.
 * In this case, the configuration sets the baseURL property to HOST_API_KEY,
 * which is the base URL for all requests made using this Axios instance.
 */
const axiosInstance = axios.create({ baseURL: HOST_API_KEY, withCredentials: true });

/** adds a response interceptor to the Axios instance.
 * This interceptor is a function that will be executed for every HTTP response received by the Axios instance.
 * The function takes two arguments: response and error.
 * If the response is successful, it returns the response object.
 * If the response contains an error. If the error is a 401 authentication, we try to refresh the authentication token.
 * Otherwise it returns a rejected Promise with the error data or a default error message.
 */
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const { status, config } = error.response;

    // If there is an authentication error, we try to refresh the access token.
    console.log(status);
    console.log(config);
    if (status === 401 && config.url === 'https://localhost:8081/api/me') {
      const refreshResponse = await axiosInstance.put(
        'https://localhost:8081/api/tokens',
        {
          access_token: localStorage.getItem('accessToken'),
        },
        {
          withCredentials: true,
        }
      );
      const { access_token: accessToken } = refreshResponse.data;
      localStorage.setItem('accessToken', accessToken);
      const configInput = localStorage.getItem('accessToken');
      console.log(configInput);
      config.headers.Authorization = `Bearer ${configInput}`;

      if (refreshResponse.status === 200) {
        return axiosInstance.request(config);
      }

      return Promise.reject((error.response && error.response.data) || 'Something went wrong');
    }
    return Promise.reject((error.response && error.response.data) || 'Something went wrong');
  }
);

export default axiosInstance;
