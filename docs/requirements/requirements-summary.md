# Especificação de Requisitos: Atlas Santos

## 1. Levantamento de Requisitos

### 1.1 Visão Geral do Sistema

O sistema Atlas Santos é uma aplicação web de cartografia colaborativa desenvolvida para organizar fotografias, memórias e aprendizagens do Estudo do Meio realizado em Santos, no período de 05 a 11 de outubro de 2026. O projeto adota o conceito de um Atlas por equipe, alimentado pelos registros dos participantes e validado por curadoria.

O objetivo principal da plataforma é entregar um acervo digital estruturado por equipe e dia de atividade, reunindo mapa interativo, galeria de imagens, percursos reconstruídos retrospectivamente a partir das fotografias, descrições assistidas por inteligência artificial (sempre sujeitas à revisão humana), reflexões pedagógicas individuais com síntese coletiva inspirada na obra Sonho Manifesto e exportação de documentos em múltiplos formatos (PDF, PNG, HTML e GeoJSON).

### 1.2 Público-Alvo

O sistema define três perfis de usuários principais, cada um com responsabilidades, permissões e fluxos de trabalho distintos dentro da plataforma:

- Participante (Estudante e Servidor): Usuário responsável por acessar o sistema por meio de convite controlado, consultar sua cota de envio (padrão de 20 fotografias por atlas), enviar arquivos de imagem diretamente para o armazenamento seguro, corrigir metadados de data e localização, preencher temas e reflexões pedagógicas opcionais no módulo Olhares sobre Santos, e acompanhar o status editorial de seus registros no painel pessoal.

- Capitão do Atlas: Usuário encarregado da curadoria e da gestão de sua respectiva equipe. Tem a responsabilidade de acessar a fila de submissões do seu atlas, revisar, aprovar, solicitar ajustes ou rejeitar (com justificativa) fotografias, legendas e reflexões, além de selecionar as descrições sugeridas pela inteligência artificial.

- Administração: Responsável por gerenciar o controle geral e a segurança da plataforma. Suas principais atribuições incluem importar e conciliar os dados dos 95 participantes (83 estudantes e 12 servidores) vindos do sistema IF-Arbitra, realizar o provisionamento dos acessos (via envio de e-mail com as credenciais) e definir as regras de cotas de fotos. Além disso, o administrador acompanha o histórico de alterações no sistema para garantir a rastreabilidade das ações (como saber quem alterou uma cota ou aprovou um registro) e gerencia solicitações de privacidade, podendo suspender ou remover conteúdos quando necessário.

### 1.3 Classificação dos Requisitos

Os requisitos para o desenvolvimento e implementação do Atlas Santos estão classificados nas seguintes categorias:

- Requisitos Funcionais (RF): Especificam os serviços e funcionalidades que o sistema deve fornecer ao usuário. Eles definem o que o sistema fará, e a forma como ele processará entradas e responderá em determinadas situações. São os requisitos obrigatórios, que descrevem o comportamento principal do software.

- Requisitos Não Funcionais (RNF): Especificam os critérios de qualidade e as restrições que o sistema deve cumprir. Eles descrevem como o sistema deve ser (rápido, seguro, intuitivo). Dessa forma, os RNF atuam como um complemento obrigatório dos requisitos funcionais.

### 1.4 Especificação dos Requisitos

#### 1.4.1 Requisitos Funcionais (RF)

##### 1.4.1.1 Acesso Controlado e Autenticação

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF001 | O sistema deve permitir que a administração mantenha o cadastro prévio dos participantes autorizados (83 estudantes e 12 servidores), suas respectivas equipes já formadas, o vínculo com o Atlas de cada grupo e a definição de quem exerce a função de capitão. | Administração | Gestão de Vínculos |
| RF002 | O sistema deve enviar automaticamente um e-mail com as credenciais de acesso para todos os usuários cadastrados. | Sistema/Administração | Provisionamento |
| RF003 | O sistema deve permitir que os usuários façam login utilizando as credenciais recebidas por e-mail, bem como realizar o logout seguro da conta a qualquer momento. | Participantes, Capitão e Administração | Login/Logout |
| RF004 | O sistema deve permitir que os usuários redefinam suas senhas caso desejem, disponibilizando essa opção diretamente na tela de login. | Participantes, Capitão e Administração | Gestão de Conta |

