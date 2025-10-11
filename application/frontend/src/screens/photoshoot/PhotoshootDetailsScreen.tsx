/**
 * Photoshoot Details Screen
 */

import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Alert,
  Dimensions,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import Toast from 'react-native-toast-message';
import { useRoute, useNavigation } from '@react-navigation/native';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { fetchPhotoshootById, deletePhotoshoot } from '../../store/slices/photoshootSlice';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Loading from '../../components/common/Loading';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

const { width } = Dimensions.get('window');
const imageSize = (width - spacing.lg * 3) / 2;

const PhotoshootDetailsScreen: React.FC = () => {
  const route = useRoute();
  const navigation = useNavigation();
  const dispatch = useAppDispatch();
  const { currentPhotoshoot, isLoading } = useAppSelector((state) => state.photoshoot);

  const photoshootId = (route.params as any)?.photoshootId;

  useEffect(() => {
    if (photoshootId) {
      dispatch(fetchPhotoshootById(photoshootId));
    }
  }, [photoshootId]);

  const handleDownloadImage = async (imageUrl: string) => {
    Toast.show({
      type: 'info',
      text1: 'Download Started',
      text2: 'Image is being downloaded',
    });
    // Implement download logic
  };

  const handleDownloadAll = async () => {
    Toast.show({
      type: 'info',
      text1: 'Download Started',
      text2: 'All images are being downloaded',
    });
    // Implement download all logic
  };

  const handleDelete = () => {
    Alert.alert(
      'Delete Photoshoot',
      'Are you sure you want to delete this photoshoot? This action cannot be undone.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Delete',
          style: 'destructive',
          onPress: async () => {
            try {
              await dispatch(deletePhotoshoot(photoshootId)).unwrap();
              Toast.show({
                type: 'success',
                text1: 'Deleted',
                text2: 'Photoshoot deleted successfully',
              });
              navigation.goBack();
            } catch (error: any) {
              Toast.show({
                type: 'error',
                text1: 'Delete Failed',
                text2: error,
              });
            }
          },
        },
      ]
    );
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

  if (isLoading || !currentPhotoshoot) {
    return <Loading fullScreen message="Loading photoshoot..." />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Icon name="arrow-left" size={24} color={colors.text.primary} />
        </TouchableOpacity>
        <Text style={styles.title}>Photoshoot Details</Text>
        <TouchableOpacity onPress={handleDelete}>
          <Icon name="delete" size={24} color={colors.error.main} />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <Card style={styles.infoCard}>
          <View style={styles.statusRow}>
            <Text style={styles.label}>Status</Text>
            <View
              style={[
                styles.statusBadge,
                { backgroundColor: getStatusColor(currentPhotoshoot.status) + '20' },
              ]}
            >
              <Text
                style={[
                  styles.statusText,
                  { color: getStatusColor(currentPhotoshoot.status) },
                ]}
              >
                {currentPhotoshoot.status.toUpperCase()}
              </Text>
            </View>
          </View>

          <View style={styles.infoRow}>
            <Icon name="tshirt-crew" size={20} color={colors.text.secondary} />
            <Text style={styles.infoText}>{currentPhotoshoot.garment_type}</Text>
          </View>

          <View style={styles.infoRow}>
            <Icon name="human" size={20} color={colors.text.secondary} />
            <Text style={styles.infoText}>
              {currentPhotoshoot.gender} • {currentPhotoshoot.age_group}
            </Text>
          </View>

          <View style={styles.infoRow}>
            <Icon name="earth" size={20} color={colors.text.secondary} />
            <Text style={styles.infoText}>{currentPhotoshoot.ethnicity}</Text>
          </View>

          <View style={styles.infoRow}>
            <Icon name="calendar" size={20} color={colors.text.secondary} />
            <Text style={styles.infoText}>
              {new Date(currentPhotoshoot.created_at).toLocaleDateString()}
            </Text>
          </View>

          {currentPhotoshoot.estimated_cost && (
            <View style={styles.infoRow}>
              <Icon name="currency-inr" size={20} color={colors.text.secondary} />
              <Text style={styles.infoText}>
                Estimated Cost: ₹{currentPhotoshoot.estimated_cost}
              </Text>
            </View>
          )}
        </Card>

        {currentPhotoshoot.generated_images &&
          currentPhotoshoot.generated_images.length > 0 && (
            <>
              <View style={styles.sectionHeader}>
                <Text style={styles.sectionTitle}>
                  Generated Images ({currentPhotoshoot.generated_images.length})
                </Text>
                <Button
                  title="Download All"
                  onPress={handleDownloadAll}
                  variant="outline"
                  size="sm"
                />
              </View>

              <View style={styles.imagesGrid}>
                {currentPhotoshoot.generated_images.map((imageUrl: string, index: number) => (
                  <TouchableOpacity
                    key={index}
                    style={styles.imageWrapper}
                    onPress={() => handleDownloadImage(imageUrl)}
                  >
                    <Image source={{ uri: imageUrl }} style={styles.image} />
                    <View style={styles.imageOverlay}>
                      <Icon name="download" size={24} color={colors.white} />
                    </View>
                  </TouchableOpacity>
                ))}
              </View>
            </>
          )}

        {currentPhotoshoot.status === 'processing' && (
          <Card style={styles.processingCard}>
            <Icon name="clock-outline" size={48} color={colors.warning.main} />
            <Text style={styles.processingTitle}>Processing</Text>
            <Text style={styles.processingText}>
              Your photoshoot is being generated. This may take a few minutes.
            </Text>
          </Card>
        )}

        {currentPhotoshoot.status === 'failed' && (
          <Card style={styles.errorCard}>
            <Icon name="alert-circle" size={48} color={colors.error.main} />
            <Text style={styles.errorTitle}>Generation Failed</Text>
            <Text style={styles.errorText}>
              {currentPhotoshoot.error_message ||
                'Something went wrong while generating your photoshoot.'}
            </Text>
          </Card>
        )}
      </ScrollView>
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
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
  content: {
    flex: 1,
    padding: spacing.lg,
  },
  infoCard: {
    padding: spacing.lg,
    marginBottom: spacing.lg,
  },
  statusRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  label: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text.primary,
  },
  statusBadge: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: spacing.borderRadius.full,
  },
  statusText: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
  },
  infoRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  infoText: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
    marginLeft: spacing.sm,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
  imagesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -spacing.xs,
  },
  imageWrapper: {
    width: imageSize,
    height: imageSize,
    margin: spacing.xs,
    borderRadius: spacing.borderRadius.md,
    overflow: 'hidden',
    position: 'relative',
  },
  image: {
    width: '100%',
    height: '100%',
    backgroundColor: colors.gray[100],
  },
  imageOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    alignItems: 'center',
    justifyContent: 'center',
    opacity: 0,
  },
  processingCard: {
    padding: spacing.xl,
    alignItems: 'center',
    marginTop: spacing.lg,
  },
  processingTitle: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginTop: spacing.md,
  },
  processingText: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
    textAlign: 'center',
    marginTop: spacing.sm,
  },
  errorCard: {
    padding: spacing.xl,
    alignItems: 'center',
    marginTop: spacing.lg,
  },
  errorTitle: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginTop: spacing.md,
  },
  errorText: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
    textAlign: 'center',
    marginTop: spacing.sm,
  },
});

export default PhotoshootDetailsScreen;

