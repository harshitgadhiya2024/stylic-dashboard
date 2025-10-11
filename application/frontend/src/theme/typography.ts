/**
 * Typography System
 */

export const typography = {
  // Font Families
  fontFamily: {
    regular: 'System',
    medium: 'System',
    bold: 'System',
    light: 'System',
  },
  
  // Font Sizes
  fontSize: {
    xs: 12,
    sm: 14,
    md: 16,
    lg: 18,
    xl: 20,
    '2xl': 24,
    '3xl': 30,
    '4xl': 36,
    '5xl': 48,
  },
  
  // Font Weights
  fontWeight: {
    light: '300' as const,
    regular: '400' as const,
    medium: '500' as const,
    semibold: '600' as const,
    bold: '700' as const,
    extrabold: '800' as const,
  },
  
  // Line Heights
  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
    loose: 2,
  },
  
  // Letter Spacing
  letterSpacing: {
    tighter: -0.5,
    tight: -0.25,
    normal: 0,
    wide: 0.25,
    wider: 0.5,
    widest: 1,
  },
  
  // Text Styles
  h1: {
    fontSize: 32,
    fontWeight: '700' as const,
    lineHeight: 1.25,
  },
  
  h2: {
    fontSize: 24,
    fontWeight: '700' as const,
    lineHeight: 1.25,
  },
  
  h3: {
    fontSize: 20,
    fontWeight: '600' as const,
    lineHeight: 1.25,
  },
  
  h4: {
    fontSize: 18,
    fontWeight: '600' as const,
    lineHeight: 1.25,
  },
  
  h5: {
    fontSize: 16,
    fontWeight: '600' as const,
    lineHeight: 1.25,
  },
  
  h6: {
    fontSize: 14,
    fontWeight: '600' as const,
    lineHeight: 1.25,
  },
  
  body1: {
    fontSize: 16,
    fontWeight: '400' as const,
    lineHeight: 1.5,
  },
  
  body2: {
    fontSize: 14,
    fontWeight: '400' as const,
    lineHeight: 1.5,
  },
  
  subtitle1: {
    fontSize: 16,
    fontWeight: '500' as const,
    lineHeight: 1.5,
  },
  
  subtitle2: {
    fontSize: 14,
    fontWeight: '500' as const,
    lineHeight: 1.5,
  },
  
  caption: {
    fontSize: 12,
    fontWeight: '400' as const,
    lineHeight: 1.5,
  },
  
  overline: {
    fontSize: 10,
    fontWeight: '500' as const,
    lineHeight: 1.5,
    textTransform: 'uppercase' as const,
    letterSpacing: 1,
  },
  
  button: {
    fontSize: 16,
    fontWeight: '600' as const,
    lineHeight: 1.5,
    textTransform: 'uppercase' as const,
  },
};

export type Typography = typeof typography;

