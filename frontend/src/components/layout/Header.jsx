import React from "react";

export function Header() {
  return (
    <header className="border-b border-slate-200 bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center text-white font-bold text-lg">
            A
          </div>
          <div>
            <h1 className="text-lg font-semibold text-slate-900 leading-tight">
              Atlas Santos
            </h1>
            <p className="text-xs text-slate-500">
              Estudo do Meio 2026 &bull; IFSP Campus Araraquara
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-xs text-slate-600 bg-slate-100 px-3 py-1.5 rounded-full border border-slate-200">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Fase 0 &bull; Fundação Ativa</span>
        </div>
      </div>
    </header>
  );
}
