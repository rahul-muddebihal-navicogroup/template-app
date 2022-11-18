import { constants } from '@brunswick/engage-core-app';

const { activeTheme: THEME } = constants.theme;

// This can be modified IF a default values is required to be updated. In case you need to add a new value, then
// modify the related ICoreTheme types first and only after that add it. DO NOT use type any.
export const activeTheme = {
  ...THEME,
};
