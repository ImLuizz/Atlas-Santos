# Módulo: Contributions (Registros Fotográficos e Submissões)

## Responsabilidades
- Ciclo de vida do registro lógico de fotografia (`PhotoRecord`): autor, atlas, dia da atividade (05 a 11/10/2026), instante de captura corrigido (RN-09).
- Painel do participante: visualização de cotas, uso atual, reservas ativas e status das fotos (RF-07).
- Edição de metadados: correção de localização manual para fotos sem GPS e ajuste de hipótese de fuso horário (RF-11, RN-10).
- Submissão de temas pedagógicos e reflexões pessoais (opcionais e independentes, RF-24, RN-13).

## Invariantes
- A data e ordenação da foto dependem do instante de captura corrigido, nunca do instante do upload (RN-09).
- Fotos sem GPS podem participar da galeria; para exibição no mapa, requerem coordenada informada/corrigida e revisada (RN-10).
- O texto da reflexão é opcional; sua ausência não impede a aprovação da fotografia (RN-13).

