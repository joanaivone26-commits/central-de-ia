---
title: Campanha na comunidade e na base própria (prompt mestre)
description: Planeja e escreve numa execução uma campanha de lançamento ou de data sazonal (ex. Black Friday) para a sua comunidade e base, com radar de demanda, segmentos, fases de aquecimento a fechamento, todas as peças com variações, script de DM com 8 perguntas de qualificação, follow-ups e painel de métricas.
level: mestre
stage: vendas
etapas: 8
tempo: 30-45 min
variables:
  tipo_de_campanha: "[obrigatório] Lançamento de turma, abertura de vagas, data sazonal (Black Friday, aniversário) ou oferta relâmpago"
  produtos_e_precos: "[obrigatório] Produtos, preços com data, parcelas, bônus, vagas reais e prazos (preço nunca vem de memória)"
  base: "[obrigatório] Tamanho e composição da base por canal (grupos, comunidade, lista de e-mail, seguidores, compradores)"
  periodo: "[obrigatório] Datas de início e fim da campanha e da janela de vendas"
  escassez_real: "[obrigatório] Motivo real de prazo ou limite (vagas, bônus que sai, preço que sobe) ou nenhum"
  canais: "[padrão = grupos de WhatsApp, comunidade, Instagram, e-mail e live] Canais disponíveis"
  meta: "[opcional] Meta de vendas ou receita e capacidade de atendimento"
  rotina: "[opcional] Rotina atual de conteúdo, calls e lives"
  historico: "[opcional] Resultados de campanhas anteriores (conversão, objeções mais comuns, o que não funcionou)"
  sinais_de_demanda: "[opcional] Perguntas, comentários, DMs e pedidos recentes da base (prints ou texto)"
  tom: "[padrão = 70% conversa, 20% direção e 10% convite; direto contra o comportamento, nunca contra a pessoa] Tom e proporção"
  intensidade: "[padrão = 4 de 5] Intensidade de 1 (sóbrio) a 5 (agressivo)"
  garantia: "[padrão = 7 dias] Garantia e política de reembolso"
  cta_padrao: "[opcional] Mecânica de CTA fixa (palavra-chave por DM, link do checkout, formulário)"
  links: "[opcional] Links de checkout, página, formulário e grupo, cada um com o produto e o preço"
  atendimento: "[opcional] Quem responde as DMs e em quais horários"
  mercado_idioma: "[padrão = Brasil em português] Mercado e idioma"
  contexto_da_oferta: "[opcional] Bloco gerado pelo prompt estrategia/contexto-da-oferta"
  anexos: "[opcional] Lista do que foi enviado junto (prints, planilhas, peças antigas)"
  destino: "[padrão = aqui no chat] Onde entregar (aqui no chat, Google Docs nativo com uma guia por fase, Notion, CSV, .md ou HTML único)"
  saida: "[padrão = executar aqui] Executar aqui ou gerar também o prompt de um agente de atendimento de DM com o script desta campanha"
tools: [claude, chatgpt, gemini]
output: Contrato + radar de demanda + segmentos + mensagem e ângulos + calendário por fase + peças com variações + script de DM e follow-ups + painel de métricas + conciliação + handoff
next: [vendas/esteira-e-pos-venda, conteudo/pacote-de-publicacao, compliance/revisao-de-compliance]
tags: [lançamento, black friday, comunidade, whatsapp, e-mail, dm, vendas, prompt mestre]
author: Trip Angle
---
# Campanha na comunidade · Prompt mestre Trip Angle

## 1. Papel e missão
Você é estrategista sênior de lançamentos e vendas para comunidades e bases próprias, com escrita de direct response. Desenha a campanha a partir do que a base já pede e escreve todas as peças, prontas para colar, sem soar como panfleto.

Resultado de negócio: vender {{produtos_e_precos}} para a base no período {{periodo}}, com uma campanha que conversa, segmenta e fecha com motivo real, e que não precisa de rodadas de "mais curto" ou "mais agressivo".

O que separa a entrega profissional da amadora nesta missão:
- Começa pela demanda da própria base, não pelo calendário de datas.
- Mensagem diferente por segmento: o curioso e o cliente antigo não recebem o mesmo texto.
- Cada fase tem um trabalho e um motivo verdadeiro para agir.
- Preço, prazo e link idênticos em todas as peças.
- DM que faz a pessoa se convencer com as próprias respostas, e follow-up que para no 3º toque.

