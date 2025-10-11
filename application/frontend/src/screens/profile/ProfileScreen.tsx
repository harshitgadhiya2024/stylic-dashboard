/**
 * Profile Screen
 */

import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { logout } from '../../store/slices/authSlice';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

const ProfileScreen: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);
  const { credits } = useAppSelector((state) => state.user);

  const handleLogout = () => {
    dispatch(logout());
  };

  const menuItems = [
    { icon: 'account-edit', title: 'Edit Profile', onPress: () => {} },
    { icon: 'wallet', title: 'Credit History', onPress: () => {} },
    { icon: 'receipt', title: 'Order History', onPress: () => {} },
    { icon: 'cog', title: 'Settings', onPress: () => {} },
    { icon: 'help-circle', title: 'Help & Support', onPress: () => {} },
  ];

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Icon name="account" size={48} color={colors.white} />
        </View>
        <Text style={styles.name}>
          {user?.first_name} {user?.last_name}
        </Text>
        <Text style={styles.email}>{user?.email}</Text>
      </View>

      <Card style={styles.creditsCard}>
        <View style={styles.creditsRow}>
          <View>
            <Text style={styles.creditsLabel}>Available Credits</Text>
            <Text style={styles.creditsValue}>{credits}</Text>
          </View>
          <Icon name="wallet" size={32} color={colors.primary.main} />
        </View>
      </Card>

      <View style={styles.menu}>
        {menuItems.map((item, index) => (
          <TouchableOpacity
            key={index}
            style={styles.menuItem}
            onPress={item.onPress}
          >
            <View style={styles.menuItemLeft}>
              <Icon name={item.icon} size={24} color={colors.text.primary} />
              <Text style={styles.menuItemText}>{item.title}</Text>
            </View>
            <Icon name="chevron-right" size={24} color={colors.gray[400]} />
          </TouchableOpacity>
        ))}
      </View>

      <Button
        title="Logout"
        onPress={handleLogout}
        variant="outline"
        fullWidth
        style={styles.logoutButton}
      />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.default,
  },
  header: {
    alignItems: 'center',
    padding: spacing.xl,
    paddingTop: spacing['2xl'],
  },
  avatar: {
    width: 96,
    height: 96,
    borderRadius: 48,
    backgroundColor: colors.primary.main,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
  },
  name: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginBottom: spacing.xs,
  },
  email: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
  },
  creditsCard: {
    margin: spacing.lg,
    padding: spacing.lg,
  },
  creditsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  creditsLabel: {
    fontSize: typography.fontSize.sm,
    color: colors.text.secondary,
    marginBottom: spacing.xs,
  },
  creditsValue: {
    fontSize: typography.fontSize['3xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.primary.main,
  },
  menu: {
    backgroundColor: colors.white,
    marginHorizontal: spacing.lg,
    borderRadius: spacing.borderRadius.lg,
    overflow: 'hidden',
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: colors.border.light,
  },
  menuItemLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  menuItemText: {
    fontSize: typography.fontSize.md,
    color: colors.text.primary,
    marginLeft: spacing.md,
  },
  logoutButton: {
    margin: spacing.lg,
  },
});

export default ProfileScreen;

