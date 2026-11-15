---
name: framework-hook-corpo-cta
description: "Framework Hook, Corpo e CTA: Divide um anúncio em três partes com trabalhos diferentes - o hook para a rolagem, o corpo convence e o CTA leva ao clique - e liga cada parte à métrica que mostra se ela funcionou. Use para escrever, revisar e diagnosticar anúncios em vídeo curto e estáticos, principalmente quando você precisa saber qual parte do criativo trocar."
---

# Hook, Corpo e CTA

## O que é
Todo anúncio faz três trabalhos em sequência. Cada um tem uma métrica que mostra se deu certo, o que permite trocar só a parte que falhou.

| Parte | Tempo (vídeo de 30 s) | Trabalho | Métrica que mostra |
|---|---|---|---|
| Hook | 0 a 3 s | parar a rolagem e abrir curiosidade | hook rate (reproduções de 3 s ÷ impressões) |
| Corpo | 3 a 25 s | cumprir o que o hook abriu, mostrar mecanismo e prova | hold rate (ThruPlays ÷ reproduções de 3 s) |
| CTA | 25 a 30 s | dizer o que fazer e o que a pessoa ganha clicando | CTR de link |

## Tipos de hook
- Situação reconhecível ("Sabe quando...").
- Contraintuitivo (o contrário do que todo mundo diz).
- Demonstração (o produto em ação no primeiro segundo).
- Resultado visível e honesto (o depois de uma tarefa, não de um corpo).
- Pergunta específica.
- Chamada de público pelo interesse ("Pra quem faz marmita no domingo").

O hook tem três camadas que somam: o que se vê, o que se ouve e o texto na tela. Teste as três.

## Passo a passo
1. Escreva o corpo primeiro: mecanismo, prova e oferta em 15 a 20 segundos.
2. Escreva 5 hooks diferentes para o mesmo corpo.
3. Escreva o CTA com verbo e benefício do clique ("Toque em Saiba mais e veja o cardápio da semana").
4. Grave o corpo uma vez e os 5 hooks separados. Monte 5 anúncios.
5. Leia as métricas: hook rate baixo → troque o hook; hook ok e hold baixo → troque o corpo; hold ok e CTR baixo → troque o CTA ou a oferta citada.

## Exemplo: ebook de marmitas da semana
- **Hook (visual):** cinco potes fechados na geladeira, câmera abrindo a porta.
- **Hook (fala):** "Fiz o almoço da semana inteira em menos de duas horas de domingo."
- **Corpo:** "O segredo é cozinhar por base, não por receita: uma proteína, dois carboidratos e três legumes que combinam entre si. O ebook traz 8 semanas de cardápio, a lista de compras e a ordem de preparo para nada esfriar enquanto o resto cozinha."
- **CTA:** "Toque em Saiba mais e veja o cardápio da primeira semana."

(O tempo de preparo citado no hook precisa ser o tempo real de quem testou o cardápio.)

## Erros comuns
- Hook que promete algo que o corpo não entrega (sobe hook rate e derruba hold e conversão).
- Logo ou apresentação pessoal antes do hook.
- CTA genérico ("clique aqui") sem benefício.
- Julgar o anúncio só pelo CPA sem saber qual parte falhou.

## Prompt para aplicar
Preencha: produto, publico, mecanismo, prova, cta_desejado e duracao.

```text
Você é roteirista de anúncios de resposta direta. Use a estrutura Hook, Corpo e CTA.

Produto: {{produto}}
Público: {{publico}}
Mecanismo: {{mecanismo}}
Prova disponível: {{prova}}
CTA desejado: {{cta_desejado}}
Duração: {{duracao}}

1. Escreva o corpo primeiro, com mecanismo e prova, no tempo certo.
2. Escreva 5 hooks de tipos diferentes para o mesmo corpo, cada um com visual, fala e texto na tela.
3. Escreva 2 CTAs com verbo e benefício do clique.
4. Diga qual métrica vai julgar cada parte.
Sem resultado garantido, sem antes e depois de corpo e sem apontar atributos pessoais do público.
```
