import { persistStore, persistReducer } from 'redux-persist';
import {
  seamlessImmutableReconciler,
  seamlessImmutableTransformCreator,
} from 'redux-persist-seamless-immutable';

import { applyMiddleware, compose, createStore } from 'redux';
import { createBrowserHistory } from 'history';
import { routerMiddleware } from 'connected-react-router';
import storage from 'redux-persist/lib/storage';
import Logger from 'redux-logger';
import thunk from 'redux-thunk';
import Reducers from './reducers';


export const history = createBrowserHistory({
  initialEntries: [{ state: { key: 'home' } }],
});
const transformerConfig = {
  whitelistPerReducer: {
    auth: ['token', 'user', 'role'],
  },
};

const persistConfig = {
  key: 'chat_client',
  storage, // Defaults to localStorage
  stateReconciler: seamlessImmutableReconciler,
  transforms: [seamlessImmutableTransformCreator(transformerConfig)],
  whitelist: ['auth'],
};

const persistedReducer = persistReducer(persistConfig, Reducers(history));

export const store = createStore(
  persistedReducer,
  compose(applyMiddleware(routerMiddleware(history), Logger, thunk))
);

export const persistor = persistStore(store);
