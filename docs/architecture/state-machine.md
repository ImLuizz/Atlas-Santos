# Ciclo do registro fotográfico

O estado editorial pertence ao registro completo da fotografia. O processamento do arquivo e de tarefas derivadas pode avançar separadamente para manter a navegação disponível (RNF003). As transições abaixo representam o comportamento a implementar.

| Acontecimento | Resultado esperado |
| --- | --- |
| Participante envia uma foto | O formulário aceita uma fotografia, com data e localização preenchidas pelo EXIF ou pelo autor. Tema e reflexão são opcionais. O registro segue à fila do capitão da equipe (RF010–RF012, RF016–RF017, RF021). |
| Capitão envia sua própria foto | O envio inicial é aprovado automaticamente para seu atlas (RF018). A autorização de exibição e a proteção do original continuam aplicáveis. |
| Capitão aprova | O registro passa a integrar o atlas conforme as permissões de exibição. Havendo localização, pode contribuir para o mapa e o percurso (RF009, RF013, RF018, RF026). |
| Capitão solicita ajustes ou rejeita | O autor recebe a justificativa e pode corrigir e reenviar o registro. O capitão revisa os dados atualizados (RF019–RF020). |
| Autor edita um registro existente | O formulário recupera a imagem e os dados. O autor altera somente o necessário. A edição volta à aprovação antes de reaparecer no atlas (RF014). |
| Autor exclui ou a administração retira | O registro deixa a galeria e o mapa. Percursos, descrições e demais resultados dependentes devem refletir a mudança antes de nova exibição (RF015, RF036, RNF008, RNF011). |

## Efeito sobre a descrição e a reflexão

O serviço de IA usa a imagem e, quando disponível, a reflexão aprovada vinculada à foto. Na ausência dessa reflexão, utiliza somente a imagem. O sistema identifica as sugestões como geradas por IA. O usuário pode escolher, editar ou descartar a sugestão. O capitão revisa a descrição escolhida junto ao registro antes de ela aparecer no atlas (RF023–RF025). A reflexão escrita pelo participante continua identificável.

RF018 prevê aprovação automática **do envio da foto** do capitão. RF014 exige retorno para aprovação após qualquer edição e RF025 exige revisão da descrição sugerida. Essas operações devem ter casos de aceite próprios para que a aprovação automática inicial não seja aplicada por engano a um texto ou a uma edição posterior.

## Percurso por equipe e dia

A aprovação, edição, exclusão ou retirada que altera o conjunto de fotos válidas pode mudar o percurso. O backend usa o horário de captura e a localização autorizada dos registros aprovados para calcular automaticamente caminhos a pé. O mapa identifica a geometria como estimada. Se os dados forem insuficientes ou o serviço falhar, os marcadores e os registros autorizados permanecem consultáveis, e qualquer geometria desatualizada deixa de ser exibida (RF026–RF028, RNF008, RNF011–RNF012, RNF024).

## Conclusão da viagem

O sistema reúne reflexões aprovadas de participantes e capitães e usa IA para propor uma síntese em diálogo com *Sonho Manifesto*, de Sidarta Ribeiro. Deve preservar o sentido das contribuições e evitar atribuições sem respaldo. Com material insuficiente, precisa indicar a limitação em vez de apresentar o texto como representativo da viagem. A administração revisa, pode editar e aprova o texto antes de sua publicação em página própria (RF029–RF032). Uma retirada ou edição que comprometa as fontes exige atualizar ou invalidar a síntese afetada (RNF008, RNF011).

