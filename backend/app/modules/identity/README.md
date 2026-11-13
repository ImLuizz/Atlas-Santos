# Módulo: Identity (Identidade, Autenticação e Sessões)

## Responsabilidades
- Gerenciamento de credenciais e tokens de acesso de participantes (estudantes e servidores).
- Emissão de tokens de convite e ativação de conta única (RF-01, pendência D-03).
- Autenticação e ciclo de vida de sessões via cookies HTTP-only seguros (RF-02, RNF-01).
- Revogação de sessões (logout voluntário e revogação administrativa).

## Invariantes e Regras de Segurança
- Não copiar senhas, hashes ou sessões de outros sistemas (ex: IF-Arbitra).
- Nenhuma informação privada de acesso é exposta como autoria pública.
- Validação estrita de expiração e invalidação imediata em logout.

## Relações com outros módulos
- **Consumidores**: Quase todos os módulos validam o ator autenticado através do contexto de sessão emitido por `identity`.

