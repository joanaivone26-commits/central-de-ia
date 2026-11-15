---
name: framework-jobs-to-be-done
description: "Framework Jobs to Be Done (o trabalho que o cliente contrata): Troca a pergunta \"quem é o cliente?\" por \"que progresso ele está tentando fazer?\". Revela por que as pessoas compram, o que disputa com o seu produto e quais forças empurram e seguram a compra. Use na pesquisa de público, antes de definir avatar e oferta, em entrevistas com compradores e quando o produto vende para perfis muito diferentes pelo mesmo motivo."
---

# Jobs to Be Done (o trabalho que o cliente contrata)

## O que é
Ninguém compra um produto pelo produto. A pessoa "contrata" uma solução para fazer um trabalho na vida dela, numa situação específica. O trabalho tem três camadas:

| Camada | Pergunta | Exemplo |
|---|---|---|
| Funcional | o que precisa ser feito? | fechar o mês sem misturar dinheiro da empresa e da casa |
| Emocional | como quer se sentir? | sem aquele frio na barriga quando chega o DAS |
| Social | como quer ser visto? | como alguém que leva o negócio a sério |

O concorrente real é tudo que o cliente poderia contratar para o mesmo trabalho, inclusive "não fazer nada" ou "uma planilha que ele mesmo faz".

## As 4 forças da compra
| Força | Direção | Pergunta de entrevista |
|---|---|---|
| Empurrão da situação atual | a favor | o que estava acontecendo quando você começou a procurar? |
| Atração da nova solução | a favor | o que você imaginou que ia mudar? |
| Ansiedade com o novo | contra | o que te deu medo antes de comprar? |
| Hábito do jeito atual | contra | o que você fazia antes e por que era difícil largar? |

A compra acontece quando empurrão + atração superam ansiedade + hábito. A copy trabalha as quatro.

## Passo a passo
1. Entreviste 5 a 10 pessoas que compraram recentemente (até 90 dias). Pergunte sobre o momento, não sobre o produto.
2. Reconstrua a linha do tempo: primeiro pensamento, busca, comparação, decisão, uso.
3. Escreva o trabalho em uma frase: "Quando [situação], eu quero [progresso], para [resultado emocional ou social]."
4. Liste as soluções concorrentes que o cliente considerou (inclusive as que não são produtos).
5. Mapeie as 4 forças com as frases dos entrevistados.
6. Leve para a copy: o empurrão vira hook, a atração vira promessa, a ansiedade vira garantia e prova, o hábito vira objeção respondida.

## Exemplo: planilha de controle financeiro para MEI
- **Trabalho:** "Quando o mês fecha e eu não sei quanto sobrou de verdade, eu quero separar o dinheiro do negócio do meu, para parar de ter medo de olhar a conta."
- **Concorrentes reais:** caderno, aplicativo de banco, contador, "deixar para ver depois".
- **Empurrão:** o mês em que faltou dinheiro para o DAS.
- **Atração:** abrir a planilha e ver o lucro do mês em um número.
- **Ansiedade:** "e se eu não souber usar planilha?"
- **Hábito:** "eu já anoto no caderno, mais ou menos funciona."
- **Na copy:** hook sobre o mês que não fecha; demonstração de 2 minutos mostrando que não precisa saber fórmula; comparação honesta com o caderno.

## Erros comuns
- Perguntar "o que você achou do produto?" em vez de "o que estava acontecendo quando você decidiu?".
- Ignorar o concorrente "não fazer nada".
- Escrever o trabalho como característica do produto.

## Prompt para aplicar
Preencha: produto, respostas_de_entrevistas (ou comentários de compradores) e alternativas_conhecidas.

```text
Você é pesquisador de Jobs to Be Done.

Produto: {{produto}}
Respostas de entrevistas ou relatos de compradores: {{respostas_de_entrevistas}}
Alternativas que o cliente usa ou considera: {{alternativas_conhecidas}}

1. Escreva o trabalho principal no formato "Quando [situação], eu quero [progresso], para [resultado]". Se houver mais de um, liste até 3.
2. Separe as camadas funcional, emocional e social.
3. Liste os concorrentes reais, inclusive não fazer nada.
4. Mapeie as 4 forças (empurrão, atração, ansiedade, hábito) com frases do material.
5. Traduza cada força em uma recomendação de copy (hook, promessa, prova, objeção).
6. Escreva 8 perguntas para a próxima rodada de entrevistas.
Use só o que está no material. Marque [HIPÓTESE] o que for dedução. Anonimize as frases.
```
