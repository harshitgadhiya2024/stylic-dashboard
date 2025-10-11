/**
 * Root Navigator
 */

import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useAppDispatch, useAppSelector } from '../store/hooks';
import { setUser, setTokens } from '../store/slices/authSlice';
import config from '../constants/config';
import AuthNavigator from './AuthNavigator';
import MainNavigator from './MainNavigator';
import Loading from '../components/common/Loading';

const Stack = createStackNavigator();

const RootNavigator: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isAuthenticated } = useAppSelector((state) => state.auth);
  const [isLoading, setIsLoading] = React.useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const [accessToken, refreshToken, userStr] = await AsyncStorage.multiGet([
        config.storageKeys.accessToken,
        config.storageKeys.refreshToken,
        config.storageKeys.user,
      ]);

      if (accessToken[1] && refreshToken[1] && userStr[1]) {
        dispatch(setTokens({
          accessToken: accessToken[1],
          refreshToken: refreshToken[1],
        }));
        dispatch(setUser(JSON.parse(userStr[1])));
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loading fullScreen message="Loading..." />;
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {isAuthenticated ? (
          <Stack.Screen name="Main" component={MainNavigator} />
        ) : (
          <Stack.Screen name="Auth" component={AuthNavigator} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default RootNavigator;

