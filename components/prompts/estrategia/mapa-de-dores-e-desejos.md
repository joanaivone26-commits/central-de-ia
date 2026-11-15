---
title: Mapa de dores e desejos
description: Organiza as dores em 4 camadas e os desejos em 5, cada item com frase de origem e contagem por fonte, reconstrói o momento de luta, monta a ponte do estado atual ao desejado com o que o produto não resolve, ranqueia as dores pelo Opportunity Score e diz onde usar cada uma na copy, com hook de exemplo.
level: modulo
stage: avatar
etapas: 7
tempo: 15-30 min
variables:
  avatar: "[obrigatório] Avatar ou persona (ficha ou handoff de estrategia/criar-avatar-completo)"
  produto: "[obrigatório] Produto, promessa e o que ele entrega de fato"
  pesquisa: "[obrigatório] Material com a voz do público (comentários, reviews, enquetes, entrevistas ou banco de frases)"
  solucoes_atuais: "[opcional] Soluções que o público já usa e como avalia cada uma"
  mercado_idioma: "[padrão = Brasil, português] Mercado e idioma"
  contexto_da_oferta: "[opcional] Bloco gerado pelo prompt estrategia/contexto-da-oferta"
  destino: "[padrão = aqui no chat] Onde entregar (aqui no chat, Google Docs nativo, Notion, CSV ou .md)"
tools: [claude, chatgpt, gemini]
output: Dores em 4 camadas + desejos em 5 camadas com N de M + momento de luta + ponte com o que o produto não resolve + Opportunity Score com top 10 + matriz urgência × intensidade + uso na copy com hook de exemplo + handoff
next: [estrategia/oferta-completa, estrategia/linguagem-do-cliente, copy/swipe-de-headlines, criativos/criativos-em-escala]
tags: [dores, desejos, avatar, opportunity score, copy]
author: Trip Angle
---

# MAPA DE DORES E DESEJOS · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista de oferta de direct response. A venda acontece na camada mais funda da dor e do desejo, e a copy erra quando fica no sintoma. Este módulo entrega o mapa que diz qual dor abrir no anúncio, qual desejo prometer na headline e qual dor de identidade aliviar na VSL.

O que separa o profissional do amador aqui:
- Cada dor e cada desejo apontam uma frase real e a contagem "N de M fontes".
- A camada de identidade aparece ("talvez eu não seja capaz"), não só o sintoma.
- A coluna "o produto não resolve" é obrigatória: ela evita promessa que a entrega não cumpre.
- A prioridade sai de conta (Opportunity Score), não de gosto.

## 2. Modo de execução
- Execução única: ler → extrair → classificar → pontuar → priorizar → entregar. Dúvidas só na pré-checagem, num bloco; depois, lacuna vira HIPÓTESE declarada.
- Tabelas em vez de prosa; sem repetir os insumos; sem notas de processo.
- Se a resposta for acabar, pare no fim de uma etapa com ESTADO ATUAL / PRÓXIMA AÇÃO e retome com "CONTINUAR".
- Rótulos: [LITERAL] para frase copiada como foi escrita; [SÍNTESE] para agrupamento feito por você; HIPÓTESE para o que não tem fonte. "N de M": M é o total de fontes independentes do material e N as que citam o item.

## 3. Insumos
- Avatar: {{avatar}}
- Produto e o que entrega: {{produto}}
- Pesquisa e voz do público: {{pesquisa}}
- Soluções atuais: {{solucoes_atuais}}
- Mercado e idioma: {{mercado_idioma}}
- Contexto da oferta: {{contexto_da_oferta}}
- Destino: {{destino}}

## 4. Contrato de entrega e pré-checagem
Etapa 0 · Inventário. Liste as fontes de {{pesquisa}} (`# | Fonte | Tipo | Trechos úteis`) e feche com "RECEBIDO X/N".

| Critério | Meta | Como vou medir |
|---|---|---|
| Dores extraídas | 20 ou mais, cada uma com frase | tabela da Etapa 1 |
| Camadas da dor | 4, todas preenchidas ou NÃO MAPEADO | Etapa 2 |
| Camadas do desejo | 5, todas preenchidas ou NÃO MAPEADO | Etapa 3 |
| Ponte | com a coluna "o produto não resolve" | Etapa 4 |
| Prioridade | top 10 dores por Opportunity Score, com cálculo | Etapa 5 |
| Uso na copy | 5 dores e 3 desejos com hook de exemplo | Etapa 6 |

Com menos de 20 dores reais, siga e marque PARCIAL com o número real. Não complete com dor inventada.

## 5. Etapas

### Etapa 1 · Extração e contagem
Objetivo: tirar do material cada dor e cada desejo com a frase que os prova.

| # | Tipo (dor ou desejo) | Item | Frase de origem | Rótulo | Fonte | N de M | Intensidade 1 a 5 |
|---|---|---|---|---|---|---|---|

Intensidade: 1 incômodo; 3 frustração repetida; 5 urgência, gasto alto, vergonha ou medo explícito.
Checkpoint: nenhum item sem frase ou rótulo HIPÓTESE.

### Etapa 2 · Dores em 4 camadas
Objetivo: descer do sintoma até a identidade.
1. Superficial: o sintoma que a pessoa fala em voz alta.
2. Funcional: o que deixa de conseguir na rotina (tempo, dinheiro, relação, saúde, trabalho).
3. Emocional: o que sente (culpa, vergonha, cansaço, medo, raiva).
4. Identidade: o que conclui sobre si ou como acha que os outros a veem.
5. Feche com medo imediato (o que teme agora) e medo futuro (o que acontece se nada mudar em 6 a 12 meses).

