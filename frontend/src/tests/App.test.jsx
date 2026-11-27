import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import React from "react";
import App from "../app/App";

describe("Página inicial do Atlas Santos", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("apresenta o acervo em preparação e consulta a API", async () => {
    const request = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ status: "healthy" }),
    });
    vi.stubGlobal("fetch", request);

    render(<App />);

    expect(screen.getByRole("heading", { name: "Atlas Santos" })).toBeInTheDocument();
    expect(
      screen.getByText("Acesse o atlas da sua equipe com sua conta.")
    ).toBeInTheDocument();
    expect(await screen.findByText("Serviço disponível.")).toBeInTheDocument();
    expect(request).toHaveBeenCalledWith(
      expect.stringMatching(/\/api\/v1\/health$/),
      expect.objectContaining({ credentials: "include" })
    );
  });

  it("informa falhas de conexão sem expor detalhes internos", async () => {
    vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("private-debug-detail")));

    render(<App />);

    expect(
      await screen.findByText("Não foi possível consultar o serviço.")
    ).toBeInTheDocument();
    expect(screen.queryByText(/private-debug-detail/)).not.toBeInTheDocument();
  });
});
