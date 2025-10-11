/**
 * Payment Redux Slice
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '../../services/api';

interface CreditPackage {
  id: string;
  name: string;
  credits: number;
  amount: number;
  description: string;
  popular: boolean;
}

interface Order {
  id: string;
  order_id: string;
  payment_id: string;
  credit: number;
  amount: number;
  status: string;
  created_at: string;
}

interface PaymentState {
  packages: CreditPackage[];
  orders: Order[];
  currentOrder: any;
  isLoading: boolean;
  error: string | null;
}

const initialState: PaymentState = {
  packages: [],
  orders: [],
  currentOrder: null,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchCreditPackages = createAsyncThunk(
  'payment/fetchCreditPackages',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/payments/packages');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch packages');
    }
  }
);

export const createOrder = createAsyncThunk(
  'payment/createOrder',
  async (data: { amount: number; credit: number; coupon_code?: string }, { rejectWithValue }) => {
    try {
      const response = await api.post('/payments/create-order', data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create order');
    }
  }
);

export const verifyPayment = createAsyncThunk(
  'payment/verifyPayment',
  async (
    data: {
      razorpay_payment_id: string;
      razorpay_order_id: string;
      razorpay_signature: string;
    },
    { rejectWithValue }
  ) => {
    try {
      const response = await api.post('/payments/verify', data);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Payment verification failed');
    }
  }
);

export const validateCoupon = createAsyncThunk(
  'payment/validateCoupon',
  async (code: string, { rejectWithValue }) => {
    try {
      const response = await api.get(`/payments/validate-coupon?code=${code}`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Invalid coupon code');
    }
  }
);

export const fetchOrders = createAsyncThunk(
  'payment/fetchOrders',
  async (params: { skip?: number; limit?: number }, { rejectWithValue }) => {
    try {
      const response = await api.get('/payments/orders', { params });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch orders');
    }
  }
);

// Slice
const paymentSlice = createSlice({
  name: 'payment',
  initialState,
  reducers: {
    clearPaymentError: (state) => {
      state.error = null;
    },
    setCurrentOrder: (state, action: PayloadAction<any>) => {
      state.currentOrder = action.payload;
    },
    resetPayment: (state) => {
      state.orders = [];
      state.currentOrder = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch Credit Packages
    builder
      .addCase(fetchCreditPackages.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchCreditPackages.fulfilled, (state, action) => {
        state.isLoading = false;
        state.packages = action.payload;
      })
      .addCase(fetchCreditPackages.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Create Order
    builder
      .addCase(createOrder.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createOrder.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentOrder = action.payload;
      })
      .addCase(createOrder.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Verify Payment
    builder
      .addCase(verifyPayment.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(verifyPayment.fulfilled, (state) => {
        state.isLoading = false;
        state.currentOrder = null;
      })
      .addCase(verifyPayment.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Validate Coupon
    builder
      .addCase(validateCoupon.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(validateCoupon.fulfilled, (state) => {
        state.isLoading = false;
      })
      .addCase(validateCoupon.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Fetch Orders
    builder
      .addCase(fetchOrders.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchOrders.fulfilled, (state, action) => {
        state.isLoading = false;
        state.orders = action.payload.data || [];
      })
      .addCase(fetchOrders.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearPaymentError, setCurrentOrder, resetPayment } = paymentSlice.actions;
export default paymentSlice.reducer;