##### 1.4.1.2 Atlas Interativo e Visualização dos Percursos

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF005 | O sistema deve disponibilizar um mapa interativo do Atlas Santos, permitindo visualizar os percursos estimados das equipes durante a viagem, organizados por equipe e dia de atividade | Participantes e Capitão | Visualização do Atlas |
| RF006 | O sistema deve permitir visualizar os percursos de todas as equipes simultaneamente, proporcionando uma visão geral das atividades realizadas durante a viagem. | Participantes e Capitão | Visão Geral dos Percursos |
| RF007 | O sistema deve disponibilizar uma legenda interativa que permita selecionar ou alternar entre equipes e dias da viagem, controlando quais percursos são exibidos no mapa. Deve ser possível visualizar o percurso de uma equipe ou todos os percursos simultaneamente. | Participantes e Capitão | Legenda e Filtros do Mapa |
| RF008 | Ao selecionar uma equipe específica, o sistema deve aproximar e centralizar o mapa em seu percurso, proporcionando uma visualização mais detalhada, com representação tridimensional do trajeto. Ao retornar à visão geral de todas as equipes, deve apresentar novamente o mapa em sua visualização geral. | Participantes e Capitão | Visualização Detalhada dos Percursos |
| RF009 | O sistema deve apresentar marcadores no mapa correspondentes às fotografias que possuem localização definida e estão autorizadas para exibição. Ao selecionar um marcador, deve permitir visualizar a fotografia e suas informações, incluindo os dados do registro, legenda e reflexão, quando disponíveis. | Participantes e Capitão | Marcadores e Detalhamento das Fotografias |

##### 1.4.1.3 Gestão e Visualização das Fotografias

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF010 | O sistema deve permitir que participantes e capitães enviem fotografias da viagem por meio de um formulário, sendo permitido o envio de uma fotografia por preenchimento e respeitando o limite de 20 fotografias por participante. O formulário também deve disponibilizar campos para o registro de uma reflexão e a seleção de um tema, quando disponível. | Participantes e Capitão | Envio de Fotografias |
| RF011 | O sistema deve identificar e extrair os metadados EXIF disponíveis nas fotografias, como data, horário e localização, utilizando essas informações para preencher automaticamente os campos correspondentes do formulário de envio. | Participantes e Capitão | Aproveitamento de Metadados |
| RF012 | O sistema deve permitir que o participante informe ou corrija manualmente os dados da fotografia, como localização, data e horário, caso estejam ausentes ou incorretos. | Participantes e Capitão | Complementação dos Dados |
| RF013 | O sistema deve disponibilizar uma galeria de fotografias aprovadas, organizadas por equipe e dia da viagem. Na visualização inicial, deve destacar a equipe à qual o usuário pertence, oferecendo acesso rápido às suas fotografias. A galeria deve permitir filtrar as fotografias por equipe, incluindo a opção de visualizar todas as equipes, e por dia da viagem, permitindo combinar os dois filtros. | Participantes e Capitão | Galeria de Fotografias |
| RF014 | O sistema deve permitir que os usuários editem os próprios registros de fotografias após o envio, carregando previamente os dados existentes, incluindo a imagem anexada. O usuário poderá alterar apenas os campos desejados, sem precisar enviar novamente a fotografia. Após qualquer edição, o registro deverá retornar para aprovação do capitão antes de voltar a ser disponibilizado no Atlas. | Participantes e Capitão | Edição das Fotografias |
| RF015 | O sistema deve permitir que o participante exclua os próprios registros de fotografias e que a administração realize a retirada de registros do Atlas quando necessário, especialmente em situações relacionadas à privacidade. A exclusão ou retirada deverá refletir na galeria, no mapa e nos percursos estimados, impedindo que o conteúdo retirado continue sendo disponibilizado. | Participantes e Administração | Exclusão e Retirada de Fotografias |

##### 1.4.1.4 Curadoria e Gestão das Fotografias pelo Capitão

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF016 | O sistema deve encaminhar os registros de fotografias enviados pelos participantes para uma fila de revisão do capitão responsável pela equipe correspondente. | Capitão | Fila de Revisão |
| RF017 | O sistema deve permitir que o capitão analise o registro completo da fotografia, incluindo a imagem, os dados informados, o tema selecionado e a reflexão registrada, quando houver. | Capitão | Análise dos Registros |
| RF018 | O sistema deve permitir que o capitão aprove os registros analisados, tornando-os disponíveis no Atlas. As fotografias enviadas pelo próprio capitão devem ser aprovadas automaticamente, sem necessidade de passar pela fila de revisão. | Capitão | Aprovação das Fotografias |
| RF019 | O sistema deve permitir que o capitão não aprove um registro, exigindo o preenchimento de uma justificativa que deverá ser disponibilizada ao participante responsável. | Capitão | Justificativa de Não Aprovação |
| RF020 | O sistema deve permitir que o capitão revise novamente os registros corrigidos pelos participantes e reenviados para aprovação, considerando todas as informações atualizadas antes de aprová-los ou não aprová-los. | Capitão | Revisão de Registros Corrigidos |

