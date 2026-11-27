import React, { useEffect, useState } from "react";
import { apiFetch } from "../../lib/api-client";

export function profileLabel(account) {
  if (account.role === "capitao") return "Capitania";
  if (account.role === "administracao") return "Administração";
  return account.participant_kind === "servidor" ? "Servidor" : "Estudante";
}

export function TeamMembers({ team, onSessionExpired }) {
  const [members, setMembers] = useState(null);
  const [error, setError] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    apiFetch(`/api/v1/teams/${team.id}/members`, { signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted) setMembers(data);
      })
      .catch((err) => {
        if (controller.signal.aborted) return;
        if (err.status === 401) onSessionExpired();
        else
          setError(
            err.status === 403
              ? "Acesso restrito à capitania desta equipe."
              : "Não foi possível carregar os integrantes."
          );
      });
    return () => controller.abort();
  }, [team.id, onSessionExpired]);
  return (
    <section aria-label="Integrantes da equipe" className="atlas-members">
      <h2>Integrantes · {team.name}</h2>
      {error ? (
        <p role="alert">{error}</p>
      ) : members ? (
        <ul>
          {members.map((member) => (
            <li key={member.id}>
              {member.name} · {profileLabel(member)}
            </li>
          ))}
        </ul>
      ) : (
        <p role="status">Carregando integrantes…</p>
      )}
    </section>
  );
}
