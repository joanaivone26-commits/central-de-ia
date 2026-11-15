---
title: Calendário de conteúdo de 30 dias
description: Planeja 30 dias de conteúdo que cabem na rotina real, com pilares, séries, etapa do funil, formato, gancho escrito e CTA ligado à etapa seguinte em cada post, datas e semana de oferta encaixadas, dias de gravação em lote, reaproveitamento e revisão semanal com regras de ajuste.
level: modulo
stage: formatos
etapas: 6
tempo: 15-20 min
variables:
  nicho: "[obrigatório] Nicho e público"
  produto: "[obrigatório] Produto ou oferta que o conteúdo apoia, com preço e link quando houver"
  plataformas: "[padrão = Instagram e TikTok] Plataformas"
  frequencia: "[obrigatório] Posts por semana que você consegue produzir e em quais formatos"
  datas: "[padrão = Dia 1 a Dia 30 sem data] Mês de referência e datas importantes (lançamento, promoção, datas comemorativas, lives)"
  pilares: "[opcional] Pilares de conteúdo que você já usa"
  recursos: "[opcional] Recursos de produção (quem grava, quantas horas por semana, edição, cenário)"
  formatos_que_funcionam: "[opcional] Formatos e posts que ficaram acima da média recentemente"
  objetivo_do_mes: "[padrão = crescer e gerar leads para a oferta] Objetivo principal do mês"
  metricas_do_perfil: "[opcional] Mediana de alcance, salvamentos e cliques dos últimos 10 a 20 posts"
  contexto_da_oferta: "[opcional] Bloco gerado pelo prompt estrategia/contexto-da-oferta"
  mercado_idioma: "[padrão = Brasil em português] Mercado e idioma"
  destino: "[padrão = aqui no chat] Onde entregar (aqui no chat, Google Docs nativo, Notion, CSV ou .md)"
tools: [claude, chatgpt, gemini]
output: Pilares e séries + calendário de 30 dias em tabela + plano de gravação em lote + reaproveitamento + revisão semanal com regras de ajuste
next: [conteudo/roteiro-reels-tiktok, conteudo/carrossel-instagram, conteudo/radar-viral-semanal]
tags: [calendário editorial, conteúdo, planejamento, redes sociais, funil de conteúdo]
author: Trip Angle
---
# Calendário de conteúdo de 30 dias · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista de conteúdo. Monta calendário que cabe na rotina real de quem produz e que leva o público, semana a semana, para perto de {{produto}}.

Resultado: 30 dias prontos para produzir, com gancho escrito e CTA em cada post, e uma rotina de revisão que corrige o rumo toda semana.

Profissional × amador:
- Volume dentro da frequência real; dia sem post fica "sem post".
- Cada post com gancho de verdade (a primeira frase), nunca "post sobre o tema X".
- Todo post de topo aponta para um de meio; todo post de meio tem CTA leve para o fundo.
- Gravação em lote planejada, para o calendário sair do papel.

## 2. Modo de execução
- Execução única; dúvidas só na pré-checagem; lacunas viram premissa declarada [PREMISSA].
- Tabelas em vez de prosa; nada de teoria de funil na saída.
- Se a resposta acabar: pare no fim de uma semana do calendário, escreva ESTADO ATUAL / PRÓXIMA AÇÃO e retome com "CONTINUAR".

## 3. Insumos
- Nicho e público: {{nicho}}
- Produto ou oferta: {{produto}}
- Plataformas: {{plataformas}}
- Frequência e formatos possíveis: {{frequencia}}
- Mês e datas: {{datas}}
- Pilares atuais: {{pilares}}
- Recursos de produção: {{recursos}}
- Formatos que funcionam: {{formatos_que_funcionam}}
- Objetivo do mês: {{objetivo_do_mes}}
- Métricas do perfil: {{metricas_do_perfil}}
- Contexto da oferta: {{contexto_da_oferta}}
- Mercado e idioma: {{mercado_idioma}}
- Destino: {{destino}}

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário
Liste o que chegou (RECEBIDO X/N). Sem mês informado, use Dia 1 a Dia 30 e registre a premissa. Sem {{produto}} ou {{frequencia}}, peça os dois juntos e espere: sem oferta o fundo não tem destino, e sem frequência o calendário não cabe.

| Critério | Meta | Como vou medir |
|---|---|---|
| Volume | Exatamente a frequência informada × 4,3 semanas | Contagem de posts |
| Gancho | 100% dos posts com a primeira frase escrita | Coluna Gancho |
| Funil | 50% topo, 30% meio, 20% fundo; semana de oferta com fundo em 40% | Contagem por etapa |
| Ligação | Todo post com CTA para a etapa seguinte | Coluna CTA |
| Produção | Dias de gravação em lote definidos | Plano de gravação |

## 5. Etapas

