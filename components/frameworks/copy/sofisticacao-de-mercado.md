---
title: Sofisticação de mercado
description: Mede quantas promessas o mercado já ouviu e diz o que a sua copy precisa fazer para ser notada - de anunciar o benefício direto até trocar a promessa por identificação. Define se a hora é de promessa, de mecanismo ou de experiência.
when: Use ao entrar num nicho, ao ver que promessas fortes pararam de funcionar ou ao decidir se a oferta precisa de mecanismo novo.
origin: Eugene Schwartz, Breakthrough Advertising (1966)
tags: [copy, estratégia, eugene schwartz, posicionamento]
author: Trip Angle
---
## O que é
Mercado também se acostuma. Quando ninguém prometeu nada, a promessa simples basta. Quando todo mundo já prometeu, a mesma frase vira ruído. A sofisticação mede esse cansaço em 5 estágios e indica a jogada de cada um.

| Estágio | Como está o mercado | O que a copy faz |
|---|---|---|
| 1 | ninguém prometeu isso ainda | anuncia o benefício direto, simples |
| 2 | a promessa existe e funciona | amplia a mesma promessa (mais rápido, mais fácil, mais específico) |
| 3 | promessas grandes já cansaram | apresenta um mecanismo novo: como o resultado acontece |
| 4 | vários mecanismos competem | melhora o mecanismo: mais concreto, mais simples, mais provado |
| 5 | o público não acredita em mais nada | troca a promessa por identificação, história e experiência |

## Como diagnosticar
1. Liste 10 anúncios ativos do nicho na Biblioteca de Anúncios.
2. Anote a promessa principal de cada um.
3. Conte quantos usam mecanismo nomeado.
4. Leia comentários: o público responde com interesse ou com "lá vem mais um"?
5. Classifique: promessas simples e pouca concorrência = 1 ou 2; muita promessa grande = 3; muitos mecanismos = 4; descrença generalizada = 5.

## Combinação com níveis de consciência
Sofisticação fala do mercado; consciência fala do leitor. Um público pode estar consciente do problema (nível 2) num mercado de estágio 5. Nesse caso, a copy começa pela dor, mas sem promessa exagerada: entra pela identificação e pela história.

## Exemplo: cursos de inglês para adultos no Brasil
Mercado em estágio 5. Todo mundo já ouviu "fluente em 6 meses", "método sem decoreba", "inglês com séries". Promessa nova não é escutada.
- **Jogada:** identificação e experiência. Ex.: um anúncio que mostra um adulto travando para pedir um café numa viagem e o que ele treinou depois, sem prometer prazo; uma aula aberta onde a pessoa sente que consegue falar no primeiro dia.
- **Se for usar mecanismo (estágio 4):** precisa ser concreto e demonstrável, como treinar só as frases que mais aparecem em situações de viagem, com prática de fala gravada e corrigida. Se for citar quantidade de frases, use o número real do material.

## Erros comuns
- Usar promessa de estágio 1 num mercado de estágio 5 ("aprenda inglês!").
- Inventar um nome de mecanismo sem mudar nada de verdade.
- Achar que estágio 5 é ruim: é só um jogo diferente, que premia confiança e experiência.

## Prompt para aplicar
Preencha: nicho, promessas_dos_concorrentes, comentarios_do_publico, produto e mecanismo.

```text
Você é estrategista de resposta direta. Use o modelo de sofisticação de mercado de Eugene Schwartz.

Nicho: {{nicho}}
Promessas dos concorrentes (de anúncios ativos): {{promessas_dos_concorrentes}}
Comentários do público: {{comentarios_do_publico}}
Meu produto: {{produto}}
Meu mecanismo: {{mecanismo}}

1. Classifique o mercado de 1 a 5 e mostre as evidências.
2. Diga qual jogada a minha copy deve fazer nesse estágio.
3. Escreva 5 hooks coerentes com o estágio.
4. Diga se o meu mecanismo é suficiente para o estágio ou o que falta.
Use só as evidências que eu passei. Marque [HIPÓTESE] onde não houver dado. Sem resultado garantido.
```
