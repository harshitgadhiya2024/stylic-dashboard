/**
 * Image Picker Component
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Image,
  ScrollView,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {
  pickImageFromGallery,
  takePhoto,
  showImagePickerOptions,
  ImageFile,
} from '../../utils/imagePickerUtils';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

interface ImagePickerProps {
  label?: string;
  multiple?: boolean;
  maxImages?: number;
  images: ImageFile[];
  onImagesChange: (images: ImageFile[]) => void;
  error?: string;
}

const ImagePickerComponent: React.FC<ImagePickerProps> = ({
  label,
  multiple = false,
  maxImages = 10,
  images,
  onImagesChange,
  error,
}) => {
  const handlePickImage = async () => {
    if (!multiple && images.length >= 1) {
      return;
    }

    if (images.length >= maxImages) {
      return;
    }

    showImagePickerOptions(
      async () => {
        const selectedImages = await pickImageFromGallery(multiple);
        if (selectedImages) {
          const newImages = multiple
            ? [...images, ...selectedImages].slice(0, maxImages)
            : selectedImages;
          onImagesChange(newImages);
        }
      },
      async () => {
        const photo = await takePhoto();
        if (photo) {
          const newImages = multiple ? [...images, photo] : [photo];
          onImagesChange(newImages);
        }
      }
    );
  };

  const handleRemoveImage = (index: number) => {
    const newImages = images.filter((_, i) => i !== index);
    onImagesChange(newImages);
  };

  return (
    <View style={styles.container}>
      {label && <Text style={styles.label}>{label}</Text>}

      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <View style={styles.imagesContainer}>
          {images.map((image, index) => (
            <View key={index} style={styles.imageWrapper}>
              <Image source={{ uri: image.uri }} style={styles.image} />
              <TouchableOpacity
                style={styles.removeButton}
                onPress={() => handleRemoveImage(index)}
              >
                <Icon name="close-circle" size={24} color={colors.error.main} />
              </TouchableOpacity>
            </View>
          ))}

          {(multiple ? images.length < maxImages : images.length === 0) && (
            <TouchableOpacity style={styles.addButton} onPress={handlePickImage}>
              <Icon name="camera-plus" size={32} color={colors.primary.main} />
              <Text style={styles.addButtonText}>
                {images.length === 0 ? 'Add Image' : 'Add More'}
              </Text>
            </TouchableOpacity>
          )}
        </View>
      </ScrollView>

      {error && <Text style={styles.error}>{error}</Text>}

      {multiple && images.length > 0 && (
        <Text style={styles.hint}>
          {images.length} / {maxImages} images selected
        </Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginBottom: spacing.md,
  },
  label: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.medium,
    color: colors.text.primary,
    marginBottom: spacing.xs,
  },
  imagesContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  imageWrapper: {
    position: 'relative',
    marginRight: spacing.md,
  },
  image: {
    width: 100,
    height: 100,
    borderRadius: spacing.borderRadius.md,
    backgroundColor: colors.gray[100],
  },
  removeButton: {
    position: 'absolute',
    top: -8,
    right: -8,
    backgroundColor: colors.white,
    borderRadius: 12,
  },
  addButton: {
    width: 100,
    height: 100,
    borderRadius: spacing.borderRadius.md,
    borderWidth: 2,
    borderColor: colors.primary.main,
    borderStyle: 'dashed',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.primary.main + '10',
  },
  addButtonText: {
    fontSize: typography.fontSize.xs,
    color: colors.primary.main,
    marginTop: spacing.xs,
    fontWeight: typography.fontWeight.medium,
  },
  error: {
    fontSize: typography.fontSize.xs,
    color: colors.error.main,
    marginTop: spacing.xs,
  },
  hint: {
    fontSize: typography.fontSize.xs,
    color: colors.text.secondary,
    marginTop: spacing.xs,
  },
});

export default ImagePickerComponent;

