// Identidades de apresentação, disponíveis apenas ao executar o Vite em desenvolvimento.
export const demoAccounts = import.meta.env.DEV
  ? [
      { email: "ana@atlas.test", name: "Ana Souza", role: "Estudante" },
      { email: "marina@atlas.test", name: "Marina Costa", role: "Capitã" },
      { email: "caio@atlas.test", name: "Caio Ribeiro", role: "Servidor" },
    ]
  : [];
export const demoPassword = import.meta.env.DEV ? "Santos2026!" : "";
export const demoSessionKey = "atlas.demo.email";
