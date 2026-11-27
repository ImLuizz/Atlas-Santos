// Cada ambiente encaminha /api à sua própria instância do Railway.
const configured = process.env.ATLAS_API_ORIGIN ||
  (process.env.VERCEL_ENV === "production" ? process.env.VITE_API_BASE_URL : undefined);
if (!configured) throw new Error("Configure ATLAS_API_ORIGIN para este ambiente da Vercel.");
const origin = new URL(configured);
if (origin.protocol !== "https:" || origin.username || origin.password ||
    origin.pathname !== "/" || origin.search || origin.hash) {
  throw new Error("ATLAS_API_ORIGIN deve ser a origem HTTPS da API, sem caminho.");
}

export const config = {
  rewrites: [
    { source: "/api/:path*", destination: origin.origin + "/api/:path*" },
    { source: "/login", destination: "/index.html" },
    { source: "/mapa", destination: "/index.html" },
  ],
};