##### 1.4.1.5 Olhares sobre Santos

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF021 | O sistema deve permitir que os participantes registrem reflexões relacionadas às fotografias enviadas, por meio dos campos disponíveis no formulário de envio, conforme descrito no RF010. | Participantes e Capitão | Registro de Reflexões |
| RF022 | O sistema deve permitir que a administração cadastre, edite e disponibilize temas e perguntas orientadoras para o módulo Olhares sobre Santos, que servirão como estímulo para as reflexões dos participantes. | Administração | Administração de Temas e Perguntas |

##### 1.4.1.6 Descrições das Fotografias por Inteligência Artificial

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF023 | O sistema deve analisar o conteúdo visual das fotografias enviadas e utilizar a reflexão aprovada associada a elas, quando disponível, como contexto complementar para a análise. Caso não exista uma reflexão aprovada, a análise deverá considerar somente o conteúdo da imagem. | Sistema | Análise de Fotografias por IA |
| RF024 | O sistema deve gerar sugestões de descrição para as fotografias com base na análise realizada, relacionando os elementos identificados na imagem à reflexão utilizada, quando disponível. As sugestões devem ser identificadas como geradas por inteligência artificial e não devem apresentar como certos elementos ou informações que não possam ser confirmados. | Sistema | Geração de Descrições por IA |
| RF025 | O sistema deve permitir que o usuário escolha uma das sugestões de descrição geradas pela inteligência artificial, edite seu conteúdo ou descarte as sugestões. A descrição escolhida ou editada deverá ser encaminhada para a revisão do capitão junto ao registro da fotografia, antes de sua disponibilização no Atlas. | Participantes e Capitão | Revisão de Descrições por IA |

##### 1.4.1.7 Reconstrução e Visualização dos Percursos

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF026 | O sistema deve gerar automaticamente percursos estimados para cada equipe e dia da viagem, utilizando como referência as fotografias aprovadas que possuem localização definida. A geração deverá considerar a sequência cronológica dos registros e utilizar um algoritmo de roteamento para conectar os pontos por caminhos disponíveis. | Sistema | Reconstrução dos Percursos |
| RF027 | O sistema deve apresentar os percursos estimados no mapa interativo descrito nos RF005 a RF008, permitindo visualizar individualmente o percurso de qualquer equipe ou os percursos de todas as equipes simultaneamente, conforme o dia da viagem selecionado. | Participantes e Capitão | Visualização dos Percursos |
| RF028 | O sistema deve tratar situações em que não existam pontos suficientes ou informações de localização para gerar um percurso estimado, mantendo disponíveis os marcadores e as fotografias que puderem ser exibidos no mapa, conforme o comportamento definido no RF009. | Sistema | Tratamento de Percursos Incompletos |

##### 1.4.1.8 Conclusão da Viagem por Inteligência Artificial

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF029 | O sistema deve reunir as reflexões aprovadas registradas pelos participantes e capitães nos diferentes registros de fotografias, considerando o conjunto de contribuições realizadas durante a viagem como base para a elaboração de sua conclusão. | Sistema | Reunião das Reflexões |
| RF030 | O sistema deve utilizar inteligência artificial para analisar o conjunto das reflexões reunidas e elaborar um texto de conclusão sobre a viagem, estabelecendo relações entre as experiências e percepções relatadas pelos participantes e capitães e as ideias presentes no livro Sonho Manifesto, de Sidarta Ribeiro. O texto deve preservar o sentido das contribuições analisadas, sem distorcer os relatos ou atribuir à obra ideias, citações ou afirmações não verificadas. Caso o conteúdo disponível seja insuficiente para uma análise consistente, o sistema não deverá apresentar uma conclusão como se fosse representativa da experiência coletiva. | Sistema | Geração da Conclusão por IA |
| RF031 | O sistema deve permitir que a administração revise o texto de conclusão gerado pela inteligência artificial antes de sua publicação, podendo aprová-lo ou realizar alterações em seu conteúdo. | Administração | Revisão da Conclusão |
| RF032 | O sistema deve disponibilizar uma página própria no Atlas Santos para apresentar a conclusão aprovada da viagem, permitindo que participantes e capitães consultem a síntese das experiências e reflexões registradas. | Participantes e Capitão | Página de Conclusão da Viagem |

