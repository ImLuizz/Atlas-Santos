const production = "https://atlas-santos-production.up.railway.app";

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "private, no-store");
  const origin = process.env.ATLAS_API_ORIGIN ||
    (process.env.VERCEL_ENV === "production" ? production : undefined);
  if (!origin) {
    return res.status(503).json({ detail: "A API de homologação ainda não foi configurada." });
  }
  const { route, ...params } = req.query;
  if (typeof route !== "string" || !/^[a-zA-Z0-9_/-]+$/.test(route)) {
    return res.status(404).end();
  }
  const headers = {};
  for (const key of ["content-type", "x-atlas-request"]) {
    if (req.headers[key]) headers[key] = req.headers[key];
  }
  const session = req.headers.cookie?.split(/;\s*/).find((c) => c.startsWith("atlas_session="));
  if (session) headers.cookie = session;
  try {
    const base = new URL(origin);
    if (base.protocol !== "https:" || base.username || base.password) throw new Error();
    const target = new URL("/api/v1/" + route, base.origin);
    for (const [key, value] of Object.entries(params)) {
      for (const item of [].concat(value)) target.searchParams.append(key, item);
    }
    const upstream = await fetch(target, {
      method: req.method,
      headers,
      body: req.body == null || ["GET", "HEAD"].includes(req.method) ? undefined :
        typeof req.body === "string" ? req.body : JSON.stringify(req.body),
      redirect: "manual",
      signal: AbortSignal.timeout(15000),
    });
    const cookies = upstream.headers.getSetCookie();
    if (cookies.length) res.setHeader("Set-Cookie", cookies);
    res.setHeader("Content-Type", upstream.headers.get("content-type") || "application/json");
    return res.status(upstream.status).end(Buffer.from(await upstream.arrayBuffer()));
  } catch {
    return res.status(502).json({ detail: "Não foi possível consultar a API do Atlas." });
  }
}
