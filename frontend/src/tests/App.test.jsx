import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import React from "react";
import App from "../app/App";

describe("Atlas Santos Frontend — Application Root Test", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  it("renders header and main presentation elements", async () => {
    // Mock health check response
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        status: "healthy",
        app_name: "Atlas Santos API",
        version: "0.1.0",
        database: "connected",
      }),
    });

    render(<App />);

    expect(screen.getByText("Atlas Santos")).toBeInTheDocument();
    expect(screen.getByText(/Estudo do Meio 2026/i)).toBeInTheDocument();
    expect(screen.getByText(/Fundação Técnica Operacional/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Operacional/i)).toBeInTheDocument();
    });
  });

  it("handles backend offline gracefully", async () => {
    global.fetch = vi.fn().mockRejectedValue(new Error("Network Error"));

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Aguardando/i)).toBeInTheDocument();
    });
  });
});
