import { AppRegistry } from 'react-native';
import { utils } from '@brunswick/engage-core-app';

import App from './App';
import { name as appName } from './app.json';

const AppWithCodepush = utils.createAppWithCodepush(App);

AppRegistry.registerComponent(appName, () => AppWithCodepush);