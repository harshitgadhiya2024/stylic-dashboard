/**
 * Photoshoot Create Screen - Complete Implementation
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Animated,
} from 'react-native';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import Toast from 'react-native-toast-message';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import { createPhotoshoot } from '../../store/slices/photoshootSlice';
import { fetchCredits } from '../../store/slices/userSlice';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import ImagePickerComponent from '../../components/common/ImagePicker';
import { ImageFile, createFormDataWithImages } from '../../utils/imagePickerUtils';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

interface FormData {
  garment_type: string;
  age_group: string;
  gender: string;
  ethnicity: string;
  height: string;
  weight: string;
  age: string;
  fitting: string;
  background_description: string;
  pose_input_method: 'predefined' | 'upload' | 'prompts';
  selected_poses: string[];
}

const PhotoshootCreateScreen: React.FC = () => {
  const dispatch = useAppDispatch();
  const { isLoading } = useAppSelector((state) => state.photoshoot);
  const { credits } = useAppSelector((state) => state.user);

  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<FormData>({
    garment_type: '',
    age_group: '',
    gender: '',
    ethnicity: '',
    height: '',
    weight: '',
    age: '',
    fitting: '',
    background_description: '',
    pose_input_method: 'predefined',
    selected_poses: [],
  });

  const [upperGarment, setUpperGarment] = useState<ImageFile[]>([]);
  const [lowerGarment, setLowerGarment] = useState<ImageFile[]>([]);
  const [poseImages, setPoseImages] = useState<ImageFile[]>([]);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const garmentTypes = ['T-Shirt', 'Shirt', 'Dress', 'Jacket', 'Pants', 'Skirt', 'Shorts'];
  const ageGroups = ['18-25', '26-35', '36-45', '46-55', '55+'];
  const genders = ['Male', 'Female', 'Unisex'];
  const ethnicities = ['Asian', 'Caucasian', 'African', 'Hispanic', 'Middle Eastern'];
  const fittings = ['Slim Fit', 'Regular Fit', 'Loose Fit', 'Oversized'];

  const updateFormData = (key: keyof FormData, value: any) => {
    setFormData({ ...formData, [key]: value });
    if (errors[key]) {
      setErrors({ ...errors, [key]: '' });
    }
  };

  const validateStep1 = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.garment_type) newErrors.garment_type = 'Required';
    if (!formData.gender) newErrors.gender = 'Required';
    if (upperGarment.length === 0) newErrors.upperGarment = 'Upload at least one garment image';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateStep2 = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!formData.age_group) newErrors.age_group = 'Required';
    if (!formData.ethnicity) newErrors.ethnicity = 'Required';
    if (!formData.height) newErrors.height = 'Required';
    if (!formData.weight) newErrors.weight = 'Required';
    if (!formData.age) newErrors.age = 'Required';
    if (!formData.fitting) newErrors.fitting = 'Required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const validateStep3 = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (formData.pose_input_method === 'upload' && poseImages.length === 0) {
      newErrors.poseImages = 'Upload at least one pose image';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (step === 1 && validateStep1()) {
      setStep(2);
    } else if (step === 2 && validateStep2()) {
      setStep(3);
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async () => {
    if (!validateStep3()) return;

    if (credits < 10) {
      Toast.show({
        type: 'error',
        text1: 'Insufficient Credits',
        text2: 'Please purchase credits to create photoshoot',
      });
      return;
    }

    try {
      const formDataToSend = createFormDataWithImages(
        {
          ...formData,
          selected_poses: JSON.stringify(formData.selected_poses),
        },
        [
          { key: 'upper_garment', files: upperGarment },
          { key: 'lower_garment', files: lowerGarment },
          { key: 'pose_images', files: poseImages },
        ]
      );

      await dispatch(createPhotoshoot(formDataToSend)).unwrap();

      Toast.show({
        type: 'success',
        text1: 'Photoshoot Created',
        text2: 'Your photoshoot is being generated',
      });

      // Refresh credits
      dispatch(fetchCredits());

      // Reset form
      setStep(1);
      setFormData({
        garment_type: '',
        age_group: '',
        gender: '',
        ethnicity: '',
        height: '',
        weight: '',
        age: '',
        fitting: '',
        background_description: '',
        pose_input_method: 'predefined',
        selected_poses: [],
      });
      setUpperGarment([]);
      setLowerGarment([]);
      setPoseImages([]);
    } catch (error: any) {
      Toast.show({
        type: 'error',
        text1: 'Creation Failed',
        text2: error,
      });
    }
  };

  const renderStep1 = () => (
    <View>
      <Text style={styles.stepTitle}>Step 1: Garment Details</Text>

      <ImagePickerComponent
        label="Upper Garment Image *"
        images={upperGarment}
        onImagesChange={setUpperGarment}
        error={errors.upperGarment}
      />

      <ImagePickerComponent
        label="Lower Garment Image (Optional)"
        images={lowerGarment}
        onImagesChange={setLowerGarment}
      />

      <Text style={styles.label}>Garment Type *</Text>
      <View style={styles.optionsGrid}>
        {garmentTypes.map((type) => (
          <TouchableOpacity
            key={type}
            style={[
              styles.optionButton,
              formData.garment_type === type && styles.optionButtonSelected,
            ]}
            onPress={() => updateFormData('garment_type', type)}
          >
            <Text
              style={[
                styles.optionText,
                formData.garment_type === type && styles.optionTextSelected,
              ]}
            >
              {type}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {errors.garment_type && <Text style={styles.error}>{errors.garment_type}</Text>}

      <Text style={styles.label}>Gender *</Text>
      <View style={styles.optionsRow}>
        {genders.map((gender) => (
          <TouchableOpacity
            key={gender}
            style={[
              styles.optionButton,
              formData.gender === gender && styles.optionButtonSelected,
            ]}
            onPress={() => updateFormData('gender', gender)}
          >
            <Text
              style={[
                styles.optionText,
                formData.gender === gender && styles.optionTextSelected,
              ]}
            >
              {gender}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {errors.gender && <Text style={styles.error}>{errors.gender}</Text>}
    </View>
  );

  const renderStep2 = () => (
    <View>
      <Text style={styles.stepTitle}>Step 2: Model Details</Text>

      <Text style={styles.label}>Age Group *</Text>
      <View style={styles.optionsRow}>
        {ageGroups.map((group) => (
          <TouchableOpacity
            key={group}
            style={[
              styles.optionButton,
              formData.age_group === group && styles.optionButtonSelected,
            ]}
            onPress={() => updateFormData('age_group', group)}
          >
            <Text
              style={[
                styles.optionText,
                formData.age_group === group && styles.optionTextSelected,
              ]}
            >
              {group}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {errors.age_group && <Text style={styles.error}>{errors.age_group}</Text>}

      <Text style={styles.label}>Ethnicity *</Text>
      <View style={styles.optionsRow}>
        {ethnicities.map((ethnicity) => (
          <TouchableOpacity
            key={ethnicity}
            style={[
              styles.optionButton,
              formData.ethnicity === ethnicity && styles.optionButtonSelected,
            ]}
            onPress={() => updateFormData('ethnicity', ethnicity)}
          >
            <Text
              style={[
                styles.optionText,
                formData.ethnicity === ethnicity && styles.optionTextSelected,
              ]}
            >
              {ethnicity}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {errors.ethnicity && <Text style={styles.error}>{errors.ethnicity}</Text>}

      <Input
        label="Height (cm) *"
        placeholder="e.g., 175"
        value={formData.height}
        onChangeText={(value) => updateFormData('height', value)}
        keyboardType="numeric"
        error={errors.height}
      />

      <Input
        label="Weight (kg) *"
        placeholder="e.g., 70"
        value={formData.weight}
        onChangeText={(value) => updateFormData('weight', value)}
        keyboardType="numeric"
        error={errors.weight}
      />

      <Input
        label="Age *"
        placeholder="e.g., 25"
        value={formData.age}
        onChangeText={(value) => updateFormData('age', value)}
        keyboardType="numeric"
        error={errors.age}
      />

      <Text style={styles.label}>Fitting *</Text>
      <View style={styles.optionsGrid}>
        {fittings.map((fitting) => (
          <TouchableOpacity
            key={fitting}
            style={[
              styles.optionButton,
              formData.fitting === fitting && styles.optionButtonSelected,
            ]}
            onPress={() => updateFormData('fitting', fitting)}
          >
            <Text
              style={[
                styles.optionText,
                formData.fitting === fitting && styles.optionTextSelected,
              ]}
            >
              {fitting}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
      {errors.fitting && <Text style={styles.error}>{errors.fitting}</Text>}
    </View>
  );

  const renderStep3 = () => (
    <View>
      <Text style={styles.stepTitle}>Step 3: Pose Selection</Text>

      <Text style={styles.label}>Pose Input Method *</Text>
      <View style={styles.optionsRow}>
        <TouchableOpacity
          style={[
            styles.optionButton,
            formData.pose_input_method === 'predefined' && styles.optionButtonSelected,
          ]}
          onPress={() => updateFormData('pose_input_method', 'predefined')}
        >
          <Icon
            name="view-grid"
            size={20}
            color={
              formData.pose_input_method === 'predefined'
                ? colors.white
                : colors.primary.main
            }
          />
          <Text
            style={[
              styles.optionText,
              formData.pose_input_method === 'predefined' && styles.optionTextSelected,
            ]}
          >
            Predefined
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[
            styles.optionButton,
            formData.pose_input_method === 'upload' && styles.optionButtonSelected,
          ]}
          onPress={() => updateFormData('pose_input_method', 'upload')}
        >
          <Icon
            name="upload"
            size={20}
            color={
              formData.pose_input_method === 'upload' ? colors.white : colors.primary.main
            }
          />
          <Text
            style={[
              styles.optionText,
              formData.pose_input_method === 'upload' && styles.optionTextSelected,
            ]}
          >
            Upload
          </Text>
        </TouchableOpacity>
      </View>

      {formData.pose_input_method === 'upload' && (
        <ImagePickerComponent
          label="Pose Images *"
          multiple
          maxImages={10}
          images={poseImages}
          onImagesChange={setPoseImages}
          error={errors.poseImages}
        />
      )}

      <Input
        label="Background Description (Optional)"
        placeholder="Describe the background you want..."
        value={formData.background_description}
        onChangeText={(value) => updateFormData('background_description', value)}
        multiline
        numberOfLines={3}
      />
    </View>
  );

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Create AI Photoshoot</Text>
        <View style={styles.creditsContainer}>
          <Icon name="wallet" size={20} color={colors.primary.main} />
          <Text style={styles.creditsText}>{credits} Credits</Text>
        </View>
      </View>

      <View style={styles.progressContainer}>
        {[1, 2, 3].map((s) => (
          <View
            key={s}
            style={[styles.progressDot, step >= s && styles.progressDotActive]}
          />
        ))}
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
      </ScrollView>

      <View style={styles.footer}>
        {step > 1 && (
          <Button
            title="Back"
            onPress={handleBack}
            variant="outline"
            style={styles.footerButton}
          />
        )}
        {step < 3 ? (
          <Button
            title="Next"
            onPress={handleNext}
            style={[styles.footerButton, step === 1 && styles.footerButtonFull]}
          />
        ) : (
          <Button
            title="Create Photoshoot"
            onPress={handleSubmit}
            loading={isLoading}
            style={styles.footerButton}
          />
        )}
      </View>
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
  creditsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.primary.main + '20',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: spacing.borderRadius.full,
  },
  creditsText: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.semibold,
    color: colors.primary.main,
    marginLeft: spacing.xs,
  },
  progressContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: spacing.md,
    backgroundColor: colors.white,
  },
  progressDot: {
    width: 40,
    height: 4,
    backgroundColor: colors.gray[200],
    marginHorizontal: spacing.xs,
    borderRadius: 2,
  },
  progressDotActive: {
    backgroundColor: colors.primary.main,
  },
  content: {
    flex: 1,
    padding: spacing.lg,
  },
  stepTitle: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginBottom: spacing.lg,
  },
  label: {
    fontSize: typography.fontSize.sm,
    fontWeight: typography.fontWeight.medium,
    color: colors.text.primary,
    marginBottom: spacing.sm,
    marginTop: spacing.md,
  },
  optionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: spacing.sm,
  },
  optionsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginBottom: spacing.sm,
  },
  optionButton: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: spacing.borderRadius.md,
    borderWidth: 1,
    borderColor: colors.primary.main,
    marginRight: spacing.sm,
    marginBottom: spacing.sm,
    flexDirection: 'row',
    alignItems: 'center',
  },
  optionButtonSelected: {
    backgroundColor: colors.primary.main,
  },
  optionText: {
    fontSize: typography.fontSize.sm,
    color: colors.primary.main,
    marginLeft: spacing.xs,
  },
  optionTextSelected: {
    color: colors.white,
  },
  error: {
    fontSize: typography.fontSize.xs,
    color: colors.error.main,
    marginTop: spacing.xs,
  },
  footer: {
    flexDirection: 'row',
    padding: spacing.lg,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.border.light,
  },
  footerButton: {
    flex: 1,
    marginHorizontal: spacing.xs,
  },
  footerButtonFull: {
    marginHorizontal: 0,
  },
});

export default PhotoshootCreateScreen;

