# Funcionalidades do frontend

A página inicial consulta a disponibilidade da API. As telas abaixo fazem parte do escopo de desenvolvimento.

| Área | Fluxo previsto |
| --- | --- |
| Acesso | Entrar com as credenciais enviadas por e-mail, redefinir a senha pela tela de login e sair (RF002–RF004). |
| Envio | Uma fotografia por formulário, cota por participante e atlas, preenchimento por EXIF, correção manual, tema e reflexão opcionais (RF010–RF012, RF021). |
| Acervo | Galeria com destaque inicial para a própria equipe e filtros por equipe e dia. Edição de um registro já enviado sem reenviar a foto, retorno à revisão e retirada dos conteúdos dependentes (RF013–RF015). |
| Curadoria | Revisão dos envios pelo capitão, devolutiva com justificativa e reenvio. O envio inicial do próprio capitão tem aprovação automática (RF016–RF020). |
| Mapa | Mapbox GL JS apresenta o mapa-base. deck.gl exibe os pontos e percursos autorizados, com visão de todas as equipes, filtros por equipe e dia, foco em 3D e acesso às fotos pelos marcadores. O backend estima os percursos pedestres a partir das fotos aprovadas em ordem cronológica. Se faltarem pontos para uma rota, continuam disponíveis os marcadores e as fotos autorizados (RF005–RF009, RF026–RF028, RNF023–RNF024). |
| Olhares sobre Santos | A administração mantém os temas e as perguntas. A IA sugere descrições identificadas como tal, que o usuário pode escolher, editar ou descartar e que o capitão revisa. A síntese coletiva das reflexões aprovadas tem revisão da administração e página própria (RF021–RF025, RF029–RF032). |
| Exportações | PDF, PNG e GeoJSON respeitam os filtros, permissões e créditos cartográficos (RF033–RF036, RNF014). A visão geral também cita HTML, sem detalhar seu conteúdo. |
| Administração | Conciliação dos dados do IF-Arbitra, equipes, capitães, cotas, histórico e retirada de registros por privacidade (seção 1.2, RF001, RF015). |

Para integrar o mapa, use o token público `VITE_MAPBOX_ACCESS_TOKEN` e mantenha os créditos exigidos pelo provedor visíveis na tela e nas exportações. Ofereça consulta alternativa em lista, navegação por teclado e indicação textual dos estados (RNF010). O frontend consome da API os dados autorizados e as geometrias já calculadas.
