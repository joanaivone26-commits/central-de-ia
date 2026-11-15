---
title: Banco de formatos por objetivo
description: Monta um banco de 25 a 30 formatos de conteúdo organizados por objetivo (alcance, autoridade, conexão, conversão e retenção), cada um com estrutura em tempos, gancho modelo, pauta específica do seu nicho, métrica com corte e dificuldade, filtrado pelos seus recursos, com top 10 para começar e regra de rotação semanal.
level: modulo
stage: formatos
etapas: 5
tempo: 10-15 min
variables:
  nicho: "[obrigatório] Nicho, público e o problema principal que o perfil resolve"
  plataformas: "[padrão = Instagram, TikTok e YouTube Shorts] Plataformas que você usa"
  objetivos: "[padrão = alcance e conversão] Objetivos do momento (alcance, autoridade, conexão, conversão, retenção)"
  recursos: "[obrigatório] Recursos reais (aparece em vídeo? grava sozinho? tem produto para mostrar? tem clientes que autorizam depoimento? edita no celular?)"
  quantidade: "[padrão = 30] Quantos formatos no banco (25 a 30)"
  frequencia: "[padrão = 5 posts por semana] Quantos posts por semana você consegue publicar"
  formatos_ja_usados: "[opcional] Formatos que você já usa e como foram (acima ou abaixo da média)"
  metricas_do_perfil: "[opcional] Mediana de views, salvamentos e compartilhamentos dos últimos 10 a 20 posts"
  contexto_da_oferta: "[opcional] Bloco gerado pelo prompt estrategia/contexto-da-oferta"
  mercado_idioma: "[padrão = Brasil em português] Mercado e idioma"
  destino: "[padrão = aqui no chat] Onde entregar (aqui no chat, Google Docs nativo, Notion, CSV ou .md)"
tools: [claude, chatgpt, gemini]
output: Banco de formatos em tabelas por objetivo + filtro de recursos + top 10 para começar + rotação semanal + regra de corte pela mediana
next: [conteudo/calendario-de-conteudo-30-dias, conteudo/radar-viral-semanal, conteudo/roteiro-reels-tiktok]
tags: [formatos, conteúdo, estratégia de conteúdo, redes sociais, banco de formatos]
author: Trip Angle
---
# Banco de formatos por objetivo · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista de conteúdo para negócios digitais. Trata formato como ferramenta: cada um faz um trabalho, e usar o errado custa alcance ou venda.

Resultado: um banco de {{quantidade}} formatos que o perfil de {{nicho}} consegue produzir com {{recursos}}, cada um com pauta específica e o número que diz se funcionou.

Profissional × amador:
- Pauta concreta do nicho em cada formato, nunca "dicas sobre o tema".
- Estrutura em tempos ou em slides, não só o nome do formato.
- Métrica com corte: "funcionou" é acima da mediana do próprio perfil.
- Filtro honesto de recursos: o que o perfil não consegue fazer agora fica marcado.

## 2. Modo de execução
- Execução única; dúvidas só na pré-checagem; lacunas viram premissa declarada [PREMISSA].
- Tabelas em vez de prosa; sem explicação de teoria de conteúdo.
- Não repita os insumos.
- Se a resposta acabar: pare no fim de um objetivo, escreva ESTADO ATUAL / PRÓXIMA AÇÃO e retome com "CONTINUAR".

## 3. Insumos
- Nicho, público e problema: {{nicho}}
- Plataformas: {{plataformas}}
- Objetivos do momento: {{objetivos}}
- Recursos reais: {{recursos}}
- Quantidade de formatos: {{quantidade}}
- Posts por semana: {{frequencia}}
- Formatos já usados: {{formatos_ja_usados}}
- Métricas do perfil: {{metricas_do_perfil}}
- Contexto da oferta: {{contexto_da_oferta}}
- Mercado e idioma: {{mercado_idioma}}
- Destino: {{destino}}

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário
Liste o que chegou (RECEBIDO X/N). Nicho vago ("marketing", "saúde") sem público e problema: peça os dois numa pergunta só e espere.

| Critério | Meta | Como vou medir |
|---|---|---|
| Banco | {{quantidade}} formatos nos 5 objetivos, ao menos 4 por objetivo | Contagem por tabela |
| Pauta | 100% com pauta específica do nicho | Leitura da coluna |
| Métrica | 100% com métrica principal e corte | Coluna preenchida |
| Recursos | 100% marcados "posso agora" ou "não agora, falta X" | Coluna preenchida |
| Top 10 | Cobre os objetivos de {{objetivos}} | Lista |

## 5. Etapas

### Etapa 1 · Recursos e régua
1. Traduza {{recursos}} em capacidades: rosto em vídeo (sim ou não), voz em off, gravação de tela, produto físico ou digital para mostrar, depoimento autorizado, edição disponível, tempo semanal.
2. Com {{metricas_do_perfil}}, fixe a mediana do perfil por métrica. Sem métricas, a régua será a média das 2 primeiras semanas [PREMISSA].
3. Leia {{formatos_ja_usados}}: o que ficou acima da média entra no banco com prioridade; o que ficou abaixo só volta com outro gancho.

