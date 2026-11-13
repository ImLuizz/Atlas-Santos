import React from "react";
import { config } from "../../lib/config";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white py-6 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
        <div>
          <span>
            Atlas Santos v{config.appVersion} &bull; Viagem realizada de 05 a 11/10/2026
          </span>
        </div>
        <div
          dangerouslySetInnerHTML={{ __html: config.map.attribution }}
          className="text-slate-400 [&_a]:underline hover:[&_a]:text-slate-600"
        />
      </div>
    </footer>
  );
}
