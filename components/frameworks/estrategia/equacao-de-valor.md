---
title: Equação de valor
description: Mostra as quatro alavancas que fazem uma oferta valer mais aos olhos do comprador - o tamanho do resultado, a confiança de que ele vem, o tempo de espera e o esforço exigido - e como mexer em cada uma sem baixar preço.
when: Use ao criar ou revisar uma oferta, ao montar o stack de bônus e quando o público diz que está caro.
origin: Alex Hormozi, $100M Offers (2021)
tags: [oferta, estratégia, valor percebido, alex hormozi]
author: Trip Angle
---
## O que é
O valor que o comprador enxerga não depende só do que você entrega. Ele cresce com duas coisas e diminui com outras duas:

| Sobe o valor | Desce o valor |
|---|---|
| Resultado sonhado: o tamanho do que a pessoa quer | Tempo de espera: quanto demora para ver o resultado |
| Confiança: o quanto ela acredita que vai conseguir | Esforço e sacrifício: o que ela precisa fazer ou abrir mão |

Lido como fração: resultado × confiança em cima, tempo × esforço embaixo. As ofertas mais fortes geralmente ganham mais diminuindo o de baixo (mais rápido, mais fácil) do que inflando o de cima.

## Quando usar
- Criar oferta do zero.
- Decidir quais bônus entram (cada bônus precisa mexer em uma alavanca).
- Responder à objeção de preço sem dar desconto.

## Passo a passo
1. **Resultado sonhado:** escreva o resultado em termos concretos, do jeito que o público fala. Sem exagero.
2. **Confiança:** liste o que faz a pessoa acreditar: provas, garantia, demonstração, acompanhamento, casos parecidos com o dela.
3. **Tempo:** encontre a primeira vitória rápida (algo que ela consegue nos primeiros dias) e coloque na frente.
4. **Esforço:** liste tudo que dá trabalho e transforme em pronto: templates, roteiros, checklists, feito com você.
5. **Obstáculos:** liste cada obstáculo entre a compra e o resultado. Cada um vira um item da oferta.
6. **Corte:** tire o que não mexe em nenhuma alavanca. Volume sem função diminui a clareza.

## Exemplo: mentoria para nutricionistas conseguirem pacientes pelo Instagram
- **Resultado sonhado:** agenda com pacientes particulares sem depender só de convênio.
- **Confiança:** casos de mentoradas com autorização, aula de diagnóstico do perfil antes da compra, garantia de 7 dias.
- **Tempo:** na primeira semana, o perfil revisado e a primeira sequência de stories de convite publicada.
- **Esforço:** 30 roteiros de conteúdo prontos para adaptar, modelo de mensagem para responder o direct, planilha de agenda.
- **Obstáculo → item:** "não sei o que postar" vira o banco de roteiros; "tenho vergonha de vender" vira o roteiro de conversa; "não tenho tempo" vira o calendário de 3 posts por semana.

## Erros comuns
- Aumentar a promessa em vez de aumentar a confiança.
- Empilhar bônus que dão mais trabalho (mais aulas = mais esforço).
- Esquecer que o tempo até a primeira vitória pesa mais que o tempo até o resultado final.
- Prometer resultado garantido para subir a confiança. Garantia de satisfação é segura; garantia de resultado só se você puder honrar e as condições estiverem claras.

## Prompt para aplicar
Preencha: produto, publico, resultado_sonhado, entregaveis_atuais, provas e preco.

```text
Você é estrategista de oferta. Use a equação de valor de Alex Hormozi (resultado sonhado e confiança em cima; tempo de espera e esforço embaixo).

Produto: {{produto}}
Público: {{publico}}
Resultado sonhado (nas palavras do público): {{resultado_sonhado}}
Entregáveis atuais: {{entregaveis_atuais}}
Provas disponíveis: {{provas}}
Preço: {{preco}}

1. Dê nota de 1 a 5 para a oferta atual em cada alavanca e justifique.
2. Liste os obstáculos entre a compra e o resultado.
3. Para cada obstáculo, proponha um item da oferta e diga qual alavanca ele mexe.
4. Proponha a primeira vitória rápida.
5. Diga o que cortar.
6. Mostre o stack final em tabela: item, obstáculo que resolve, alavanca.
Não invente provas nem valores. Sem resultado garantido.
```
