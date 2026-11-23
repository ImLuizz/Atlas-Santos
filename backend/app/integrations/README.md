# Contratos de serviços externos

Os arquivos `base.py` descrevem as interfaces de armazenamento privado compatível com S3 (RNF021), roteamento a pé pelo backend (RNF024) e IA para descrições e conclusão da viagem (RNF025). Não há clientes de produção ou processadores registrados para esses serviços nesta versão.

Ao implementar uma integração, limitar o envio aos dados autorizados, prever falhas sem bloquear a navegação e respeitar as atribuições exigidas pelo provedor (RNF008, RNF012 e RNF014).
