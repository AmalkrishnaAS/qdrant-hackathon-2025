import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';

// Base URL can be overridden via NEXT_PUBLIC_API_BASE_URL for different environments
const BASE_URL: string = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:5000';

// In-memory auth token cache to avoid repeated localStorage access
let cachedAuthToken: string | null = null;

export const setAuthToken = (token: string | null): void => {
  cachedAuthToken = token;
};

// Create a shared Axios instance
export const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

// Attach auth and any per-request defaults
apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  // Optionally pull token from localStorage if not cached (client-side only)
  if (typeof window !== 'undefined' && !cachedAuthToken) {
    try {
      const tokenFromStorage = window.localStorage.getItem('auth_token');
      if (tokenFromStorage) cachedAuthToken = tokenFromStorage;
    } catch {
      // ignore storage errors
    }
  }

  if (cachedAuthToken) {
    // Support both AxiosHeaders (preferred) and plain object headers
    const headers: any = config.headers;
    if (headers?.set) {
      headers.set('Authorization', `Bearer ${cachedAuthToken}`);
    } else {
      config.headers = {
        ...(headers ?? {}),
        Authorization: `Bearer ${cachedAuthToken}`,
      } as any;
    }
  }

  return config;
});

// Unified response handling (keeps full response but also returns as-is)
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    // Normalize common error shape
    const status = error.response?.status;
    const message =
      (error.response?.data as any)?.message ||
      (error as any).message ||
      'Request failed';

    const normalized = new Error(`${status ?? 'ERR'}: ${message}`);
    (normalized as any).status = status;
    (normalized as any).data = error.response?.data;
    return Promise.reject(normalized);
  }
);

// Convenience typed helpers
export async function getJson<T = unknown>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await apiClient.get<T>(url, config);
  return res.data;
}

export async function postJson<T = unknown, B = unknown>(
  url: string,
  body?: B,
  config?: AxiosRequestConfig
): Promise<T> {
  const res = await apiClient.post<T>(url, body, config);
  return res.data;
}

export async function putJson<T = unknown, B = unknown>(
  url: string,
  body?: B,
  config?: AxiosRequestConfig
): Promise<T> {
  const res = await apiClient.put<T>(url, body, config);
  return res.data;
}

export async function patchJson<T = unknown, B = unknown>(
  url: string,
  body?: B,
  config?: AxiosRequestConfig
): Promise<T> {
  const res = await apiClient.patch<T>(url, body, config);
  return res.data;
}

export async function deleteJson<T = unknown>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await apiClient.delete<T>(url, config);
  return res.data;
}

// File upload helper (multipart)
export async function uploadForm<T = unknown>(
  url: string,
  formData: FormData,
  config?: AxiosRequestConfig
): Promise<T> {
  const res = await apiClient.post<T>(url, formData, {
    ...config,
    headers: {
      ...(config?.headers ?? {}),
      'Content-Type': 'multipart/form-data',
    },
  });
  return res.data;
}

// Simple health-check convenience for Flask-RESTX default root or /health
export async function pingServer(paths: string[] = ['/', '/health', '/api/health']): Promise<{
  reachable: boolean;
  path?: string;
}> {
  for (const path of paths) {
    try {
      await apiClient.get(path, { timeout: 4000 });
      return { reachable: true, path };
    } catch {
      // try next path
    }
  }
  return { reachable: false };
}


