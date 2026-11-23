# Contratos HTTP do Atlas Santos

## Rotas implementadas

| Método e caminho | O que verifica |
| --- | --- |
| `GET /health` | Estado da API e conectividade com o banco configurado. |
| `GET /api/v1/health` | O mesmo diagnóstico, sob o prefixo versionado. |

Com o banco conectado, a sonda responde HTTP 200 com `status: healthy` e `database: connected`. Se a consulta falhar, responde HTTP 503 com `status: degraded` e `database: disconnected`. Em ambos os casos o JSON inclui `app_name`, `version`, `environment` e `timestamp` em UTC. Para verificar um fluxo como upload ou curadoria é preciso exercitar o respectivo contrato de negócio.

Com `DEBUG=true`, o aplicativo disponibiliza `/docs`, `/redoc` e `/openapi.json`. O roteador registrado no código e o esquema gerado identificam os contratos executáveis. [Registro de rotas](../../backend/app/api/v1/router.py) · [Sondas de saúde](../../backend/app/api/v1/endpoints/health.py) · [Configuração da API](../../backend/app/main.py)

## Contratos a desenvolver

Os requisitos definem comportamentos, sem prescrever URLs para cada operação. O prefixo previsto para novas rotas é `/api/v1`. O navegador deverá consumir esses contratos à medida que a equipe os implementar, documentar e testar.

| Área | Comportamento a expor |
| --- | --- |
| Acesso | Vínculos e capitães, provisionamento automático por e-mail, login, logout e redefinição de senha (RF001–RF004). |
| Mapa e galeria | Consultas autorizadas por dia e equipe ou todas as equipes, marcadores com detalhes, percursos estimados e alternativa em lista (RF005–RF009, RF013, RF026–RF028, RNF010). |
| Fotos e curadoria | Enviar uma foto por formulário, preencher ou corrigir metadados, editar ou excluir a própria contribuição, revisar o registro completo e justificar a não aprovação (RF010–RF020). |
| Olhares sobre Santos | Registrar reflexões opcionais por fotografia e permitir à administração manter temas e perguntas (RF021–RF022). |
| IA | Sugerir descrições, receber a escolha ou edição do usuário e revisão do capitão. Gerar a síntese das reflexões aprovadas, receber revisão administrativa e fornecer a conclusão aprovada (RF023–RF025, RF029–RF032). |
| Exportações | Identificar o recorte permitido, disponibilizar PDF, PNG e GeoJSON com as restrições de conteúdo e precisão vigentes. A visão geral também inclui HTML e seus detalhes estão em aberto (RF033–RF036, seção 1.1). |

O contrato de cada nova operação deverá indicar formato de entrada, resultado, permissões e falhas esperadas. RNF016 requer erros consistentes e compreensíveis, sem mensagens internas ou rastros de execução. Status editoriais, decisões do capitão ou arquivos só podem ser revelados ao solicitante autorizado (RNF005–RNF008).

