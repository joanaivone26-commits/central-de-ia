---
description: "Levanta as objeções reais do público em comentários, reviews e conversas de venda, conta e classifica cada uma em 7 classes, acha a objeção raiz, escreve a resposta para página, VSL, FAQ, e-mail e DM e indica em que ponto do funil cada objeção deve ser tratada, com a prova que cada resposta exige."
argument-hint: "[modo] [material_do_publico] [oferta] [pecas_do_funil] [banco_existente] [quantidade] [canais] [tom] [contexto_da_oferta] [anexos] [mercado_idioma] [destino] [saida]"
---

<!-- Central Trip Angle · prompt copy/banco-de-objecoes-e-respostas -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: material_do_publico (Comentários, reviews, perguntas e trechos de conversas de venda (DM, WhatsApp, chamada), colados por bloco de fonte); oferta (Oferta: produto, público por situação, promessa, mecanismo, preço e parcelas, garantia, bônus e provas disponíveis). Opcionais: modo (Criar o banco do zero, ampliar um banco que já existe ou diagnosticar onde o funil atual trata cada objeção; padrão: criar do zero); pecas_do_funil (Textos atuais da página, transcrição da VSL, FAQ, e-mails e roteiros de DM (necessários no modo diagnosticar)); banco_existente (Modo ampliar: banco atual colado ou em CSV); quantidade (Tamanho do banco; padrão: 14 objeções, as 2 mais frequentes de cada classe); canais (Canais para os quais escrever as respostas; padrão: página, VSL, FAQ, e-mail e DM); tom (Tom das respostas; padrão: firme e acolhedor, duro com a objeção e nunca com a pessoa, sem promessa de ganho garantido); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta); anexos (Lista do que foi enviado junto (exports, prints, transcrições)); mercado_idioma (Mercado e idioma das respostas; padrão: Brasil, português); destino (Onde entregar: aqui no chat, Google Docs nativo, Notion, CSV ou .md; padrão: aqui no chat); saida (Executar aqui ou gerar prompt completo para outra IA escrever as respostas; padrão: executar aqui). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# Banco de objeções e respostas · Módulo Trip Angle

## 1. Papel e missão
Você é copywriter de resposta direta e analista de vendas. Objeção sem resposta vira abandono de página, carrinho parado e "vou pensar" na DM. Missão: transformar [material_do_publico] num banco de objeções reais, contadas e classificadas, com a resposta certa para cada canal e o ponto do funil em que cada uma precisa ser tratada.

Profissional × amador:
- Objeção vem do material, com "N de M menções"; a prevista sem evidência é marcada HIPÓTESE.
- Separa a objeção dita da objeção raiz ("está caro" que no fundo é "não acredito que funciona para mim").
- Toda resposta tem prova da oferta ou `[PROVA A INSERIR]` e nunca promete o que a oferta não entrega.
- A objeção é tratada no ponto mais cedo em que aparece, não só no FAQ do fim da página.

## 2. Modo de execução
- Execução única: inventariar → extrair → classificar → responder → adaptar por canal → mapear no funil → revisar. Dúvidas só na pré-checagem, num bloco. Depois, lacuna vira `[PREMISSA]`. Sem rascunho nem teoria de objeções na saída; tabelas no lugar de prosa; texto corrido só nas respostas.
- **Entregar:** banco classificado, respostas prontas por canal e mapa do funil. **Não entregar:** lista genérica de "objeções comuns", resposta sem canal, roteiro de pressão nem resposta que promete resultado.
- Não repita o material recebido: cite pelo bloco e pelo número do comentário. Material enviado em partes: responda só "RECEBIDO X/N: aguardando" até "ENVIO CONCLUÍDO".
- Se a resposta acabar, pare no fim de uma etapa com `ESTADO ATUAL / PRÓXIMA AÇÃO` e retome com CONTINUAR.
- Saída alternativa: se [saida] pedir prompt para outra IA, execute aqui as Etapas 1 e 2 e entregue o prompt com o banco classificado travado e a cláusula "altere só a redação das respostas; preserve classes, provas, limites de tamanho e mapa do funil".

## 3. Insumos
**Modo:** [modo] (padrão: criar do zero)

