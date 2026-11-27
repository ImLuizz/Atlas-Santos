import React, { lazy, Suspense, useCallback, useEffect, useState } from "react";
import LoginPage from "../features/auth/LoginPage";
import LandingPage from "../features/landing/LandingPage";
import { apiFetch } from "../lib/api-client";

const AtlasPage = lazy(() => import("../features/atlas/AtlasPage"));

export function App() {
  if (/^\/(login|mapa)\/?$/.test(window.location.pathname)) return <Access />;
  return <LandingPage />;
}

function Access() {
  const [account, setAccount] = useState(null);
  const [status, setStatus] = useState("checking");
  const [attempt, setAttempt] = useState(0);
  const [leaving, setLeaving] = useState(false);
  const [error, setError] = useState("");

  function showAccount(user) {
    setAccount(user);
    setStatus("ready");
    setError("");
    window.history.replaceState(null, "", user ? "/mapa" : "/login");
  }

  const sessionExpired = useCallback(() => showAccount(null), []);

  useEffect(() => {
    const controller = new AbortController();
    apiFetch("/api/v1/auth/me", { signal: controller.signal })
      .then((user) => {
        if (!controller.signal.aborted) showAccount(user);
      })
      .catch((err) => {
        if (controller.signal.aborted) return;
        if (err.status === 401) showAccount(null);
        else setStatus("unavailable");
      });
    function restore(event) {
      if (event.persisted) window.location.reload();
    }
    window.addEventListener("pageshow", restore);
    return () => {
      controller.abort();
      window.removeEventListener("pageshow", restore);
    };
  }, [attempt]);

  async function enter(email, password) {
    const user = await apiFetch("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    showAccount(user);
  }

  async function leave() {
    setLeaving(true);
    setError("");
    try {
      await apiFetch("/api/v1/auth/logout", { method: "POST" });
      showAccount(null);
    } catch {
      setError("Não foi possível encerrar a sessão. Tente sair novamente.");
    } finally {
      setLeaving(false);
    }
  }

  if (status === "checking") return <p role="status">Consultando sua sessão…</p>;
  if (status === "unavailable")
    return (
      <main>
        <p role="alert">Não foi possível consultar sua sessão.</p>
        <button
          onClick={() => {
            setStatus("checking");
            setAttempt(attempt + 1);
          }}
        >
          Tentar novamente
        </button>
      </main>
    );
  if (!account) return <LoginPage onLogin={enter} />;
  return (
    <Suspense fallback={<p role="status">Abrindo o atlas…</p>}>
      {error && <p role="alert">{error}</p>}
      {account.team ? (
        <AtlasPage
          account={account}
          onLogout={leave}
          leaving={leaving}
          onSessionExpired={sessionExpired}
        />
      ) : (
        <main>
          <h1>{account.name}</h1>
          <p>Sua conta ainda não tem uma equipe vinculada.</p>
          <button onClick={leave} disabled={leaving}>
            Sair
          </button>
        </main>
      )}
    </Suspense>
  );
}

export default App;
