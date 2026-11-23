import React from "react";
import { config } from "../../lib/config";

export function Header() {
  return (
    <header className="border-b border-slate-200 bg-white">
      <div className="mx-auto max-w-4xl px-4 py-4 sm:px-6">
        <h1 className="text-xl font-semibold text-slate-900">{config.appTitle}</h1>
        <p className="text-sm text-slate-600">Estudo do Meio 2026</p>
      </div>
    </header>
  );
}
