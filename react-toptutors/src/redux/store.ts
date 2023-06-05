// Import necessary dependencies from Redux and Redux Persist
import { configureStore } from '@reduxjs/toolkit';
import {
  TypedUseSelectorHook,
  useDispatch as useAppDispatch,
  useSelector as useAppSelector,
} from 'react-redux';
import { persistStore, persistReducer } from 'redux-persist';
import rootReducer, { rootPersistConfig } from './rootReducer';
import * as Sentry from '@sentry/react';

// ----------------------------------------------------------------------
// Define RootState type, which is derived from the rootReducer
export type RootState = ReturnType<typeof rootReducer>;

// Define AppDispatch type, which is derived from the store.dispatch function
export type AppDispatch = typeof store.dispatch;

// Create a Sentry Redux enhancer
const sentryReduxEnhancer = Sentry.createReduxEnhancer({
  // Optionally pass options listed in Sentry Docs here
});

// Configure the Redux store with the persisted rootReducer and middleware options
const store = configureStore({
  reducer: persistReducer(rootPersistConfig, rootReducer),
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
      immutableCheck: false,
    }),
  // The Sentry Redux enhancer
  enhancers: (defaultEnhancers) => [sentryReduxEnhancer, ...defaultEnhancers],
});

// Create a persistor instance to handle the persistence of the store
const persistor = persistStore(store);

// Destructure the dispatch function from the store
const { dispatch } = store;

// Create a typed useSelector hook with RootState type
const useSelector: TypedUseSelectorHook<RootState> = useAppSelector;

const useDispatch = () => useAppDispatch<AppDispatch>();

export { store, persistor, dispatch, useSelector, useDispatch };
