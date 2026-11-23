import React, { useEffect, useState } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { apiFetch } from "../lib/api-client";

export function App() {
  const [serviceStatus, setServiceStatus] = useState("Consultando serviço…");

  useEffect(() => {
    const controller = new AbortController();
    apiFetch("/api/v1/health", { signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted) {
          setServiceStatus(
            data.status === "healthy"
              ? "Serviço disponível."
              : "Serviço temporariamente indisponível."
          );
        }
      })
      .catch(() => {
        if (!controller.signal.aborted) {
          setServiceStatus("Não foi possível consultar o serviço.");
        }
      });

    return () => controller.abort();
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <Header />
      <main className="mx-auto w-full max-w-4xl flex-1 px-4 py-10 sm:px-6">
        <h2 className="text-2xl font-bold text-slate-900">O estudo do meio em Santos</h2>
        <p className="mt-4 max-w-prose">
          De 5 a 11 de outubro de 2026, estudantes e servidores do IFSP Campus Araraquara
          participaram do estudo do meio. As equipes poderão reunir fotografias e
          reflexões em seus próprios atlas e consultar os percursos estimados de cada dia.
        </p>
        <p className="mt-4">O acesso aos atlas está em preparação.</p>
        <p role="status" className="mt-8 text-sm text-slate-600">
          {serviceStatus}
        </p>
      </main>
      <Footer />
    </div>
  );
}

export default App;
