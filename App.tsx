import React, { useEffect, useState } from 'react';
import { useWindowDimensions, Platform, StatusBar } from 'react-native';

// import from engage core app
import { Block, UIText } from '@brunswick/react-native-ui-kit';
import { CodepushStatus } from '@brunswick/engage-core-app/lib/src/types';

import Splash from './src/screens/splash';

interface IApp {
  codePushStatus: CodepushStatus;
}

const App = ({ codePushStatus }: IApp) => {
  const [loadSplash, setLoadSplash] = useState(true);
  const { height, width } = useWindowDimensions();
  const bottomBarHeight = 50;

  /**
  * Hiding the splash screen animation.
  */
   const hideSplash = () => {
    setTimeout(() => setLoadSplash(false), 2000);
  };

  useEffect(() => {
    hideSplash ();
  }, []);

  useEffect(() => {
    if (Platform.OS === 'android') {
      StatusBar.setBackgroundColor('transparent');
      StatusBar.setTranslucent(true);
    }
  }, []);

  

  return (
    <>
      <Block style={{ display:'flex', flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <UIText typography='h0'>Welcome</UIText>
      </Block>
      {loadSplash && (
        <Block style={{ position: 'absolute', height: height + bottomBarHeight, width, zIndex: 1 }}>
          <Splash />
        </Block>
      )}
    </>
  );
};

export default App;
