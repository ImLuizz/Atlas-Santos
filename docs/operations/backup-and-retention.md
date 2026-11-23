# Backup e restauração do acervo

RNF017 exige que a equipe possa recuperar tanto o banco quanto os arquivos, preservar os vínculos entre eles e respeitar exclusões e retiradas já efetuadas. RF015, RF036 e RNF008 estendem essa proteção à galeria, ao mapa, aos percursos e às exportações.

## Estado no repositório

O repositório inclui migrações do banco. Elas recriam estruturas de dados, mas não recuperam as fotos nem o conteúdo perdido. Ainda há trabalho operacional para configurar e demonstrar cópias recuperáveis de PostgreSQL e Railway Buckets, manter o registro de retiradas recuperável e executar um ensaio de restauração.

## Preparação

A equipe deve escolher a frequência das cópias, sua retenção, o tempo de recuperação pretendido e os responsáveis conforme volume, custos e condições dos ambientes. A especificação não fixa números para esses parâmetros. Verificar quais mecanismos de cópia o ambiente contratado realmente oferece para o banco e para os objetos.

Guardar cópias privadas do banco e dos arquivos e registrar os pontos de recuperação compatíveis. Manter informação suficiente para reconhecer exclusões e retiradas posteriores à cópia restaurada. Uma cópia antiga que também desfaz o registro de retirada pode voltar a exibir material que a administração já retirou.

## Ensaio de recuperação em homologação

1. Com dados de teste, registrar uma foto com seu identificador de objeto e produzir uma cópia do banco e dos arquivos. Depois, realizar uma retirada de conteúdo e guardar evidência dessa decisão.
2. Em um ambiente isolado, restaurar o banco e os objetos do mesmo ponto de recuperação. Conferir que os registros ativos apontam para seus arquivos e identificar arquivos faltantes antes de liberar o acesso.
3. Reaplicar as exclusões e retiradas posteriores. Invalidar derivados e resultados afetados, incluindo trajetos, síntese e exportações acessíveis. Manter os originais privados durante a restauração.
4. Verificar com os perfis do Atlas que a foto mantida continua disponível ao público autorizado e que o registro retirado deixou de ser consultável ou baixável. Registrar duração, ponto recuperado, perdas identificadas e correções necessárias para repetir o procedimento.

O resultado do ensaio deve indicar o ambiente e o que foi efetivamente recuperado. A configuração de um agendamento por si só não demonstra restaurabilidade.

