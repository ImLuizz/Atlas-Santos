import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import App from "../app/App";
import { demoAccounts, demoPassword } from "../lib/demo-access";

vi.mock("../app/SantosMap", () => ({
  default: () => <section aria-label="Mapa interativo de Santos" />,
}));

afterEach(() => {
  sessionStorage.clear();
  window.history.replaceState(null, "", "/");
});

it.each(demoAccounts)(
  "abre o atlas como $role, preserva a sessão e permite sair",
  async (account) => {
    window.history.replaceState(null, "", "/mapa");
    const view = render(<App />);
    expect(window.location.pathname).toBe("/login");
    expect(screen.queryByText(/demonstração/i)).not.toBeInTheDocument();
    expect(screen.queryByText(demoPassword)).not.toBeInTheDocument();
    fireEvent.change(screen.getByLabelText("E-mail"), {
      target: { value: account.email },
    });
    fireEvent.change(screen.getByLabelText("Senha", { exact: true }), {
      target: { value: demoPassword },
    });
    fireEvent.click(screen.getByRole("button", { name: "Entrar" }));
    expect(
      await screen.findByRole("heading", { name: "Atlas Santos 2026" })
    ).toBeVisible();
    expect(window.location.pathname).toBe("/mapa");
    expect(screen.getByText(account.name)).toBeInTheDocument();
    expect(screen.queryByText(/demonstração/i)).not.toBeInTheDocument();
    view.unmount();
    render(<App />);
    expect(
      await screen.findByRole("region", { name: "Mapa interativo de Santos" })
    ).toBeVisible();
    fireEvent.click(screen.getByRole("button", { name: "Sair" }));
    expect(screen.getByRole("heading", { name: "Entrar no Atlas" })).toBeVisible();
    expect(window.location.pathname).toBe("/login");
  }
);
