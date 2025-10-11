/**
 * Payment Screen - Credit Packages
 */

import React, { useEffect, useState } from 'react';
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
import RazorpayCheckout from 'react-native-razorpay';
import { useAppDispatch, useAppSelector } from '../../store/hooks';
import {
  fetchCreditPackages,
  createOrder,
  verifyPayment,
  validateCoupon,
} from '../../store/slices/paymentSlice';
import { fetchCredits } from '../../store/slices/userSlice';
import Card from '../../components/common/Card';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import Loading from '../../components/common/Loading';
import config from '../../constants/config';
import { colors } from '../../theme/colors';
import { typography } from '../../theme/typography';
import { spacing } from '../../theme/spacing';

const PaymentScreen: React.FC = () => {
  const dispatch = useAppDispatch();
  const { packages, isLoading } = useAppSelector((state) => state.payment);
  const { user } = useAppSelector((state) => state.auth);
  const { credits } = useAppSelector((state) => state.user);

  const [selectedPackage, setSelectedPackage] = useState<any>(null);
  const [couponCode, setCouponCode] = useState('');
  const [discount, setDiscount] = useState(0);
  const [finalAmount, setFinalAmount] = useState(0);
  const [processingPayment, setProcessingPayment] = useState(false);

  useEffect(() => {
    dispatch(fetchCreditPackages());
  }, []);

  useEffect(() => {
    if (selectedPackage) {
      const discountAmount = (selectedPackage.price * discount) / 100;
      setFinalAmount(selectedPackage.price - discountAmount);
    }
  }, [selectedPackage, discount]);

  const handleValidateCoupon = async () => {
    if (!couponCode.trim()) {
      Toast.show({
        type: 'error',
        text1: 'Invalid Coupon',
        text2: 'Please enter a coupon code',
      });
      return;
    }

    try {
      const result = await dispatch(validateCoupon(couponCode)).unwrap();
      setDiscount(result.discount_percentage);
      Toast.show({
        type: 'success',
        text1: 'Coupon Applied',
        text2: `${result.discount_percentage}% discount applied`,
      });
    } catch (error: any) {
      Toast.show({
        type: 'error',
        text1: 'Invalid Coupon',
        text2: error,
      });
    }
  };

  const handlePurchase = async () => {
    if (!selectedPackage) {
      Toast.show({
        type: 'error',
        text1: 'No Package Selected',
        text2: 'Please select a credit package',
      });
      return;
    }

    setProcessingPayment(true);

    try {
      // Create order
      const orderData = await dispatch(
        createOrder({
          package_id: selectedPackage.id,
          coupon_code: couponCode || undefined,
        })
      ).unwrap();

      // Open Razorpay checkout
      const options = {
        description: `Purchase ${selectedPackage.credits} credits`,
        image: 'https://your-logo-url.com/logo.png',
        currency: 'INR',
        key: config.razorpayKeyId,
        amount: orderData.amount,
        name: 'Stylic AI',
        order_id: orderData.razorpay_order_id,
        prefill: {
          email: user?.email,
          contact: user?.phone || '',
          name: `${user?.first_name} ${user?.last_name}`,
        },
        theme: { color: colors.primary.main },
      };

      const data = await RazorpayCheckout.open(options);

      // Verify payment
      await dispatch(
        verifyPayment({
          razorpay_order_id: data.razorpay_order_id,
          razorpay_payment_id: data.razorpay_payment_id,
          razorpay_signature: data.razorpay_signature,
        })
      ).unwrap();

      Toast.show({
        type: 'success',
        text1: 'Payment Successful',
        text2: `${selectedPackage.credits} credits added to your account`,
      });

      // Refresh credits
      dispatch(fetchCredits());

      // Reset
      setSelectedPackage(null);
      setCouponCode('');
      setDiscount(0);
    } catch (error: any) {
      console.error('Payment error:', error);
      Toast.show({
        type: 'error',
        text1: 'Payment Failed',
        text2: error.description || error,
      });
    } finally {
      setProcessingPayment(false);
    }
  };

  if (isLoading && packages.length === 0) {
    return <Loading fullScreen message="Loading packages..." />;
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Buy Credits</Text>
        <View style={styles.creditsContainer}>
          <Icon name="wallet" size={20} color={colors.primary.main} />
          <Text style={styles.creditsText}>{credits} Credits</Text>
        </View>
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        <Text style={styles.sectionTitle}>Select a Package</Text>

        {packages.map((pkg: any) => (
          <TouchableOpacity
            key={pkg.id}
            onPress={() => setSelectedPackage(pkg)}
            activeOpacity={0.8}
          >
            <Card
              style={[
                styles.packageCard,
                selectedPackage?.id === pkg.id && styles.packageCardSelected,
              ]}
            >
              <View style={styles.packageHeader}>
                <View>
                  <Text style={styles.packageName}>{pkg.name}</Text>
                  <Text style={styles.packageCredits}>{pkg.credits} Credits</Text>
                </View>
                {selectedPackage?.id === pkg.id && (
                  <Icon name="check-circle" size={32} color={colors.primary.main} />
                )}
              </View>

              <View style={styles.packagePricing}>
                <Text style={styles.packagePrice}>₹{pkg.price}</Text>
                <Text style={styles.packagePerCredit}>
                  ₹{(pkg.price / pkg.credits).toFixed(2)} per credit
                </Text>
              </View>

              {pkg.discount_percentage > 0 && (
                <View style={styles.discountBadge}>
                  <Text style={styles.discountText}>
                    {pkg.discount_percentage}% OFF
                  </Text>
                </View>
              )}
            </Card>
          </TouchableOpacity>
        ))}

        {selectedPackage && (
          <View style={styles.couponSection}>
            <Text style={styles.sectionTitle}>Have a Coupon?</Text>
            <View style={styles.couponRow}>
              <Input
                placeholder="Enter coupon code"
                value={couponCode}
                onChangeText={setCouponCode}
                style={styles.couponInput}
              />
              <Button
                title="Apply"
                onPress={handleValidateCoupon}
                variant="outline"
                size="sm"
                style={styles.couponButton}
              />
            </View>
          </View>
        )}

        {selectedPackage && (
          <Card style={styles.summaryCard}>
            <Text style={styles.summaryTitle}>Order Summary</Text>

            <View style={styles.summaryRow}>
              <Text style={styles.summaryLabel}>Package</Text>
              <Text style={styles.summaryValue}>{selectedPackage.name}</Text>
            </View>

            <View style={styles.summaryRow}>
              <Text style={styles.summaryLabel}>Credits</Text>
              <Text style={styles.summaryValue}>{selectedPackage.credits}</Text>
            </View>

            <View style={styles.summaryRow}>
              <Text style={styles.summaryLabel}>Price</Text>
              <Text style={styles.summaryValue}>₹{selectedPackage.price}</Text>
            </View>

            {discount > 0 && (
              <View style={styles.summaryRow}>
                <Text style={[styles.summaryLabel, { color: colors.success.main }]}>
                  Discount ({discount}%)
                </Text>
                <Text style={[styles.summaryValue, { color: colors.success.main }]}>
                  -₹{((selectedPackage.price * discount) / 100).toFixed(2)}
                </Text>
              </View>
            )}

            <View style={styles.summaryDivider} />

            <View style={styles.summaryRow}>
              <Text style={styles.summaryTotal}>Total</Text>
              <Text style={styles.summaryTotal}>₹{finalAmount.toFixed(2)}</Text>
            </View>
          </Card>
        )}
      </ScrollView>

      {selectedPackage && (
        <View style={styles.footer}>
          <Button
            title={`Pay ₹${finalAmount.toFixed(2)}`}
            onPress={handlePurchase}
            loading={processingPayment}
            fullWidth
          />
        </View>
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
  content: {
    flex: 1,
    padding: spacing.lg,
  },
  sectionTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginBottom: spacing.md,
  },
  packageCard: {
    marginBottom: spacing.md,
    padding: spacing.lg,
    position: 'relative',
  },
  packageCardSelected: {
    borderWidth: 2,
    borderColor: colors.primary.main,
  },
  packageHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  packageName: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
  packageCredits: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
    marginTop: spacing.xs,
  },
  packagePricing: {
    flexDirection: 'row',
    alignItems: 'baseline',
  },
  packagePrice: {
    fontSize: typography.fontSize['2xl'],
    fontWeight: typography.fontWeight.bold,
    color: colors.primary.main,
    marginRight: spacing.sm,
  },
  packagePerCredit: {
    fontSize: typography.fontSize.sm,
    color: colors.text.secondary,
  },
  discountBadge: {
    position: 'absolute',
    top: spacing.md,
    right: spacing.md,
    backgroundColor: colors.success.main,
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs,
    borderRadius: spacing.borderRadius.md,
  },
  discountText: {
    fontSize: typography.fontSize.xs,
    fontWeight: typography.fontWeight.bold,
    color: colors.white,
  },
  couponSection: {
    marginTop: spacing.lg,
  },
  couponRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  couponInput: {
    flex: 1,
    marginRight: spacing.sm,
  },
  couponButton: {
    marginTop: 20,
  },
  summaryCard: {
    marginTop: spacing.lg,
    padding: spacing.lg,
  },
  summaryTitle: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
    marginBottom: spacing.md,
  },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  summaryLabel: {
    fontSize: typography.fontSize.md,
    color: colors.text.secondary,
  },
  summaryValue: {
    fontSize: typography.fontSize.md,
    fontWeight: typography.fontWeight.medium,
    color: colors.text.primary,
  },
  summaryDivider: {
    height: 1,
    backgroundColor: colors.border.light,
    marginVertical: spacing.md,
  },
  summaryTotal: {
    fontSize: typography.fontSize.xl,
    fontWeight: typography.fontWeight.bold,
    color: colors.text.primary,
  },
  footer: {
    padding: spacing.lg,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.border.light,
  },
});

export default PaymentScreen;