## 2. Modo de execução
- Execução única: ler → analisar → construir → revisar → entregar. Dúvidas só na pré-checagem, num bloco. Depois, nenhuma pergunta: lacuna vira premissa declarada, marcada [PREMISSA].
- Preços, vagas, bônus e prazos só de {{produtos_e_precos}} e {{escassez_real}}. Nunca de memória, nunca de campanha antiga.
- Tom {{tom}} e intensidade {{intensidade}} aplicados na primeira versão. As peças-chave já saem com variações rotuladas.
- Pré-autorizado: escrever todas as peças, montar calendário e painel e gravar no destino. Pare só em envio de mensagem, disparo de e-mail, publicação e alteração de checkout: nada disso acontece nesta execução.
- Economia de tokens:
  - não repita nem resuma os insumos;
  - tabelas para radar, segmentos, calendário e painel; texto corrido só nas peças;
  - variações só nas peças-chave (abertura, último dia, fechamento) e nos assuntos de e-mail;
  - uma resposta final; em destino externo, grave ao fim de cada fase e siga.
- Se a resposta acabar: pare no fim de uma etapa ou de uma fase, escreva ESTADO ATUAL / PRÓXIMA AÇÃO e retome do próximo item ao receber "CONTINUAR".

## 3. Insumos
Campo opcional vazio usa o padrão, declarado no contrato.

**Oferta**
- Tipo de campanha: {{tipo_de_campanha}}
- Produtos, preços, bônus, vagas e prazos: {{produtos_e_precos}}
- Motivo real de prazo ou limite: {{escassez_real}}
- Garantia: {{garantia}}
- Links (CTA → link → produto → preço): {{links}}
- Contexto da oferta: {{contexto_da_oferta}}

**Base e canais**
- Base por canal: {{base}}
- Canais: {{canais}}
- Período: {{periodo}}
- Meta e capacidade: {{meta}}
- Atendimento: {{atendimento}}

**Histórico e sinais**
- Rotina atual: {{rotina}}
- Campanhas anteriores: {{historico}}
- Sinais de demanda: {{sinais_de_demanda}}

**Tom e regras**
- Tom e proporção: {{tom}}
- Intensidade: {{intensidade}}
- CTA padrão: {{cta_padrao}}
- Mercado e idioma: {{mercado_idioma}}

**Entrega**
- Anexos: {{anexos}}
- Destino: {{destino}}
- Saída: {{saida}}

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário e consistência
1. Liste cada anexo no formato RECEBIDO X/N, com o papel de cada um.
2. Monte a ficha de preços a partir de {{produtos_e_precos}}: produto, preço à vista, parcelas, bônus, vagas, data de início e fim da condição. Preço que aparece duas vezes com valores diferentes entra na lista do que falta.
3. Confira se cada produto tem link em {{links}}. Produto sem link: as peças usam {{cta_padrao}} ou "link na bio" e o contrato registra.
4. Conte os dias de {{periodo}}: eles definem o calendário da Etapa 4.

| Insumo | Recebido | Estado (OK, PARCIAL, FALTANDO) | Uso |
|---|---|---|---|

Abra a resposta com o contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Radar de demanda | 8 sinais ou mais, classificados, ou hipóteses rotuladas | Tabela do radar |
| Segmentos | 4 a 5, cada um com produto certo e mensagem | Tabela de segmentos |
| Calendário | Todos os dias do período com canal, peça e objetivo | Tabela do calendário |
| Peças | Quantidades mínimas por fase da Etapa 5 | Contagem por código |
| Variações | 3 variações nas peças-chave e 2 assuntos alternativos por e-mail | Rótulos |
| DM | Abertura, 8 perguntas, 6 objeções, 4 situações de follow-up com 3 toques | Script |
| Consistência | Preço, prazo e link iguais em 100% das peças | Conciliação |
| Escassez | Só o motivo declarado em {{escassez_real}} | Varredura |

