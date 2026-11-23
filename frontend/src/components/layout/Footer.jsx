import React from "react";
import { config } from "../../lib/config";

export function Footer() {
  return (
    <footer className="border-t border-slate-200 bg-white">
      <div className="mx-auto max-w-4xl px-4 py-4 text-sm text-slate-600 sm:px-6">
        IFSP Campus Araraquara · {config.appTitle} v{config.appVersion}
      </div>
    </footer>
  );
}
