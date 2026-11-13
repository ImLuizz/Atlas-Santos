# Módulo: Routes (Reconstrução e Edição de Percursos)

## Responsabilidades
- Reconstrução retrospectiva de percursos do atlas por dia com base nos pontos fotográficos de referência (RF-18, RN-11).
- Integração com provedor de roteamento pedestre através de adaptador desacoplado (RN-11, RNF-08).
- Edição do capitão: seleção de fotos de referência, reordenação, divisão de trechos da equipe e inserção de pontos intermediários (RF-19, RN-12).
- Tratamento de percursos incompletos, lacunas temporais/espaciais e falhas de serviço externo (RF-20).

## Invariantes
- O percurso é sempre rotulado como "percurso reconstruído pelas fotos", distinguindo a sugestão do serviço do ajuste editorial humano (RN-11).
- Linhas retas entre fotos não são apresentadas como ruas recuperadas (RF-18).
- Falha no serviço de roteamento não bloqueia o acesso à galeria nem aos marcadores fotográficos (RF-20, Risco 02).
- Distância calculada é uma estimativa de geometria, não medição de caminhada efetiva (RN-11).

