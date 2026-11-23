# Auditoria do Atlas Santos · 23 de novembro de 2026

A revisão comparou o [estado inicial do repositório](https://github.com/ImLuizz/Atlas-Santos/tree/1e4b5120fb5e6213e2de09bb561f6655883b3e85) com o documento de requisitos entregue pela equipe. A [matriz](requirements-summary.md) identifica os 36 requisitos funcionais e os 25 não funcionais, suas páginas de origem e o que ainda precisa ser demonstrado. O escopo da inspeção foi o repositório. A validação com o acervo da viagem e a homologação no Railway continuam pendentes.

| O que a equipe encontraria na versão anterior | Correção e impacto |
| --- | --- |
| O catálogo tinha 30 requisitos funcionais e a numeração do plano divergia do PDF. | A matriz e o [plano de implementação](../../TODO.md) usam os identificadores do documento. Cada funcionalidade tem um comportamento que a equipe pode conferir. |
| A documentação previa aprovação do percurso pelo capitão e reordenação manual. | O backend deverá ordenar as fotos aprovadas e localizadas por horário e estimar o percurso pedestre por equipe e dia. A curadoria incide sobre os registros. [Regras de estado](../architecture/state-machine.md) |
| O frontend carregava recursos do Leaflet, enquanto o PDF especifica Mapbox e deck.gl. | A dependência e a folha de estilo externa foram substituídas. A renderização dos mapas e a integração com o roteamento pedestre seguem no plano. |
| O planejamento de IA deixava de fora a conclusão coletiva da viagem. | A especificação distingue as sugestões de descrição de cada foto da síntese das reflexões aprovadas. A administração revisa a síntese antes da publicação. |
| A documentação da API misturava operações propostas com as disponíveis. | O [inventário da API](../api/README.md) identifica as duas consultas de saúde existentes. Login, envio de fotos, curadoria, mapas, galeria e exportações ainda precisam de implementação e testes de ponta a ponta. |
| O fluxo de integração contínua continha uma URL SQLite que impedia a leitura do YAML. | O workflow foi corrigido e inclui verificação das migrações contra PostgreSQL. |
| As instruções de operação antecipavam definições de retenção e rotinas da equipe. | O [guia de backup](../operations/backup-and-retention.md) indica o que a equipe precisa configurar e demonstrar, incluindo um teste de restauração. |

Para homologar o primeiro fluxo completo, a equipe precisa conseguir importar um participante do IF-Arbitra, entrar com seu perfil, enviar uma foto e vê-la no atlas da equipe após a aprovação prevista para aquele perfil. Esse fluxo verifica em conjunto identidade, cota, curadoria e visibilidade. Os critérios para os percursos, a IA e as exportações estão na matriz.
