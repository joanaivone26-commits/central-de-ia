---
title: Níveis de consciência
description: Classifica o público em cinco estágios, do que não percebe o problema ao que já quer comprar, e define por onde a copy deve começar em cada um. É a base para escolher hook, lead e página.
when: Use antes de escrever qualquer anúncio, lead ou página, para decidir o ponto de entrada da mensagem e por que um criativo funciona em remarketing e falha no público frio.
origin: Eugene Schwartz, Breakthrough Advertising (1966)
tags: [copy, estratégia, eugene schwartz, consciência]
author: Trip Angle
---
## O que é
A pergunta central é: o que esta pessoa já sabe? Quem não sabe que tem o problema não vai clicar numa oferta. Quem já quer comprar não precisa de uma aula sobre o problema. A copy entra no ponto em que o leitor está e o leva um degrau por vez.

| Nível | O que a pessoa sabe | Onde a copy começa |
|---|---|---|
| 1. Inconsciente | não percebe o problema ou não liga | história, curiosidade, identificação com uma situação |
| 2. Consciente do problema | sente a dor, não sabe que há solução | a dor nas palavras dela e a promessa de saída |
| 3. Consciente da solução | sabe que existem soluções, não conhece a sua | o mecanismo: por que este caminho é diferente |
| 4. Consciente do produto | conhece o seu produto, não decidiu | provas, comparação, resposta a objeções |
| 5. Totalmente consciente | quer comprar, espera a condição certa | oferta, preço, bônus, prazo |

## Como usar
1. Descreva em uma frase o que o público do canal sabe hoje.
2. Escolha o nível de entrada. Tráfego frio costuma estar entre 1 e 3; remarketing e base, entre 4 e 5.
3. Escreva o hook e o lead para esse nível.
4. Planeje o caminho: qual peça leva do nível atual ao próximo (anúncio → conteúdo → VSL → oferta).
5. Confira o desalinhamento: anúncio de nível 5 (preço e desconto) para público de nível 2 queima verba.

## Sinais de que o nível está errado
- CTR bom e conversão baixa: o anúncio prometeu algo que a página não continuou.
- Hook rate baixo no frio com criativo que vende bem no remarketing: o criativo é de nível alto.
- Comentários perguntando "o que é isso?": você começou num nível acima do público.

## Exemplo: curso de fotografia de produto com celular para lojistas
- **Nível 1:** uma história curta: a lojista que mudou a mesa de fotos para perto da janela e passou a receber perguntas de tamanho e prazo em vez de "quanto custa?". A lojista ainda não pensa em foto como problema; a história faz ela perceber.
- **Nível 2:** "Foto escura e com fundo bagunçado faz o produto parecer mais barato do que é."
- **Nível 3:** "Não precisa de câmera nem estúdio: uma janela, uma cartolina branca e duas configurações do celular resolvem a maior parte das fotos de catálogo."
- **Nível 4:** "Veja as fotos feitas pelas alunas no primeiro exercício do curso."
- **Nível 5:** "Curso de foto com celular com o bônus do kit de fundos até domingo."

## Erros comuns
- Escrever tudo para o nível 5 porque é mais fácil.
- Achar que nível é fixo: o mesmo público sobe de nível depois de ver seus conteúdos.
- Confundir nível de consciência com sofisticação do mercado (um fala do leitor, o outro fala de quanto o mercado já prometeu).

## Prompt para aplicar
Preencha: produto, publico, canal, o_que_o_publico_ja_sabe e mecanismo.

```text
Você é estrategista de resposta direta. Use os 5 níveis de consciência de Eugene Schwartz.

Produto: {{produto}}
Público: {{publico}}
Canal: {{canal}}
O que o público já sabe hoje: {{o_que_o_publico_ja_sabe}}
Mecanismo: {{mecanismo}}

1. Diga em qual nível está a maior parte desse público e por quê. Marque [HIPÓTESE] se não houver dado.
2. Para cada um dos 5 níveis, escreva: hook, primeira frase do lead e CTA.
3. Recomende o nível de entrada para este canal e a sequência de peças até a compra.
Sem resultado garantido e sem apontar atributos pessoais do leitor.
```