Saída:

| Capacidade | Tem? | O que libera |
|---|---|---|

### Etapa 2 · Banco por objetivo
1. Distribua {{quantidade}} formatos entre os 5 objetivos:
   - Alcance: chegar em quem não conhece o perfil;
   - Autoridade: mostrar que o perfil sabe;
   - Conexão: fazer o público gostar e se identificar;
   - Conversão: levar para lead, DM ou venda;
   - Retenção: manter a base ativa e comprando de novo.
2. Repertório de partida, ajustável: erro comum, mito × verdade, tutorial em 3 passos, lista de ferramentas, comparação, reação a conteúdo do nicho, POV, história pessoal, bastidores, opinião contrária, estudo de caso, checklist salvável, caixinha de perguntas, desafio de 7 dias, objeção respondida, oferta direta, depoimento autorizado, live com perguntas, tour do produto, "antes de comprar X, veja isso", notícia do nicho comentada, prova de processo, dia na rotina. Acrescente os formatos nativos de cada plataforma de {{plataformas}}.
3. Para cada formato: como funciona, estrutura em tempos (vídeo) ou em slides (carrossel), gancho modelo, pauta específica do nicho, plataforma ideal, métrica principal com corte, dificuldade de 1 a 3 e se o perfil consegue fazer agora.
4. Com {{contexto_da_oferta}}, os formatos de conversão levam à oferta pelo mecanismo ou pelo problema, nunca por promessa de resultado.

Saída (uma tabela por objetivo):

| Formato | Como funciona | Estrutura (tempos ou slides) | Gancho modelo | Pauta no nicho | Plataforma | Métrica e corte | Dificuldade | Posso agora? |
|---|---|---|---|---|---|---|---|---|

### Etapa 3 · Métricas de referência por objetivo
Use esta régua na coluna "Métrica e corte", sempre contra a mediana do perfil:

| Objetivo | Métrica principal | Corte para "funcionou" |
|---|---|---|
| Alcance | contas alcançadas fora da base, compartilhamentos por mil views | acima da mediana em 2 publicações |
| Autoridade | salvamentos, comentários com pergunta | acima da mediana em salvamentos |
| Conexão | respostas, DMs, comentários pessoais | acima da mediana em respostas |
| Conversão | cliques no link, DMs com palavra-chave, leads | meta declarada por post [PREMISSA] |
| Retenção | respostas de clientes, uso do produto, recompra | variação contra o mês anterior |

### Etapa 4 · Top 10 para começar
1. Pontue cada formato marcado "posso agora" de 0 a 2 em aderência aos objetivos de {{objetivos}}, facilidade de produção e histórico do perfil.
2. Escolha os 10 de maior soma, cobrindo todos os objetivos pedidos.
3. Para cada um, a primeira pauta pronta para gravar.

Saída:

| # | Formato | Objetivo | Primeira pauta | Por que agora |
|---|---|---|---|---|

### Etapa 5 · Rotação semanal e regra de corte
1. Divida {{frequencia}} entre os objetivos (ponto de partida: 50% alcance e conexão, 30% autoridade, 20% conversão e retenção; em semana de oferta, 40% conversão).
2. Regra de corte: formato que fica abaixo da mediana em 2 publicações com ganchos diferentes sai da rotação por 30 dias.
3. Regra de entrada: formato novo entra no lugar de um cortado, nunca somando volume além de {{frequencia}}.

Saída: tabela Dia | Objetivo | Formato do top 10.

## 6. Entregável final
Ordem: resumo de 3 linhas → capacidades → banco (5 tabelas) → régua de métricas → top 10 → rotação e regras. Em CSV ou Notion ({{destino}}), uma linha por formato com as colunas da Etapa 2 mais "Objetivo". Texto limpo em Docs, sem # ou *.

Handoff em 4 linhas: top 3 formatos · mediana usada · rotação da semana · próximo prompt (conteudo/calendario-de-conteudo-30-dias para virar calendário, ou conteudo/radar-viral-semanal para ver o que está em alta).

## 7. Autoverificação final
- [ ] {{quantidade}} formatos, ao menos 4 por objetivo.
- [ ] Toda pauta específica do nicho; nenhuma genérica.
- [ ] Estrutura em tempos ou slides em todos.
- [ ] Métrica e corte em todos, contra a mediana do perfil.
- [ ] Recursos respeitados e marcados.
- [ ] Top 10 cobre os objetivos pedidos.
- [ ] Rotação cabe na frequência real.
Status por item: CONCLUÍDO, PARCIAL (com o porquê) ou BLOQUEADO. Varredura: remova "placeholder", "a confirmar" e comentários sobre o processo.

## 8. Limites e riscos
- Depoimento só de cliente real e com autorização; criança ou cliente nunca identificável sem consentimento.
- Pautas sem promessa de resultado garantido; o que precisar de prova fica [PROVA A INSERIR].
- Formato de outro criador é referência de estrutura, nunca de texto, rosto ou cenário.
- Compliance é do jurídico interno; riscos em até 5 linhas no fim.
