/**
 * Lightweight HTTP client wrapper for backend API communication.
 */
export async function apiFetch(endpoint, options = {}) {
  const defaultHeaders = {
    ...(options.body ? { "Content-Type": "application/json" } : {}),
    ...(options.method === "POST" ? { "X-Atlas-Request": "1" } : {}),
  };

  const response = await fetch(endpoint, {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    credentials: "include",
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
