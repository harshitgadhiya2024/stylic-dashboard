/**
 * Image Picker Utilities
 */

import { launchCamera, launchImageLibrary, ImagePickerResponse } from 'react-native-image-picker';
import { Alert, Platform } from 'react-native';
import config from '../constants/config';

export interface ImageFile {
  uri: string;
  type: string;
  name: string;
  size?: number;
}

/**
 * Pick image from gallery
 */
export const pickImageFromGallery = async (
  multiple: boolean = false
): Promise<ImageFile[] | null> => {
  try {
    const result = await launchImageLibrary({
      mediaType: 'photo',
      quality: 0.8,
      selectionLimit: multiple ? 10 : 1,
      includeBase64: false,
    });

    if (result.didCancel) {
      return null;
    }

    if (result.errorCode) {
      Alert.alert('Error', result.errorMessage || 'Failed to pick image');
      return null;
    }

    if (!result.assets || result.assets.length === 0) {
      return null;
    }

    // Validate and format images
    const images: ImageFile[] = [];
    for (const asset of result.assets) {
      if (!asset.uri) continue;

      // Validate file size
      if (asset.fileSize && asset.fileSize > config.maxFileSize) {
        Alert.alert(
          'File Too Large',
          `Image ${asset.fileName} exceeds ${config.maxFileSize / 1024 / 1024}MB limit`
        );
        continue;
      }

      // Validate file type
      const type = asset.type || 'image/jpeg';
      if (!config.allowedImageTypes.includes(type)) {
        Alert.alert('Invalid File Type', `${asset.fileName} is not a supported image format`);
        continue;
      }

      images.push({
        uri: asset.uri,
        type: type,
        name: asset.fileName || `image_${Date.now()}.jpg`,
        size: asset.fileSize,
      });
    }

    return images.length > 0 ? images : null;
  } catch (error) {
    console.error('Error picking image:', error);
    Alert.alert('Error', 'Failed to pick image');
    return null;
  }
};

/**
 * Take photo with camera
 */
export const takePhoto = async (): Promise<ImageFile | null> => {
  try {
    const result = await launchCamera({
      mediaType: 'photo',
      quality: 0.8,
      saveToPhotos: true,
      includeBase64: false,
    });

    if (result.didCancel) {
      return null;
    }

    if (result.errorCode) {
      Alert.alert('Error', result.errorMessage || 'Failed to take photo');
      return null;
    }

    if (!result.assets || result.assets.length === 0) {
      return null;
    }

    const asset = result.assets[0];
    if (!asset.uri) return null;

    return {
      uri: asset.uri,
      type: asset.type || 'image/jpeg',
      name: asset.fileName || `photo_${Date.now()}.jpg`,
      size: asset.fileSize,
    };
  } catch (error) {
    console.error('Error taking photo:', error);
    Alert.alert('Error', 'Failed to take photo');
    return null;
  }
};

/**
 * Show image picker options
 */
export const showImagePickerOptions = (
  onGallery: () => void,
  onCamera: () => void
): void => {
  Alert.alert(
    'Select Image',
    'Choose an option',
    [
      {
        text: 'Camera',
        onPress: onCamera,
      },
      {
        text: 'Gallery',
        onPress: onGallery,
      },
      {
        text: 'Cancel',
        style: 'cancel',
      },
    ],
    { cancelable: true }
  );
};

/**
 * Create FormData for file upload
 */
export const createFormDataWithImages = (
  data: Record<string, any>,
  images: { key: string; files: ImageFile[] }[]
): FormData => {
  const formData = new FormData();

  // Add regular fields
  Object.keys(data).forEach((key) => {
    const value = data[key];
    if (value !== null && value !== undefined) {
      if (typeof value === 'object' && !Array.isArray(value)) {
        formData.append(key, JSON.stringify(value));
      } else if (Array.isArray(value)) {
        formData.append(key, JSON.stringify(value));
      } else {
        formData.append(key, value.toString());
      }
    }
  });

  // Add image files
  images.forEach(({ key, files }) => {
    files.forEach((file, index) => {
      const fileData: any = {
        uri: Platform.OS === 'ios' ? file.uri.replace('file://', '') : file.uri,
        type: file.type,
        name: file.name,
      };
      formData.append(key, fileData);
    });
  });

  return formData;
};

/**
 * Validate image file
 */
export const validateImage = (file: ImageFile): { valid: boolean; error?: string } => {
  // Check file size
  if (file.size && file.size > config.maxFileSize) {
    return {
      valid: false,
      error: `File size exceeds ${config.maxFileSize / 1024 / 1024}MB limit`,
    };
  }

  // Check file type
  if (!config.allowedImageTypes.includes(file.type)) {
    return {
      valid: false,
      error: 'Invalid file type. Only JPEG, PNG, and WebP are allowed',
    };
  }

  return { valid: true };
};