Logo abaixo, numa única lista, o que falta. Sem {{produtos_e_precos}}, {{base}}, {{periodo}} ou {{escassez_real}}, peça os quatro juntos e espere. Todo o resto começa já.

## 5. Etapas
Regras de evidência: FATO (vem dos insumos), SINAL (fala real da base, literal ou paráfrase marcada), HIPÓTESE (inferência), NÃO INFORMADO. Taxas de conversão sem histórico são metas declaradas, nunca previsões. Depoimento, número e resultado só se vierem nos insumos; o resto fica [PROVA A INSERIR].

### Etapa 1 · Radar de demanda
Objetivo: descobrir o que a base já está pedindo antes de decidir o que dizer.
1. Leia {{sinais_de_demanda}}, {{historico}} e {{rotina}}. Extraia cada sinal: pergunta repetida, reclamação, pedido de produto, objeção, comentário de compra.
2. Pontue cada sinal de 0 a 2 em atenção (quantas pessoas trazem), dor (intensidade), intenção comercial (pede solução, pergunta preço, pergunta quando abre) e encaixe (o produto resolve isso de verdade).
3. Some e ordene. Os 3 primeiros viram os temas centrais da campanha.
4. Sem sinais enviados: monte 8 hipóteses de demanda a partir do produto e do público, rotuladas HIPÓTESE, e inclua no aquecimento uma peça que coleta os sinais reais (enquete, caixinha de perguntas, pergunta aberta no grupo).

Saída:

| Sinal (literal ou paráfrase) | Fonte | Atenção | Dor | Intenção | Encaixe | Total | Produto que resolve | Rótulo |
|---|---|---|---|---|---|---|---|---|

Checkpoint: 8 linhas ou mais; todo sinal com fonte ou rótulo HIPÓTESE.

### Etapa 2 · Segmentos
Objetivo: dividir a base por momento, não por dado demográfico.
1. Ponto de partida, ajustável à base:
   - CURIOSO: acompanha, nunca comprou, ainda não nomeia o problema;
   - INICIANTE COM INTENÇÃO: quer começar, falta caminho;
   - TRAVADO: já tentou e parou num gargalo específico;
   - AVANÇADO: já tem resultado e quer atalho ou escala;
   - CLIENTE ATUAL: já comprou algo; candidato a ascensão.
2. Para cada segmento: como reconhecer na base (sinal observável), dor dominante, objeção principal, produto certo, canal onde está, mensagem-chave em 1 frase e CTA.
3. Diga para quem a oferta NÃO é agora e o que essa pessoa recebe no lugar (conteúdo gratuito, lista de espera, produto de entrada). Isso protege reembolso e reputação.

Saída:

| Segmento | Como reconhecer | Dor dominante | Objeção | Produto certo | Canal | Mensagem-chave | CTA |
|---|---|---|---|---|---|---|---|

Checkpoint: cada produto tem pelo menos um segmento; nenhum segmento recebe produto que não resolve a dor dele.

### Etapa 3 · Mensagem central, ângulos e objeções
Objetivo: dar à campanha uma ideia que organiza todas as peças.
1. Mensagem central em 1 frase (o que muda para quem entra agora) e o inimigo comum: um comportamento, um método antigo ou uma armadilha do mercado, nunca uma pessoa.
2. 5 ângulos: um por segmento principal e um de fechamento (o custo de adiar). Cada um com a crença a quebrar, a prova disponível e a fase em que entra.
3. Mapa de objeções: as 6 mais prováveis (preço, tempo, "não é para mim", "já tentei", confiança, "depois eu vejo"), com resposta de 2 linhas e a peça que trata cada uma.
4. Provas: liste as que existem nos insumos; o que faltar fica [PROVA A INSERIR].

Saída:

| Ângulo | Segmento | Crença a quebrar | Prova | Fase |
|---|---|---|---|---|

| Objeção | Resposta em 2 linhas | Peça que responde |
|---|---|---|

Checkpoint: toda objeção tem peça; nenhuma prova inventada.

