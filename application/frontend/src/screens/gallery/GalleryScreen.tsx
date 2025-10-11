/**
 * Gallery Screen
 */

import React, { useEffect } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Image } from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { fetchPhotoshoots } from '../../store/slices/photoshootSlice';
import Card from '../../components/common/Card';
import Loading from '../../components/common/Loading';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

const GalleryScreen: React.FC = () => {
  const navigation = useNavigation();
  const dispatch = useAppDispatch();
  const { photoshoots, isLoading } = useAppSelector((state) => state.photoshoot);

  useEffect(() => {
    dispatch(fetchPhotoshoots({}));
  }, []);

  const handleRefresh = () => {
    dispatch(fetchPhotoshoots({}));
  };

  const handlePhotoshootPress = (photoshootId: string) => {
    navigation.navigate('PhotoshootDetails' as never, { photoshootId } as never);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return colors.success.main;
      case 'processing':
        return colors.warning.main;
      case 'failed':
        return colors.error.main;
      default:
        return colors.gray[500];
    }
  };

  if (isLoading && photoshoots.length === 0) {
    return <Loading fullScreen message="Loading gallery..." />;
  }

  const renderItem = ({ item }: any) => (
    <TouchableOpacity
      onPress={() => handlePhotoshootPress(item.photoshoot_id)}
      activeOpacity={0.8}
    >
      <Card style={styles.card}>
        {item.generated_images && item.generated_images.length > 0 && (
          <Image
            source={{ uri: item.generated_images[0] }}
            style={styles.thumbnail}
          />
        )}
        <View style={styles.cardContent}>
          <View style={styles.cardHeader}>
            <Text style={styles.cardTitle}>{item.garment_type}</Text>
            <View
              style={[
                styles.statusBadge,
                { backgroundColor: getStatusColor(item.status) + '20' },
              ]}
            >
              <Text
                style={[styles.statusText, { color: getStatusColor(item.status) }]}
              >
                {item.status.toUpperCase()}
              </Text>
            </View>
          </View>

          <View style={styles.cardDetails}>
            <View style={styles.detailRow}>
              <Icon name="human" size={16} color={colors.text.secondary} />
              <Text style={styles.detailText}>
                {item.gender} • {item.age_group}
              </Text>
            </View>
            <View style={styles.detailRow}>
              <Icon name="calendar" size={16} color={colors.text.secondary} />
              <Text style={styles.detailText}>
                {new Date(item.created_at).toLocaleDateString()}
              </Text>
            </View>
          </View>

          {item.generated_images && item.generated_images.length > 0 && (
            <View style={styles.imageCount}>
              <Icon name="image-multiple" size={16} color={colors.primary.main} />
              <Text style={styles.imageCountText}>
                {item.generated_images.length} images
              </Text>
            </View>
          )}
        </View>
      </Card>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Gallery</Text>
        <TouchableOpacity onPress={handleRefresh}>
          <Icon name="refresh" size={24} color={colors.primary.main} />
        </TouchableOpacity>
      </View>

      {photoshoots.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Icon name="image-off" size={64} color={colors.gray[300]} />
          <Text style={styles.emptyText}>No photoshoots yet</Text>
          <Text style={styles.emptySubtext}>Create your first photoshoot to get started</Text>
        </View>
      ) : (
        <FlatList
          data={photoshoots}
          renderItem={renderItem}
          keyExtractor={(item) => item.photoshoot_id}
          contentContainerStyle={styles.list}
          refreshing={isLoading}
          onRefresh={handleRefresh}
        />
      )}
    </View>
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
    backgroundColor: colors.white,
  },
  title: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
  list: {
    padding: spacing.lg,
  },
  card: {
    marginBottom: spacing.md,
    padding: 0,
    overflow: 'hidden',
  },
  thumbnail: {
    width: '100%',
    height: 200,
    backgroundColor: colors.gray[100],
  },
  cardContent: {
    padding: spacing.md,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  cardTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text.primary,
  },
  statusBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: spacing.borderRadius.full,
  },
  statusText: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
  },
  cardDetails: {
    marginBottom: spacing.sm,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  detailText: {
    fontSize: typography.fontSize.sm,
    color: colors.text.secondary,
    marginLeft: spacing.xs,
  },
  imageCount: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  imageCountText: {
    fontSize: typography.fontSize.sm,
    color: colors.primary.main,
    marginLeft: spacing.xs,
    fontWeight: typography.fontWeight.medium,
  },
  emptyContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  emptyText: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text.primary,
    marginTop: spacing.md,
    marginBottom: spacing.xs,
  },
  emptySubtext: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
    textAlign: 'center',
  },
});

export default GalleryScreen;

