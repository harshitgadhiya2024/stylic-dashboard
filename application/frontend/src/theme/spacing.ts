/**
 * Spacing System
 */

export const spacing = {
  // Base spacing unit (4px)
  unit: 4,
  
  // Spacing scale
  xs: 4,    // 4px
  sm: 8,    // 8px
  md: 16,   // 16px
  lg: 24,   // 24px
  xl: 32,   // 32px
  '2xl': 48,  // 48px
  '3xl': 64,  // 64px
  '4xl': 96,  // 96px
  
  // Specific use cases
  screenPadding: 16,
  cardPadding: 16,
  sectionSpacing: 24,
  itemSpacing: 12,
  
  // Border radius
  borderRadius: {
    none: 0,
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16,
    '2xl': 24,
    full: 9999,
  },
  
  // Icon sizes
  iconSize: {
    xs: 16,
    sm: 20,
    md: 24,
    lg: 32,
    xl: 48,
  },
  
  // Button heights
  buttonHeight: {
    sm: 32,
    md: 44,
    lg: 56,
  },
  
  // Input heights
  inputHeight: {
    sm: 36,
    md: 44,
    lg: 52,
  },
};

export type Spacing = typeof spacing;