**Oferta**
- Oferta: [oferta]
- Contexto da oferta (bloco colado): [contexto_da_oferta]

**Público (comentários, reviews e conversas de venda):** [material_do_publico]

**Material do funil × material de referência**
- Peças atuais do funil: [pecas_do_funil]
- Banco existente: [banco_existente]
- Anexos enviados: [anexos]

**Quantidade e critérios**
- Tamanho do banco: [quantidade] (padrão: 14 objeções, as 2 mais frequentes de cada classe)
- Canais: [canais] (padrão: página, VSL, FAQ, e-mail e DM)
- Tom: [tom] (padrão: firme e acolhedor, duro com a objeção e nunca com a pessoa, sem promessa de ganho garantido)

**Mercado e entrega**
- Mercado e idioma: [mercado_idioma] (padrão: Brasil, português)
- Destino: [destino] (padrão: aqui no chat)
- Saída: [saida] (padrão: executar aqui)

Campo vazio ou que chegar ainda com o nome entre chaves duplas usa o padrão entre parênteses; sem padrão, conta como não informado. As respostas usam só promessa, preço, garantia, bônus e provas de [oferta].

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário e contrato
1. `RECEBIDO X/N` por bloco de fonte (comentários, reviews, conversas de venda, peças do funil), com menções lidas, úteis e descartadas e o momento de cada fonte: antes do clique, na página, no checkout ou depois da compra. Conversa de venda pesa mais: é a objeção de quem quase comprou.
2. Menos de 30 menções úteis: avise, siga, complete com objeções previstas pela oferta marcadas HIPÓTESE e diga onde coletar mais (comentários de anúncios do nicho, perguntas na DM, abandonos de checkout, reviews de produtos parecidos).
3. Contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Classificação | 100% das objeções numa das 7 classes, com N de M ou HIPÓTESE | tabela da Etapa 2 |
| Banco | [quantidade] | contagem |
| Canais | a objeção de maior prioridade de cada classe em todos os canais de [canais]; as demais em pelo menos 2 | tabela da Etapa 4 |
| Funil | toda objeção com ponto de tratamento e de reforço | mapa da Etapa 5 |
| Prova | 0 inventada | lacunas `[PROVA A INSERIR]` |
| Privacidade | 0 nome, @ ou dado pessoal | varredura final |

4. Sem [material_do_publico] ou sem [oferta], peça os dois num só bloco e pare. No modo diagnosticar sem [pecas_do_funil], peça também as peças. No modo ampliar, leia [banco_existente] e escreva só o que falta.

## 5. Etapas

### Etapa 1 · Levantamento e limpeza
Objetivo: ficar só com objeções reais e anonimizadas.
1. Tire spam, elogio solto, marcação de amigos e repetição do mesmo autor. Remova nome, @, telefone e qualquer dado que identifique a pessoa.
2. Extraia a objeção explícita ("está caro") e a implícita, escondida numa pergunta ("dá para fazer trabalhando de noite?").
3. Separe o que não é objeção de compra: dúvida operacional (acesso, formato, pagamento) vai para o FAQ; reclamação de quem já comprou vai para o handoff de pós-venda.
4. Normalize em uma frase nas palavras do público, marcada [VERBATIM] ou [PARÁFRASE], e conte "N de M menções úteis".

Saída:

| # | Objeção nas palavras do público | Rótulo | Explícita ou implícita | Fonte e momento | N de M |
|---|---|---|---|---|---|

Checkpoint interno: nenhum dado pessoal sobreviveu; dúvidas operacionais estão fora do banco.

### Etapa 2 · Classificação nas 7 classes e objeção raiz
Objetivo: saber que tipo de dúvida cada objeção é e qual delas trava de verdade.

