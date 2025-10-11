/**
 * Main App Component
 */

import React from 'react';
import { StatusBar } from 'react-native';
import { Provider as ReduxProvider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import Toast from 'react-native-toast-message';
import { store, persistor } from './store/store';
import RootNavigator from './navigation/RootNavigator';
import Loading from './components/common/Loading';
import { colors } from './theme/colors';

const App: React.FC = () => {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <ReduxProvider store={store}>
        <PersistGate loading={<Loading fullScreen />} persistor={persistor}>
          <StatusBar
            barStyle="dark-content"
            backgroundColor={colors.background.default}
          />
          <RootNavigator />
          <Toast />
        </PersistGate>
      </ReduxProvider>
    </GestureHandlerRootView>
  );
};

export default App;

