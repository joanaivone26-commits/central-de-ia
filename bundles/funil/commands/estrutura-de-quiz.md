---
description: "Desenha o quiz completo com 10 a 14 perguntas que mudam o resultado, telas de reforço, captura opcional com consentimento, loading que usa as respostas, resultado por perfil com plano fechado e preço só no fim, mais métricas por tela e a configuração pronta para implementar."
argument-hint: "[oferta] [avatar] [objetivo_do_quiz] [perfis] [para_onde_leva] [perguntas_quiz] [captura] [duracao_do_plano] [saida] [tom] [contexto_da_oferta] [mercado_idioma] [destino]"
---

<!-- Central de IA Trip Angle · prompt funil/estrutura-de-quiz -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: oferta (Produto e oferta final, com planos, preços e o que cada plano entrega); avatar (Avatar por situação, com sinais do problema, tentativas, desejos e objeções). Opcionais: objetivo_do_quiz (Objetivo (segmentar, aquecer, captar lead, levar à VSL ou ao checkout); padrão: segmentar e levar à oferta certa); perfis (Perfis de resultado, se você já tiver); para_onde_leva (Para onde o quiz leva no fim (VSL, página, checkout, WhatsApp); padrão: página de oferta com os planos); perguntas_quiz (Número de perguntas (10 a 14); padrão: 12); captura (Pedir e-mail ou WhatsApp antes do resultado (sim ou não); padrão: sem captura); duracao_do_plano (Duração do plano que o resultado recomenda; padrão: 28 dias); saida (Tabelas e textos, configuração em JSON para o modelo de quiz ou prompt para Lovable; padrão: tabelas e textos); tom (Tom das telas; padrão: acolhedor e direto); contexto_da_oferta (Bloco de contexto gerado pelo prompt estrategia/contexto-da-oferta); mercado_idioma (Mercado e idioma do quiz; padrão: Brasil, português); destino (Onde entregar: aqui, Google Docs nativo, Notion ou .md; padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# Estrutura de quiz · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista de funil. Usa o quiz para a pessoa se enxergar no problema e chegar à oferta convencida de que ela foi feita para o caso dela. Missão: entregar o quiz completo, com toda a copy das telas e a lógica, pronto para implementar.

Profissional × amador:
- Toda pergunta muda o resultado, a recomendação ou a segmentação. Pergunta decorativa sai.
- A primeira pergunta é de 1 toque; o compromisso cresce aos poucos.
- O loading só existe se o resultado usa as respostas, e mostra quais.
- O resultado cita respostas reais da pessoa e recomenda um plano fechado. O preço só aparece no fim.

## 2. Modo de execução
- Execução única: perfis → perguntas → telas → resultados → métricas → configuração. Dúvidas só na pré-checagem, num bloco. Depois, lacuna vira `[PREMISSA]`.
- **Entregar:** todas as telas com texto final, lógica e a configuração em [saida]. **Não entregar:** lista de ideias de perguntas, quiz sem resultado, perguntas sem lógica.
- Não repita os insumos. Tabelas para a lógica, texto final só nas telas.
- Se a resposta acabar, pare no fim de uma etapa com `ESTADO ATUAL / PRÓXIMA AÇÃO` e retome com CONTINUAR.

## 3. Insumos
- Oferta: [oferta]
- Avatar: [avatar]
- Contexto da oferta (bloco colado): [contexto_da_oferta]
- Objetivo do quiz: [objetivo_do_quiz] (padrão: segmentar e levar à oferta certa)
- Perfis já definidos: [perfis]
- Para onde leva no fim: [para_onde_leva] (padrão: página de oferta com os planos)
- Número de perguntas: [perguntas_quiz] (padrão: 12)
- Captura: [captura] (padrão: sem captura)
- Duração do plano: [duracao_do_plano] (padrão: 28 dias)
- Tom: [tom] (padrão: acolhedor e direto)
- Mercado e idioma: [mercado_idioma] (padrão: Brasil, português)
- Formato de saída: [saida] (padrão: tabelas e textos)
- Destino: [destino] (padrão: aqui no chat)

Campo vazio ou que chegar ainda com o nome entre chaves duplas usa o padrão entre parênteses; sem padrão, conta como não informado.

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário
1. `RECEBIDO X/N` dos insumos.
2. Contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Perguntas | [perguntas_quiz] (entre 10 e 14) | contagem |
| Efeito | 100% mudam perfil, plano, texto ou segmentação | coluna "o que muda" sem vazio |
| Perfis | 3 ou 4, todos alcançáveis | simulação de caminhos |
| Preço | só depois do resultado | posição no mapa de telas |
| Captura | conforme [captura], com consentimento | texto da tela |
| Prova | 0 número sem fonte | reforços com fonte ou `[PROVA A INSERIR]` |

3. Se faltar a oferta ou o avatar, pergunte só isso, num bloco, e pare.

## 5. Etapas

### Etapa 1 · Perfis e lógica
1. Defina 3 ou 4 perfis (ou valide [perfis]), nomeados pela situação, nunca por rótulo negativo.
2. Para cada perfil: a situação, as respostas que levam a ele, o plano recomendado e o motivo de a oferta servir.
3. Escolha a lógica: pontuação por perfil (cada opção soma pontos) ou árvore (respostas-chave decidem). Diga como resolve empate.

**Saída:**

| Perfil | Situação | Respostas que levam a ele | Plano recomendado | Por que a oferta serve |
|---|---|---|---|---|

### Etapa 2 · Entrada e perguntas
1. **Tela de entrada:** headline com a promessa do quiz (o que a pessoa descobre), tempo estimado, botão e a primeira escolha de 1 toque.
2. **[perguntas_quiz] perguntas** em blocos: aquecimento → situação e rotina → sinais do problema → tentativas anteriores → desejo → obstáculos e objeções → compromisso.
3. Cada pergunta: texto curto, de 3 a 6 opções, tipo (única ou múltipla), o que muda no resultado e a lógica. Em múltipla, "nenhuma das anteriores" é exclusiva.
4. Unidades conforme [mercado_idioma] (kg ou lb, R$ ou US$).

**Saída:**

| # | Bloco | Pergunta | Opções | Tipo | O que muda no resultado | Lógica (pontos ou salto) |
|---|---|---|---|---|---|---|

### Etapa 3 · Reforços, captura e loading
1. **2 ou 3 telas de reforço** entre blocos: explicação curta do mecanismo, acolhimento ("isso é mais comum do que parece") ou dado com fonte. Sem fonte, troque o dado por explicação ou marque `[PROVA A INSERIR]`.
2. **Captura** (se [captura] for sim): depois de entregar valor e antes do resultado; só os campos que serão usados; consentimento claro e link de privacidade. Não peça dado de saúde, religião ou orientação sem necessidade real.
3. **Loading** de 3 a 5 s, listando as variáveis que de fato entram no resultado ("cruzando sua rotina, seu objetivo e o que você já tentou").

### Etapa 4 · Resultados e ponte para a oferta
1. Um resultado por perfil: título pela situação, diagnóstico em linguagem simples que cita pelo menos 3 respostas da pessoa, o mecanismo em 2 frases e o plano de [duracao_do_plano] com o que acontece em cada fase.
2. Projeção plausível: nada de número de resultado que a oferta não prova. Em saúde, fale de perfil e hábitos, não de doença.
3. Ponte: "o seu plano está pronto" → oferta em [para_onde_leva], com os planos lado a lado, o do meio em destaque quando houver 3, preços exatamente como em [oferta].

**Saída:** um bloco por perfil com título, diagnóstico, plano, ponte e CTA, mais o mapa de telas: `Entrada → Bloco 1 → Reforço → ... → Captura → Loading → Resultado → Oferta`.

### Etapa 5 · Métricas e QA
1. Métricas por tela: taxa de início, avanço por pergunta, conclusão, preenchimento da captura, clique no CTA do resultado.
2. Sinal de problema: queda acima da média numa tela aponta pergunta invasiva, longa ou sem efeito aparente.
3. QA: progresso preservado ao voltar; cada perfil alcançável; resultado coerente com as respostas; mobile de 375 a 430 px com opções de 44 px ou mais.

**Saída:**

| Tela | Métrica | Evento | Sinal de problema |
|---|---|---|---|

### Etapa 6 · Configuração para implementar
Conforme [saida]:
1. **Tabelas e textos:** o que já saiu nas etapas anteriores, organizado por tela.
2. **JSON:** um objeto com entrada, perguntas (texto, tipo, opções e pontos por perfil), reforços, captura, loading, perfis e destino, por exemplo `{"perguntas": [{"id": 1, "texto": "...", "tipo": "unica", "opcoes": [{"texto": "...", "pontos": {"perfil_a": 2}}]}]}`.
3. **Prompt para Lovable:** objetivo, telas em ordem, conteúdo exato, lógica, eventos por tela, UTMs repassadas até o checkout, critérios de aceite do QA, "altere só o quiz; preserve o resto" e "não publique".

## 6. Entregável final
1. Resumo de até 3 linhas: perfis, número de perguntas, destino, status do contrato.
2. Mapa de telas, perfis e lógica (Etapas 1 e 4).
3. Perguntas (Etapa 2) e textos de entrada, reforços, captura e loading (Etapa 3).
4. Resultados por perfil (Etapa 4).
5. Métricas e QA (Etapa 5).
6. Configuração no formato pedido (Etapa 6), num bloco copiável.
7. Handoff:
```
HANDOFF
Etapa concluída: estrutura de quiz
Artefatos: mapa de telas, perguntas e lógica, resultados, configuração
Provas pendentes: lista dos marcadores
Eventos a configurar: início, conclusão, captura, clique no resultado
Próximo prompt: funil/pagina-advertorial-e-quiz (página da oferta e implementação) ou compliance/revisao-de-compliance
Próxima ação única:
```

## 7. Autoverificação final
- [ ] [perguntas_quiz] perguntas, entre 10 e 14.
- [ ] Toda pergunta com "o que muda" preenchido.
- [ ] Primeira pergunta de 1 toque.
- [ ] 3 ou 4 perfis, todos alcançáveis, sem rótulo negativo.
- [ ] Loading só com uso real das respostas.
- [ ] Resultado cita pelo menos 3 respostas e recomenda plano fechado.
- [ ] Preço só depois do resultado, idêntico à oferta.
- [ ] Captura com consentimento e só os dados usados.
- [ ] Nenhum dado sem fonte e nenhuma projeção além do que a oferta prova.
Status por item: CONCLUÍDO, PARCIAL ou BLOQUEADO. Varredura: remova "status", "versão", "a confirmar", "lorem" e notas de processo.

## 8. Limites e riscos
- Sem aviso legal dentro das telas. O consentimento da captura é parte do design. Riscos vão numa seção de até 5 linhas, separada.
- O quiz não faz diagnóstico médico, psicológico, nutricional ou financeiro: fala de perfil, hábitos e situação.
- LGPD: peça só o dado que vai usar e diga para quê.
- O que não puder fazer vai para "Não executado e por quê".
