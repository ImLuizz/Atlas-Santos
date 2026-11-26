import React, { useRef, useState } from "react";
import logo from "../assets/atlas-santos.png";
import centro from "../assets/centro-santos.jpg";
import { demoAccounts, demoPassword } from "../lib/demo-access";
import "./login.css";

export function Login({ onDemoLogin }) {
  const [recovering, setRecovering] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [notice, setNotice] = useState("");
  const email = useRef(null);
  const password = useRef(null);

  function switchForm() {
    setRecovering(!recovering);
    setShowPassword(false);
    setErrors({});
    setNotice("");
    email.current.focus();
  }

  function submit(event) {
    event.preventDefault();
    const issues = {};
    if (!email.current.validity.valid) issues.email = "Informe um e-mail válido.";
    if (!recovering && !password.current.value) issues.password = "Informe sua senha.";
    setErrors(issues);
    if (issues.email || issues.password) {
      setNotice("");
      (issues.email ? email : password).current.focus();
      return;
    }
    if (recovering) {
      setNotice(
        "A recuperação de senha estará disponível quando o acesso às contas for ativado."
      );
      return;
    }
    if (demoAccounts.length) {
      const address = email.current.value.trim().toLowerCase();
      const entry = demoAccounts.find((account) => account.email === address);
      if (entry && password.current.value === demoPassword) {
        onDemoLogin(entry);
        return;
      }
      setNotice("E-mail ou senha incorretos.");
    } else {
      setNotice("O acesso às contas estará disponível em breve.");
    }
    if (password.current) password.current.value = "";
  }

  function clearFeedback(event) {
    const { name } = event.target;
    if (errors[name]) setErrors({ ...errors, [name]: undefined });
    setNotice("");
  }

  return (
    <div className="atlas-access">
      <header className="access-header">
        <a href="/" aria-label="Atlas Santos — página inicial">
          <img src={logo} alt="Atlas Santos" />
        </a>
        <a className="access-back" href="/">
          <span aria-hidden="true">←</span> Página inicial
        </a>
      </header>
      <main className="access-spread">
        <figure className="access-photo">
          <img
            src={centro}
            alt="Fachadas do centro de Santos com a Bolsa Oficial de Café ao fundo."
          />
          <figcaption>
            <span>Santos, SP</span>
            <strong>Centro Histórico</strong>
            <small>Bolsa Oficial de Café</small>
          </figcaption>
        </figure>
        <section className="access-panel" aria-labelledby="access-title">
          <div className="access-content">
            <h1 id="access-title">
              {recovering ? "Recuperar senha" : "Entrar no Atlas"}
            </h1>
            <p className="access-intro">
              {recovering
                ? "Informe o e-mail cadastrado na sua conta."
                : "Entre com seu e-mail e senha para acessar o atlas da equipe."}
            </p>
            <form noValidate onSubmit={submit} onChange={clearFeedback}>
              <label htmlFor="atlas-email">E-mail</label>
              <input
                id="atlas-email"
                name="email"
                type="email"
                autoComplete="username"
                ref={email}
                placeholder="seu@email.com"
                required
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? "email-error" : undefined}
              />
              {errors.email && (
                <p id="email-error" className="access-error">
                  {errors.email}
                </p>
              )}
              {!recovering && (
                <>
                  <label htmlFor="atlas-password">Senha</label>
                  <div className="access-password">
                    <input
                      id="atlas-password"
                      name="password"
                      type={showPassword ? "text" : "password"}
                      autoComplete="current-password"
                      ref={password}
                      placeholder="Sua senha"
                      required
                      aria-invalid={!!errors.password}
                      aria-describedby={errors.password ? "password-error" : undefined}
                    />
                    <button
                      type="button"
                      aria-label={showPassword ? "Ocultar senha" : "Mostrar senha"}
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      {showPassword ? "Ocultar" : "Mostrar"}
                    </button>
                  </div>
                  {errors.password && (
                    <p id="password-error" className="access-error">
                      {errors.password}
                    </p>
                  )}
                  <button className="access-link" type="button" onClick={switchForm}>
                    Esqueci minha senha
                  </button>
                </>
              )}
              <button type="submit" className="access-submit">
                {recovering ? "Solicitar recuperação" : "Entrar"}{" "}
                <span aria-hidden="true">→</span>
              </button>
              {recovering && (
                <button className="access-link" type="button" onClick={switchForm}>
                  Voltar ao login
                </button>
              )}
              <p className="access-notice" role="status">
                {notice}
              </p>
            </form>
          </div>
        </section>
      </main>
      <footer className="access-footer">
        <span>IFSP · Campus Araraquara</span>
        <span>Estudo do Meio · 2026</span>
      </footer>
    </div>
  );
}
