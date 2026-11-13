# Camada de Integrações e Adaptadores Externos — Atlas Santos

Este diretório implementa o padrão **Hexagonal / Ports and Adapters** para isolar o núcleo da aplicação de provedores externos proprietários (ver [ADR-06](../../../docs/decisions/ADR-0001-modular-monolith-and-worker.md)).

## Diretrizes
1. O domínio de negócio conversa apenas com a interface abstrata (`base.py`).
2. Implementações concretas de fornecedores de IA, Roteamento e Armazenamento podem ser substituídas sem alterar os casos de uso.
3. Tratamento defensivo de falhas: timeouts, retentativas com backoff e circuit breakers são implementados nos adaptadores (Risco 02).

