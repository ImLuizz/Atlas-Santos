# Entregas do Atlas Santos

A entrega do projeto está prevista para **4 de dezembro de 2026**. A ordem abaixo segue as dependências entre os fluxos. O [quadro de requisitos](docs/requirements/requirements-summary.md) traz os 36 RF e os 25 RNF, os critérios para demonstrá-los e as questões em aberto.

## Base disponível

A aplicação tem um frontend React, uma API FastAPI com consultas de saúde, uma migração para a fila de tarefas e testes da fundação. As interfaces de integração descrevem serviços a conectar. O banco atual ainda não contém o acervo ou os cadastros do estudo do meio.

## Trabalho restante

| Entrega | Depende de | Como demonstrar |
| --- | --- | --- |
| Acesso e organização (RF001–RF004) | Cadastro autorizado do IF-Arbitra e configuração do e-mail | Conciliar 83 estudantes e 12 servidores em equipes com capitães e um atlas por equipe. Provisionar por e-mail, entrar, redefinir senha a partir do login e sair. |
| Foto e Olhares (RF010–RF012, RF014–RF015, RF021–RF022) | Acesso, PostgreSQL e bucket privado | Preencher uma foto com EXIF, outra sem GPS, corrigir os campos, incluir tema e reflexão opcionais e respeitar a cota individual. Reabrir uma foto sem reenviar o arquivo. |
| Curadoria e galeria (RF013, RF016–RF020) | Registros e papéis autorizados | Aprovar o registro da equipe, justificar uma recusa e revisar o reenvio. Distinguir o envio inicial do capitão. Ver na galeria a própria equipe primeiro, combinar filtros e conferir a retirada. |
| Mapa e percursos (RF005–RF009, RF026–RF028) | Fotos aprovadas e localizadas, serviço pedestre via backend | Alternar todas as equipes/uma equipe, dia e vista 3D; abrir foto pelo marcador. Recalcular com as fotos em ordem cronológica. Preservar pontos disponíveis quando faltar um trajeto. |
| Descrições e síntese da viagem (RF023–RF025, RF029–RF032) | Imagens derivadas, reflexões aprovadas, integração de IA e papéis de revisão | Escolher, editar ou descartar a descrição. Testar uma imagem sem reflexão. Gerar síntese com relatos aprovados, revisar na administração e consultar a página publicada; tratar o caso sem base suficiente. |
| Exportações (RF033–RF036 e §1.1) | Permissões, registros, mapa e atribuição | Gerar PDF e PNG filtrados; em seguida, HTML e GeoJSON. Comparar campos, créditos, coordenadas e retiradas com o conteúdo autorizado. |
| Homologação e entrega (RNF001–RNF025) | Fluxos integrados e ambiente Railway | Testar acesso concorrente e 1.900 fotos de teste, navegação por teclado e lista, falhas/retentativas e restauração de banco e bucket. Verificar configuração e privacidade antes de usar dados reais. |

Para registrar progresso, vincule o requisito ao código e ao resultado de uma verificação reproduzível. Implantação, backup e ensaios exigem evidência do ambiente correspondente.
