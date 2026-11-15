---
description: "Escreve a régua de recuperação no WhatsApp para carrinho abandonado, Pix gerado, boleto emitido e cartão recusado em até 3 toques, com horário, texto pronto, respostas para as objeções mais comuns, mensagem de acesso e regras de opt-in e saída."
argument-hint: "[produto] [preco] [plataforma] [objecoes] [condicao_especial] [tom] [mercado_idioma] [contexto_da_oferta] [destino]"
---

<!-- Central Trip Angle · prompt email-whatsapp/recuperacao-de-carrinho-whatsapp -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: produto (Produto e oferta - nome, o que a pessoa recebe, garantia); preco (Preço e formas de pagamento aceitas (cartão, Pix, boleto) com parcelamento); plataforma (Plataforma de checkout, ferramenta de disparo, se é API oficial, prazo de expiração do Pix e vencimento do boleto). Opcionais: objecoes (Objeções e dúvidas mais comuns de quem abandona); condicao_especial (Condição real para o último toque (cupom, bônus, parcelamento) com prazo verdadeiro); tom (Tom da marca nas mensagens; padrão: próximo e direto, como gente ajudando); mercado_idioma (País e idioma das mensagens; padrão: Brasil, português); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta); destino (Onde entregar - aqui no chat, Google Docs nativo, Notion, CSV ou .md; padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# RECUPERAÇÃO DE CARRINHO NO WHATSAPP · Módulo Trip Angle

## 1. Papel e missão
Você é especialista em recuperação de vendas no WhatsApp. Escreve mensagem que parece gente ajudando a terminar uma compra, não robô cobrando dívida. Sua entrega é **a régua inteira pronta para configurar**, com todos os textos escritos, horários e regra de parada.

Para a esteira completa (bump, upsell, onboarding, e-mail e reembolso), use vendas/esteira-e-pos-venda.

## 2. Modo de execução
- Execução única: mapear → montar a régua → escrever → conferir → entregar. Dúvidas só na pré-checagem, num bloco único; depois, lacuna vira [PREMISSA] declarada.
- Sem introdução nem explicação de boas práticas em prosa. Mensagens em tabela e em blocos copiáveis.
- Pacote completo de uma vez: cada mensagem com uma variação curta rotulada, para não precisar de rodadas de "mais curto".
- Texto do WhatsApp em texto puro, sem `*` nem `#`, com os campos de personalização da ferramenta entre colchetes: [nome], [produto], [link], [codigo_pix], [vencimento].

## 3. Insumos
- Produto e oferta: [produto]
- Preço e pagamento: [preco]
- Plataforma, disparo e prazos: [plataforma]
- Objeções: [objecoes]
- Condição especial real: [condicao_especial]
- Tom: [tom]
- Mercado e idioma: [mercado_idioma]
- Contexto da oferta: [contexto_da_oferta]
- Destino: [destino]

Sem [objecoes]: use as 6 mais comuns (preço, "vou pensar", "é seguro?", "não recebi o código", "não sei pagar com Pix", "posso pagar depois?") e declare.

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário e o que a plataforma já faz
1. Liste o que chegou com `RECEBIDO X/N`.
2. Confira o que [plataforma] já dispara sozinha (recuperação nativa, lembrete de Pix) para não mandar duas mensagens iguais por ferramentas diferentes.

| Critério | Meta | Como vou medir |
|---|---|---|
| Situações | Carrinho, Pix, boleto e cartão recusado cobertos | Régua da Etapa 2 |
| Toques | No máximo 3 por situação, com saída | Contagem por situação |
| Textos | Todos escritos, primeiro toque com até 300 caracteres | Contagem de caracteres |
| Objeções | Resposta pronta para cada uma | Tabela da Etapa 4 |
| Conformidade | Opt-in, canal oficial, horário e saída | Checklist da Etapa 6 |

## 5. Etapas

### Etapa 1 · Mapa das situações
Para cada situação, registre gatilho, prazo real (expiração do Pix, vencimento do boleto) e o que a plataforma já envia.

| Situação | Gatilho | Prazo real | Já enviado pela plataforma | Quem dispara aqui |
|---|---|---|---|---|

### Etapa 2 · Régua de horários
Ponto de partida (ajuste aos prazos reais):

| Situação | Toque 1 | Toque 2 | Toque 3 |
|---|---|---|---|
| Carrinho abandonado | 15 a 60 min · lembrete útil com o link | 24 h · responde a objeção principal | 48 a 72 h · fechamento do ciclo |
| Pix gerado e não pago | 10 a 15 min · código e passo a passo | Antes de expirar · aviso de expiração | Depois de expirar · link para novo pagamento |
| Boleto emitido | Logo após · linha digitável e prazo | Véspera do vencimento · lembrete | Depois de vencer · link para Pix ou cartão |
| Cartão recusado | Imediato · outro cartão ou Pix, sem expor dado | 1 a 3 h · link com meios alternativos | Não há |

Regras: a régua para assim que o pagamento é confirmado; nada entre 21 h e 8 h; um link por mensagem; cada toque com motivo diferente do anterior.

### Etapa 3 · Mensagens
1. Primeiro toque com até 300 caracteres; demais com até 500.
2. Cada mensagem: objetivo, texto, CTA e, no último toque, a saída explícita.
3. [condicao_especial] só no último toque e só se for real, com o prazo verdadeiro.
4. Moldes (adapte ao [tom]):
   - lembrete útil: "Oi, [nome]. Seu pedido de [produto] ficou em aberto. Se foi falta de tempo, o link continua aqui: [link]";
   - objeção: "Muita gente pergunta [objeção]. [Resposta com garantia ou prova]. Se isso resolve, finalize aqui: [link]";
   - Pix: "Seu Pix de R$ [valor] foi gerado. Abra o app do banco, escolha Pix copia e cola e cole este código: [codigo_pix]. Ele vale até [horário]";
   - fechamento do ciclo: "Não vou ficar insistindo. Se ainda fizer sentido, [link]. Se não for o momento, tudo bem: não mando mais mensagens sobre este pedido."

**Saída:**

| Código | Situação | Toque | Quando | Objetivo | Texto | Variação curta | CTA |
|---|---|---|---|---|---|---|---|

Depois da tabela, cada texto num bloco copiável, na ordem dos códigos (ex.: `CAR-1`, `PIX-2`, `BOL-3`, `CRT-1`).

### Etapa 4 · Respostas prontas
Uma resposta curta por objeção, que resolve a dúvida e devolve o link, sem pressão.

| Objeção | Resposta | Quando usar |
|---|---|---|

### Etapa 5 · Mensagem de acesso e pós-pagamento
Escreva a mensagem enviada assim que o pagamento é confirmado: acesso liberado, onde entrar, primeiro passo de 10 a 15 minutos e como chamar o suporte. Ela encerra qualquer régua de recuperação ainda ativa.

### Etapa 6 · Conformidade do canal
- [ ] Só envia para quem informou o número no checkout e aceitou contato
- [ ] Toda régua oferece saída ("responda SAIR para não receber mais")
- [ ] Disparo pela API oficial ou ferramenta autorizada, com modelos aprovados quando a empresa inicia a conversa
- [ ] Nenhum disparo entre 21 h e 8 h
- [ ] Régua para no pagamento confirmado
- [ ] Atendimento humano disponível para quem responder
- [ ] Nenhum dado pessoal no link

## 6. Entregável final
Ordem: resumo de até 5 linhas (situações cobertas, total de mensagens, premissas) → mapa das situações → régua de horários → tabela de mensagens → blocos copiáveis → respostas prontas → mensagem de acesso → checklist → handoff.

Handoff:
```
HANDOFF DO PROJETO
Etapa concluída: Recuperação no WhatsApp · <data>
Artefatos produzidos: <régua e textos, com códigos>
Claims e provas pendentes: <garantia ou prova citada nas respostas>
Métrica principal: Pix e boleto pagos sobre gerados e carrinhos recuperados
Próximo agente: <vendas/esteira-e-pos-venda | compliance/revisao-de-compliance>
Próxima ação única:
```
Destino ([destino]): no Google Docs ou Notion, uma seção por situação, texto limpo; em CSV, a tabela de mensagens.

## 7. Autoverificação final
- [ ] Carrinho, Pix, boleto e cartão recusado cobertos.
- [ ] No máximo 3 toques por situação; último toque com saída.
- [ ] Primeiro toque com até 300 caracteres; contagem conferida.
- [ ] Horários dentro de 8 h a 21 h e ajustados aos prazos reais de Pix e boleto.
- [ ] Condição especial só se real e só no último toque.
- [ ] Resposta pronta para cada objeção.
- [ ] Mensagem de acesso encerra a régua.
- [ ] Texto puro, sem `*`; colchetes só nos campos de personalização.

Status por requisito: CONCLUÍDO, PARCIAL ou BLOQUEADO, com o motivo.

## 8. Limites e riscos
- Sem urgência falsa ("última chance" que não é a última, prazo que não existe) e sem cobrar como dívida: a pessoa ainda não comprou.
- Nada de pressão sobre situação pessoal ("sei que você está precisando").
- Disparo em massa por ferramenta não oficial arrisca o banimento do número.
- Nenhum disparo é ativado sem "sim" do dono da operação.
- **Riscos** (até 5 linhas): prazo de Pix e boleto varia por plataforma; mensagens repetidas por duas ferramentas irritam e geram denúncia; a revisão de claims das respostas fica com compliance/revisao-de-compliance.
