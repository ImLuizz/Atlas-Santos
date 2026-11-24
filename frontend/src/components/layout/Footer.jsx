import React from "react";

export function Footer() {
  return (
    <footer className="landing-footer">
      <strong>Atlas Santos</strong>
      <span>IFSP · Campus Araraquara</span>
      <details>
        <summary>Créditos fotográficos</summary>
        <p>
          Vista aérea de Santos, Agência CNT (2012). Fotografia com recorte de exibição.{" "}
          <a href="https://www.flickr.com/photos/51889924@N04/8866575201">Original</a> ·{" "}
          <a href="https://creativecommons.org/licenses/by/2.0/">CC BY 2.0</a>.
        </p>
      </details>
    </footer>
  );
}