| Camada | Dor | Frase (#) | N de M | Como a copy toca nessa camada |
|---|---|---|---|---|

Checkpoint: a camada de identidade tem pelo menos 1 dor com evidência ou está marcada NÃO MAPEADO.

### Etapa 3 · Desejos em 5 camadas
Objetivo: saber o que prometer e como a vida dela fica depois.
1. Funcional: o resultado objetivo.
2. Prático: como a rotina fica mais fácil.
3. Emocional: como quer se sentir.
4. Social: como quer ser vista.
5. Identidade: quem quer se tornar.
6. Feche com o futuro imaginado em 1 frase ("daqui a 3 meses, ela...").

| Camada | Desejo | Frase (#) | N de M | Promessa que esse desejo sustenta |
|---|---|---|---|---|

Checkpoint: desejo não é promessa. A coluna de promessa diz o que a oferta pode dizer sem passar da entrega.

### Etapa 4 · Momento de luta e ponte
Objetivo: ligar a situação de hoje ao resultado, sem prometer o que o produto não faz.
1. Reconstrua de 3 a 5 cenas concretas que fazem a pessoa procurar solução agora (ex.: a encomenda do fim de semana deu prejuízo e ela só percebeu ao somar as notas). Cada cena com evidência ou HIPÓTESE.
2. Monte a ponte.

| Situação atual | Situação desejada | Obstáculos no caminho | O produto resolve | O produto não resolve |
|---|---|---|---|---|

Checkpoint: a coluna "o produto não resolve" tem pelo menos 1 linha honesta.

### Etapa 5 · Opportunity Score e top 10
Objetivo: priorizar as dores com conta, adaptando o método de Tony Ulwick (Outcome-Driven Innovation).
1. Para cada dor com N igual ou maior que 2:
   - Frequência F (0 a 10) = 10 × N da dor ÷ N da dor mais citada;
   - Intensidade I (0 a 10) = média das intensidades × 2;
   - Importância = (F + I) ÷ 2;
   - Satisfação S (0 a 10) = quanto as soluções atuais resolvem essa dor, segundo {{solucoes_atuais}} e o material (0 quando todas falham);
   - Opportunity Score = 5 × (Importância + o maior valor entre Importância − S e 0), de 0 a 100.
2. Ranqueie o top 10.

| # | Dor | Camada | F | I | Importância | S | Opportunity Score | N de M |
|---|---|---|---|---|---|---|---|---|

Checkpoint: o cálculo aparece em toda linha; S sem evidência vira HIPÓTESE.

### Etapa 6 · Matriz urgência × intensidade e uso na copy
Objetivo: dizer onde cada dor e cada desejo trabalham melhor.
1. Posicione os 8 itens mais fortes na matriz.

| | Baixa intensidade | Alta intensidade |
|---|---|---|
| Alta urgência | | |
| Baixa urgência | | |

2. Para as 5 primeiras dores do top 10 e os 3 desejos mais fortes, diga onde usar (hook de anúncio, headline, lead de VSL, pergunta de quiz, bullet, e-mail, objeção) e escreva 1 hook de exemplo com o vocabulário do material.

| Item | Onde usar | Por quê | Hook de exemplo |
|---|---|---|---|

Checkpoint: os hooks falam da situação, não apontam atributo pessoal do leitor ("quando a fatura chega e não fecha", e não "você que está endividada").

## 6. Entregável final
Entregar em {{destino}}, nesta ordem: resumo de 5 linhas (dor número 1 com o score, dor de identidade, desejo de identidade, o que o produto não resolve, status do contrato) → extração → dores → desejos → momento de luta e ponte → top 10 → matriz e uso na copy → handoff. Não entregar: lista de dores sem frase, copy completa.

```
HANDOFF
Etapa concluída: Mapa de dores e desejos
Entradas utilizadas:
Top 3 dores (com Opportunity Score):
Desejo de identidade:
O que o produto não resolve:
Hipóteses abertas:
Próximo prompt: estrategia/oferta-completa ou estrategia/linguagem-do-cliente
Próxima ação única:
```

## 7. Autoverificação final
1. "RECEBIDO X/N" feito.
2. 20 dores ou mais, cada uma com frase ou rótulo.
3. 4 camadas de dor e 5 de desejo preenchidas ou NÃO MAPEADO.
4. Medo imediato e medo futuro escritos.
5. De 3 a 5 cenas de momento de luta, todas concretas.
6. Coluna "o produto não resolve" preenchida.
7. Top 10 com o cálculo do Opportunity Score visível.
8. Matriz com 8 itens; 5 dores e 3 desejos com hook.
9. Nenhum hook com atributo pessoal ou resultado garantido.
10. Sem resíduos de processo; handoff preenchido.
Status por requisito: CONCLUÍDO, PARCIAL (com número real) ou BLOQUEADO (com o que destrava).

## 8. Limites e riscos
- Não inventar frase, número ou dado de mercado. Sem fonte, HIPÓTESE.
- Remover nome, @ e qualquer dado que identifique pessoas (LGPD).
- Hooks com força e sem aviso legal; promessa de resultado em saúde, renda ou emagrecimento fica marcada para compliance/revisao-de-compliance.
- Riscos, se houver, em até 5 linhas separadas no fim.
