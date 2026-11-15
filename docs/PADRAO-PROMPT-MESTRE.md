# Padrão de prompt mestre Trip Angle

Um prompt mestre conduz uma missão inteira numa única execução: **ler → pesquisar → construir → revisar → entregar**. Recebe todos os insumos de uma vez, executa as etapas em ordem com checagem interna, revisa a própria entrega e termina com o entregável final pronto para usar e um bloco de passagem para a missão seguinte.

Ele substitui a sequência de prompts pequenos e o pedido em "micro-turnos", que é o que mais gasta crédito: cada volta reenvia todo o contexto.

## Princípios (vêm do jeito que a operação Trip Angle trabalha)

1. **Execução única.** Dúvidas só na pré-checagem, num bloco só. Depois de começar, nada de perguntas: lacunas viram premissas declaradas e reversíveis.
2. **Meta é meta.** Quantidade, corte e critério definidos nos insumos não são reduzidos nem contornados (não troca nicho, país ou idioma para bater número). Se não atingir, expande em até 3 ciclos e entrega aprovados + "quase passou" com números reais.
3. **Escopo inteiro.** Não entrega parte achando que basta. Se precisar parar por limite de resposta, para no fim de uma etapa e retoma dali com "CONTINUAR".
4. **Evidência rotulada.** FATO (com fonte), ALEGAÇÃO (do anunciante), HIPÓTESE (inferência), NÃO MAPEADO. Nunca inventa URL, ID, métrica ou depoimento.
5. **Força na copy, jurídico à parte.** Nenhum aviso legal, selo ou matriz de claims dentro das peças. Riscos vão numa seção separada e curta. Limites reais continuam valendo: não fabricar depoimento, não usar marca de veículo ou pessoa real, não copiar texto literal de concorrente, não acessar área restrita.
6. **Entrega limpa.** Sem resíduos de processo ("status", "versão", "placeholder", "a confirmar"), sem marcação que quebra no destino quando o destino é Google Docs ou Notion.
7. **Linguagem que não trava o modelo.** No corpo do prompt, use "análise de concorrência", "mineração de ofertas" e "pesquisa de mercado". Evite termos que os modelos associam a invasão ("espionagem avançada", "hackear", "burlar").

8. **Entregar X, não entregar Y.** Todo prompt diz o artefato exato (ex.: "o prompt para gerar a imagem, não a imagem"; "página web única, não slides nem PDF"; "texto puro sem asteriscos para o YouTube") e o que é proibido entregar no lugar.
9. **Decisões travadas.** Nicho, mercado, idioma, funil exigido, marca e preços informados nos insumos não podem ser trocados pelo modelo.
10. **Anexos primeiro.** Etapa 0 obrigatória: inventário do que foi enviado (anexos, links, transcrições) com o protocolo "RECEBIDO X/N"; nada é analisado antes de tudo estar listado. Fonte inacessível tem plano B declarado (pedir export, print, transcrição ou CSV), nunca senha.
11. **Lotes com estado.** Em entregas grandes, cada lote termina com "ESTADO ATUAL / PRÓXIMA AÇÃO" para retomar sem refazer.
12. **Sem calibragem em micro-rodadas.** O prompt já pede tom, intensidade e tamanho nos insumos (ex.: `[padrão = agressivo contra o comportamento, sem promessa de ganho]`) para não precisar de 6 a 10 pedidos de "mais curto" ou "mais agressivo".

## Quando é prompt mestre e quando é módulo

| Tipo | Uso | Tamanho |
|---|---|---|
| **Prompt mestre** (`level: mestre`) | Uma missão completa da Trilha DR | 180 a 450 linhas |
| **Módulo** (`level: modulo`) | Uma parte da missão feita sozinha (ex.: só os leads, só a matriz de ângulos). Mesmo esqueleto, menos etapas | 90 a 200 linhas |

## Frontmatter

```yaml
---
title: VSL do zero (prompt mestre)
description: Do briefing ao roteiro final revisado, numa execução: lead pela matriz consciência × sofisticação, 14 blocos com minutagem, 3 leads alternativos, cortes de 2–4 min e 60–90 s e notas de B-roll.
level: mestre
stage: copy
etapas: 9
tempo: 20-30 min
variables:
  produto: "[obrigatório] Produto: nome, formato e o que a pessoa recebe"
  duracao: "[padrão = 12 a 18 min] Duração alvo da VSL"
  destino: "[padrão = aqui no chat] Onde entregar: aqui, Google Docs (uma guia por item) ou Notion"
tools: [claude, chatgpt, gemini]
output: Contrato de entrega + roteiro em 14 blocos com minutagem + 3 leads + 2 cortes + handoff
next: [criativos/criativos-em-escala, funil/pagina-advertorial-e-quiz]
tags: [vsl, copy, prompt mestre]
author: Trip Angle
---
```

