/**
 * Frontend environment configuration helper.
 * Reads public Vite environment variables with safe defaults.
 */
export const config = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
  appTitle: import.meta.env.VITE_APP_TITLE || "Atlas Santos",
  appVersion: import.meta.env.VITE_APP_VERSION || "0.1.0",
  map: {
    defaultLat: parseFloat(import.meta.env.VITE_MAP_DEFAULT_LAT || "-23.9608"),
    defaultLng: parseFloat(import.meta.env.VITE_MAP_DEFAULT_LNG || "-46.3336"),
    defaultZoom: parseInt(import.meta.env.VITE_MAP_DEFAULT_ZOOM || "13", 10),
    tileLayerUrl:
      import.meta.env.VITE_MAP_TILE_LAYER_URL ||
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution:
      import.meta.env.VITE_MAP_ATTRIBUTION ||
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  },
};
