import React from "react";
import { fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, expect, it, vi } from "vitest";
import App from "../app/App";

vi.mock("../features/atlas/SantosMap", () => ({
  default: () => <section aria-label="Mapa interativo de Santos" />,
}));

afterEach(() => {
  window.history.replaceState(null, "", "/");
  vi.unstubAllGlobals();
});

const user = {
  id: "member",
  name: "Maria Silva",
  role: "capitao",
  participant_kind: "estudante",
  team: { id: "team", name: "Porto", atlas_name: "Memórias do Porto" },
};

function json(status, value) {
  return { ok: status === 200, status, json: async () => value };
}

it("autentica pela API, restaura a sessão e encerra o acesso direto ao mapa", async () => {
  const request = vi
    .fn()
    .mockResolvedValueOnce(json(401, {}))
    .mockResolvedValueOnce(json(200, user))
    .mockResolvedValueOnce(json(200, user))
    .mockResolvedValueOnce(json(200, [user]))
    .mockResolvedValueOnce(json(200, { ok: true }))
    .mockResolvedValueOnce(json(401, {}));
  vi.stubGlobal("fetch", request);
  window.history.replaceState(null, "", "/mapa");
  const view = render(<App />);
  await screen.findByRole("heading", { name: "Entrar no Atlas" });
  expect(window.location.pathname).toBe("/login");
  fireEvent.change(screen.getByLabelText("E-mail"), {
    target: { value: "maria@example.org" },
  });
  fireEvent.change(screen.getByLabelText("Senha", { exact: true }), {
    target: { value: "test-pass" },
  });
  fireEvent.click(screen.getByRole("button", { name: "Entrar" }));
  expect(
    await screen.findByRole("heading", { name: user.team.atlas_name })
  ).toBeVisible();
  expect(request).toHaveBeenCalledWith(
    "/api/v1/auth/login",
    expect.objectContaining({
      method: "POST",
      credentials: "include",
      body: JSON.stringify({ email: "maria@example.org", password: "test-pass" }),
      headers: expect.objectContaining({ "X-Atlas-Request": "1" }),
    })
  );
  expect(window.location.pathname).toBe("/mapa");
  view.unmount();
  const reloaded = render(<App />);
  fireEvent.click(await screen.findByRole("button", { name: "Gestão do grupo" }));
  const roster = await screen.findByRole("region", { name: "Integrantes da equipe" });
  expect(await within(roster).findByText(/Maria Silva/)).toBeVisible();
  fireEvent.click(screen.getByRole("button", { name: "Sair" }));
  expect(await screen.findByRole("heading", { name: "Entrar no Atlas" })).toBeVisible();
  expect(request).toHaveBeenCalledWith(
    "/api/v1/auth/logout",
    expect.objectContaining({ method: "POST" })
  );
  reloaded.unmount();
  window.history.replaceState(null, "", "/mapa");
  render(<App />);
  expect(await screen.findByRole("heading", { name: "Entrar no Atlas" })).toBeVisible();
});

it("exibe servidor participante e permite repetir uma saída que falhou", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockResolvedValueOnce(
        json(200, {
          ...user,
          role: "participante",
          participant_kind: "servidor",
        })
      )
      .mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce(json(200, { ok: true }))
  );
  window.history.replaceState(null, "", "/mapa");
  render(<App />);
  expect(await screen.findByText("Servidor · Porto")).toBeVisible();
  expect(screen.queryByRole("button", { name: "Gestão do grupo" })).toBeNull();
  fireEvent.click(screen.getByRole("button", { name: "Sair" }));
  expect(await screen.findByRole("alert")).toHaveTextContent("Não foi possível encerrar");
  fireEvent.click(screen.getByRole("button", { name: "Sair" }));
  expect(await screen.findByRole("heading", { name: "Entrar no Atlas" })).toBeVisible();
});

it("permite repetir a consulta da sessão após falha da API", async () => {
  vi.stubGlobal(
    "fetch",
    vi
      .fn()
      .mockRejectedValueOnce(new Error("offline"))
      .mockResolvedValueOnce(json(200, user))
  );
  window.history.replaceState(null, "", "/mapa");
  render(<App />);
  fireEvent.click(await screen.findByRole("button", { name: "Tentar novamente" }));
  expect(
    await screen.findByRole("heading", { name: user.team.atlas_name })
  ).toBeVisible();
});
