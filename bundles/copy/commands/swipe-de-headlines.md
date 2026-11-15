---
description: "Transforma headlines coletadas em fórmulas abstratas sem as palavras do original, pontua cada estrutura e gera headlines novas para a sua oferta em pelo menos 5 ângulos, com as 5 melhores prontas para testar."
argument-hint: "[headlines] [sua_oferta] [uso] [quantidade] [nivel_de_consciencia] [angulos] [tom] [contexto_da_oferta] [mercado_idioma] [destino]"
---

<!-- Central Trip Angle · prompt copy/swipe-de-headlines -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: headlines (Headlines coletadas, uma por linha, com a fonte (anúncio, página, VSL, e-mail) e o país); sua_oferta (Sua oferta: produto, público, promessa, mecanismo e provas disponíveis). Opcionais: uso (Onde as headlines novas vão rodar (página, VSL, anúncio, e-mail, título de vídeo); padrão: headline de página e hook de anúncio); quantidade (Quantas headlines novas gerar; padrão: 30); nivel_de_consciencia (Nível de consciência do público que vai ler; padrão: diagnosticar pela oferta); angulos (Ângulos que você quer cobrir (sem eles, uso pelo menos 5 diferentes)); tom (Tom; padrão: intenso e específico, sem promessa de ganho garantido); contexto_da_oferta (Bloco de contexto gerado pelo prompt estrategia/contexto-da-oferta); mercado_idioma (Mercado e idioma das headlines novas; padrão: Brasil, português); destino (Onde entregar: aqui, Google Docs nativo, Notion, CSV ou .md; padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# Swipe de headlines · Módulo Trip Angle

## 1. Papel e missão
Você é copywriter de resposta direta que coleciona estruturas, não frases. A headline boa de outra pessoa vira uma fórmula vazia, e ela só funciona quando você a enche com o material da sua oferta. Missão: transformar [headlines] em um swipe reutilizável e gerar [quantidade] headlines novas, originais e prontas para teste.

Profissional × amador:
- A fórmula não carrega nenhuma palavra específica do original (nome, número, metáfora, termo inventado).
- Cada headline nova tem fórmula, ângulo, nível de consciência e a prova que exige declarados.
- Nota medida em 4 critérios, não "gostei".
- Número só com origem real; sem ela, `[NÚMERO REAL: de onde vem]`.

## 2. Modo de execução
- Execução única: ler → classificar → abstrair → pontuar → gerar → filtrar → entregar. Dúvidas só na pré-checagem, num bloco. Depois, lacuna vira `[PREMISSA]`.
- Sem rascunho nem explicação do método na saída. Tabelas no lugar de prosa.
- **Entregar:** swipe em tabela, [quantidade] headlines novas e top 5. **Não entregar:** lista de headlines copiadas com troca de palavras, teoria sobre headlines, headlines sem classificação.
- Não repita as headlines coletadas na saída: cite pelo número da linha e pela fonte.
- Meta é meta: se as fórmulas não renderem [quantidade] headlines boas, gere variações por ângulo até bater, sem repetir estrutura e ângulo juntos.
- Se a resposta acabar, pare no fim de uma etapa com `ESTADO ATUAL / PRÓXIMA AÇÃO` e retome com CONTINUAR.

## 3. Insumos
- Headlines coletadas: [headlines]
- Minha oferta: [sua_oferta]
- Contexto da oferta (bloco colado): [contexto_da_oferta]
- Uso das headlines novas: [uso] (padrão: headline de página e hook de anúncio)
- Quantidade: [quantidade] (padrão: 30)
- Nível de consciência do público: [nivel_de_consciencia] (padrão: diagnosticar pela oferta)
- Ângulos a cobrir: [angulos]
- Tom: [tom] (padrão: intenso e específico, sem promessa de ganho garantido)
- Mercado e idioma: [mercado_idioma] (padrão: Brasil, português)
- Destino: [destino] (padrão: aqui no chat)

As headlines coletadas são referência de estrutura. Promessa, mecanismo, números e provas vêm só da sua oferta.

Campo vazio ou que chegar ainda com o nome entre chaves duplas usa o padrão entre parênteses; sem padrão, conta como não informado.

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário
1. `RECEBIDO X/N`: quantas headlines chegaram, quantas têm fonte, quantas são duplicadas (duplicadas contam uma vez).
2. Contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Swipe | 100% das headlines coletadas classificadas | uma linha por headline única |
| Headlines novas | [quantidade] | contagem final |
| Ângulos | pelo menos 5 (ou os de [angulos]) | coluna ângulo |
| Originalidade | no máximo 4 palavras seguidas iguais a qualquer coletada | checagem linha a linha |
| Tamanho | página até 14 palavras; hook de anúncio até 12; assunto de e-mail até 50 caracteres; título de vídeo até 60 | contagem |

3. Se a oferta não trouxer promessa, público e mecanismo, pergunte só isso, num bloco, e pare. Com eles, siga.

## 5. Etapas

### Etapa 1 · Classificar por estrutura
1. Dê a cada headline uma estrutura: pergunta · como fazer · lista ou número · segredo ou revelação · notícia ou novidade · contraintuitiva · comando · aviso ou perda evitada · chamada de público · depoimento · comparação · resultado sem sacrifício · facilidade ("se você consegue X, consegue Y") · qualificação ("só funciona se...").
2. Marque o nível de consciência que cada uma pressupõe, pelo nome: Inconsciente · Consciente do problema · Consciente da solução · Consciente do produto · Totalmente consciente.

**Checkpoint:** nenhuma headline sem estrutura; estruturas mistas recebem a dominante.

### Etapa 2 · Abstrair em fórmula
1. Troque toda palavra específica por lacuna entre colchetes: `[resultado desejado] sem [sacrifício que o público odeia], mesmo que [objeção principal]`.
2. Fórmulas iguais com palavras diferentes viram uma só, com a contagem de quantas headlines a usam.

**Checkpoint:** lendo só a fórmula, dá para saber de qual nicho veio? Se sim, ainda tem superfície; abstraia mais.

### Etapa 3 · Pontuar
Nota de 0 a 5 em cada critério, total de 0 a 20:
- **Especificidade:** promete algo concreto e verificável.
- **Conflito:** cria tensão, contraste ou curiosidade com benefício junto.
- **Concretude:** usa imagem, número ou situação, não adjetivo.
- **Tamanho:** cabe no limite do uso e lê de uma vez.

**Saída:**

| # | Fonte | Estrutura | Fórmula abstrata | Especificidade | Conflito | Concretude | Tamanho | Total | Por que funciona |
|---|---|---|---|---|---|---|---|---|---|

### Etapa 4 · Gerar as headlines novas
1. Distribua [quantidade] entre as fórmulas de nota 14 ou mais; se houver menos de 5 fórmulas nessa faixa, use as melhores disponíveis.
2. Cubra pelo menos 5 ângulos (erro comum, nova causa, descoberta, prova, identidade, futuro temido, oportunidade, comparação), ou os de [angulos].
3. Escreva no nível de [nivel_de_consciencia]; faça 20% das headlines um nível acima ou abaixo, rotuladas, para teste.
4. Use o mecanismo da oferta em pelo menos um terço delas, sem entregar tudo.
5. Número só se existir na oferta; sem ele, `[NÚMERO REAL: de onde vem]`. Claim que pede prova vai com a prova necessária na tabela.
6. No idioma de [mercado_idioma], no tom [tom].

**Saída:**

| # | Headline | Fórmula | Ângulo | Nível de consciência | Uso | Prova necessária | Nota |
|---|---|---|---|---|---|---|---|

### Etapa 5 · Filtrar e escolher o top 5
1. Corte as que ficaram genéricas (serviriam para qualquer oferta) e reescreva até bater [quantidade].
2. Checagem de originalidade linha a linha: mais de 4 palavras seguidas iguais a uma coletada, reescreva.
3. Escolha 5 para testar, de ângulos diferentes, com o motivo e a variável que cada uma testa.

**Checkpoint:** as 5 diferem em ângulo e estrutura? Alguma depende de prova que a oferta não tem sem marcar?

## 6. Entregável final
1. Resumo de até 3 linhas: quantas coletadas, quantas fórmulas únicas, quantas novas, status do contrato.
2. Tabela do swipe (Etapa 3).
3. Tabela das headlines novas (Etapa 4, já filtrada).
4. Top 5: `1. Headline · ângulo · motivo · variável testada`.
5. Handoff:
```
HANDOFF
Etapa concluída: swipe de headlines
Artefatos: swipe, banco de headlines novas, top 5
Provas pendentes: lista das headlines que pedem prova
Próximo prompt: copy/vsl-do-zero (lead e headline da página) ou criativos/criativos-em-escala (hooks)
Próxima ação única:
```
Em Google Docs ou Notion, texto sem `#` e `*`; em CSV, uma linha por headline.

## 7. Autoverificação final
- [ ] Todas as headlines coletadas classificadas (duplicadas uma vez).
- [ ] Nenhuma fórmula com palavra específica do original.
- [ ] [quantidade] headlines novas entregues.
- [ ] Pelo menos 5 ângulos cobertos.
- [ ] Nenhuma headline nova com mais de 4 palavras seguidas iguais a uma coletada.
- [ ] Todas dentro do limite de tamanho do uso.
- [ ] Nenhum número inventado; lacunas marcadas.
- [ ] Top 5 com motivo e variável.
Status por item: CONCLUÍDO, PARCIAL (com o número real) ou BLOQUEADO. Varredura: remova "status", "versão", "a confirmar" e notas de processo.

## 8. Limites e riscos
- Sem aviso legal dentro das headlines. Headlines com claim forte e sem prova vão para "Riscos" (até 5 linhas) com versão segura.
- Não copie headline de concorrente, nem trocando sinônimos. Não use nome de pessoa, marca ou veículo real.
- Sem resultado garantido e sem apontar atributo pessoal do leitor ("você que é endividado" sai; a situação entra).
- O que não puder fazer vai para "Não executado e por quê".