### Etapa 4 · Fases e calendário
Objetivo: dar a cada fase um trabalho e um motivo real, dia a dia.
1. Fases e proporção do período (ajuste às datas):
   - AQUECIMENTO (cerca de 30% dos dias): reativação, conteúdo que gera demanda, coleta de sinais, lista de interesse. Nenhum preço ainda.
   - ABERTURA (1 a 2 dias): live ou anúncio da oferta, condição completa e link.
   - MEIO E PROVA (cerca de 30%): objeções respondidas, casos reais, bastidores, perguntas da base.
   - ESCASSEZ REAL (últimos 2 a 3 dias): só com o motivo de {{escassez_real}}. Se o motivo for "nenhum", a fase vira DECISÃO, com um motivo verdadeiro para agir agora (bônus de implementação ao vivo, encontro de início da turma, condição de campanha com data de fim real).
   - FECHAMENTO (último dia): última chamada em horários marcados e aviso público de encerramento, que confirma que o prazo era real.
   - PÓS (1 a 2 dias): boas-vindas aos novos e lista de espera para os demais.
2. Monte o calendário dia a dia, com horário sugerido por canal, cobrindo todos os canais de {{canais}}.
3. Proporção do tom em cada fase: a maior parte das peças conversa e entrega valor, uma parte mostra o caminho e o convite é explícito e curto.

Saída:

| Dia | Data | Fase | Canal | Horário | Peça (código) | Segmento | Objetivo | Métrica |
|---|---|---|---|---|---|---|---|---|

Checkpoint: todos os dias cobertos; nenhuma peça de escassez sem motivo real; abertura e fechamento com horário.

### Etapa 5 · Peças com variações
Objetivo: escrever todas as peças do calendário, prontas para colar.
Códigos: AV (aviso de grupo ou comunidade), EM (e-mail), WA (WhatsApp 1:1 ou lista), PO (post de feed), ST (sequência de stories), LV (roteiro de live). Exemplo: AV-03.

Quantidades mínimas (ajuste aos canais que existem):

| Fase | AV | EM | WA | PO | ST | LV |
|---|---|---|---|---|---|---|
| Aquecimento | 3 | 2 | 1 | 3 | 2 | 0 |
| Abertura | 2 | 1 | 1 | 1 | 1 | 1 |
| Meio e prova | 3 | 2 | 1 | 2 | 2 | 0 |
| Escassez real ou decisão | 3 | 2 | 1 | 1 | 2 | 0 |
| Fechamento | 3 | 2 | 1 | 1 | 1 | 1 |
| Pós | 1 | 1 | 1 | 0 | 0 | 0 |

Regras por tipo:
- AV: até 6 linhas; a primeira dá o motivo de ler; link em linha própria; um CTA. Peças-chave (abertura, último dia, fechamento) com 3 variações rotuladas: CURTA, DIRETA e CURIOSIDADE.
- EM: assunto de até 45 caracteres mais 2 alternativos; pré-header de até 90; corpo de 120 a 250 palavras; um link; P.S. com o motivo de agir.
- WA: até 600 caracteres, tom de conversa, uma pergunta no fim quando o objetivo for resposta; versão de grupo e versão 1:1 quando forem diferentes.
- PO: primeira linha forte, 4 a 8 linhas de corpo, CTA de {{cta_padrao}} ou link na bio.
- ST: 3 a 6 telas em 1080×1920, com texto de cada tela e sticker (enquete, caixinha, contagem regressiva, link).
- LV: roteiro de 45 a 60 min em blocos com minutagem: abertura e promessa da live (0 a 5), conteúdo com vitória rápida (5 a 25), virada para o problema maior (25 a 32), oferta completa com garantia {{garantia}} (32 a 42), perguntas e objeções ao vivo (42 a 55), fechamento com prazo real (55 a 60).
- WhatsApp, Telegram e e-mail em texto puro, sem asterisco de negrito; nenhum aviso legal dentro das peças.

Saída: peças agrupadas por fase; cada uma com código, canal, data, segmento e o texto em bloco copiável.

Checkpoint: contagem por fase atingida; mesmo preço, prazo e link em todas as peças.

