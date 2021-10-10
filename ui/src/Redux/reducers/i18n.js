import immutable from 'seamless-immutable';
import { createReducer, createActions } from 'reduxsauce';
import { i18nContent } from '../../I18n';

const { Types, Creators } = createActions({
  i18nLanguage: ['language'],
  i18nClear: [],
});
const INITIAL_STATE = immutable({
  language: 'en',
  content: i18nContent['en'],
  error: false,
  errorMessage: null,
});

function clear(state, action) {
  return INITIAL_STATE;
}
function setLanguage(state, action) {
  const { language } = action;
  switch (language) {
    case 'es':
      return state.merge({
        language: 'es',
        content: i18nContent['es'],
      });
    default:
      return state.merge({
        language: 'en',
        content: i18nContent['en'],
      });
  }
}

const HANDLERS = {
  [Types.I18N_CLEAR]: clear,
  [Types.I18N_LANGUAGE]: setLanguage,
};

export const I18n = Creators;
export const i18nTypes = Types;
export default createReducer(INITIAL_STATE, HANDLERS);
