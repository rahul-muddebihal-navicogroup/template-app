import React, { useEffect, useRef } from 'react';
import { Animated, StatusBar, useWindowDimensions } from 'react-native';
import { Block } from '@brunswick/react-native-ui-kit';
import { activeTheme } from '../constants/theme';

const Splash = () => {
  const { assets, colors } = activeTheme;

  const fadeValue = useRef(new Animated.Value(0)).current;

  /**
   * Each time the user opens the app, the splash screen is shown.
   */
  useEffect(() => {
    Animated.sequence([
      Animated.sequence([
        Animated.timing(fadeValue, {
          duration: 400,
          toValue: 1,
          delay: 400,
          useNativeDriver: true,
        }),
        Animated.timing(fadeValue, {
          duration: 800,
          toValue: 0,
          delay: 2500,
          useNativeDriver: true,
        }),
      ]),
    ]).start();
  }, []);

  return (
    <Block flex={1} color={colors.black}>
      <StatusBar barStyle="light-content" />
    </Block>
  );
};

export default Splash;