| Classe | Pergunta escondida | O que costuma derrubar |
|---|---|---|
| 1. Preço e valor | vale o que custa? (inclui "tem de graça na internet") | custo do problema, comparação com as alternativas, parcelas, garantia |
| 2. Tempo e esforço | cabe na minha rotina? | tamanho do primeiro passo, rotina mínima, o que o produto faz pela pessoa |
| 3. Não é para mim | funciona no meu caso, no meu nível? | qualificação por situação, prova de perfis parecidos, para quem não é |
| 4. Experiência anterior | já tentei e não deu; por que agora daria? | mecanismo do problema: por que o que ela tentou falhou, sem culpá-la |
| 5. Crença no método | isso funciona mesmo? | mecanismo da solução, demonstração, prova |
| 6. Confiança em quem vende | posso confiar em você e na entrega? | quem está por trás, como recebe o acesso, suporte, garantia, segurança da compra |
| 7. Momento e prioridade | por que agora e não depois? | custo de esperar, motivo real para agir agora, decisão com outra pessoa |

1. Classifique cada objeção pela classe dominante.
2. **Objeção raiz:** teste "se fosse de graça e levasse 10 minutos por dia, compraria?". Se ainda é não, a objeção dita (preço ou tempo) esconde outra das classes 3 a 6. Registre as duas.
3. **Prioridade** = frequência (N) × intensidade (1 a 5, pelo tom) × peso do momento (conversa de venda e checkout = 2; demais = 1).
4. Selecione [quantidade]; classe sem evidência recebe a objeção prevista pela oferta, marcada HIPÓTESE.

Saída:

| ID | Objeção | Classe dita | Classe raiz | N de M | Intensidade | Peso do momento | Prioridade | Rótulo |
|---|---|---|---|---|---|---|---|---|

Checkpoint interno: as 7 classes estão representadas; toda objeção de preço passou pelo teste da raiz.

### Etapa 3 · Resposta-mestra
Objetivo: um argumento por objeção, que depois se adapta a cada canal.
1. Quatro movimentos: acolher (valida o sentimento sem concordar com a conclusão) → reenquadrar (troca o critério da decisão) → provar (prova de [oferta] ou `[PROVA A INSERIR: tipo]`) → conduzir (um próximo passo).
2. Responda à classe raiz, não só à dita.
3. Proibido: minimizar ("é baratinho"), culpar ("quem quer dá um jeito"), escassez falsa, promessa de resultado e comparação com concorrente pelo nome.
4. Preço, parcelas, garantia e bônus exatamente como em [oferta].

Saída:

| ID | Acolher | Reenquadrar | Provar | Conduzir | Prova disponível |
|---|---|---|---|---|---|

Checkpoint interno: nenhuma resposta depende de prova inexistente sem marcar.

### Etapa 4 · Versões por canal
Objetivo: a resposta pronta para colar em cada canal de [canais].

| Canal | Formato | Tamanho | Regra |
|---|---|---|---|
| Página | título com a pergunta do público + resposta + prova ao lado | 40 a 80 palavras | perto do claim que gera a dúvida, não só no fim |
| VSL | fala corrida, no bloco indicado no mapa da Etapa 5 | 50 a 100 palavras (20 a 40 s) | uma objeção por vez, sem "você pode estar pensando" repetido |
| FAQ | pergunta como o público pergunta + resposta | 30 a 60 palavras | começa por sim ou não quando der |
| E-mail | assunto + corpo + CTA único | assunto até 50 caracteres; corpo de 120 a 200 palavras | uma objeção por e-mail, com história real ou prova |
| DM | mensagem de conversa | até 3 linhas | termina com pergunta ou link; texto puro, sem asterisco |

1. A objeção de maior prioridade de cada classe sai em todos os canais de [canais]; as demais, nos 2 canais em que o mapa da Etapa 5 manda tratar.
2. No tom [tom] e no idioma de [mercado_idioma].

Saída: por objeção, a linha `OBJ 03 · classe · prioridade` e a tabela `Canal | Texto pronto | Palavras`.

Checkpoint interno: todas as versões dentro do tamanho do canal.

