# Contribuição ao Atlas Santos

A [matriz de requisitos](docs/requirements/requirements-summary.md) é a referência para comportamento e critérios de aceite. Use IDs como `RF018` ou `RNF023` ao descrever uma alteração que atenda a um requisito.

## Convenções do repositório

- Mantenha a documentação em português. Siga os nomes e o estilo usados no módulo alterado.
- Trabalhe em uma branch por tarefa. No pull request, explique o que mudou e como reproduzir a verificação. As mensagens de commit usam o formato `tipo(escopo): resumo`.
- Versione alterações de esquema com Alembic. Para operações com impacto em dados existentes, descreva a estratégia de migração e recuperação.
- Preserve dados de estudantes e servidores. Use dados fictícios em testes e exemplos. Originais, coordenadas precisas e tokens de provedores exigem os controles previstos em RNF006–RNF008.
- Teste a alteração pelo ponto de entrada que o usuário ou o serviço utiliza. Para upload, verifique a cota sob concorrência; para publicação, verifique revisão, autorização e retirada; para integrações, verifique também a resposta a falhas.

## Antes de integrar

No backend, execute `ruff check .`, `ruff format --check .` e `pytest`. No frontend, execute `npm run lint`, `npm run test:run` e `npm run build`. Peça revisão de outro integrante e registre no PR os testes executados e as pendências de ambiente.

O [fluxo da equipe](docs/team/development-workflow.md) e os [acordos de colaboração](docs/team/working-agreements.md) complementam este guia.
