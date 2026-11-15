---
title: Estrutura de VSL de resposta direta
description: Sequência de blocos de uma VSL de venda, do hook ao fechamento, com a função e o tempo aproximado de cada um. Serve para escrever do zero ou revisar uma VSL que não converte.
when: Use para ofertas vendidas por vídeo em tráfego frio ou morno, principalmente produtos de ticket baixo e médio com página de VSL e checkout direto.
origin: Formato de VSL popularizado por Jon Benson; sequência organizada pela Trip Angle a partir da prática de resposta direta
tags: [vsl, copy, estrutura, vídeo de vendas]
author: Trip Angle
---
## O que é
A VSL é uma carta de vendas falada. Cada bloco tem um trabalho e prepara o próximo. Se um bloco falha, a retenção cai ali e o resto não importa. Por isso a estrutura vem antes do texto.

## Os blocos
| # | Bloco | Trabalho | Peso aproximado |
|---|---|---|---|
| 1 | Hook | prender nos primeiros 10 a 30 segundos | 3% |
| 2 | Promessa e qualificação | dizer o que a pessoa vai descobrir e para quem é | 3% |
| 3 | Prova rápida | mostrar cedo que vale a pena ficar | 3% |
| 4 | História ou identificação | fazer o público se ver no problema | 10% |
| 5 | Problema e culpado | tirar a culpa do público e apontar a causa | 10% |
| 6 | Mecanismo do problema | explicar por que as tentativas anteriores falharam | 8% |
| 7 | Mecanismo da solução | explicar por que este caminho funciona | 10% |
| 8 | Apresentação do produto | o que é, como funciona, o que vem dentro | 10% |
| 9 | Provas | depoimentos autorizados, demonstração, dados | 12% |
| 10 | Oferta e stack | tudo que a pessoa recebe | 8% |
| 11 | Ancoragem e preço | comparação honesta e preço final | 5% |
| 12 | Garantia | tirar o risco da decisão | 4% |
| 13 | Urgência real | motivo verdadeiro para agir agora | 3% |
| 14 | CTA | o que fazer e onde clicar | 3% |
| 15 | FAQ e objeções | responder o que ainda trava | 8% |

Os pesos são ponto de partida. Público mais desconfiado pede mais história e prova; público mais quente pede oferta mais cedo.

## Passo a passo
1. Defina avatar, nível de consciência, big idea e mecanismo antes de escrever.
2. Escreva primeiro os blocos 6 e 7 (mecanismo). Eles sustentam o resto.
3. Escreva 10 hooks e escolha 3 para testar.
4. Escreva os blocos na ordem, com loops abertos: prometa algo no começo que só é entregue mais adiante.
5. Leia em voz alta e cronometre. Ritmo natural fica em torno de 140 a 160 palavras por minuto.
6. Revise compliance: sem resultado garantido, sem depoimento sem autorização, sem escassez falsa.
7. Depois de rodar, olhe a retenção por minuto e reescreva o bloco onde a queda é maior.

## Exemplo: curso de amigurumi para vender (estrutura resumida)
- **Hook:** a peça de crochê que esgota na feira do bairro não é a mais difícil de fazer.
- **Identificação:** quem faz crochê há anos e nunca conseguiu vender pelo preço justo.
- **Culpado:** escolher peças pelo gosto de quem faz, não pelo que o cliente procura.
- **Mecanismo:** escolher modelos pela procura, padronizar o tempo de produção e precificar por hora.
- **Produto:** aulas de 12 modelos escolhidos por procura, com planilha de preço.
- **Oferta:** curso + planilha + aula de fotos com celular, garantia de 7 dias, CTA para o checkout.

## Erros comuns
- Hook longo, com apresentação pessoal antes de qualquer promessa.
- Mecanismo vago ("um método exclusivo") sem explicação.
- Preço jogado sem stack e sem ancoragem.
- FAQ ausente: a objeção que trava fica sem resposta.

## Prompt para aplicar
Preencha: produto, avatar, nivel_de_consciencia, big_idea, mecanismo, provas, oferta e duracao.

```text
Você é copywriter de VSL de resposta direta. Escreva o roteiro de uma VSL seguindo a estrutura de 15 blocos (Hook, Promessa e qualificação, Prova rápida, História, Problema e culpado, Mecanismo do problema, Mecanismo da solução, Produto, Provas, Oferta e stack, Ancoragem e preço, Garantia, Urgência real, CTA, FAQ).

Produto: {{produto}}
Avatar: {{avatar}}
Nível de consciência: {{nivel_de_consciencia}}
Big idea: {{big_idea}}
Mecanismo: {{mecanismo}}
Provas reais: {{provas}}
Oferta (entregáveis, preço, garantia): {{oferta}}
Duração desejada: {{duracao}}

1. Antes do roteiro, mostre uma tabela com os blocos, o tempo de cada um e o loop aberto principal.
2. Escreva 5 hooks e use o mais forte.
3. Escreva o roteiro completo, bloco a bloco, rotulado.
4. Onde faltar prova ou detalhe real, marque [NECESSÁRIO] em vez de inventar.
5. No fim, liste os 3 pontos de maior risco de queda de retenção.
Sem resultado garantido, sem apontar atributos pessoais do ouvinte, sem urgência falsa.
```
