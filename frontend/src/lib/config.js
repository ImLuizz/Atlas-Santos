/**
 * Frontend environment configuration helper.
 * Reads public Vite environment variables with safe defaults.
 */
export const config = {
  appTitle: import.meta.env.VITE_APP_TITLE || "Atlas Santos",
  appVersion: import.meta.env.VITE_APP_VERSION || "0.1.0",
  map: {
    defaultLat: parseFloat(import.meta.env.VITE_MAP_DEFAULT_LAT || "-23.9682"),
    defaultLng: parseFloat(import.meta.env.VITE_MAP_DEFAULT_LNG || "-46.3322"),
    defaultZoom: parseFloat(import.meta.env.VITE_MAP_DEFAULT_ZOOM || "16"),
    accessToken: import.meta.env.VITE_MAPBOX_ACCESS_TOKEN || "",
  },
};
