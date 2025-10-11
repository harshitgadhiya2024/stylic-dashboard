/**
 * Dashboard Screen
 */

import React, { useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { fetchProfile, fetchStatistics } from '../../store/slices/userSlice';
import Card from '../../components/common/Card';
import Loading from '../../components/common/Loading';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

const DashboardScreen: React.FC = () => {
  const navigation = useNavigation();
  const dispatch = useAppDispatch();
  const { profile, credits, statistics, isLoading } = useAppSelector((state) => state.user);

  useEffect(() => {
    dispatch(fetchProfile());
    dispatch(fetchStatistics());
  }, []);

  if (isLoading && !profile) {
    return <Loading fullScreen message="Loading dashboard..." />;
  }

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Hello,</Text>
          <Text style={styles.name}>{profile?.first_name || 'User'}</Text>
        </View>
        <TouchableOpacity style={styles.notificationButton}>
          <Icon name="bell-outline" size={24} color={colors.text.primary} />
        </TouchableOpacity>
      </View>

      {/* Credits Card */}
      <Card style={styles.creditsCard} elevation="md">
        <View style={styles.creditsHeader}>
          <Text style={styles.creditsLabel}>Available Credits</Text>
          <Icon name="wallet-outline" size={24} color={colors.primary.main} />
        </View>
        <Text style={styles.creditsAmount}>{credits}</Text>
        <TouchableOpacity
          style={styles.buyCreditsButton}
          onPress={() => navigation.navigate('Payment' as never)}
        >
          <Text style={styles.buyCreditsText}>Buy Credits</Text>
          <Icon name="plus" size={16} color={colors.primary.main} />
        </TouchableOpacity>
      </Card>

      {/* Statistics */}
      <View style={styles.statsContainer}>
        <Text style={styles.sectionTitle}>Statistics</Text>
        <View style={styles.statsGrid}>
          <Card style={styles.statCard}>
            <Icon name="image-multiple" size={32} color={colors.primary.main} />
            <Text style={styles.statValue}>{statistics?.total_photoshoots || 0}</Text>
            <Text style={styles.statLabel}>Photoshoots</Text>
          </Card>
          <Card style={styles.statCard}>
            <Icon name="image" size={32} color={colors.secondary.main} />
            <Text style={styles.statValue}>{statistics?.total_images || 0}</Text>
            <Text style={styles.statLabel}>Images</Text>
          </Card>
          <Card style={styles.statCard}>
            <Icon name="receipt" size={32} color={colors.success.main} />
            <Text style={styles.statValue}>{statistics?.total_orders || 0}</Text>
            <Text style={styles.statLabel}>Orders</Text>
          </Card>
          <Card style={styles.statCard}>
            <Icon name="currency-usd" size={32} color={colors.warning.main} />
            <Text style={styles.statValue}>₹{statistics?.total_spent || 0}</Text>
            <Text style={styles.statLabel}>Spent</Text>
          </Card>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.actionsContainer}>
        <Text style={styles.sectionTitle}>Quick Actions</Text>
        <Card style={styles.actionCard}>
          <Icon name="plus-circle" size={48} color={colors.primary.main} />
          <Text style={styles.actionTitle}>Create Photoshoot</Text>
          <Text style={styles.actionDescription}>
            Generate AI photoshoots with custom poses
          </Text>
        </Card>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.default,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: spacing.lg,
    paddingTop: spacing.xl,
  },
  greeting: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
  },
  name: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
  notificationButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.white,
    alignItems: 'center',
    justifyContent: 'center',
  },
  creditsCard: {
    margin: spacing.lg,
    padding: spacing.lg,
  },
  creditsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  creditsLabel: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
  },
  creditsAmount: {
    fontSize: typography.fontSize['4xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.primary.main,
    marginBottom: spacing.md,
  },
  buyCreditsButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.sm,
  },
  buyCreditsText: {
    fontSize: typography.fontSize.md,
    color: colors.primary.main,
    fontWeight: typography.fontWeight.semibold,
    marginRight: spacing.xs,
  },
  statsContainer: {
    padding: spacing.lg,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginBottom: spacing.md,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    width: '48%',
    padding: spacing.md,
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  statValue: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginTop: spacing.sm,
  },
  statLabel: {
    fontSize: typography.fontSize.sm,
    color: colors.text.secondary,
    marginTop: spacing.xs,
  },
  actionsContainer: {
    padding: spacing.lg,
  },
  actionCard: {
    padding: spacing.lg,
    alignItems: 'center',
  },
  actionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text.primary,
    marginTop: spacing.md,
  },
  actionDescription: {
    fontSize: typography.fontSize.sm,
    color: colors.text.secondary,
    textAlign: 'center',
    marginTop: spacing.xs,
  },
});

export default DashboardScreen;