##### 1.4.1.9 Exportação do Atlas

| ID | Descrição | Autor(es) | Base |
| --- | --- | --- | --- |
| RF033 | O sistema deve permitir a exportação do Atlas em formato PDF, considerando o recorte selecionado pelo usuário, como equipe e dia da viagem. O documento deverá apresentar o mapa, a legenda, a identificação do conteúdo exportado e os créditos correspondentes, permitindo incluir fotografias selecionadas e seus textos aprovados. | Participantes e Capitão | Exportação em PDF |
| RF034 | O sistema deve permitir a exportação da visualização do mapa em formato PNG, considerando os filtros aplicados e apresentando os percursos estimados, marcadores e elementos visuais correspondentes ao recorte selecionado. A imagem deverá manter proporções adequadas e resolução suficiente para leitura das informações, sem tentar incluir uma galeria extensa de fotografias. | Participantes e Capitão | Exportação em PNG |
| RF035 | O sistema deve permitir a exportação dos dados geográficos do Atlas em formato GeoJSON, incluindo os pontos correspondentes às fotografias com localização definida e os segmentos dos percursos estimados. Os dados deverão respeitar o padrão do formato, utilizando longitude antes de latitude e identificando os percursos como reconstruções estimadas. | Participantes e Capitão | Exportação em GeoJSON |
| RF036 | O sistema deve verificar as permissões de acesso e a autorização de exibição dos registros antes de gerar e disponibilizar os arquivos exportados. Os arquivos não devem conter informações privadas, metadados EXIF brutos, credenciais ou dados de acesso ao armazenamento das fotografias, nem informações de localização mais precisas do que as autorizadas. | Sistema | Controle de Exportações |

#### 1.4.2 Requisitos Não Funcionais (RNF)

##### 1.4.2.1 Desempenho

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF001 | O sistema deverá suportar o acesso dos 95 participantes previstos, mantendo o funcionamento adequado de suas funcionalidades durante os períodos de utilização simultânea. | Desempenho |
| RNF002 | O sistema deverá suportar o armazenamento e a consulta de aproximadamente 1.900 fotografias, considerando o limite previsto de 20 fotografias por participante, sem comprometer o funcionamento das funcionalidades de visualização, filtros e navegação. | Desempenho |
| RNF003 | O processamento de fotografias, geração de descrições por inteligência artificial, reconstrução de percursos e exportação de arquivos não deverá bloquear as operações comuns de consulta e navegação do sistema. | Desempenho |

##### 1.4.2.2 Segurança

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF004 | O sistema deverá utilizar comunicação segura por HTTPS em ambiente de produção, protegendo as informações transmitidas entre os usuários e o servidor. | Segurança |
| RNF005 | O sistema deverá validar, no servidor, as permissões dos usuários antes de permitir operações sobre contas, fotografias, registros e demais recursos, impedindo o acesso não autorizado por meio da alteração direta de identificadores ou endereços de acesso. | Segurança |
| RNF006 | As sessões dos usuários deverão ser protegidas contra utilização indevida, incluindo o armazenamento seguro das credenciais e a invalidação do acesso após o encerramento ou revogação da sessão. Informações sensíveis e segredos de integração deverão permanecer protegidos no servidor, sem exposição no código disponibilizado ao navegador. | Segurança |

##### 1.4.2.3 Privacidade e Proteção de Dados

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF007 | O sistema deverá proteger as fotografias originais, informações pessoais e dados de localização precisa, permitindo seu acesso somente a usuários e serviços autorizados. Os arquivos derivados destinados à exibição deverão ter seus metadados EXIF removidos, preservando apenas as informações necessárias ao funcionamento do Atlas. | Privacidade |
| RNF008 | O compartilhamento de informações com serviços externos, incluindo provedores de inteligência artificial, deverá limitar-se aos dados necessários para a operação solicitada, respeitando as permissões de acesso e as condições de privacidade estabelecidas para o conteúdo. As exportações e os percursos deverão respeitar as mesmas restrições de divulgação aplicadas aos registros de origem. | Privacidade |

##### 1.4.2.4 Usabilidade e Acessibilidade

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF009 | A interface deverá ser responsiva, permitindo a utilização das funcionalidades principais em computadores, tablets e dispositivos móveis, sem comprometer a visualização e a navegação. | Usabilidade |
| RNF010 | A interface deverá oferecer recursos básicos de acessibilidade, incluindo identificação dos campos de formulário, indicação visual de foco, navegação por teclado e mensagens de erro associadas aos campos correspondentes. As informações apresentadas no mapa também deverão possuir uma alternativa de consulta em formato de lista, e os estados do sistema não deverão depender exclusivamente da utilização de cores. | Acessibilidade |

