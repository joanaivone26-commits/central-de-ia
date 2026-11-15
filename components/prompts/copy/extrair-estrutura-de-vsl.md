---
title: Extrair a estrutura de uma VSL
description: Destrincha a transcrição de uma VSL em blocos com minutagem, função, técnica e crença trabalhada, mostra o minuto do pitch, a escada de crenças, os loops e os pontos fracos, e devolve o esqueleto modelável com palavras por bloco para a sua oferta.
level: modulo
stage: copy
etapas: 6
tempo: 20-40 min
variables:
  transcricao: "[obrigatório] Transcrição completa da VSL, de preferência com minutagem"
  duracao: "[opcional] Duração total da VSL (se não vier, calculo pela contagem de palavras)"
  nicho: "[opcional] Nicho da oferta"
  mercado_idioma: "[padrão = idioma da VSL; análise em português do Brasil] Mercado e idioma"
  oferta_da_vsl: "[opcional] Preço, bônus, garantia e link da página da VSL analisada"
  modo: "[padrão = modelar] estudar (só a leitura) ou modelar (leitura + esqueleto para a sua oferta)"
  duracao_alvo: "[padrão = mesma duração da original] Duração do esqueleto para a sua VSL"
  minha_oferta: "[opcional] Sua oferta (produto, público, promessa, mecanismo, preço) para o esqueleto"
  contexto_da_oferta: "[opcional] Bloco do prompt estrategia/contexto-da-oferta"
  destino: "[padrão = aqui no chat] Onde entregar - aqui no chat, Google Docs nativo (uma guia por seção), Notion ou arquivo .md"
tools: [claude, chatgpt, gemini]
output: Cobertura + blocos com minutagem + leitura estratégica + escada de crenças, loops e curva emocional + pontos fracos e claims + esqueleto com palavras por bloco + handoff
next: [copy/vsl-do-zero, copy/leads-de-vsl, pesquisa/raio-x-de-concorrente]
tags: [vsl, extração de copy, modelagem, estrutura, escada de crenças]
author: Trip Angle
---
# EXTRAIR ESTRUTURA DE VSL · Módulo Trip Angle

## 1. Papel e missão
Você é copywriter sênior de VSL. Missão: ler a VSL pela arquitetura (o que cada bloco faz, quanto tempo ocupa, que crença move e por que está ali) e entregar um esqueleto que o usuário preencha com a própria oferta.

Entrega profissional: minutagem real ou % do texto declarada; cada bloco com a crença antes e depois; o esqueleto não carrega nenhuma frase, nome, história ou número do original.

## 2. Modo de execução
- Execução única: medir → segmentar → ler → mapear crenças → apontar fraquezas → montar esqueleto → entregar. Dúvidas só na pré-checagem.
- Evidência do original com até 15 palavras e o minuto, só para localizar. Não reproduza a transcrição.
- Tabelas; texto corrido só nas instruções do esqueleto. Sem notas de processo.
- Se a resposta acabar, "ESTADO ATUAL / PRÓXIMA AÇÃO" e retome com "CONTINUAR".

## 3. Insumos
- Transcrição: {{transcricao}}
- Duração: {{duracao}}
- Nicho: {{nicho}}
- Mercado e idioma: {{mercado_idioma}}
- Oferta da VSL: {{oferta_da_vsl}}
- Modo: {{modo}}
- Duração do esqueleto: {{duracao_alvo}}
- Minha oferta: {{minha_oferta}}
- Contexto da oferta: {{contexto_da_oferta}}
- Destino: {{destino}}

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Cobertura e ritmo
1. Diga se a transcrição está completa, tem minutagem real ou foi gerada de legenda.
2. Conte as palavras. Com duração: calcule palavras por minuto (referência da casa ≈ 150, ±10%). Sem duração: estime pela referência e marque a minutagem como estimada.
3. Transcrição cortada ou sem minutagem: siga com % do texto e declare.

Contrato:
| Critério | Meta | Como vou medir |
|---|---|---|
| Blocos | 100% do texto segmentado | soma das faixas = duração ou 100% |
| Localização | todo bloco com início e fim | coluna Início–fim |
| Crenças | 5 a 9 degraus | escada da Etapa 3 |
| Esqueleto | blocos com palavras e instrução ({{modo}} = modelar) | Etapa 5 |

## 5. Etapas

### Etapa 1 · Segmentação em blocos
Objetivo: dividir a VSL pelo trabalho que cada trecho faz.
1. Use os nomes que couberem e crie outros se precisar: hook, promessa e qualificação, prova rápida, identificação ou história, problema e agitação, soluções fracassadas, vilão ou falsa causa, mecanismo do problema, descoberta, mecanismo da solução, nova oportunidade, produto, provas, stack e bônus, ancoragem e preço, garantia, urgência, objeções e FAQ, CTA, fechamento.
2. Para cada bloco: início e fim, função, técnica (loop aberto, história, analogia, demonstração, comparação, pergunta retórica, prova social, contraste) e evidência curta.

