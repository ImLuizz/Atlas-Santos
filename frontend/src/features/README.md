# Organização de Features no Frontend — Atlas Santos

Este diretório agrupa os módulos de interface orientados a recursos/domínios do usuário:

- `auth/`: Telas e hooks de login, aceitação de convite e encerramento de sessão.
- `contributions/`: Painel do participante, visualização de cotas e submissão de fotos.
- `curation/`: Fila de trabalho do capitão, revisão de mídia e aprovação de textos.
- `atlas-explorer/`: Mapa interativo (React-Leaflet), percursos reconstruídos e galeria de fotos.
- `exports/`: Solicitação e download de cadernos em PDF, painéis PNG, HTML e GeoJSON.
- `admin/`: Conciliação dos 95 participantes, importação do IF-Arbitra e auditoria.

## Convenções de Componentes
- Use **PascalCase** para nomes de arquivos de componentes (`PhotoCard.jsx`, `MapViewer.jsx`).
- Use **camelCase** para hooks e funções utilitárias (`useAuth.js`, `formatDate.js`).
- Não faça chamadas diretas com `fetch` solto nos componentes; utilize o cliente centralizado em `lib/api-client.js`.

