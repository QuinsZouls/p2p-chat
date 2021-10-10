import { combineReducers } from 'redux';
import { connectRouter } from 'connected-react-router';

import auth from './auth';
import i18n from './i18n';

const reducer = (history) =>
  combineReducers({
    router: connectRouter(history),
    auth,
    i18n,
  });

export default reducer;