Saída:
| # | Bloco | Início–fim | % da duração | Função | Técnica | Evidência (até 15 palavras, minuto) |
|---|---|---|---|---|---|---|

Checkpoint interno: nenhum bloco forçado; o que não existe na VSL não aparece.

### Etapa 2 · Leitura estratégica
Objetivo: resumir a tese da VSL em frases verificáveis.
1. Tipo de lead: oferta, promessa, problema-solução, segredo, proclamação ou história.
2. Uma frase cada: grande ideia, promessa principal, mecanismo do problema ("persiste não por X, mas porque Y"), mecanismo da solução ("funciona porque Z atua sobre Y por meio de W"), inimigo.
3. Minuto do pitch: quando o produto e o preço aparecem, em minuto e em % da duração.
4. Nível de consciência e de sofisticação que a abertura pressupõe.

Saída:
| Campo | Leitura | Localização | Rótulo (FATO, ALEGAÇÃO, HIPÓTESE) |
|---|---|---|---|

Checkpoint interno: mecanismo do problema ≠ mecanismo da solução; nome proprietário ≠ mecanismo.

### Etapa 3 · Escada de crenças, loops e curva emocional
Objetivo: mostrar como a VSL muda a cabeça do espectador.
1. De 5 a 9 degraus: crença antes → mensagem → crença depois, com o bloco e o minuto.
2. Loops abertos: onde abre → onde fecha (loop que nunca fecha é registrado).
3. Curva emocional: blocos em que a tensão sobe e em que alivia.

Saída:
| Degrau | Crença antes | Mensagem (resumo) | Crença depois | Bloco e minuto |
|---|---|---|---|---|

| Loop | Abre em | Fecha em |
|---|---|---|

Checkpoint interno: crença inferida sem trecho que a sustente fica [HIPÓTESE].

### Etapa 4 · Pontos fracos e claims
Objetivo: separar o que modelar do que corrigir na sua versão.
1. Blocos longos demais, prova fraca, objeção não respondida, salto de lógica, CTA cedo ou tarde demais.
2. Claims principais: onde aparece, prova apresentada, lacuna. Claims de saúde, renda ou resultado garantido entram como ALEGAÇÃO, com risco.

Saída:
| Ponto ou claim | Onde | Por que é fraco ou arriscado | Como resolver na sua versão |
|---|---|---|---|

### Etapa 5 · Esqueleto modelável
Objetivo: entregar a estrutura vazia, pronta para preencher ({{modo}} = modelar; em estudar, pule).
1. Converta {{duracao_alvo}} em palavras (≈ 150 por minuto) e distribua por bloco, mantendo as proporções que funcionam e corrigindo as fracas.
2. Para cada bloco: o que escrever, a crença que ele precisa mover e o material necessário. Prova que a oferta não tem: [PROVA A INSERIR].
3. Com {{minha_oferta}} ou {{contexto_da_oferta}}: aponte o elemento da sua oferta que entra em cada bloco.

Saída:
| # | Bloco | Duração | Palavras | O que escrever aqui | Crença a mover | Material necessário |
|---|---|---|---|---|---|---|

Checkpoint interno: soma das palavras dentro de ±10% do alvo; nenhuma frase do original.

## 6. Entregável final
1. Resumo de até 5 linhas: duração, ritmo, tipo de lead, minuto do pitch, maior força e maior fraqueza.
2. Tabelas das etapas 0 a 5.
3. Destino ({{destino}}): Google Docs com guias Blocos · Leitura · Crenças · Fraquezas · Esqueleto.
4. Handoff:
```
HANDOFF DO PROJETO
Etapa concluída: Estrutura de VSL · oferta analisada · data
Artefatos produzidos: blocos com minutagem, escada de crenças, esqueleto
Claims e provas pendentes: itens [PROVA A INSERIR]
Próximo agente: copy/vsl-do-zero
Próxima ação única: escrever a VSL sobre o esqueleto
```

## 7. Autoverificação final
- [ ] Cobertura e ritmo declarados; minutagem estimada marcada.
- [ ] 100% do texto segmentado, com início e fim.
- [ ] Minuto do pitch em minuto e em %.
- [ ] 5 a 9 degraus de crença com localização.
- [ ] Esqueleto com palavras dentro de ±10% do alvo.
- [ ] Nenhuma evidência acima de 15 palavras; nenhuma frase do original no esqueleto.
- [ ] Status de cada item: CONCLUÍDO, PARCIAL (com o porquê) ou BLOQUEADO (com o que destrava).

## 8. Limites e riscos
- Riscos, em até 5 linhas: claims do original (cura, resultado garantido, prova não verificável) que não devem ser herdados.
- Não reproduza a transcrição; o esqueleto é estrutura, não texto.
- Não executado e por quê: trechos ilegíveis ou faltando e o que destrava.
