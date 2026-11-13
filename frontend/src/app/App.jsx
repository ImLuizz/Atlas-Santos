import React, { useEffect, useState } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { apiFetch } from "../lib/api-client";
import { config } from "../lib/config";

export function App() {
  const [healthStatus, setHealthStatus] = useState({
    loading: true,
    healthy: false,
    detail: "Verificando backend...",
  });

  useEffect(() => {
    let isMounted = true;
    apiFetch("/api/v1/health")
      .then((data) => {
        if (isMounted) {
          setHealthStatus({
            loading: false,
            healthy: data.status === "healthy",
            detail: `Conectado: ${data.app_name} (v${data.version}) | DB: ${data.database}`,
          });
        }
      })
      .catch((err) => {
        if (isMounted) {
          setHealthStatus({
            loading: false,
            healthy: false,
            detail: `Backend offline ou inicializando (${err.message})`,
          });
        }
      });

    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-800">
      <Header />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Banner de Boas-Vindas */}
        <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 sm:p-8 mb-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <span className="inline-block px-2.5 py-1 text-xs font-semibold rounded-md bg-sky-100 text-sky-800 mb-2">
                Fundação Técnica Operacional
              </span>
              <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight">
                {config.appTitle} — Cartografia Colaborativa
              </h2>
              <p className="mt-2 text-sm text-slate-600 max-w-3xl leading-relaxed">
                Repositório estruturado para desenvolvimento colaborativo de cinco
                desenvolvedores. Acervo de fotografias, memórias e percursos do Estudo do
                Meio em Santos (05 a 11/10/2026), compreendendo 95 participantes (83
                estudantes e 12 servidores).
              </p>
            </div>
            <div className="border border-slate-200 rounded-lg p-4 bg-slate-50 min-w-[240px]">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Status da Conexão API
              </span>
              <div className="flex items-center gap-2">
                <span
                  className={`w-3 h-3 rounded-full ${
                    healthStatus.loading
                      ? "bg-amber-400 animate-pulse"
                      : healthStatus.healthy
                        ? "bg-emerald-500"
                        : "bg-rose-500"
                  }`}
                />
                <span className="text-xs font-medium text-slate-700">
                  {healthStatus.loading
                    ? "Consultando..."
                    : healthStatus.healthy
                      ? "Operacional"
                      : "Aguardando"}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1 font-mono break-all">
                {healthStatus.detail}
              </p>
            </div>
          </div>
        </section>

        {/* Grid de Informações de Fundação */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-lg p-5 border border-slate-200 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900 mb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-sky-500" />
              Arquitetura Monolítica Modular
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Organizada em 10 domínios bem delimitados com serviços desacoplados e worker
              assíncrono baseado em persistência PostgreSQL (Transactional Outbox).
            </p>
          </div>

          <div className="bg-white rounded-lg p-5 border border-slate-200 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900 mb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              Cartografia React Leaflet
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Base de visualização configurada com centro em Santos/SP (
              {config.map.defaultLat}, {config.map.defaultLng}) e tiles OpenStreetMap
              atribuídos.
            </p>
          </div>

          <div className="bg-white rounded-lg p-5 border border-slate-200 shadow-sm">
            <h3 className="text-sm font-semibold text-slate-900 mb-2 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-indigo-500" />
              Qualidade e CI
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              Pipelines GitHub Actions configurados com Ruff, Pytest, ESLint, Vitest e
              pre-commit checks garantindo padronização contínua.
            </p>
          </div>
        </div>

        {/* Informações dos Dias do Estudo do Meio */}
        <section className="bg-white rounded-xl shadow-sm border border-slate-200 p-6">
          <h3 className="text-base font-semibold text-slate-900 mb-3">
            Cronograma do Acervo de Santos (Outubro de 2026)
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-3">
            {[
              { day: "05/10", label: "Dia 1 (Seg)" },
              { day: "06/10", label: "Dia 2 (Ter)" },
              { day: "07/10", label: "Dia 3 (Qua)" },
              { day: "08/10", label: "Dia 4 (Qui)" },
              { day: "09/10", label: "Dia 5 (Sex)" },
              { day: "10/10", label: "Dia 6 (Sáb)" },
              { day: "11/10", label: "Dia 7 (Dom)" },
            ].map((item) => (
              <div
                key={item.day}
                className="border border-slate-200 rounded-lg p-3 text-center bg-slate-50 hover:bg-sky-50 hover:border-sky-300 transition-colors"
              >
                <span className="block text-sm font-bold text-slate-800">{item.day}</span>
                <span className="block text-[11px] text-slate-500">{item.label}</span>
              </div>
            ))}
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
}

export default App;