##### 1.4.2.5 Integridade e Consistência dos Dados

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF011 | O sistema deverá preservar a integridade dos registros de fotografias e de suas informações associadas, garantindo que alterações, exclusões e novas aprovações sejam refletidas corretamente nas informações disponibilizadas no Atlas. Conteúdos que dependam de registros alterados ou retirados, como descrições geradas por inteligência artificial e percursos estimados, deverão ser atualizados ou invalidados para impedir a apresentação de informações desatualizadas. | Integridade |

##### 1.4.2.6 Confiabilidade e Recuperação de Operações

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF012 | O sistema deverá tratar falhas durante o processamento de fotografias, geração de descrições por inteligência artificial, reconstrução de percursos e exportação de arquivos, permitindo a recuperação ou nova tentativa das operações sem provocar perda dos registros já enviados ou apresentar resultados como concluídos quando houver falha. A indisponibilidade de serviços externos não deverá impedir o funcionamento das funcionalidades que não dependam deles. | Confiabilidade |

##### 1.4.2.7 Segurança de Arquivos e Conteúdos

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF013 | O sistema deverá validar os arquivos enviados pelos usuários, verificando seu formato, tamanho e características necessárias ao processamento, recusando arquivos inválidos ou incompatíveis. Os conteúdos textuais e visuais enviados pelos participantes deverão ser tratados como dados, não podendo executar códigos ou alterar instruções e permissões internas do sistema. | Segurança |

##### 1.4.2.8 Integrações e Serviços Externos

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF014 | Os serviços externos utilizados pelo sistema, incluindo provedores de mapas, roteamento e inteligência artificial, deverão respeitar suas respectivas condições de uso e atribuição. Os mapas e arquivos exportados deverão apresentar os créditos cartográficos exigidos pelos provedores utilizados. | Interoperabilidade |

##### 1.4.2.9 Implantação e Manutenibilidade

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF015 | A aplicação deverá ser hospedada na plataforma Railway, utilizando configurações específicas para os ambientes de desenvolvimento, homologação e produção. | Manutenibilidade |
| RNF016 | O sistema deverá documentar os endpoints e os contratos de sua API, padronizando as respostas de erro para facilitar a identificação e a manutenção de problemas. As mensagens apresentadas aos usuários não deverão expor informações técnicas sensíveis, como detalhes internos do servidor ou rastros de execução. | Manutenibilidade |

##### 1.4.2.10 Backup e Recuperação dos Dados

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF017 | O sistema deverá possuir mecanismos de backup e recuperação do banco de dados e dos arquivos armazenados, considerando a necessidade de proteger ambos os componentes. O procedimento de restauração deverá preservar os vínculos entre os registros e os arquivos correspondentes, respeitando também as exclusões e retiradas de conteúdo realizadas no Atlas. | Confiabilidade |

##### 1.4.2.11 Ferramentas

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF018 | O backend do sistema deverá ser desenvolvido utilizando a linguagem Python e o framework FastAPI, responsáveis pela implementação da API e da lógica de negócio. | Tecnologia |
| RNF019 | A interface do sistema deverá ser desenvolvida utilizando a biblioteca React, com Vite como ferramenta de construção e gerenciamento do frontend, e Tailwind CSS para a estilização dos componentes. | Tecnologia |
| RNF020 | O banco de dados utilizado para o armazenamento persistente das informações deverá ser o PostgreSQL, com SQLAlchemy para o mapeamento objeto-relacional e Alembic para o gerenciamento das migrações. | Tecnologia |
| RNF021 | O armazenamento das fotografias e dos arquivos gerados pelo sistema deverá utilizar Railway Buckets, por meio de uma integração compatível com o padrão S3. | Tecnologia |
| RNF022 | A aplicação deverá ser hospedada na plataforma Railway, utilizando configurações específicas para os ambientes de desenvolvimento e produção. | Tecnologia |
| RNF023 | A cartografia do sistema deverá utilizar Mapbox como provedor de mapas e deck.gl para a renderização e visualização dos dados geográficos, incluindo os pontos e os percursos reconstruídos. | Tecnologia |
| RNF024 | A reconstrução dos percursos deverá utilizar um serviço de roteamento adequado para trajetos a pé, integrado ao sistema por meio do backend. | Tecnologia |
| RNF025 | A geração de sugestões de descrição das fotografias e a elaboração da conclusão da viagem deverão utilizar um serviço de inteligência artificial integrado ao backend. | Tecnologia |