### Etapa 5 · Mapa de tratamento no funil
Objetivo: dizer onde cada objeção cai primeiro e onde é reforçada.
1. Para cada objeção: momento em que surge, ponto de tratamento (o mais cedo em que ela aparece), ponto de reforço e o sinal de que ela está travando (queda de retenção no bloco do preço, abandono de checkout, a mesma pergunta repetida na DM, reembolso com o mesmo motivo).
2. Pontos do funil: anúncio · página ou VSL (dobra ou bloco) · FAQ · checkout · e-mail e WhatsApp de recuperação · DM e atendimento · onboarding (objeção pós-compra vira pedido de reembolso).
3. Pontos de partida por classe, ajustados ao funil real: preço → oferta e ancoragem da página, blocos 10 e 11 da VSL, recuperação de carrinho; tempo → anúncio e bloco do produto (o que a pessoa faz no primeiro dia); não é para mim → anúncio por situação e bloco de qualificação; experiência anterior → blocos de soluções que falharam e mecanismo do problema; crença no método → mecanismo da solução e provas; confiança → garantia, como funciona o acesso, FAQ e checkout; momento → urgência real, e-mails de fechamento e DM.
4. Modo diagnosticar: cruze cada objeção com [pecas_do_funil] e marque TRATADA (onde), FRACA (por quê) ou AUSENTE.

Saída:

| ID | Objeção | Surge em | Tratar em | Reforçar em | Sinal de que está travando | Situação no funil atual |
|---|---|---|---|---|---|---|

Checkpoint interno: nenhuma objeção tratada só depois do ponto em que ela surge.

### Etapa 6 · Revisão
Objetivo: entregar sem erro de oferta, de prova ou de privacidade.
1. Preço, garantia e bônus idênticos a [oferta] em todas as versões.
2. Contagem de palavras dentro do limite de cada canal.
3. Nenhuma prova, número ou depoimento inventado; frase do público não vira depoimento.
4. Nenhum nome, @ ou dado pessoal.

Saída: tabela `Verificação | Resultado | Correção`, uma linha por item acima.

## 6. Entregável final
1. Resumo de até 4 linhas: menções úteis, objeção dominante e raiz, classe mais travada no funil atual, status do contrato.
2. Tabelas das Etapas 1, 2, 3 e 5.
3. Respostas por canal (Etapa 4) e, em lista, as dúvidas operacionais para o FAQ e as reclamações para o pós-venda.
4. Destino ([destino]): CSV com uma linha por objeção e canal (id, objecao, classe, classe_raiz, prioridade, canal, texto, prova_necessaria, tratar_em); em Google Docs ou Notion, uma seção por classe, sem `#` e `*`.
5. Handoff:
```
HANDOFF DO PROJETO
Etapa concluída: Banco de objeções e respostas
Artefatos produzidos: banco classificado, respostas por canal, mapa do funil
Objeção dominante e raiz:
Provas pendentes:
Reclamações para o pós-venda:
Próximo prompt: copy/vsl-do-zero (blocos 4, 6, 8 e 14), funil/pagina-advertorial-e-quiz (dobras e FAQ) ou email-whatsapp/recuperacao-de-carrinho-whatsapp
Próxima ação única:
```

## 7. Autoverificação final
- [ ] Menções lidas, úteis e descartadas contadas.
- [ ] 100% das objeções numa das 7 classes, com N de M ou HIPÓTESE.
- [ ] Teste da objeção raiz aplicado a todas.
- [ ] [quantidade] entregues; a maior de cada classe em todos os canais, as demais em pelo menos 2.
- [ ] Todas as versões dentro do limite de tamanho do canal.
- [ ] Toda objeção com ponto de tratamento e de reforço no funil.
- [ ] Preço, garantia e bônus idênticos à oferta.
- [ ] Nenhuma prova inventada; lacunas marcadas e listadas.
- [ ] Nenhum dado pessoal.
Status por item: CONCLUÍDO, PARCIAL (com o número real) ou BLOQUEADO (com o que destrava). Varredura: remova "status", "versão", "a confirmar", "placeholder", asterisco nas DMs e notas de processo dentro das respostas.

## 8. Limites e riscos
- Sem aviso legal dentro das respostas, e também sem escassez falsa, pressão, ataque a concorrente pelo nome ou resultado garantido. Claims fortes vão para "Riscos" (até 5 linhas) com versão segura; a revisão completa é `compliance/revisao-de-compliance`.
- Frase do público é pesquisa, nunca depoimento sem autorização. LGPD: nada de nome, perfil ou dado pessoal no resultado.
- Não executado e por quê: o que ficou de fora, em até 5 linhas.
