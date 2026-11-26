import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import App from "../app/App";

afterEach(() => {
  window.history.replaceState({}, "", "/");
  vi.unstubAllGlobals();
});

it("valida as credenciais localmente e permite conferir a senha", () => {
  const request = vi.fn();
  vi.stubGlobal("fetch", request);
  window.history.replaceState({}, "", "/login");
  render(<App />);
  const enter = screen.getByRole("button", { name: "Entrar" });
  fireEvent.click(enter);
  expect(screen.getByLabelText("E-mail")).toHaveFocus();
  expect(screen.getByText("Informe sua senha.")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("E-mail"), {
    target: { value: "teste@example.org" },
  });
  const password = screen.getByLabelText("Senha", { exact: true });
  fireEvent.change(password, { target: { value: "exemplo" } });
  fireEvent.click(screen.getByRole("button", { name: "Mostrar senha" }));
  expect(password).toHaveAttribute("type", "text");
  fireEvent.click(enter);
  expect(screen.getByRole("status")).toHaveTextContent("E-mail ou senha incorretos");
  expect(request).not.toHaveBeenCalled();
});

it("abre a recuperação, valida o e-mail e permite voltar ao login", () => {
  window.history.replaceState({}, "", "/login/");
  render(<App />);
  fireEvent.click(screen.getByText("Esqueci minha senha"));
  expect(screen.getByRole("heading", { name: "Recuperar senha" })).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("E-mail"), { target: { value: "incompleto" } });
  fireEvent.click(screen.getByText("Solicitar recuperação"));
  expect(screen.getByText("Informe um e-mail válido.")).toBeInTheDocument();
  fireEvent.change(screen.getByLabelText("E-mail"), {
    target: { value: "teste@example.org" },
  });
  fireEvent.click(screen.getByText("Solicitar recuperação"));
  expect(screen.getByRole("status")).toHaveTextContent(
    "quando o acesso às contas for ativado"
  );
  fireEvent.click(screen.getByText("Voltar ao login"));
  expect(screen.getByLabelText("Senha", { exact: true })).toHaveAttribute(
    "type",
    "password"
  );
});
