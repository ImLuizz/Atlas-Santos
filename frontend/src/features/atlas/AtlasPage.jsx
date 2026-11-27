import React, { useState } from "react";
import logo from "../../assets/atlas-santos.png";
import AtlasFilters from "./AtlasFilters";
import SantosMap from "./SantosMap";
import { profileLabel, TeamMembers } from "./TeamMembers";
import "./atlas.css";

const icons = {
  map: (
    <>
      <path d="m3 6 5-3 8 3 5-3v15l-5 3-8-3-5 3Z" />
      <path d="M8 3v15M16 6v15" />
    </>
  ),
  image: (
    <>
      <rect x="3" y="4" width="18" height="16" rx="2" />
      <circle cx="9" cy="10" r="2" />
      <path d="m21 15-5-5L5 20" />
    </>
  ),
  upload: (
    <>
      <path d="M12 16V4M7 9l5-5 5 5" />
      <path d="M4 15v5h16v-5" />
    </>
  ),
  users: (
    <>
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
    </>
  ),
  download: (
    <>
      <path d="M12 3v12m-5-5 5 5 5-5" />
      <path d="M4 19h16" />
    </>
  ),
  menu: <path d="M4 7h16M4 12h16M4 17h16" />,
};

function Icon({ name }) {
  return (
    <svg
      width="19"
      height="19"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {icons[name]}
    </svg>
  );
}

export default function AtlasPage({ account, onLogout, leaving, onSessionExpired }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [showMembers, setShowMembers] = useState(false);
  const [day, setDay] = useState("");
  const [theme, setTheme] = useState("");
  return (
    <div className="team-atlas">
      <aside className="atlas-rail">
        <div className="atlas-brand">
          <a href="/" aria-label="Atlas Santos — página inicial">
            <img src={logo} alt="Atlas Santos" />
          </a>
          <button
            className="atlas-menu-toggle"
            aria-label={menuOpen ? "Fechar menu" : "Abrir menu"}
            aria-expanded={menuOpen}
            aria-controls="atlas-sidebar-content"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            <Icon name="menu" />
          </button>
        </div>
        <div
          id="atlas-sidebar-content"
          className={`atlas-rail-body ${menuOpen ? "is-open" : ""}`}
        >
          <nav aria-label="Navegação do atlas">
            <a href="#atlas-title" aria-current="page" onClick={() => setMenuOpen(false)}>
              <Icon name="map" />
              Atlas da equipe
            </a>
            <button disabled>
              <Icon name="image" />
              Meu painel
            </button>
            <button disabled>
              <Icon name="upload" />
              Minhas fotos
            </button>
            {account.role === "capitao" && (
              <button
                aria-expanded={showMembers}
                onClick={() => {
                  setShowMembers(!showMembers);
                  setMenuOpen(false);
                }}
              >
                <Icon name="users" />
                Gestão do grupo
              </button>
            )}
          </nav>
          <div className="atlas-profile">
            <span className="atlas-avatar" aria-hidden="true">
              {account.name
                .split(" ")
                .map((part) => part[0])
                .join("")}
            </span>
            <div>
              <strong>{account.name}</strong>
              <small>
                {profileLabel(account)} · {account.team.name}
              </small>
            </div>
            <button onClick={onLogout} disabled={leaving}>
              {leaving ? "Saindo…" : "Sair"}
            </button>
          </div>
        </div>
      </aside>
      <main className="atlas-main">
        <div className="atlas-scope">
          Equipe <strong>{account.team.name}</strong>
          <span aria-hidden="true">/</span> Atlas{" "}
          <strong>{account.team.atlas_name}</strong>
        </div>
        <header className="atlas-heading">
          <div>
            <p className="atlas-eyebrow">Atlas da equipe</p>
            <h1 id="atlas-title">{account.team.atlas_name}</h1>
            <p>Percursos do estudo do meio em Santos.</p>
          </div>
          <button className="atlas-export" disabled>
            <Icon name="download" />
            Exportar
          </button>
        </header>
        {showMembers && (
          <TeamMembers team={account.team} onSessionExpired={onSessionExpired} />
        )}
        <div className="atlas-stats">
          <span>
            <strong>1</strong> equipe
          </span>
          <span>
            <strong>0</strong> registros no filtro
          </span>
          <span>
            <strong>{account.team.name}</strong> equipe responsável
          </span>
        </div>
        <div className="atlas-toolbar">
          <div className="atlas-tabs" aria-label="Visualizações do atlas" role="group">
            <span aria-current="page">Mapa</span>
            <button disabled>Galeria</button>
            <button disabled>Equipes</button>
          </div>
          <AtlasFilters
            day={day}
            theme={theme}
            onDayChange={setDay}
            onThemeChange={setTheme}
          />
        </div>
        <SantosMap />
      </main>
    </div>
  );
}
