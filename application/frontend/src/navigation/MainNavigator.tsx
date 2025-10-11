/**
 * Main Navigator with Bottom Tabs and Stack Navigators
 */

import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { colors } from '../theme/colors';
import { spacing } from '../theme/spacing';

// Screens
import DashboardScreen from '../screens/dashboard/DashboardScreen';
import PhotoshootCreateScreen from '../screens/photoshoot/PhotoshootCreateScreen';
import PhotoshootDetailsScreen from '../screens/photoshoot/PhotoshootDetailsScreen';
import GalleryScreen from '../screens/gallery/GalleryScreen';
import ProfileScreen from '../screens/profile/ProfileScreen';
import PaymentScreen from '../screens/payment/PaymentScreen';

export type MainTabParamList = {
  Dashboard: undefined;
  Create: undefined;
  Gallery: undefined;
  Profile: undefined;
};

export type MainStackParamList = {
  MainTabs: undefined;
  PhotoshootDetails: { photoshootId: string };
  Payment: undefined;
};

const Tab = createBottomTabNavigator<MainTabParamList>();
const Stack = createStackNavigator<MainStackParamList>();

const MainTabs: React.FC = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: string;

          switch (route.name) {
            case 'Dashboard':
              iconName = focused ? 'view-dashboard' : 'view-dashboard-outline';
              break;
            case 'Create':
              iconName = focused ? 'plus-circle' : 'plus-circle-outline';
              break;
            case 'Gallery':
              iconName = focused ? 'image-multiple' : 'image-multiple-outline';
              break;
            case 'Profile':
              iconName = focused ? 'account' : 'account-outline';
              break;
            default:
              iconName = 'circle';
          }

          return <Icon name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: colors.primary.main,
        tabBarInactiveTintColor: colors.gray[400],
        tabBarStyle: {
          height: 60,
          paddingBottom: spacing.sm,
          paddingTop: spacing.xs,
        },
        headerShown: false,
      })}
    >
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ title: 'Home' }}
      />
      <Tab.Screen
        name="Create"
        component={PhotoshootCreateScreen}
        options={{ title: 'Create' }}
      />
      <Tab.Screen
        name="Gallery"
        component={GalleryScreen}
        options={{ title: 'Gallery' }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: 'Profile' }}
      />
    </Tab.Navigator>
  );
};

const MainNavigator: React.FC = () => {
  return (
    <Stack.Navigator
      screenOptions={{
        headerShown: false,
      }}
    >
      <Stack.Screen name="MainTabs" component={MainTabs} />
      <Stack.Screen
        name="PhotoshootDetails"
        component={PhotoshootDetailsScreen}
        options={{
          headerShown: true,
          title: 'Photoshoot Details',
        }}
      />
      <Stack.Screen
        name="Payment"
        component={PaymentScreen}
        options={{
          headerShown: true,
          title: 'Buy Credits',
        }}
      />
    </Stack.Navigator>
  );
};

export default MainNavigator;

