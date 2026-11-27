import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { expect, it, vi } from "vitest";
import LoginPage from "../features/auth/LoginPage";

it("valida os campos, permite conferir a senha e informa a recusa da API", async () => {
  const login = vi.fn().mockRejectedValue({ status: 401 });
  render(<LoginPage onLogin={login} />);
  const enter = screen.getByRole("button", { name: "Entrar" });
  fireEvent.click(enter);
  expect(screen.getByLabelText("E-mail")).toHaveFocus();
  expect(screen.getByText("Informe sua senha.")).toBeInTheDocument();
  expect(login).not.toHaveBeenCalled();
  fireEvent.change(screen.getByLabelText("E-mail"), {
    target: { value: "teste@example.org" },
  });
  const password = screen.getByLabelText("Senha", { exact: true });
  fireEvent.change(password, { target: { value: "exemplo" } });
  fireEvent.click(screen.getByRole("button", { name: "Mostrar senha" }));
  expect(password).toHaveAttribute("type", "text");
  fireEvent.click(enter);
  expect(await screen.findByText("E-mail ou senha incorretos.")).toBeVisible();
  expect(password).toHaveValue("");
});

it("orienta a recuperação de acesso sem prometer o envio de e-mail", () => {
  render(<LoginPage onLogin={vi.fn()} />);
  fireEvent.click(screen.getByText("Esqueci minha senha"));
  expect(screen.getByText(/procure a equipe responsável/)).toBeVisible();
  fireEvent.click(screen.getByText("Voltar ao login"));
  expect(screen.getByLabelText("Senha", { exact: true })).toHaveAttribute(
    "type",
    "password"
  );
});
