---
description: "Encontra o mecanismo do problema (por que as tentativas falharam) e o da solução (por que este produto resolve) a partir do que o produto faz de verdade, compara 3 opções pontuadas, gera 30 nomes e pontua os 6 melhores, roda os testes do especialista cético e do nome removido e entrega o one-liner e a explicação de 30 segundos."
argument-hint: "[produto] [como_funciona] [avatar] [tentativas_anteriores] [concorrentes] [provas] [sofisticacao] [mercado_idioma] [contexto_da_oferta] [destino]"
---

<!-- Central Trip Angle · prompt estrategia/mecanismo-unico -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: produto (Produto e promessa); como_funciona (Como o produto funciona de verdade (método, passos, ferramentas, diferencial)); avatar (Avatar ou persona); tentativas_anteriores (O que o público já tentou e por que não funcionou (ou o cemitério de soluções do dossiê de avatar)). Opcionais: concorrentes (Mecanismos e promessas que os concorrentes usam); provas (Provas disponíveis (demonstração, dados próprios, casos, credenciais)); sofisticacao (Estágio de sofisticação do mercado, de 1 a 5); mercado_idioma (Mercado e idioma; padrão: Brasil, português); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta); destino (Onde entregar (aqui no chat, Google Docs nativo, Notion ou .md); padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# CONSTRUIR O MECANISMO ÚNICO · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista de oferta de direct response. Mecanismo não é invenção: é uma forma nova e clara de explicar o que o produto já faz. Este módulo entrega a explicação que faz o público pensar "então é por isso que nada funcionou comigo" e a ponte lógica até a solução.

O que separa o profissional do amador aqui:
- O mecanismo do problema tira a culpa da pessoa e aponta uma causa específica.
- O mecanismo da solução ataca exatamente essa causa, e cada passo existe no produto.
- O nome é escolhido entre 30, com nota, e sobrevive ao teste do nome removido.
- Em mercado sofisticado (estágio 3 em diante), o mecanismo é a principal arma; em estágio 1 e 2, ele reforça a promessa.

A divisão em mecanismo do problema, função e solução segue a leitura de Derick Carneiro; o papel do mecanismo por estágio de sofisticação segue Eugene Schwartz.

## 2. Modo de execução
- Execução única: ler → comparar causas → gerar opções → pontuar → nomear → testar → entregar. Dúvidas só na pré-checagem; depois, lacuna vira HIPÓTESE declarada.
- Opções em tabela com nota e sem prosa; só a vencedora é desenvolvida; os 30 nomes em lista de uma linha.
- Se a resposta for acabar, pare no fim de uma etapa com ESTADO ATUAL / PRÓXIMA AÇÃO e retome com "CONTINUAR".
- Rótulos: FATO, INFERÊNCIA, HIPÓTESE, ALEGAÇÃO, NÃO MAPEADO. Prova ausente vira [PROVA A INSERIR].

## 3. Insumos
- Produto e promessa: [produto]
- Como funciona: [como_funciona]
- Avatar: [avatar]
- Tentativas anteriores: [tentativas_anteriores]
- Concorrentes: [concorrentes]
- Provas: [provas]
- Sofisticação: [sofisticacao]
- Mercado e idioma: [mercado_idioma]
- Contexto da oferta: [contexto_da_oferta]
- Destino: [destino]

## 4. Contrato de entrega e pré-checagem
Etapa 0 · Inventário. Liste os insumos e feche com "RECEBIDO X/N". Sem [como_funciona], pergunte uma vez antes de começar: sem saber o que o produto faz, não existe mecanismo honesto.

| Critério | Meta | Como vou medir |
|---|---|---|
| Causas | toda tentativa anterior com causa aparente e causa real | Etapa 1 |
| Mecanismo do problema | 3 opções pontuadas de 0 a 30 | Etapa 2 |
| Mecanismo da solução | todo passo ligado a um componente do produto | Etapa 3 |
| Nomes | 30 listados, top 6 pontuados de 0 a 30 | Etapa 5 |
| Testes | 4 testes com resultado | Etapa 6 |
| Apresentação | one-liner e explicação de 70 a 80 palavras | Etapa 6 |

## 5. Etapas

### Etapa 1 · Causa aparente × causa real
Objetivo: ver o que cada tentativa atacava de fato.

| Tentativa | O que prometia | Causa que atacava | Era sintoma ou causa? | Por que falhou para esta persona |
|---|---|---|---|---|

Checkpoint: pelo menos 1 causa real que nenhuma tentativa atacou.

### Etapa 2 · Mecanismo do problema
Objetivo: a explicação que tira a culpa e abre espaço para a solução.
1. Escreva 3 opções na estrutura "problema aparente → causa real → consequência → necessidade de um novo caminho".
2. Pontue de 0 a 5 em 6 critérios: tira a culpa da pessoa; explica as tentativas da Etapa 1; é plausível e defensável; é novo para o estágio [sofisticacao]; liga com o produto; pode ser demonstrado.
3. Escolha uma e diga em 1 linha por que as outras perdem.

| Opção | Problema aparente | Causa real | Consequência | Novo caminho | Tira culpa | Explica falhas | Plausível | Novo | Liga ao produto | Demonstrável | Total /30 |
|---|---|---|---|---|---|---|---|---|---|---|---|

Checkpoint: a vencedora cabe em 1 frase e não depende de algo que o produto não faz.

### Etapa 3 · Mecanismo da solução
Objetivo: mostrar como o produto ataca exatamente a causa escolhida.
1. Fórmula: "a solução atua em [causa] por meio de [processo], permitindo [resultado intermediário visível] antes de [resultado final]".
2. Camada da função: o que precisa acontecer, na lógica, para a causa ser resolvida.
3. Tipo do mecanismo: funcional (como funciona), visual (o que dá para mostrar), nominal (nome do método) ou comportamental (como facilita a execução).

| Passo do mecanismo | O que o produto entrega para isso | Resultado intermediário visível | Prova disponível |
|---|---|---|---|

Checkpoint: nenhum passo sem componente real; prova ausente marcada [PROVA A INSERIR].

### Etapa 4 · Diferença real para os concorrentes
Objetivo: confirmar que o mecanismo é diferente de verdade, não só de nome.

| Concorrente | Mecanismo deles | O que o meu explica que o deles não | Diferença real ou só nome |
|---|---|---|---|

Sem [concorrentes], compare com as soluções da Etapa 1 e marque a comparação como INFERÊNCIA.
Checkpoint: pelo menos 1 diferença real; se for só nome, volte à Etapa 2.

### Etapa 5 · 30 nomes e top 6
Objetivo: um nome que gruda e descreve a função.
1. Gere 30 nomes: 10 descritivos, 10 de curiosidade ou metáfora, 10 com palavra-recipiente (método, protocolo, sistema, mapa, código, ciclo). Um por linha, sem explicação.
2. Pontue os 6 melhores de 0 a 5 em: falável em voz alta; desperta curiosidade; descreve a função; diferente do mercado; sem promessa embutida e sem termo regulado (médico, financeiro); demonstrável no produto.

| Nome | Falável | Curiosidade | Descreve | Diferente | Sem risco | Demonstrável | Total /30 |
|---|---|---|---|---|---|---|---|

Checkpoint: vencedor com 20 ou mais de 30; nenhum nome que pareça diagnóstico, cura ou rendimento garantido.

### Etapa 6 · Testes e apresentação
Objetivo: provar que o mecanismo aguenta a pressão e entregá-lo pronto para a copy.
1. Teste do "então é por isso": a persona sente alívio ao ouvir a explicação?
2. Teste da prova: o que sustenta o mecanismo (demonstração, dado próprio, lógica, experiência)?
3. Teste do especialista cético: o que um profissional sério do nicho contestaria, e a resposta.
4. Teste do nome removido: a lógica se sustenta sem o nome?

| Teste | Resultado | O que falta para passar |
|---|---|---|

5. One-liner em 1 frase.
6. Explicação de 30 segundos (70 a 80 palavras), pronta para VSL ou anúncio.
7. Como demonstrar o mecanismo em 1 cena de criativo (o que aparece na tela).
Checkpoint: os 4 testes respondidos; o que falhou vira pendência.

## 6. Entregável final
Entregar em [destino], nesta ordem: resumo de 5 linhas (mecanismo do problema, mecanismo da solução, nome vencedor, prova que falta, status do contrato) → causas → 3 opções → solução e passos → diferença para concorrentes → 30 nomes e top 6 → testes → one-liner, explicação de 30 segundos e cena de demonstração → handoff. Não entregar: VSL ou anúncio completos.

```
HANDOFF
Etapa concluída: Construir o mecanismo único
Mecanismo do problema:
Mecanismo da solução e nome:
One-liner:
Provas pendentes ([PROVA A INSERIR]):
Hipóteses abertas:
Próximo prompt: estrategia/big-idea ou estrategia/oferta-completa
Próxima ação única:
```

## 7. Autoverificação final
1. "RECEBIDO X/N" feito; [como_funciona] recebido.
2. Toda tentativa com causa aparente e causa real.
3. 3 mecanismos do problema pontuados e um escolhido.
4. Cada passo da solução ligado a um componente real.
5. Diferença real para os concorrentes escrita.
6. 30 nomes listados e top 6 pontuados; vencedor com 20 ou mais.
7. 4 testes com resultado.
8. One-liner e explicação de 70 a 80 palavras.
9. Nenhum estudo, cientista, descoberta ou dado inventado.
10. Sem resíduos de processo; handoff preenchido.
Status por requisito: CONCLUÍDO, PARCIAL (com número real) ou BLOQUEADO (com o que destrava).

## 8. Limites e riscos
- O mecanismo corresponde ao que o produto entrega. Se a explicação depende de algo que o produto não faz, ela é descartada.
- Não inventar estudo, cientista, descoberta ou número; o que precisa de prova fica [PROVA A INSERIR].
- Não reutilizar o nome ou a explicação de mecanismo de um concorrente.
- Em saúde, finanças e emagrecimento, nada de termo que soe como diagnóstico, cura ou rendimento garantido. Riscos, se houver, em até 5 linhas separadas no fim, sem aviso dentro das frases de apresentação.
