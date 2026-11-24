import React, { useEffect, useState } from "react";
import { Header } from "../components/layout/Header";
import { Footer } from "../components/layout/Footer";
import { apiFetch } from "../lib/api-client";
import { Login } from "./Login";
import vista from "../assets/santos-aerea.jpg";
import centro from "../assets/centro-santos.jpg";
import "./landing.css";

export function App() {
  if (["/login", "/login/"].includes(window.location.pathname)) return <Login />;
  return <Home />;
}

function Home() {
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
    <div className="landing">
      <Header />
      <main>
        <section className="landing-hero" aria-labelledby="atlas-title">
          <img
            className="landing-cover"
            src={vista}
            alt="Vista aérea da orla, da cidade e do porto de Santos."
          />
          <div className="landing-hero-copy">
            <p className="landing-kicker">Estudo do meio · IFSP Araraquara</p>
            <h1 id="atlas-title">
              Atlas <em>Santos</em>
            </h1>
            <p className="landing-lead">
              Os caminhos de uma viagem pelas fotografias e memórias de quem esteve lá.
            </p>
            <a className="landing-cta" href="#estudo">
              Conheça o projeto <span aria-hidden="true">↓</span>
            </a>
          </div>
          <div className="landing-caption">
            <span>Santos, São Paulo</span>
            <span>Vista aérea · Agência CNT</span>
          </div>
        </section>

        <section id="estudo" className="landing-story" aria-labelledby="study-title">
          <div>
            <p className="landing-kicker">5 a 11 de outubro de 2026</p>
            <h2 id="study-title">
              Uma cidade,
              <br />
              <em>muitos olhares.</em>
            </h2>
            <p>
              Durante sete dias, 83 estudantes e 12 servidores do IFSP Campus Araraquara
              fizeram de Santos sua sala de aula. Cada equipe voltou com um percurso
              próprio e fotografias para contar o que encontrou.
            </p>
            <p>
              No Atlas, essas imagens vão ganhar lugar no mapa. As equipes poderão
              revisitar os caminhos de cada dia e reunir suas reflexões em{" "}
              <i>Olhares sobre Santos</i>.
            </p>
            <a className="landing-text-link" href="/login">
              Acessar minha conta <span aria-hidden="true">↗</span>
            </a>
          </div>
          <figure>
            <img
              src={centro}
              loading="lazy"
              alt="Fachadas do Centro Histórico e a Bolsa Oficial de Café ao fundo."
            />
            <figcaption>
              Centro Histórico <span>Bolsa Oficial de Café</span>
            </figcaption>
          </figure>
        </section>
        <aside className="landing-status" aria-label="Disponibilidade do Atlas">
          <p>O acesso aos atlas está em preparação.</p>
          <p role="status">{serviceStatus}</p>
        </aside>
      </main>
      <Footer />
    </div>
  );
}

export default App;
