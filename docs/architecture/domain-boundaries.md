# Responsabilidades dos módulos

A tabela relaciona os diretórios existentes de `backend/app/modules` aos comportamentos previstos. Estes módulos ainda não oferecem contratos de negócio executáveis. A divisão de pastas é uma escolha de organização do código. Os requisitos descrevem o comportamento observável pela equipe e pelos participantes.

| Módulo | Responsabilidade prevista | Referências |
| --- | --- | --- |
| `identity` | Provisionar acesso por e-mail, autenticar, redefinir senha e invalidar a sessão no logout ou na revogação. | RF002–RF004, RNF006 |
| `organization` | Associar cada equipe ao seu atlas, identificar participantes e capitão e manter as cotas de envio por participante. | RF001, RF010, seção 1.2 |
| `contributions` | Registrar uma foto por formulário, data e localização confirmadas pelo autor, tema e reflexão opcionais. Permitir edição com a imagem existente, exclusão pelo autor e consulta à galeria. | RF010–RF015, RF021 |
| `media` | Controlar o envio ao armazenamento privado, validar a imagem e extrair EXIF para o formulário. Produzir versões de exibição sem EXIF. | RF010–RF012, RNF007, RNF013, RNF021 |
| `curation` | Revisar registros completos, justificar ajustes ou rejeição, liberar registros aprovados e receber os corrigidos. Tratar o envio do capitão da própria equipe conforme RF018. | RF014, RF016–RF020, RF025 |
| `routes` | Reconstruir percursos automaticamente por equipe e dia e fornecer trajetos estimados e marcadores permitidos para as vistas geral e detalhada. | RF005–RF009, RF026–RF028, RNF023–RNF024 |
| `ai` | Gerar sugestões de descrição das imagens e propostas de conclusão da viagem. Usar reflexões aprovadas nos dois casos, quando aplicáveis, e manter a versão das fontes para invalidar os resultados afetados. | RF023–RF025, RF029–RF032, RNF008, RNF011, RNF025 |
| `publication` | Aplicar aprovação, autorização e retiradas à exibição. Atualizar a galeria, o mapa e os conteúdos dependentes após edições ou exclusões. Disponibilizar apenas a conclusão aprovada pela administração. | RF009, RF013–RF015, RF018, RF032, RNF005–RNF008, RNF011 |
| `exports` | Gerar PDF, PNG e GeoJSON autorizados, com os filtros, a precisão e os créditos apropriados. O HTML consta da visão geral do produto. | Seção 1.1, RF033–RF036, RNF008, RNF014 |
| `administration` | Conciliar o cadastro do IF-Arbitra, administrar cotas, temas e perguntas, atender retiradas e revisar a conclusão antes da publicação. | Seção 1.2, RF001, RF015, RF022, RF031 |

## Relações entre os dados

Uma equipe possui um atlas. Cada registro pertence ao seu autor e atlas. A data usada pelo mapa e pela galeria corresponde ao dia da atividade. A ausência de coordenadas impede a exibição daquele marcador e permite a consulta do registro aprovado na galeria. Um percurso referencia os registros válidos daquela equipe e daquele dia. A conclusão da viagem reúne reflexões de diferentes registros, inclusive contribuições dos capitães.

As alterações de autoria, publicação e visibilidade exigem autorização no servidor. As tarefas de edição e exclusão previstas para participantes alcançam os próprios registros. Os filtros “todas as equipes” disponibilizam somente os conteúdos autorizados ao leitor. Atribuir um registro a um atlas tampouco torna pública a localização exata de seu original. [Fluxo editorial](state-machine.md)

