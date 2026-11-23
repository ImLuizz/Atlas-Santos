# ADR-0002 · Tecnologias do Atlas Santos

Registro original de 12/11/2026, revisto conforme RNF018–RNF025 da especificação enviada. A tabela descreve a tecnologia exigida e o papel que terá no produto. A instalação de uma biblioteca é apenas uma parte da implementação.

| Componente | Tecnologia | Uso no Atlas | Requisito |
| --- | --- | --- | --- |
| API | Python e FastAPI | Autorização, lógica de negócio, contratos e integrações. | RNF018 |
| Interface | React com JavaScript/JSX, Vite e Tailwind CSS | Formulário de foto, galeria, mapa, curadoria e página da conclusão. | RNF019 |
| Persistência | PostgreSQL, SQLAlchemy e Alembic | Vínculos, registros e migrações. O SQLite atende testes locais e não substitui a validação no PostgreSQL. | RNF020 |
| Arquivos | Railway Buckets com API compatível com S3 | Originais privados, imagens de exibição e exportações. | RNF021 |
| Hospedagem | Railway | Configuração específica de desenvolvimento, homologação e produção. | RNF015, RNF022 |
| Cartografia | Mapbox e deck.gl | Mapbox fornece o mapa-base. deck.gl renderiza pontos e percursos, incluindo a vista detalhada da equipe. | RNF023, RF005–RF009 |
| Percursos | Serviço de roteamento a pé integrado ao backend | Conectar fotos aprovadas em ordem cronológica por equipe e dia. A especificação deixa o fornecedor de roteamento em aberto. | RNF024, RF026–RF028 |
| IA | Serviço integrado ao backend | Sugerir descrições das fotos e elaborar a conclusão coletiva com as revisões humanas previstas. O provedor também permanece em aberto. | RNF025, RF023–RF025, RF029–RF032 |

O mapa, os derivados e as exportações devem respeitar a precisão permitida e os créditos dos provedores. Credenciais privadas do armazenamento, do roteamento e da IA ficam no servidor. O frontend pode receber a configuração pública necessária ao mapa-base (RNF006–RNF008, RNF014). As versões utilizadas na compilação estão nos manifestos e no arquivo de dependências do frontend. [Manifesto do backend](../../backend/pyproject.toml) · [Manifesto do frontend](../../frontend/package.json) · [Dependências resolvidas do frontend](../../frontend/package-lock.json)

