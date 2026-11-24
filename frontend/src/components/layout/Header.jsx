import React from "react";
import logo from "../../assets/atlas-santos.png";

export function Header() {
  return (
    <header className="landing-header">
      <a href="/" aria-label="Atlas Santos — início">
        <img src={logo} alt="Atlas Santos" />
      </a>
      <nav aria-label="Navegação principal">
        <a href="#estudo">O projeto</a>
        <a className="landing-login" href="/login">
          Entrar <span aria-hidden="true">↗</span>
        </a>
      </nav>
    </header>
  );
}
