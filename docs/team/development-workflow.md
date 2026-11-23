# Fluxo de desenvolvimento

1. Selecione um item do [plano de trabalho](../../TODO.md). Confira o RF ou RNF correspondente na [matriz](../requirements/requirements-summary.md).
2. Atualize a `main` e abra uma branch com nome relacionado à tarefa. Prefira mudanças que possam ser testadas como uma unidade.
3. Execute a API e o frontend conforme o [README](../../README.md). Se a entrega envolver uma tarefa assíncrona, execute também o worker e confira o resultado persistido.
4. Rode os testes da área alterada. Indique quais cenários usaram dados locais e quais foram exercitados em homologação.
5. Abra um pull request com comportamento anterior, comportamento esperado e evidências de verificação. Solicite revisão antes de integrar.
