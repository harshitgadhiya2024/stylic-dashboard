/**
 * Photoshoot Redux Slice
 */

import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '../../services/api';

interface Photoshoot {
  photoshoot_id: string;
  status: string;
  garment_type: string;
  gender: string;
  created_at: string;
  all_images?: string[];
  [key: string]: any;
}

interface PhotoshootState {
  photoshoots: Photoshoot[];
  currentPhotoshoot: Photoshoot | null;
  total: number;
  isLoading: boolean;
  error: string | null;
}

const initialState: PhotoshootState = {
  photoshoots: [],
  currentPhotoshoot: null,
  total: 0,
  isLoading: false,
  error: null,
};

// Async thunks
export const fetchPhotoshoots = createAsyncThunk(
  'photoshoot/fetchPhotoshoots',
  async (params: { skip?: number; limit?: number; status?: string }, { rejectWithValue }) => {
    try {
      const response = await api.get('/photoshoots', { params });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch photoshoots');
    }
  }
);

export const fetchPhotoshootById = createAsyncThunk(
  'photoshoot/fetchPhotoshootById',
  async (id: string, { rejectWithValue }) => {
    try {
      const response = await api.get(`/photoshoots/${id}`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to fetch photoshoot');
    }
  }
);

export const createPhotoshoot = createAsyncThunk(
  'photoshoot/createPhotoshoot',
  async (formData: FormData, { rejectWithValue }) => {
    try {
      const response = await api.post('/photoshoots', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to create photoshoot');
    }
  }
);

export const deletePhotoshoot = createAsyncThunk(
  'photoshoot/deletePhotoshoot',
  async (id: string, { rejectWithValue }) => {
    try {
      await api.delete(`/photoshoots/${id}`);
      return id;
    } catch (error: any) {
      return rejectWithValue(error.response?.data?.detail || 'Failed to delete photoshoot');
    }
  }
);

// Slice
const photoshootSlice = createSlice({
  name: 'photoshoot',
  initialState,
  reducers: {
    clearPhotoshootError: (state) => {
      state.error = null;
    },
    setCurrentPhotoshoot: (state, action: PayloadAction<Photoshoot | null>) => {
      state.currentPhotoshoot = action.payload;
    },
    resetPhotoshoots: (state) => {
      state.photoshoots = [];
      state.currentPhotoshoot = null;
      state.total = 0;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // Fetch Photoshoots
    builder
      .addCase(fetchPhotoshoots.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPhotoshoots.fulfilled, (state, action) => {
        state.isLoading = false;
        state.photoshoots = action.payload.photoshoots || [];
        state.total = action.payload.total || 0;
      })
      .addCase(fetchPhotoshoots.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Fetch Photoshoot By ID
    builder
      .addCase(fetchPhotoshootById.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(fetchPhotoshootById.fulfilled, (state, action) => {
        state.isLoading = false;
        state.currentPhotoshoot = action.payload;
      })
      .addCase(fetchPhotoshootById.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Create Photoshoot
    builder
      .addCase(createPhotoshoot.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(createPhotoshoot.fulfilled, (state, action) => {
        state.isLoading = false;
      })
      .addCase(createPhotoshoot.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });

    // Delete Photoshoot
    builder
      .addCase(deletePhotoshoot.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(deletePhotoshoot.fulfilled, (state, action) => {
        state.isLoading = false;
        state.photoshoots = state.photoshoots.filter(
          (p) => p.photoshoot_id !== action.payload
        );
        state.total -= 1;
      })
      .addCase(deletePhotoshoot.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.payload as string;
      });
  },
});

export const { clearPhotoshootError, setCurrentPhotoshoot, resetPhotoshoots } = photoshootSlice.actions;
export default photoshootSlice.reducer;

