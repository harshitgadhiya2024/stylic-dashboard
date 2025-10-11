/**
 * Custom Button Component
 */

import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ActivityIndicator,
  ViewStyle,
  TextStyle,
} from 'react-native';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  fullWidth = false,
  style,
  textStyle,
}) => {
  const getButtonStyle = (): ViewStyle => {
    const baseStyle: ViewStyle = {
      borderRadius: spacing.borderRadius.md,
      alignItems: 'center',
      justifyContent: 'center',
      flexDirection: 'row',
    };

    // Size styles
    const sizeStyles: Record<string, ViewStyle> = {
      sm: { height: spacing.buttonHeight.sm, paddingHorizontal: spacing.md },
      md: { height: spacing.buttonHeight.md, paddingHorizontal: spacing.lg },
      lg: { height: spacing.buttonHeight.lg, paddingHorizontal: spacing.xl },
    };

    // Variant styles
    const variantStyles: Record<string, ViewStyle> = {
      primary: {
        backgroundColor: colors.primary.main,
      },
      secondary: {
        backgroundColor: colors.secondary.main,
      },
      outline: {
        backgroundColor: 'transparent',
        borderWidth: 1,
        borderColor: colors.primary.main,
      },
      text: {
        backgroundColor: 'transparent',
      },
    };

    // Disabled style
    const disabledStyle: ViewStyle = disabled
      ? {
          backgroundColor: colors.gray[300],
          borderColor: colors.gray[300],
        }
      : {};

    // Full width style
    const widthStyle: ViewStyle = fullWidth ? { width: '100%' } : {};

    return {
      ...baseStyle,
      ...sizeStyles[size],
      ...variantStyles[variant],
      ...disabledStyle,
      ...widthStyle,
    };
  };

  const getTextStyle = (): TextStyle => {
    const baseStyle: TextStyle = {
      fontWeight: typography.fontWeight.semibold,
    };

    // Size styles
    const sizeStyles: Record<string, TextStyle> = {
      sm: { fontSize: typography.fontSize.sm },
      md: { fontSize: typography.fontSize.md },
      lg: { fontSize: typography.fontSize.lg },
    };

    // Variant styles
    const variantStyles: Record<string, TextStyle> = {
      primary: { color: colors.white },
      secondary: { color: colors.white },
      outline: { color: colors.primary.main },
      text: { color: colors.primary.main },
    };

    // Disabled style
    const disabledStyle: TextStyle = disabled
      ? { color: colors.gray[500] }
      : {};

    return {
      ...baseStyle,
      ...sizeStyles[size],
      ...variantStyles[variant],
      ...disabledStyle,
    };
  };

  return (
    <TouchableOpacity
      style={[getButtonStyle(), style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
    >
      {loading ? (
        <ActivityIndicator
          color={variant === 'outline' || variant === 'text' ? colors.primary.main : colors.white}
          size="small"
        />
      ) : (
        <Text style={[getTextStyle(), textStyle]}>{title}</Text>
      )}
    </TouchableOpacity>
  );
};

export default Button;

