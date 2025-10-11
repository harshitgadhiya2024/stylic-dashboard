/**
 * Reset Password Screen - Placeholder
 */

import React, { useState } from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

const ResetPasswordScreen: React.FC = () => {
  const [otp, setOtp] = useState('');
  const [password, setPassword] = useState('');

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Reset Password</Text>
      </View>
      <Input label="OTP" placeholder="Enter OTP" value={otp} onChangeText={setOtp} />
      <Input
        label="New Password"
        placeholder="Enter new password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      <Button title="Reset Password" onPress={() => {}} fullWidth />
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: spacing.lg,
    justifyContent: 'center',
    backgroundColor: colors.background.default,
  },
  header: {
    marginBottom: spacing.xl,
    alignItems: 'center',
  },
  title: {
    fontSize: typography.fontSize['3xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
});

export default ResetPasswordScreen;

