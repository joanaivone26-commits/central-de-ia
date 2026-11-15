---
title: Matriz de ângulos criativos
description: Cruza ângulos (por qual motivo a pessoa compra) com formatos (como a mensagem aparece) e personas para gerar um plano de criativos organizado, em vez de ideias soltas. Mostra o que já foi testado e o que falta.
when: Use ao planejar a rodada de criativos de uma oferta, quando os criativos começam a se repetir ou quando a conta depende de um único vencedor.
origin: Prática de testes de criativos em tráfego pago; versão Trip Angle
tags: [criativos, ângulos, testes, planejamento]
author: Trip Angle
---
## O que é
Criativo novo não é só um vídeo novo. É uma combinação de três escolhas:

| Eixo | Pergunta | Exemplos |
|---|---|---|
| Ângulo | por qual motivo a pessoa compraria? | dor, desejo, medo, mecanismo, prova social, inimigo comum, economia de tempo, custo de não agir |
| Formato | como a mensagem chega? | UGC, talking head, voz em off com B-roll, demonstração, estático, carrossel, print, entrevista |
| Persona | para quem, especificamente? | iniciante, quem já tentou, quem compra para outra pessoa, profissional |

A matriz força variedade de verdade: dez vídeos com o mesmo ângulo em formatos diferentes ainda são um teste só de ângulo.

## Como montar
1. Liste de 6 a 10 ângulos a partir da pesquisa (dores, desejos, objeções, comentários).
2. Liste os 4 a 6 formatos que você consegue produzir.
3. Liste de 2 a 4 personas da oferta.
4. Monte a tabela ângulo x formato. Marque o que já rodou e o resultado.
5. Escolha a próxima rodada: primeiro teste ângulos (mesmo formato, ângulos diferentes). Depois que um ângulo vence, teste formatos dentro dele. Por último, personas.
6. Dê um código para cada célula (ex. A3-F2-P1) e use na nomenclatura do anúncio. Assim o relatório mostra qual eixo está ganhando.

## Exemplo: curso de design de sobrancelhas
| Ângulo \ Formato | UGC | Demonstração | Estático | Talking head |
|---|---|---|---|---|
| A1 Renda com agenda flexível | testado: médio | | | |
| A2 Mecanismo (mapeamento com linha) | | testado: vencedor | | a testar |
| A3 Medo de errar na cliente | a testar | | | |
| A4 Prova social (alunas atendendo) | | | a testar | |
| A5 Custo de não agir (continuar no emprego que não gosta) | | | | a testar |

Leitura: A2 em demonstração venceu. Próxima rodada: A2 em talking head e UGC, e abrir A3 em UGC para achar o próximo ângulo. Se A1 for usado, falar de agenda e de aprender uma profissão, sem prometer valor de renda.

## Erros comuns
- Testar formato antes de achar o ângulo.
- Chamar de "ângulo novo" o mesmo ângulo com outra frase.
- Não registrar o que já foi testado e repetir teste.
- Ângulo de renda com promessa de valor ("ganhe R$ 5 mil"). Fale do caminho, não de quanto a pessoa vai ganhar.

## Prompt para aplicar
Preencha: oferta, pesquisa_de_publico, formatos_possiveis, personas e criativos_ja_testados.

```text
Você é estrategista de criativos de performance. Monte uma matriz de ângulos criativos.

Oferta: {{oferta}}
Pesquisa de público (dores, desejos, objeções): {{pesquisa_de_publico}}
Formatos que consigo produzir: {{formatos_possiveis}}
Personas: {{personas}}
Criativos já testados e resultado: {{criativos_ja_testados}}

1. Liste 8 ângulos com código (A1...A8) e a fonte de cada um na pesquisa.
2. Liste os formatos com código (F1...) e as personas com código (P1...).
3. Monte a tabela ângulo x formato marcando o que já foi testado.
4. Proponha a próxima rodada com 6 criativos, explicando a ordem (ângulo antes de formato).
5. Para cada criativo da rodada, escreva o hook e o código (ex. A3-F1-P2).
Sem resultado garantido, sem promessa de renda e sem apontar atributos pessoais do público.
```
