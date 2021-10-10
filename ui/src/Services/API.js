import { create } from 'apisauce';
import { store } from '../Redux/store';
import { getServer } from '../Utils/url';

export const token = () => store.getState().auth.token;
// Define the api
const API = create({
  baseURL: getServer(),
});

export async function login(email, password) {
  return await API.post('/auth', { email, password });
}