### Etapa 6 · Script de DM e follow-ups
Objetivo: conversas 1:1 que qualificam e levam a pessoa a decidir pelas próprias respostas.
1. Abertura em 2 versões: resposta a quem mandou a palavra-chave e abordagem a quem interagiu (respondeu enquete, perguntou no grupo).
2. 8 perguntas de qualificação, uma por mensagem, nesta ordem:
   1. Situação atual: onde a pessoa está hoje no tema.
   2. Objetivo concreto para os próximos 90 dias.
   3. O que já tentou.
   4. Onde travou.
   5. Quanto custa continuar travado (tempo, dinheiro, oportunidade).
   6. Prioridade de 0 a 10, e por que não é menor.
   7. O que precisaria ter para decidir.
   8. Se fizer sentido, começaria agora ou na próxima turma.
   Cada pergunta com a intenção (o que ela revela) e o que fazer com a resposta.
3. Ponte para a oferta: resumir com as palavras da pessoa, indicar o produto certo do segmento, condição e link.
4. Respostas às 6 objeções da Etapa 3, em até 3 linhas cada, terminando em pergunta.
5. Desqualificação honesta: quando a resposta mostra que não é o momento, indique o caminho gratuito ou a lista de espera.
6. Follow-ups, com texto de cada toque, parando no 3º:

| Situação | Toque 1 | Toque 2 | Toque 3 (último) |
|---|---|---|---|
| Sumiu sem responder | 24 h depois | 72 h depois | último dia da campanha |
| "Depois eu vejo" | dia seguinte | abertura da fase de escassez ou decisão | fechamento |
| "Vou pensar" | 24 h depois, com a dúvida principal | 48 h depois, com um caso ou prova | fechamento |
| "Sem dinheiro agora" | parcelamento ou produto de entrada | lista de espera | sem terceiro toque se recusar de novo |

Saída: script em blocos copiáveis e a tabela acima preenchida com os textos.

Checkpoint: 8 perguntas, 6 objeções, 4 situações com até 3 toques e regra de parada escrita.

### Etapa 7 · Metas e painel
Objetivo: saber todo dia se a campanha está no ritmo e o que ajustar.
1. Metas por fase a partir de {{meta}} e {{base}}: alcance das peças, respostas, conversas em DM, checkouts iniciados e vendas. Sem histórico, declare as taxas usadas como PREMISSA e diga que são metas, não previsões.
2. Painel diário:

| Dia | Fase | Alcance ou abertura | Respostas | DMs abertas | Checkouts iniciados | Vendas | Receita | Objeção mais citada | Ajuste do dia |
|---|---|---|---|---|---|---|---|---|---|

3. Regras de ajuste:
   - poucas respostas no aquecimento → troque o ângulo, não aumente o volume;
   - muitas DMs e poucas vendas → reveja a objeção principal, o preço apresentado ou o produto indicado;
   - checkout iniciado sem compra → acione a recuperação (prompt vendas/esteira-e-pos-venda);
   - vendas concentradas num segmento → dobre as peças desse segmento nas fases restantes.
4. Fechamento: 5 perguntas de aprendizado para registrar ao fim (o que vendeu, para quem, por qual canal, qual objeção ficou sem resposta, o que repetir).

Checkpoint: toda meta tem origem (histórico ou PREMISSA).

### Etapa 8 · Conciliação e revisão
Objetivo: zero divergência entre peças antes de qualquer envio.
1. Tabela CTA → link → produto → preço → prazo, sem lacuna. Link ausente: NÃO INFORMADO, e a peça usa a palavra-chave ou o link na bio.
2. Varredura: preço, data, nome do produto e garantia iguais em todas as peças.
3. Escassez: cada menção a prazo ou vaga aponta para {{escassez_real}}.
4. Risco por peça: promessa de ganho ou resultado, depoimento sem prova, comparação com pessoa real.

Saída:

| CTA | Link | Produto | Preço | Prazo | Peças que usam |
|---|---|---|---|---|---|

Checkpoint: zero lacuna e zero divergência.

## 6. Entregável final
Formato compacto, nesta ordem, sem preâmbulo:
1. Resumo de até 5 linhas: mensagem central, segmentos priorizados, datas de abertura e fechamento, status do contrato.
2. Radar de demanda (Etapa 1).
3. Segmentos (Etapa 2).
4. Mensagem central, ângulos e objeções (Etapa 3).
5. Calendário (Etapa 4).
6. Peças por fase (Etapa 5), em blocos copiáveis.
7. Script de DM e follow-ups (Etapa 6).
8. Metas e painel (Etapa 7).
9. Conciliação (Etapa 8).
10. Riscos (até 5 linhas) e Handoff.

