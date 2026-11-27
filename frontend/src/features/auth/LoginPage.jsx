import React, { useRef, useState } from "react";
import logo from "../../assets/atlas-santos.png";
import centro from "../../assets/centro-santos.jpg";
import "./login.css";

export default function LoginPage({ onLogin }) {
  const [recovering, setRecovering] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [notice, setNotice] = useState("");
  const [pending, setPending] = useState(false);
  const email = useRef(null);
  const password = useRef(null);

  function switchForm() {
    setRecovering(!recovering);
    setShowPassword(false);
    setErrors({});
    setNotice("");
  }

  async function submit(event) {
    event.preventDefault();
    if (pending) return;
    const issues = {};
    if (!email.current.validity.valid) issues.email = "Informe um e-mail válido.";
    if (!password.current.value) issues.password = "Informe sua senha.";
    setErrors(issues);
    if (issues.email || issues.password) {
      setNotice("");
      (issues.email ? email : password).current.focus();
      return;
    }
    setPending(true);
    setNotice("");
    try {
      await onLogin(email.current.value.trim(), password.current.value);
    } catch (error) {
      if (error.status === 401) {
        setNotice("E-mail ou senha incorretos.");
        password.current.value = "";
        password.current.focus();
      } else {
        setNotice("Não foi possível acessar o Atlas. Tente novamente.");
      }
    } finally {
      setPending(false);
    }
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
                ? "Para recuperar seu acesso, procure a equipe responsável pelo Atlas."
                : "Entre com seu e-mail e senha para acessar o atlas da equipe."}
            </p>
            {recovering ? (
              <button className="access-link" type="button" onClick={switchForm}>
                Voltar ao login
              </button>
            ) : (
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
                <button
                  className="access-link"
                  type="button"
                  disabled={pending}
                  onClick={switchForm}
                >
                  Esqueci minha senha
                </button>
                <button type="submit" className="access-submit" disabled={pending}>
                  {pending ? "Entrando…" : "Entrar"} <span aria-hidden="true">→</span>
                </button>
                <p className="access-notice" role="status">
                  {notice}
                </p>
              </form>
            )}
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