Cada rótulo começa com **[obrigatório]**, **[opcional]** ou **[padrão = X]** (opcional com valor padrão). O site mostra isso no formulário e o comando do Claude Code pede de uma vez só os obrigatórios que faltarem. Todo prompt mestre tem os campos **destino**, **mercado/idioma** e, quando houver volume, **quantidade**.

## Estrutura do corpo (as 8 seções, nesta ordem)

```markdown
# <MISSÃO> · Prompt mestre Trip Angle

## 1. Papel e missão
Uma linha de papel sênior + o resultado de negócio esperado + o que separa entrega profissional de amadora nesta missão (3 a 6 linhas concretas).

## 2. Modo de execução
Texto fixo: execução única; dúvidas só na pré-checagem; premissas declaradas; sem planejamento extra nem rascunhos intermediários; sem notas de processo; regras de economia (abaixo); como continuar se a resposta acabar.

## 3. Insumos
Formulário com todas as {{variaveis}}, agrupadas: Oferta · Público · Mercado e idioma · Material de referência (o que é só referência × o que é da oferta) · Quantidade e critérios · Destino.
Inclui o espaço opcional {{contexto_da_oferta}} para colar o bloco de contexto gerado pelo Prompt Mestre 0, o campo {{modo}} quando a missão admite criar, modelar ou diagnosticar, e {{anexos}} para listar o que foi enviado.

## 4. Contrato de entrega e pré-checagem
Etapa 0: inventário de anexos e acessos ("RECEBIDO X/N"). Depois o modelo abre a resposta com a tabela `Critério | Meta | Como vou medir`, montada a partir dos insumos, e lista numa única vez o que falta (insumo obrigatório, acesso, ferramenta). Tudo o que não depende disso começa já.

## 5. Etapas
### Etapa N · <nome>
Objetivo · Passos numerados · Saída (formato exato) · Checkpoint interno (autoavaliação contra critério, nunca pergunta).
Inclui regras de evidência (FATO, ALEGAÇÃO, HIPÓTESE, NÃO MAPEADO) e o **fallback**: o que fazer quando não atinge o mínimo, quando a ferramenta falha ou quando aparece login.

## 6. Entregável final
Formato compacto, nesta ordem: resumo de até 5 linhas com o status do contrato → tabelas → links em texto puro, um por linha → anexos/destino → **Handoff** (bloco com os dados mínimos para a próxima missão e a próxima ação única).

## 7. Autoverificação final
Checklist de 8 a 15 itens verificáveis + varredura de resíduos. Status por requisito: CONCLUÍDO, PARCIAL (com o porquê e o número real) ou BLOQUEADO (com o que destrava). Corrija o que falhar antes de entregar.

## 8. Limites e riscos
Modo jurídico interno: nada de aviso dentro das peças; seção "Riscos" de até 5 linhas, separada. Limites reais (depoimento, marcas e pessoas reais, cópia literal, área restrita). O que não puder fazer vai para "Não executado e por quê".
```

## Regras de economia de tokens (vão na seção 2 de todo prompt)

- Não repita nem resuma os insumos. Não explique o que vai fazer.
- Tabelas em vez de prosa. Texto corrido só no que é peça final (copy, roteiro, e-mail).
- Pare a pesquisa ao atingir a meta mais 10% de folga.
- Alternativas só onde decidem resultado (headline, hook, lead); nunca várias versões completas.
- Uma resposta final. Em lotes grandes, grave no destino ao fim de cada lote e retome do próximo item sem refazer.

## Saída alternativa

Todo prompt mestre aceita `{{saida}}` com `[padrão = executar aqui]` ou `gerar prompt para <ferramenta>` (Lovable, Claude, Gemini, Kling, Veo). No segundo caso, a entrega é uma solicitação completa para a outra ferramenta, com a cláusula "altere só X; preserve Y".

## Formatos e números da casa

- Roteiros de 60–90 s = 150–225 palavras, com contagem informada; VSL ≈ 150 palavras por minuto (±10%).
- Imagens: Feed 1080×1350, Stories/Reels 1080×1920 (área segura 64–1016 × 260–1500), YouTube 1280×720, imagens de checkout abaixo de 2 MB. Entregar Feed e Stories por padrão.
- Variedade: cada peça difere das outras em pelo menos 3 dimensões (ângulo, formato, cenário, hook, paleta).
- Títulos e nomes: 10 opções pontuadas de 0 a 5 (especificidade, conflito, concretude, tamanho); entregar a melhor + 2.
- Links: texto puro, um por linha, ordem fixa (anúncio → página do anunciante → cada etapa do funil → checkout → perfil).

## Validação no build

`tools/build.py` avisa quando um prompt `level: mestre` não tem as seções 1 a 8, tem menos de 180 linhas, não declara `etapas` e `stage`, ou tem variável sem `[obrigatório]`, `[opcional]` ou `[padrão = …]`.
