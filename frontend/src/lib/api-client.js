import { config } from "./config";

/**
 * Lightweight HTTP client wrapper for backend API communication.
 */
export async function apiFetch(endpoint, options = {}) {
  const url = `${config.apiBaseUrl}${endpoint}`;
  const defaultHeaders = {
    "Content-Type": "application/json",
  };

  const response = await fetch(url, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    credentials: "include", // send session cookies across origins
  });

  if (!response.ok) {
    const errorBody = await response.json().catch(() => ({}));
    const error = new Error(
      errorBody.detail || `Request failed with status ${response.status}`
    );
    error.status = response.status;
    error.payload = errorBody;
    throw error;
  }

  return response.json();
}
