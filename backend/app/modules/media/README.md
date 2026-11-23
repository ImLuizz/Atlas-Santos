# Mídia

O formulário envia uma foto de cada vez ao armazenamento privado. A extração de EXIF auxilia o preenchimento de data, horário e localização antes de o participante confirmar ou corrigir os dados (RF010 a RF012).

O backend deve validar o formato, tamanho e características da imagem. Os originais e a localização precisa têm acesso restrito. Os derivados de exibição precisam perder o EXIF, inclusive as coordenadas nele contidas (RNF007 e RNF013). Fotografias e arquivos gerados usam Railway Buckets por meio de uma integração compatível com S3 (RNF021).
