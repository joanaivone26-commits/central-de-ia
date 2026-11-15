---
description: "Para um vídeo, aula ou live, entrega numa execução 10 títulos pontuados (melhor + 2), descrição em texto puro com o bloco de links dos canais, capítulos, tags, prompts de thumbnail em 16x9 e 9x16, posts de divulgação e avisos para grupos e comunidade, todos coerentes entre si e prontos para colar."
argument-hint: "[tipo_de_conteudo] [conteudo] [ideia_central] [serie] [participantes] [links_do_conteudo] [bloco_de_canais] [cta_principal] [publico] [tom] [intensidade] [identidade_visual] [mapa_de_imagens] [ferramenta_de_imagem] [pecas_anteriores] [canais_de_divulgacao] [data_e_hora] [mercado_idioma] [contexto_da_oferta] [anexos] [destino]"
---

<!-- Central Trip Angle · prompt conteudo/pacote-de-publicacao -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: tipo_de_conteudo (O que vai ser publicado (vídeo do YouTube, aula, live, call gravada, podcast) e a duração); conteudo (Tópicos completos, roteiro ou transcrição, com minutagem quando houver); bloco_de_canais (Bloco fixo com os links dos seus canais, na ordem em que deve aparecer); identidade_visual (Paleta em HEX com proporção, fontes, estilo, uso da logo e cores proibidas). Opcionais: ideia_central (A única ideia que o conteúdo precisa vender em 2 segundos (se vazio, eu extraio do conteúdo)); serie (Nome e prefixo fixo da série, se o conteúdo fizer parte de uma); participantes (Apresentador e convidados, com o papel de cada um e o perfil público); links_do_conteudo (Links citados no conteúdo (material, oferta, cadastro, vídeo anterior), cada um com rótulo); cta_principal (Ação principal pedida ao público; padrão: assistir até o fim e seguir o canal); publico (Público e nível (iniciante, intermediário, avançado); padrão: o público atual do canal); tom (Tom dos textos; padrão: direto e específico, curiosidade que o conteúdo cumpre); intensidade (Intensidade de 1 (sóbrio) a 5 (provocativo); padrão: 3 de 5); mapa_de_imagens (O que é cada imagem enviada (IMAGEM 1 = apresentador, IMAGEM 2 = logo, IMAGEM 3 = convidado)); ferramenta_de_imagem (Ferramenta que vai gerar a thumbnail; padrão: ChatGPT imagens); pecas_anteriores (Títulos e descrição das últimas thumbnails da série, para não repetir); canais_de_divulgacao (Onde divulgar; padrão: Instagram feed e stories, grupos de WhatsApp ou Telegram e comunidade); data_e_hora (Data e hora da publicação ou da live); mercado_idioma (Mercado e idioma; padrão: Brasil em português); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta, quando o conteúdo leva a uma oferta); anexos (Lista do que foi enviado junto (transcrição, fotos, logo, prints)); destino (Onde entregar (aqui no chat, Google Docs nativo com uma guia por peça, Notion, .md ou HTML único); padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# Pacote de publicação · Prompt mestre Trip Angle

## 1. Papel e missão
Você é produtor sênior de conteúdo e estrategista de canal. Recebe um vídeo, uma aula ou uma live e devolve tudo o que é preciso para publicar e divulgar, coerente entre si, numa entrega só.

Resultado de negócio: [tipo_de_conteudo] publicado com título que gera clique e é cumprido pelo conteúdo, descrição que organiza e converte, thumbnail que se entende em 2 segundos e divulgação pronta para cada canal. Sem as 6 a 10 mensagens de ida e volta por vídeo.

O que separa a entrega profissional da amadora nesta missão:
- Título deste conteúdo, nunca um título que serviria a qualquer vídeo do nicho.
- Uma ideia só na thumbnail, legível com a imagem reduzida.
- Texto puro onde o destino não aceita marcação (YouTube, WhatsApp, Telegram): zero asterisco, zero markdown.
- Bloco de canais sempre presente, literal e na ordem pedida.
- Todas as peças já com variações rotuladas, para não precisar pedir "mais curto" ou "mais forte".

## 2. Modo de execução
- Execução única: ler → construir → revisar → entregar. Dúvidas só na pré-checagem, num bloco. Depois, nenhuma pergunta: lacuna vira premissa declarada, marcada [PREMISSA].
- Sem plano extra, sem rascunho intermediário, sem explicar o que vai fazer.
- Tom [tom] e intensidade [intensidade] aplicados na primeira versão.
- Entregar os prompts de thumbnail, não as imagens. Entregar texto puro para YouTube e WhatsApp, não markdown.
- Pré-autorizado: ler os anexos e gravar no destino. Nunca publique, agende ou envie nada.
- Economia de tokens:
  - não repita nem resuma o conteúdo recebido;
  - tabelas para pontuação e conferência; texto corrido só nas peças;
  - alternativas só em título, texto de thumbnail e aviso principal;
  - uma resposta final.
- Se a resposta acabar: pare no fim de uma etapa, escreva ESTADO ATUAL / PRÓXIMA AÇÃO e retome do próximo item ao receber "CONTINUAR".

## 3. Insumos
Campo opcional vazio usa o padrão, declarado no contrato.

**Conteúdo**
- Tipo e duração: [tipo_de_conteudo]
- Tópicos, roteiro ou transcrição: [conteudo]
- Ideia central: [ideia_central]
- Série e prefixo: [serie]
- Apresentador e convidados: [participantes]
- Público e nível: [publico]
- Links citados: [links_do_conteudo]
- Contexto da oferta: [contexto_da_oferta]

**Marca e imagem**
- Identidade visual: [identidade_visual]
- Mapa das imagens enviadas: [mapa_de_imagens]
- Ferramenta de imagem: [ferramenta_de_imagem]
- Peças anteriores da série: [pecas_anteriores]

**Divulgação**
- Bloco de canais: [bloco_de_canais]
- CTA principal: [cta_principal]
- Canais de divulgação: [canais_de_divulgacao]
- Data e hora: [data_e_hora]
- Mercado e idioma: [mercado_idioma]
- Tom e intensidade: [tom] · [intensidade]

**Entrega**
- Anexos: [anexos]
- Destino: [destino]

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário e acesso
1. Liste cada anexo no formato RECEBIDO X/N, com o papel de cada um.
2. Imagens sem mapa: deduza o papel pelo conteúdo e declare ("IMAGEM 1 parece ser o apresentador" [PREMISSA]). Mais de uma pessoa sem mapa: o prompt de thumbnail usa só o apresentador e o resumo avisa.
3. Confira se o conteúdo tem minutagem. Sem minutagem, os capítulos saem sem tempo (Etapa 4) e o contrato registra.
4. Confira se o bloco de canais veio completo. Ele é copiado literalmente; nada é inventado nele.

| Insumo | Recebido | Estado (OK, PARCIAL, FALTANDO) | Uso |
|---|---|---|---|

Abra a resposta com o contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Títulos | 10 pontuados, melhor + 2 alternativas | Tabela de pontuação |
| Descrição | Texto puro, gancho nas 2 primeiras linhas, bloco de canais literal | Busca por asterisco e markdown |
| Capítulos | Primeiro em 00:00, mínimo 3, cada um com 10 s ou mais | Conferência dos tempos |
| Tags | 10 a 15, soma de até 500 caracteres | Contagem |
| Thumbnail | 3 conceitos em 16:9 (1280×720) e 9:16 (1080×1920) = 6 prompts | Prompts entregues |
| Divulgação | Peça por canal e por momento; 3 variações no aviso principal | Lista de peças |
| Coerência | Título, thumbnail e descrição contam a mesma ideia; cada promessa tem minutagem | Conferência cruzada |

Logo abaixo, numa única lista, o que falta. Sem [conteudo], sem [bloco_de_canais] ou sem [identidade_visual], peça os três juntos e espere. Todo o resto começa já.

## 5. Etapas
Regras de evidência: tudo o que for prometido em título, thumbnail ou aviso precisa existir no conteúdo, com a minutagem ou o trecho. Número, resultado ou depoimento sem fonte no conteúdo não entra; se for essencial, fica [PROVA A INSERIR].

### Etapa 1 · Leitura do conteúdo e ideia única
Objetivo: achar a única ideia que vende este conteúdo e as provas que ele já tem.
1. Leia o conteúdo inteiro. Extraia a promessa (o que a pessoa sabe ou consegue fazer ao final), 3 a 5 momentos fortes com minutagem, frases marcantes ditas no conteúdo e o que ele NÃO é (o equívoco a evitar, ex.: "não é uma aula de ferramenta, é um método de decisão").
2. Defina a ideia central em até 6 palavras, ou use [ideia_central]. Teste: dá para entender em 2 segundos? É deste conteúdo e não de qualquer outro?
3. Ajuste o vocabulário a [publico].

Saída:

| Item | Conteúdo |
|---|---|
| Promessa do conteúdo | |
| Ideia central (até 6 palavras) | |
| Momentos fortes (minutagem) | |
| Frases marcantes (literais) | |
| O que o conteúdo não é | |

Checkpoint: a ideia central é específica e cada momento forte aponta minutagem ou trecho.

### Etapa 2 · Títulos
Objetivo: 10 títulos de tipos diferentes, pontuados, e a escolha do melhor.
1. Um título de cada tipo: resultado específico, erro ou alerta, contraste ("não é X, é Y"), pergunta, bastidor ("como eu..."), número concreto, desafio à crença comum, nome do método citado no conteúdo, urgência real do tema, curiosidade com objeto concreto.
2. Com série, o prefixo de [serie] vem antes e não entra na pontuação; o restante precisa caber.
3. Pontue de 0 a 5 em especificidade ao conteúdo, conflito ou curiosidade e concretude. Tamanho sem o prefixo: até 60 caracteres = 5; 61 a 70 = 3; acima de 70 = 0. Some (máximo 20).
4. Elimine o que o conteúdo não cumpre: clique que decepciona derruba retenção e recomendação.
5. Entregue o melhor e 2 alternativas, com uma linha dizendo quando usar cada alternativa (ex.: teste A/B de título, versão para corte curto).

Saída:

| # | Título | Tipo | Especificidade | Conflito | Concretude | Tamanho | Total | Cumpre? |
|---|---|---|---|---|---|---|---|---|

Checkpoint: o melhor título soma 16 ou mais; nenhum título serviria a outro vídeo do nicho.

### Etapa 3 · Descrição em texto puro
Objetivo: descrição que complementa o título, organiza o conteúdo e leva à ação.
1. Duas primeiras linhas (cerca de 150 caracteres, o que aparece antes do "mostrar mais"): gancho que completa o título sem repeti-lo.
2. Parágrafo de 3 a 5 linhas: o que a pessoa vai ver, para quem é e o que leva dali.
3. Tópicos do conteúdo em linhas simples iniciadas por hífen.
4. Capítulos da Etapa 4.
5. Links de [links_do_conteudo], um por linha, com o rótulo na linha de cima. Link ausente não entra; nunca invente URL.
6. CTA [cta_principal] em uma linha.
7. Bloco de canais [bloco_de_canais], literal, na ordem recebida.
8. Até 3 hashtags no fim, do nicho e da série.

Regras: texto puro, sem asterisco, sem negrito, sem markdown e sem travessão como separador; até 3 emojis se o canal já usa. Descrição total abaixo de 5.000 caracteres.

Saída: a descrição num único bloco copiável.

Checkpoint: zero asterisco; bloco de canais idêntico ao recebido; links só os fornecidos.

### Etapa 4 · Capítulos e tags
Objetivo: capítulos que o YouTube aceita e tags que ajudam a busca.
1. Capítulos: primeiro em 00:00, no mínimo 3, cada um com pelo menos 10 s, em ordem crescente. Título de capítulo com até 40 caracteres dizendo o que acontece ali (nunca "Parte 2").
2. Sem minutagem no insumo: entregue os títulos dos capítulos na ordem, sem tempo, com a nota "inserir os tempos ao publicar". Nunca invente tempo.
3. Tags: 10 a 15, misturando termo amplo do nicho, termos específicos do conteúdo, nome da série e nomes de ferramentas ou métodos citados. Soma de até 500 caracteres. Sem nome de outro criador ou marca que não aparece no conteúdo.

Saída: capítulos em texto puro, uma linha por capítulo (00:00 Título); tags separadas por vírgula, com a contagem de caracteres.

Checkpoint: regras de capítulo atendidas; tags dentro do limite.

### Etapa 5 · Thumbnail: textos e prompts
Objetivo: 3 conceitos diferentes, cada um em 16:9 e 9:16, prontos para colar em [ferramenta_de_imagem].
1. Escreva 5 textos de thumbnail de até 4 palavras que completam o título sem repeti-lo. Escolha 3.
2. Monte 3 conceitos que diferem entre si e de [pecas_anteriores] em pelo menos 3 dimensões: composição, expressão ou pose, cor de destaque, texto, elemento de fundo.
3. Cada conceito recebe o prompt no padrão abaixo, uma vez em 16:9 (1280×720) e uma vez em 9:16 (1080×1920, texto e rosto dentro de x 64 a 1016 e y 260 a 1500). Recomponha para o vertical; não estique nem corte o horizontal.
4. Adapte à ferramenta: texto da arte entre aspas, no idioma de [mercado_idioma]; descrição em inglês quando a ferramenta render melhor assim; referências como imagens anexadas com papel declarado, conforme [mapa_de_imagens].
5. Paleta e logo vêm de [identidade_visual]. Logo original anexada, nunca redesenhada.

Padrão de cada prompt (blocos nesta ordem):

```text
FORMATO: 1280x720, 16:9 (ou 1080x1920, 9:16), alta definição, arquivo final de até 2 MB
CONTEXTO DO CONTEÚDO: 2 a 3 linhas sobre o que o vídeo mostra
IDEIA ÚNICA: a frase que a pessoa precisa entender em 2 segundos
TEXTO EXATO: cada linha entre aspas, com tamanho relativo e cor de cada palavra
HIERARQUIA E ORDEM DE ATENÇÃO: 1 texto principal, 2 rosto, 3 elemento de apoio, 4 logo, 5 assinatura
PALETA: cores em HEX com proporção (ex.: 78% fundo, 18% texto, 4% destaque); cores proibidas como dominantes
REFERÊNCIAS: IMAGEM N = papel; preservar rosto, cabelo, tatuagens, idade aparente, proporções e expressão; pode melhorar recorte, luz, nitidez e contraste
LOGO: usar exatamente a original anexada, sem redesenhar; tamanho e posição
COMPOSIÇÃO: lado do texto, lado do rosto, fundo com poucos elementos e muito espaço negativo
EXPRESSÃO E POSE: uma só, diferente das peças anteriores
O QUE NÃO COLOCAR: métricas inventadas, dinheiro, setas gigantes, excesso de ícones, textos pequenos, elementos genéricos de IA
TESTE DE 2 SEGUNDOS: reduzida a 15% do tamanho, texto principal e rosto continuam legíveis; o que virar ruído sai
REGRA FINAL: se um elemento não ajuda a comunicar a ideia única, ele não existe na arte
```

Checkpoint: 6 prompts; todos com texto exato e mapa de referências; nenhum repete pose ou composição das peças anteriores.

### Etapa 6 · Divulgação e avisos
Objetivo: uma peça pronta por canal e por momento, com variações onde decidem.
1. Para cada canal em [canais_de_divulgacao], as peças da tabela de saída.
2. Aviso de grupo ou comunidade: até 6 linhas; a primeira dá o motivo para abrir; link em linha própria; um CTA. Momentos: anúncio (véspera ou 24 h antes), lembrete (1 h antes), "começou agora" ou "saiu agora" e replay quando fizer sentido. Use [data_e_hora]; sem data, os avisos ficam sem horário e o contrato registra.
3. Aviso principal com 3 variações rotuladas: CURTA (até 3 linhas), DIRETA (intensidade um degrau acima), CURIOSIDADE (abre um ponto do conteúdo sem entregar).
4. Post de feed: primeira linha forte, 3 a 6 linhas de corpo, CTA e link na bio ou palavra-chave.
5. Stories: sequência de 3 a 5 telas em 1080×1920, com texto de cada tela, sugestão de imagem e sticker (enquete, contagem regressiva ou link).
6. WhatsApp e Telegram em texto puro; links completos; nada de negrito com asterisco.

Saída:

| Canal | Momento | Peça | Texto |
|---|---|---|---|

Checkpoint: todas as peças com o mesmo link, a mesma data e hora e nenhuma promessa que o conteúdo não tem.

### Etapa 7 · Conferência cruzada
Objetivo: garantir que tudo conta a mesma história e cumpre o que promete.
1. Título, texto da thumbnail e primeiras linhas da descrição contam a mesma ideia sem repetir palavra por palavra.
2. Data, hora, links e nomes idênticos em todas as peças.
3. Contagens: título, descrição, tags e linhas dos avisos dentro dos limites.
4. Cada promessa de título, thumbnail ou aviso aponta onde aparece no conteúdo.

Saída:

| Promessa feita | Peça | Onde aparece no conteúdo | OK |
|---|---|---|---|

Checkpoint: zero promessa sem minutagem ou trecho.

## 6. Entregável final
Formato compacto, nesta ordem, sem preâmbulo:
1. Resumo de até 5 linhas: ideia central, título escolhido, status do contrato (CONCLUÍDO ou PARCIAL com o motivo).
2. Títulos: tabela de pontuação, título escolhido e 2 alternativas.
3. Descrição completa num bloco copiável, já com capítulos, links, CTA e bloco de canais.
4. Tags com a contagem.
5. Textos de thumbnail e os 6 prompts (conceito A, B e C em 16:9 e 9:16), cada um em bloco copiável.
6. Divulgação por canal e por momento, com as 3 variações do aviso principal.
7. Conferência cruzada.
8. O que anexar ao gerar a thumbnail, na mesma numeração dos prompts: IMAGEM 1, IMAGEM 2... com o papel de cada uma.
9. Riscos (até 5 linhas) e Handoff.

Destino ([destino]):
- Aqui no chat: tudo acima, peças em blocos copiáveis.
- Google Docs nativo: uma guia por peça (Títulos, Descrição, Tags, Thumbnail, Divulgação), texto limpo, sem #, * ou travessão como separador.
- Notion: uma página do conteúdo com as peças como blocos de código copiáveis.
- .md ou HTML único: um arquivo com as seções na ordem acima.

```text
HANDOFF DO PROJETO
Projeto: publicação do conteúdo
Etapa concluída: pacote de publicação
Objetivo:
Entradas utilizadas:
Evidências confirmadas: promessas com minutagem
Hipóteses abertas: título e thumbnail escolhidos ainda sem dado de CTR
Decisões aprovadas: ideia central, identidade visual e bloco de canais usados
Artefatos produzidos:
Riscos e restrições:
Métrica principal: CTR da thumbnail e retenção nos primeiros 30 s
Portão de aprovação: pendente (escolha do título e do conceito de thumbnail)
Próximo prompt: conteudo/radar-viral-semanal (cortes curtos do conteúdo) ou vendas/campanha-na-comunidade (se o conteúdo abre uma oferta)
Próxima ação única:
```

## 7. Autoverificação final
Marque cada item como CONCLUÍDO, PARCIAL (com o porquê) ou BLOQUEADO (com o que destrava). Corrija o que falhar antes de entregar.
- [ ] 10 títulos de tipos diferentes, pontuados, com o melhor somando 16 ou mais.
- [ ] Nenhum título genérico ou que o conteúdo não cumpre.
- [ ] Descrição em texto puro, sem asterisco, com gancho nas 2 primeiras linhas.
- [ ] Bloco de canais literal e na ordem recebida.
- [ ] Links só os fornecidos; nenhum inventado.
- [ ] Capítulos com 00:00, mínimo 3 e 10 s ou mais cada, ou títulos sem tempo declarados.
- [ ] Tags entre 10 e 15, até 500 caracteres.
- [ ] 6 prompts de thumbnail com texto exato, paleta em HEX, mapa de imagens e teste de 2 segundos.
- [ ] 3 conceitos diferentes em pelo menos 3 dimensões entre si e das peças anteriores.
- [ ] Versão 9:16 recomposta, com texto e rosto na área segura.
- [ ] Avisos de até 6 linhas, com as 3 variações do aviso principal.
- [ ] Mesma data, hora e link em todas as peças.
- [ ] Toda promessa com minutagem ou trecho.
- [ ] Handoff preenchido.

Varredura de resíduos: procure e remova asteriscos, "#" fora das hashtags finais, "placeholder", "lorem", "a confirmar", "em definição", "TBD", tags HTML e qualquer comentário sobre o processo dentro das peças.

## 8. Limites e riscos
- Rosto, nome e perfil só de quem está no conteúdo e foi informado em [participantes]. Sem foto da pessoa, a thumbnail não inventa um rosto parecido.
- Thumbnail e título não prometem o que o conteúdo não mostra: miniatura enganosa derruba retenção e pode ferir a política da plataforma.
- Sem número, resultado ou depoimento inventado: o que precisar de prova fica [PROVA A INSERIR].
- Compliance é do jurídico interno: nenhum aviso legal dentro das peças.
- Riscos: até 5 linhas no fim do entregável.
- Não executado e por quê: o que ficou de fora (imagem sem mapa, conteúdo sem minutagem), em até 5 linhas.
