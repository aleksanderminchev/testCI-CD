// ----------------------------------------------------------------------

// The ActionMapType type is a generic type that maps a given object M to an action object.
// If the value of a key in M is undefined, the action object will have a type property with the key as the value.
// If the value of a key in M is not undefined,
// the action object will have two properties:
// a type property with the key as the value and a payload property with the value of the key.
export type ActionMapType<M extends { [index: string]: any }> = {
  [Key in keyof M]: M[Key] extends undefined
    ? {
        type: Key;
      }
    : {
        type: Key;
        payload: M[Key];
      };
};

// The AuthUserType type is a union type that can be either null or a Record with a string index and values of any type.
export type AuthUserType = null | Record<string, any>;

// The AuthStateType type is an object that contains information about the authentication state of the application. It has three properties:
export type AuthStateType = {
  isAuthenticated: boolean;
  isInitialized: boolean;
  user: AuthUserType;
};

// ----------------------------------------------------------------------

export type JWTContextType = {
  method: string;
  isAuthenticated: boolean;
  isInitialized: boolean;
  user: AuthUserType;
  login: (email: string, password: string) => Promise<void>;
  confirmation: (
    email: string,
    password: string,
    confirmationPassword: string,
    token: string
  ) => Promise<boolean>;
  register: (email: string, password: string, firstName: string, lastName: string) => Promise<void>;
  logout: () => void;
  loginWithGoogle?: () => void;
  loginWithGithub?: () => void;
  loginWithTwitter?: () => void;
};
