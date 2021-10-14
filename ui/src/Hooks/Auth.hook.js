import { useSelector, useDispatch } from 'react-redux';
import { persistor } from '../Redux/store';

import { Auth } from '../Redux/reducers/auth';
export function useAuth() {
  const { auth } = useSelector((state) => ({ auth: state.auth }));
  const dispatch = useDispatch();
  async function post(token) {
    dispatch(Auth.authSuccess(token));
  }
  function logout() {
    dispatch(Auth.authClear());
    persistor.flush();
    persistor.purge();
  }
  return [auth, post, logout];
}
