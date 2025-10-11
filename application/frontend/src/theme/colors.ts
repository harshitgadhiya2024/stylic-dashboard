/**
 * Color Palette - Matching Flask Dashboard
 */

export const colors = {
  // Primary Colors
  primary: {
    main: '#6366f1',      // Indigo 500
    light: '#818cf8',     // Indigo 400
    dark: '#4f46e5',      // Indigo 600
    contrast: '#ffffff',
  },
  
  // Secondary Colors
  secondary: {
    main: '#8b5cf6',      // Purple 500
    light: '#a78bfa',     // Purple 400
    dark: '#7c3aed',      // Purple 600
    contrast: '#ffffff',
  },
  
  // Status Colors
  success: {
    main: '#10b981',      // Green 500
    light: '#34d399',     // Green 400
    dark: '#059669',      // Green 600
    contrast: '#ffffff',
  },
  
  warning: {
    main: '#f59e0b',      // Amber 500
    light: '#fbbf24',     // Amber 400
    dark: '#d97706',      // Amber 600
    contrast: '#ffffff',
  },
  
  error: {
    main: '#ef4444',      // Red 500
    light: '#f87171',     // Red 400
    dark: '#dc2626',      // Red 600
    contrast: '#ffffff',
  },
  
  info: {
    main: '#3b82f6',      // Blue 500
    light: '#60a5fa',     // Blue 400
    dark: '#2563eb',      // Blue 600
    contrast: '#ffffff',
  },
  
  // Neutral Colors
  gray: {
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  },
  
  // Background Colors
  background: {
    default: '#f9fafb',   // Gray 50
    paper: '#ffffff',
    dark: '#111827',      // Gray 900
  },
  
  // Surface Colors
  surface: {
    main: '#ffffff',
    light: '#f9fafb',
    dark: '#1f2937',
  },
  
  // Text Colors
  text: {
    primary: '#111827',   // Gray 900
    secondary: '#6b7280', // Gray 500
    disabled: '#9ca3af',  // Gray 400
    hint: '#d1d5db',      // Gray 300
    inverse: '#ffffff',
  },
  
  // Border Colors
  border: {
    main: '#e5e7eb',      // Gray 200
    light: '#f3f4f6',     // Gray 100
    dark: '#d1d5db',      // Gray 300
  },
  
  // Divider
  divider: '#e5e7eb',     // Gray 200
  
  // Overlay
  overlay: 'rgba(0, 0, 0, 0.5)',
  
  // Transparent
  transparent: 'transparent',
  
  // White & Black
  white: '#ffffff',
  black: '#000000',
};

export type ColorPalette = typeof colors;

