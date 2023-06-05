import { createContext, useEffect, useReducer, useCallback, useMemo } from 'react';
import { Buffer } from 'buffer';

// utils
import axios from '../utils/axios';
import localStorageAvailable from '../utils/localStorageAvailable';
import { setSession } from './utils';
import { ActionMapType, AuthStateType, AuthUserType, JWTContextType } from './types';

// ----------------------------------------------------------------------

// The Types enum contains string values for four different types of actions: INITIAL, LOGIN, REGISTER, and LOGOUT.
enum Types {
  INITIAL = 'INITIAL',
  LOGIN = 'LOGIN',
  REGISTER = 'REGISTER',
  LOGOUT = 'LOGOUT',
}

// The Payload type is an object with keys that correspond to the values in the Types enum.
// The values for each key in Payload are objects that contain information relevant to each action type.
// For example, for the LOGIN action type, there is a user property with a value of type AuthUserType.
type Payload = {
  [Types.INITIAL]: {
    isAuthenticated: boolean;
    user: AuthUserType;
  };
  [Types.LOGIN]: {
    user: AuthUserType;
  };
  [Types.REGISTER]: {
    user: AuthUserType;
  };
  [Types.LOGOUT]: undefined;
};

// The ActionsType type is the result of mapping the Payload object to the ActionMapType type, and taking the key of the resulting object.
// It represents a union of all possible actions that can be dispatched in the application.
type ActionsType = ActionMapType<Payload>[keyof ActionMapType<Payload>];

// ----------------------------------------------------------------------

// The initial state of the application.
const initialState: AuthStateType = {
  isInitialized: false,
  isAuthenticated: false,
  user: null,
};

const reducer = (state: AuthStateType, action: ActionsType) => {
  if (action.type === Types.INITIAL) {
    return {
      isInitialized: true,
      isAuthenticated: action.payload.isAuthenticated,
      user: action.payload.user,
    };
  }
  if (action.type === Types.LOGIN) {
    return {
      ...state,
      isAuthenticated: true,
      user: action.payload.user,
    };
  }
  if (action.type === Types.REGISTER) {
    return {
      ...state,
      isAuthenticated: true,
      user: action.payload.user,
    };
  }
  if (action.type === Types.LOGOUT) {
    return {
      ...state,
      isAuthenticated: false,
      user: null,
    };
  }
  return state;
};

// ----------------------------------------------------------------------

export const AuthContext = createContext<JWTContextType | null>(null);

// ----------------------------------------------------------------------

type AuthProviderProps = {
  children: React.ReactNode;
};

export function AuthProvider({ children }: AuthProviderProps) {
  const [state, dispatch] = useReducer(reducer, initialState);

  const storageAvailable = localStorageAvailable();

  const initialize = useCallback(async () => {
    try {
      const accessToken = storageAvailable ? localStorage.getItem('accessToken') : '';

      // Checks if the user is authenticated
      if (accessToken) {
        setSession(accessToken);

        // Get user data
        const response = await axios.get('https://localhost:8081/api/me', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
          withCredentials: true,
        });

        const user = response.data;

        if (user.is_verified) {
          dispatch({
            type: Types.INITIAL,
            payload: {
              isAuthenticated: user.is_verified,
              user,
            },
          });
        } else {
          throw Error(`User is not authenticated`);
        }
      } else {
        dispatch({
          type: Types.INITIAL,
          payload: {
            isAuthenticated: false,
            user: null,
          },
        });
      }
    } catch (error) {
      dispatch({
        type: Types.INITIAL,
        payload: {
          isAuthenticated: false,
          user: null,
        },
      });
    }
  }, [storageAvailable]);

  useEffect(() => {
    initialize();
  }, [initialize]);

  // LOGIN
  /** Login by sending a POST request to /api/tokens
   * Passing the username and password in a standard basic authentication header.
   */
  const login = useCallback(async (email: string, password: string) => {
    const response = await axios.post('https://localhost:8081/api/tokens', null, {
      headers: {
        Authorization: `Basic ${Buffer.from(`${email}:${password}`).toString('base64')}`,
      },
      withCredentials: true,
    });

    const accessToken = response.data;
    // Sets the access token to local storage.
    setSession(accessToken.access_token);
    if (accessToken) {
      // Get user data
      const userResponse = await axios.get('https://localhost:8081/api/me', {
        headers: {
          Authorization: `Bearer ${accessToken.access_token}`,
          'Content-Type': 'application/json',
        },
        withCredentials: true,
      });

      const user = userResponse.data;
      if (user.is_verified) {
        dispatch({
          type: Types.INITIAL,
          payload: {
            isAuthenticated: user.is_verified,
            user,
          },
        });
      } else {
        throw Error(`User is not authenticated`);
      }
    } else {
      dispatch({
        type: Types.INITIAL,
        payload: {
          isAuthenticated: false,
          user: null,
        },
      });
    }
  }, []);
  // Confirmation
  /** Confirmation by sending a PUT request to /api/tokens/confirmation
   * Passing the username, password and confirmPassword in a standard basic authentication header.
   */
  const confirmation = useCallback(
    async (email: string, password: string, confirmPassword: string, token: string) => {
      const response = await axios.put('https://localhost:8081/api/tokens/confirmation', {
        email: email,
        password: password,
        confirm: confirmPassword,
        token: token,
      });

      // Sets the access token to local storage.
      if (response.status === 200) {
        return true;
      } else {
        dispatch({
          type: Types.INITIAL,
          payload: {
            isAuthenticated: false,
            user: null,
          },
        });
        return false;
      }
    },
    []
  );
  // REGISTER
  const register = useCallback(
    async (email: string, password: string, firstName: string, lastName: string) => {
      const response = await axios.post('/api/users', {
        email,
        password,
        first_name: firstName,
        last_name: lastName,
      });

      const { access_token: accessToken } = response.data;

      localStorage.setItem('accessToken', accessToken);

      dispatch({
        type: Types.REGISTER,
        payload: {
          user: null,
        },
      });
    },
    []
  );

  // LOGOUT
  const logout = useCallback(() => {
    const logoutServer = async () => {
      await axios.delete('https://localhost:8081/api/tokens');
    };

    logoutServer().then(() => {
      // Delete access token from local storage and axios default header
      setSession(null);
      dispatch({
        type: Types.LOGOUT,
      });
    });
  }, []);

  // eslint-disable-next-line @typescript-eslint/no-empty-function
  const noop = () => {};

  const memoizedValue = useMemo(
    () => ({
      isInitialized: state.isInitialized,
      isAuthenticated: state.isAuthenticated,
      user: state.user,
      method: 'jwt',
      login,
      confirmation,
      loginWithGoogle: noop,
      loginWithGithub: noop,
      loginWithTwitter: noop,
      register,
      logout,
    }),
    [state.isAuthenticated, state.isInitialized, state.user, login, logout, register, confirmation]
  );

  return <AuthContext.Provider value={memoizedValue}>{children}</AuthContext.Provider>;
}