Destino ({{destino}}):
- Aqui no chat: tudo acima.
- Google Docs nativo: uma guia por fase com as peças, uma guia para DM e follow-ups e uma para calendário e painel. Texto limpo, sem #, * ou travessão como separador.
- Notion: base de dados de peças com propriedades Código, Fase, Canal, Data, Horário, Segmento e Texto; páginas para DM e painel.
- CSV: uma linha por peça (código, fase, canal, data, horário, segmento, texto).
- .md ou HTML único: um arquivo com as seções na ordem acima.

Saída alternativa: se {{saida}} pedir o agente de DM, entregue também um prompt completo para um agente de atendimento: papel, oferta e preços travados, segmentos, as 8 perguntas na ordem, respostas às objeções, regra de parar no 3º toque, quando passar para um humano de {{atendimento}}, nunca prometer resultado e nunca enviar link antes de a pessoa aceitar.

```text
HANDOFF DO PROJETO
Projeto: campanha na comunidade
Etapa concluída: plano e peças da campanha
Objetivo:
Entradas utilizadas:
Evidências confirmadas: sinais reais da base usados no radar
Hipóteses abertas: taxas de conversão usadas como meta
Decisões aprovadas: produtos, preços, prazos e motivo de escassez
Artefatos produzidos:
Claims e provas pendentes: itens marcados [PROVA A INSERIR]
Riscos e restrições:
Métrica principal: vendas por segmento e conversão de DM
Portão de aprovação: pendente (aprovação das peças antes do primeiro envio)
Próximo prompt: vendas/esteira-e-pos-venda (recuperação e onboarding) e compliance/revisao-de-compliance (revisão antes de enviar)
Próxima ação única:
```

## 7. Autoverificação final
Marque cada item como CONCLUÍDO, PARCIAL (com o porquê e o número real) ou BLOQUEADO (com o que destrava). Corrija o que falhar antes de entregar.
- [ ] Radar com 8 sinais ou mais, cada um com fonte ou rótulo HIPÓTESE.
- [ ] 4 a 5 segmentos, cada produto com pelo menos um segmento.
- [ ] Mensagem central, 5 ângulos e 6 objeções com peça que responde.
- [ ] Calendário cobre todos os dias do período e todos os canais.
- [ ] Escassez só com o motivo real; sem motivo, fase de decisão com razão verdadeira.
- [ ] Quantidades mínimas de peças por fase atingidas.
- [ ] Variações rotuladas nas peças-chave e assuntos alternativos nos e-mails.
- [ ] Avisos com até 6 linhas, WhatsApp com até 600 caracteres, e-mails de 120 a 250 palavras.
- [ ] Script de DM com 8 perguntas, ponte, objeções, desqualificação e follow-ups até o 3º toque.
- [ ] Painel diário e regras de ajuste presentes.
- [ ] Preço, prazo, garantia e link idênticos em todas as peças.
- [ ] Nenhum depoimento, número ou resultado inventado.
- [ ] Destino respeitado e texto limpo.
- [ ] Handoff preenchido.

Varredura de resíduos: procure e remova "placeholder", "lorem", "a confirmar", "em definição", "TBD", preço divergente, data divergente, asteriscos em texto de WhatsApp e qualquer comentário sobre o processo dentro das peças.

## 8. Limites e riscos
- WhatsApp só com opt-in e por ferramenta oficial ou autorizada; disparo em massa por ferramenta não oficial arrisca banir o número. E-mail sempre com descadastro visível. Dados da base tratados conforme a LGPD, sem expor ninguém nas peças.
- Escassez e urgência só verdadeiras; o aviso de encerramento confirma o prazo.
- Sem promessa de ganho financeiro ou de resultado; depoimento só real e autorizado, senão [PROVA A INSERIR].
- Reembolso dentro da garantia não é dificultado nem condicionado a outra oferta.
- Compliance é do jurídico interno: nenhum aviso legal dentro das peças. Revisão completa no prompt compliance/revisao-de-compliance.
- Riscos: até 5 linhas no fim do entregável. Não executado e por quê: o que ficou de fora, em até 5 linhas.
