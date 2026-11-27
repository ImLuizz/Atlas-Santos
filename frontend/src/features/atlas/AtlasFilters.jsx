import React from "react";

const days = [5, 6, 7, 8, 9, 10, 11];
const themes = [
  "Memória e ancestralidade",
  "Cidade e meio ambiente",
  "Experiências vividas",
  "Futuros possíveis",
];
export default function AtlasFilters({ day, theme, onDayChange, onThemeChange }) {
  return (
    <div className="atlas-filters">
      <select aria-label="Filtrar por equipe" disabled>
        <option>Equipe atual</option>
      </select>
      <select
        aria-label="Filtrar por dia"
        value={day}
        onChange={(e) => onDayChange(e.target.value)}
      >
        <option value="">Todos os dias</option>
        {days.map((d) => (
          <option value={d} key={d}>
            {d} de outubro
          </option>
        ))}
      </select>
      <select
        aria-label="Filtrar por olhar"
        value={theme}
        onChange={(e) => onThemeChange(e.target.value)}
      >
        <option value="">Todos os olhares</option>
        {themes.map((t) => (
          <option key={t}>{t}</option>
        ))}
      </select>
    </div>
  );
}