### Etapa 1 · Capacidade e proporção
1. Converta {{frequencia}} em total de posts do mês e em horas de produção por semana, com base em {{recursos}}.
2. Ponto de partida do funil: topo 50% (alcance e descoberta), meio 30% (autoridade e consideração), fundo 20% (conversão). Na semana de promoção ou lançamento de {{datas}}: 30% topo, 30% meio, 40% fundo. Diga quantos posts isso dá por semana.
3. Com {{formatos_que_funcionam}}, reserve a maior parte do topo para esses formatos.

Saída:

| Semana | Posts | Topo | Meio | Fundo | Horas de produção |
|---|---|---|---|---|---|

### Etapa 2 · Pilares e séries
1. Defina 4 ou 5 pilares (ou ajuste {{pilares}}), cada um com objetivo, etapa do funil predominante e um exemplo de pauta do nicho.
2. Crie 2 a 3 séries recorrentes (mesmo nome, mesmo dia, mesmo formato), que facilitam produção e criam hábito no público.

Saída:

| Pilar | Objetivo | Etapa predominante | Exemplo de pauta |
|---|---|---|---|

| Série | Pilar | Dia da semana | Formato | Promessa da série |
|---|---|---|---|---|

### Etapa 3 · Calendário
1. Distribua os posts pelos 30 dias respeitando a capacidade da Etapa 1 e as datas de {{datas}}.
2. Antes de cada data importante, 3 a 5 posts de aquecimento (problema, mecanismo, prova, bastidor), sem preço antes da abertura.
3. Para cada post: plataforma, formato, pilar, etapa, tema, gancho (a primeira frase, escrita), CTA e o post para onde ele leva.
4. Alinhe ao {{objetivo_do_mes}}; com {{contexto_da_oferta}}, os posts de fundo usam o mecanismo e a promessa da oferta sem prometer resultado garantido.

Saída:

| Dia | Data e dia da semana | Plataforma | Formato | Pilar | Etapa | Tema | Gancho | CTA | Leva para |
|---|---|---|---|---|---|---|---|---|---|

### Etapa 4 · Gravação em lote e reaproveitamento
1. Agrupe os posts em 1 a 2 dias de gravação por semana: o que gravar em cada sessão, com cenário e roupa iguais quando possível.
2. Cada conteúdo principal da semana (live, vídeo longo, carrossel âncora) vira 3 a 5 peças menores: corte, carrossel, story, frase de feed.

Saída:

| Sessão de gravação | Data | Posts gravados | Cenário e recursos |
|---|---|---|---|

| Conteúdo principal | Vira | Onde e quando |
|---|---|---|

### Etapa 5 · Métricas e régua
1. Métrica por etapa: topo com alcance fora da base e compartilhamentos; meio com salvamentos e visitas ao perfil; fundo com cliques, DMs com palavra-chave e leads.
2. Régua: a mediana de {{metricas_do_perfil}}. Sem métricas, as 2 primeiras semanas criam a régua [PREMISSA].

### Etapa 6 · Revisão semanal (15 minutos)
1. Liste os 3 posts com mais alcance e os 3 com mais salvamentos ou cliques.
2. O que eles têm em comum: formato, gancho, tema ou série.
3. Regras de ajuste:
   - alcance caindo → suba o topo e troque ganchos;
   - alcance sem venda → suba meio e fundo e reforce a ligação entre etapas;
   - série abaixo da mediana por 2 semanas → troque o formato da série, não o tema;
   - post acima da mediana → vira série ou ganha versão em outro formato.

Saída: checklist de revisão em 5 linhas para colar na agenda.

## 6. Entregável final
Ordem: resumo de 3 linhas → capacidade → pilares e séries → calendário → gravação e reaproveitamento → métricas → revisão semanal. Em CSV ou Notion ({{destino}}), uma linha por post com as colunas do calendário; em Google Docs, uma guia por semana, texto limpo, sem # ou *.

Handoff em 4 linhas: total de posts e proporção · séries criadas · data da primeira revisão · próximo prompt (conteudo/roteiro-reels-tiktok e conteudo/carrossel-instagram para escrever as peças da semana 1).

## 7. Autoverificação final
- [ ] Volume igual à capacidade real; dias sem post marcados.
- [ ] Gancho escrito em todos os posts.
- [ ] Proporção do funil respeitada, ajustada na semana de oferta.
- [ ] Todo post com CTA e destino.
- [ ] Datas importantes com aquecimento antes.
- [ ] Gravação em lote e reaproveitamento definidos.
- [ ] Revisão semanal com regras de ajuste.
Status por item: CONCLUÍDO, PARCIAL (com o porquê) ou BLOQUEADO. Varredura: remova "post sobre", "placeholder", "a confirmar" e comentários sobre o processo.

## 8. Limites e riscos
- Posts de fundo sem promessa de resultado garantido; o que precisar de prova fica [PROVA A INSERIR].
- Escassez e urgência só verdadeiras e ligadas às datas reais de {{datas}}.
- Depoimento só real e autorizado.
- Compliance é do jurídico interno; riscos em até 5 linhas no fim.
