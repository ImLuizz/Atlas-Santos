# Módulo: Organization (Equipes, Atlas, Vínculos e Cotas)

## Responsabilidades
- Cadastro e manutenção de Equipes e seus respectivos Atlas (relação 1:1, RN-01).
- Vínculos de participação (`Membership`): vincula participante ao atlas com papel (participante, capitão do atlas, admin) e direito de contribuição (RF-03).
- Gestão atômica de cotas de fotos por vínculo (padrão de 20 fotos por participante em cada atlas autorizado, RN-03, RN-05).
- Configuração de exceções individuais de cotas e audiência da equipe.

## Invariantes
- Não existe entidade denominada `Projeto`; a unidade de organização é `Atlas` pertencente a uma `Equipe`.
- Servidor responsável importado do IF-Arbitra não recebe automaticamente papel de capitão nem permissão editorial (RF-03, RN-02).
- Troca de identificador de equipe ou participante deve impedir acesso não autorizado cruzado.
- Operações de reserva e consumo de cota devem ser atômicas no PostgreSQL com locks ou transações ACID (RN-05, RNF-03).

