# Módulo: Administration (Administração, Importação e Auditoria)

## Responsabilidades
- Importação pontual em JSON de dados de participantes e equipes do IF-Arbitra (RF-04, RF-05).
- Prévia de importação e conciliação dos 95 participantes (83 estudantes + 12 servidores) (RF-06).
- Idempotência na confirmação de lotes administrativos sem sobrescrever autoria ou fotos (RF-05, RNF-14).
- Consulta unificada de auditoria: log de ações críticas (aprovações, alterações de cota, lotes confirmados e exclusões) (RF-29).

## Invariantes
- A integração com IF-Arbitra é pontual via arquivo administrativo JSON; o Atlas não consulta o IF-Arbitra em runtime (RF-05).
- IDs internos do Atlas são preservados em reimportações (RF-05).
- Relatórios de conciliação devem demonstrar explicitamente os 83 estudantes e 12 servidores sem descartar participantes não alocados na origem (RF-06, RN-02).

