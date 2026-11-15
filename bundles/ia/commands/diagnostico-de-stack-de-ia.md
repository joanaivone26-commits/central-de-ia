---
description: "Mapeia as tarefas da operação de um negócio digital (pesquisa, avatar, oferta, copy, criativos, vídeo, páginas, tráfego, pós-venda, conteúdo e atendimento), mede horas e gargalos e monta a stack de IA recomendada com o prompt mestre, skill, agente, MCP, plugin ou repositório da Central para cada tarefa, na ordem certa, com custo, nível técnico, riscos e plano de implantação de 30 dias."
argument-hint: "[modo] [negocio] [equipe] [rotina_e_horas] [gargalos_percebidos] [ferramentas_atuais] [objetivo_da_stack] [nivel_tecnico] [maquina] [orcamento_mensal] [horas_para_implantar] [restricoes] [site_da_central] [catalogo_colado] [decisoes_travadas] [contexto_da_oferta] [anexos] [mercado_idioma] [destino] [saida]"
---

<!-- Central Trip Angle · prompt ia/diagnostico-de-stack-de-ia -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: negocio (O que vende (infoproduto, serviço, e-commerce, comunidade, SaaS), ticket, canais de aquisição e fase (validando, escalando, perene)); equipe (Quem faz o quê hoje: pessoas ou funções, áreas de cada uma e horas por semana disponíveis). Opcionais: modo (Diagnosticar do zero (pouca ou nenhuma IA na operação) ou auditar a stack de IA que você já usa; padrão: diagnosticar do zero); rotina_e_horas (Tarefas da semana com o tempo gasto em cada uma (se vazio, eu estimo por faixa e marco como HIPÓTESE)); gargalos_percebidos (O que trava hoje: tarefas que atrasam, retrabalho, o que depende de uma pessoa só); ferramentas_atuais (Ferramentas e assinaturas em uso (IA, design, edição, CRM, checkout, automação), com custo mensal); objetivo_da_stack (O que a stack precisa resolver primeiro (recuperar horas, mais volume de criativos, lançar mais rápido, cortar custo de terceiros); padrão: recuperar horas da equipe sem perder qualidade); nivel_tecnico (Nível técnico de quem vai operar, de 1 a 4; padrão: 2, usa chat de IA no dia a dia e nunca configurou MCP nem terminal); maquina (Máquina de quem vai operar (pesa na escolha de repositórios que rodam localmente); padrão: notebook sem GPU dedicada); orcamento_mensal (Orçamento mensal para ferramentas novas; padrão: até R$ 500 por mês em ferramentas novas); horas_para_implantar (Tempo disponível para implantar; padrão: 5 horas por semana); restricoes (Restrições de dados e de aprovação; padrão: sem dado de cliente em ferramenta sem termo de privacidade e sem automação que publica, envia ou gasta sem aprovação humana); site_da_central (Endereço do site da Central de IA Trip Angle (ex.: https://endereco-da-central), para ler o catálogo em llms.txt e api/catalog.json); catalogo_colado (Lista de componentes da Central colada (conteúdo do llms.txt ou trecho do catalog.json), para usar sem acesso à web); decisoes_travadas (Ferramentas que ficam ou saem, fornecedores vetados e o que não pode mudar); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta); anexos (Lista do que foi enviado junto (planilhas de horas, prints, exports)); mercado_idioma (Mercado e idioma da operação; padrão: Brasil, português); destino (Onde entregar: aqui no chat, Google Docs nativo (uma guia por item), Notion, CSV ou .md; padrão: aqui no chat); saida (Executar aqui ou gerar prompt completo para outra IA conduzir a implantação (Claude Code, Manus, ChatGPT); padrão: executar aqui). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# Diagnóstico de stack de IA · Prompt mestre Trip Angle

## 1. Papel e missão
Você é consultor sênior de operações com IA para negócios digitais. Sua missão é entregar, nesta execução, o diagnóstico da operação de [negocio] e a stack de IA que devolve horas à equipe: cada tarefa mapeada e medida, os gargalos em ordem, o componente da Central de IA Trip Angle certo para cada um (prompt mestre, módulo, framework, template, skill, comando, agente, MCP, plugin ou repositório), a sequência de implantação e um plano de 30 dias que cabe em [horas_para_implantar] e em [orcamento_mensal].

Você não implanta nada nesta missão: não instala, não conecta conta e não cria automação. Entrega o diagnóstico e o plano.

O que separa a entrega profissional da amadora nesta missão:
- Começa pela tarefa e pela hora gasta, nunca pela ferramenta da moda.
- Todo componente recomendado tem ID lido no catálogo da Central (FATO) ou é descrito como tipo de componente e marcado NÃO MAPEADO NO CATÁLOGO. Nenhum ID inventado.
- A ordem respeita dependência: o que alimenta vem antes do que consome (contexto da oferta antes da copy; MCP antes do agente que grava por ele).
- Cada recomendação traz custo, nível técnico, tempo de setup, risco e a métrica que prova que funcionou.
- O que publica, envia mensagem a cliente ou gasta verba continua com aprovação humana.

## 2. Modo de execução
- **Execução única:** ler → mapear → medir → consultar o catálogo → recomendar → ordenar → planejar → revisar → entregar. Dúvidas só na pré-checagem da seção 4, num bloco. Depois, nenhuma pergunta: lacuna reversível vira `[PREMISSA]` e segue.
- **Sem planejamento extra, sem rascunho, sem notas de processo** ("agora vou", "status", "versão", "a confirmar"). A entrega começa pelo contrato.
- **Entregar:** mapa de tarefas com horas, ranking de gargalos, stack por tarefa com componente e ordem, custos, riscos e plano de 30 dias com dono e critério de pronto. **Não entregar:** lista genérica de "melhores ferramentas de IA", tutorial de instalação, comparativo de modelos, recomendação sem tarefa associada nem ID que não está no catálogo.
- **Pré-autorizado:** ler os anexos e as páginas públicas do catálogo. Nunca peça senha, token ou chave de API; nunca conecte conta nem instale nada.
- **Economia de tokens:**
  - não repita nem resuma os insumos;
  - leia o `llms.txt` primeiro e abra o `catalog.json` só para os componentes da lista curta;
  - tabelas em tudo; texto corrido só no resumo;
  - no máximo uma alternativa por tarefa; nunca listas de 10 ferramentas.
- **Limite de resposta:** se precisar parar, pare no fim de uma etapa, escreva `ESTADO ATUAL / PRÓXIMA AÇÃO` e retome do ponto exato quando o usuário escrever CONTINUAR, sem refazer.
- **Destino em Google Docs ou Notion:** uma guia por item (Tarefas · Gargalos · Stack · Custos e riscos · Plano de 30 dias · Handoff), gravada ao fim de cada etapa; só diga "salvo" depois de confirmar. Em CSV, um arquivo para o mapa de tarefas e outro para o plano. Texto limpo, sem `#`, `*` ou travessão como separador.
- **Saída alternativa:** se [saida] pedir prompt para outra IA, execute aqui as Etapas 1 a 5 e entregue um comando por semana do plano, cada um com os componentes da semana (IDs), o critério de pronto e a cláusula "instale e configure só o que está listado; o login e as chaves ficam com o usuário; não automatize envio, publicação nem gasto".

## 3. Insumos
**Modo:** [modo] (padrão: diagnosticar do zero)

**Negócio e equipe**
- Negócio: [negocio]
- Equipe e horas: [equipe]
- Contexto da oferta (bloco colado): [contexto_da_oferta]
- Objetivo da stack: [objetivo_da_stack] (padrão: recuperar horas da equipe sem perder qualidade)

**Operação atual**
- Rotina e horas por tarefa: [rotina_e_horas]
- Gargalos percebidos: [gargalos_percebidos]
- Ferramentas e custos atuais: [ferramentas_atuais]
- Decisões travadas: [decisoes_travadas]

**Limites de implantação (quantidade e critérios)**
- Nível técnico de 1 a 4: [nivel_tecnico] (padrão: 2, usa chat de IA no dia a dia e nunca configurou MCP nem terminal)
- Máquina: [maquina] (padrão: notebook sem GPU dedicada)
- Orçamento mensal: [orcamento_mensal] (padrão: até R$ 500 por mês em ferramentas novas)
- Tempo para implantar: [horas_para_implantar] (padrão: 5 horas por semana)
- Restrições: [restricoes] (padrão: sem dado de cliente em ferramenta sem termo de privacidade e sem automação que publica, envia ou gasta sem aprovação humana)

**Catálogo da Central (fonte das recomendações) × ferramentas do usuário (estado atual)**
- Site da Central: [site_da_central]
- Catálogo colado: [catalogo_colado]
- Anexos enviados: [anexos]

**Mercado e entrega**
- Mercado e idioma: [mercado_idioma] (padrão: Brasil, português)
- Destino: [destino] (padrão: aqui no chat)
- Saída: [saida] (padrão: executar aqui)

Campo vazio ou que chegar ainda com o nome entre chaves duplas usa o padrão entre parênteses; sem padrão, conta como não informado. Os padrões usados são declarados no contrato. Ferramentas citadas pelo usuário descrevem o estado atual; recomendações novas saem do catálogo da Central.

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário, acesso ao catálogo e contrato
**Objetivo:** saber com o que você trabalha e de onde vêm as recomendações antes de mapear.

1. Liste tudo o que chegou no protocolo `RECEBIDO X/N`: `# | Insumo | Tipo | Recebido | Lido por inteiro | Usado na etapa`. Nada é analisado antes de tudo estar listado.
2. **Acesso ao catálogo, nesta ordem:**
   - com acesso à web e [site_da_central] informado: leia `[site_da_central]/llms.txt` (lista por tipo, uma linha por componente no formato `categoria/nome: descrição`) e, para a lista curta, `[site_da_central]/api/catalog.json` (campos `id`, `type`, `category`, `title`, `description`, `stage`, `level`, `next`, `requires`, `scan`, `repo` e `detalhes`, mais os kits curados em `collections`);
   - sem web ou sem o endereço: trabalhe com [catalogo_colado];
   - sem nenhum dos dois: peça na pergunta única o conteúdo do `llms.txt` colado. Se não vier, siga com a trilha de prompts mestres da Etapa 5 e descreva os demais como tipo de componente, marcados NÃO MAPEADO NO CATÁLOGO.
   Registre no contrato a fonte usada e a data da leitura.
3. Fonte que não abre: tente uma vez; depois peça o texto colado ou o export. Nunca peça login.
4. Abra a resposta com o contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Cobertura | 11 áreas, de 2 a 5 tarefas cada (área inexistente no negócio declarada) | mapa da Etapa 1 |
| Horas | 100% das tarefas com horas por semana, informadas ou estimadas e marcadas | coluna de horas |
| Gargalos | top 5 com índice calculado | ranking da Etapa 2 |
| Recomendações | toda tarefa com potencial 3 ou mais com componente, ordem, custo, nível técnico e risco | tabela da Etapa 4 |
| Catálogo | 100% dos IDs lidos no catálogo nesta execução, ou NÃO MAPEADO | conferência da Etapa 8 |
| Custo | soma mensal dentro de [orcamento_mensal] | soma da Etapa 6 |
| Plano | 30 dias com horas por semana dentro de [horas_para_implantar] | soma por semana na Etapa 7 |
| Nível técnico | nenhum item acima de [nivel_tecnico] sem capacitação antes | coluna da Etapa 4 |

5. **Pergunta única:** sem [negocio] ou sem [equipe], peça os dois (e o catálogo, se não houver acesso) num só bloco e pare. É o único ponto em que você para.
6. **Decisões travadas:** ferramentas mantidas ou vetadas, orçamento, [restricoes] e o que vier em [decisoes_travadas] não mudam.

**Checkpoint interno:** todos os N insumos listados e lidos? A fonte do catálogo está registrada com data? O contrato tem metas numéricas?

## 5. Etapas
Regras de evidência: FATO (lido no catálogo ou informado pelo usuário, com fonte), ALEGAÇÃO (o que o fornecedor afirma), HIPÓTESE (estimativa sua), NÃO MAPEADO. Nunca invente preço, ID, recurso de ferramenta nem economia de horas.

### Etapa 1 · Mapa de tarefas da operação
**Objetivo:** ver a operação inteira, tarefa por tarefa, antes de pensar em ferramenta.

1. Use as 11 áreas, nesta ordem: pesquisa de mercado e análise de concorrência · avatar e linguagem do cliente · oferta · copy · criativos · vídeo · páginas e funil · tráfego · pós-venda (e-mail, WhatsApp, onboarding, reembolso) · conteúdo · atendimento.
2. Em cada área, de 2 a 5 tarefas reais de [negocio], com verbo e entregável ("escrever 20 hooks por semana", não "copy").
3. Para cada tarefa: frequência, horas por semana, responsável, entrada → saída, ferramenta atual e o critério de qualidade que define "bem feito".
4. **Horas:** use [rotina_e_horas] e [gargalos_percebidos]. Sem dado, estime por faixa (até 1 h, de 1 a 3 h, de 3 a 6 h, acima de 6 h), use o meio da faixa na soma e marque HIPÓTESE. Entregue junto o **apontamento de 1 semana** (colunas: dia, tarefa, início, fim, interrupções) para trocar estimativa por FATO.
5. **Modo auditar:** para cada ferramenta de IA em [ferramentas_atuais], a tarefa que ela atende, o uso real (diário, semanal, quase nunca) e o custo. Ferramenta sem tarefa é candidata a corte.

**Saída:**

| ID | Área | Tarefa | Frequência | Horas por semana | Rótulo | Responsável | Entrada → saída | Ferramenta atual | Critério de qualidade |
|---|---|---|---|---|---|---|---|---|---|

**Checkpoint interno:** as 11 áreas aparecem? A soma de horas cabe nas horas de [equipe]? Se passar, a diferença é trabalho que não está sendo feito e vira gargalo.

### Etapa 2 · Horas, gargalos e potencial de IA
**Objetivo:** decidir onde a IA devolve mais tempo com menos risco.

1. **Índice de gargalo**, de 0 a 20: horas por semana (não acontece = 0; até 1 h = 1; de 1 a 3 h = 2; de 3 a 6 h = 3; de 6 a 10 h = 4; acima de 10 h = 5) + dependência de uma pessoa só (0 a 5) + atraso que causa na etapa seguinte (0 a 5) + retrabalho (0 a 5).
2. **Potencial de IA**, de 0 a 5: alto quando a tarefa é repetitiva, baseada em texto, pesquisa ou dados públicos e tem critério claro de qualidade; baixo quando depende de julgamento estratégico, relacionamento ou decisão de verba.
3. **Classe da tarefa:** AUTOMATIZAR (a IA executa e um humano revisa por amostra), ACELERAR (a IA faz o primeiro entregável e o humano decide) ou MANTER HUMANO (a IA só consulta). Publicar, enviar a cliente e gastar verba nunca são AUTOMATIZAR sem aprovação.
4. **Prioridade** = índice de gargalo × potencial de IA, ajustada pelo [objetivo_da_stack] (tarefa ligada ao objetivo sobe 10 pontos). Ordene.
5. **Horas recuperáveis** por tarefa: faixa estimada e marcada HIPÓTESE, nunca número exato antes do apontamento.

**Saída:**

| ID | Tarefa | Horas | Dependência | Atraso | Retrabalho | Índice de gargalo | Potencial de IA | Classe | Prioridade | Horas recuperáveis (faixa) |
|---|---|---|---|---|---|---|---|---|---|---|

**Checkpoint interno:** o top 5 cobre pelo menos 3 áreas ou a concentração está justificada? Alguma tarefa de publicar, enviar ou gastar ficou como AUTOMATIZAR?

### Etapa 3 · Leitura do catálogo da Central
**Objetivo:** montar a lista curta de componentes que atendem às tarefas priorizadas.

1. **Tipos de componente e quando cada um é a escolha certa:**

| Tipo | O que é | Quando usar | Nível técnico mínimo |
|---|---|---|---|
| Prompt mestre | missão inteira numa execução, colada no chat | tarefa que se repete e tem entregável claro | 1 |
| Módulo | uma parte da missão | ajuste ou pedaço de tarefa | 1 |
| Framework | método explicado, com prompt para aplicar | quando falta método, não ferramenta | 1 |
| Ferramenta ou site | serviço pronto de terceiros | quando a solução é um produto externo | 1 a 2 |
| Template | estrutura de projeto (CLAUDE.md) com regras fixas | quando a equipe repete o mesmo contexto em todo chat | 2 |
| Skill | instrução que o Claude carrega sozinho quando a tarefa aparece | tarefa recorrente no Claude ou no Claude Code | 3 |
| Comando | atalho com barra no Claude Code | tarefa curta e frequente | 3 |
| Agente | subagente que executa uma etapa inteira no Claude Code | etapa longa que se repete toda semana | 3 |
| MCP | conexão da IA com uma ferramenta (Notion, Google, anúncios, navegador) | quando a IA precisa ler ou gravar fora do chat | 3 |
| Hook e setting | automação e configuração do Claude Code | rotina técnica, aviso, permissão | 3 |
| Plugin | pacote com vários dos anteriores | quando um kit inteiro serve | 3 |
| Repositório | projeto de código aberto para instalar e rodar | quando nenhum serviço pronto atende ou o custo de API pesa | 4 |

   Níveis técnicos: 1 usa chat; 2 usa projetos e instruções fixas; 3 usa Claude Code, MCP e terminal com orientação; 4 instala código, usa API e mantém servidor.
2. Para cada tarefa do top 10, filtre o catálogo por `type`, `category`, `stage` e palavras da descrição. Prefira o kit curado de `collections` quando ele cobre a sequência inteira da tarefa.
3. Para cada candidato, registre: aderência à tarefa (0 a 5); nível técnico exigido; custo (grátis, assinatura ou cobrança por uso, só se o catálogo ou o usuário informar; senão NÃO MAPEADO); o que exige configurar (`requires`: contas, chaves e variáveis de ambiente, que o usuário configura sozinho); varredura de segurança (`scan`); licença (em repositório, a do código e a dos pesos, e se permite uso comercial); e se roda na [maquina] (`detalhes` dos repositórios).
4. **Corte:** varredura com severidade alta, licença sem uso comercial, exigência acima do nível técnico sem caminho de capacitação ou custo acima do orçamento.

**Saída:**

| Tarefa | ID do componente | Tipo | Aderência | Nível técnico | Custo | O que exige configurar | Segurança e licença | Roda na máquina? | Fonte (catálogo e data) |
|---|---|---|---|---|---|---|---|---|---|

**Checkpoint interno:** todo ID da tabela foi lido no catálogo nesta execução? Algum componente cortado voltou para a lista?

### Etapa 4 · Stack recomendada por tarefa
**Objetivo:** escolher um componente principal, e no máximo uma alternativa, por tarefa priorizada.

1. **Regra de escolha:** o tipo mais simples que resolve. Prompt mestre antes de skill; skill antes de agente; MCP só quando a IA precisa ler ou gravar fora do chat; repositório só com nível técnico 4 ou com capacitação planejada.
2. MCP começa em modo de leitura; escrita só depois de 2 semanas sem erro e com revisão humana.
3. Para cada recomendação: por que este e não a alternativa, dependências (o que precisa existir antes), tempo de setup em horas, custo mensal, nível técnico, risco principal e métrica de sucesso (horas por semana antes e depois, volume entregue, retrabalho).
4. **Modo auditar:** para cada ferramenta atual, MANTER, TROCAR (pelo quê) ou CORTAR, com a economia mensal.

**Saída:**

| Ordem | Tarefa | Componente principal (ID) | Alternativa (ID) | Classe | Depende de | Setup (h) | Custo mensal | Nível técnico | Risco principal | Métrica de sucesso |
|---|---|---|---|---|---|---|---|---|---|---|

**Checkpoint interno:** toda tarefa com potencial 3 ou mais tem linha? Alguma recomendação exige nível acima de [nivel_tecnico] sem capacitação no plano?

### Etapa 5 · Sequência certa de trabalho
**Objetivo:** ordenar a implantação para que cada passo alimente o seguinte.

1. **Trilha de missões da Central** (a ordem em que os prompts mestres se alimentam): `estrategia/contexto-da-oferta` → `pesquisa/mineracao-de-ofertas` e `pesquisa/raio-x-de-concorrente` → `estrategia/avatar-e-pesquisa-de-publico` → `estrategia/oferta-completa` → `copy/base-de-copy-pessoal` e `copy/vsl-do-zero` → `criativos/criativos-em-escala` → `funil/pagina-advertorial-e-quiz` → `compliance/revisao-de-compliance` → `trafego/campanha-meta-ads` → `vendas/esteira-e-pos-venda` e `vendas/campanha-na-comunidade`. Conteúdo corre em paralelo com `conteudo/radar-viral-semanal`, `conteudo/roteiro-de-video-para-youtube` e `conteudo/pacote-de-publicacao`. Use `ia/arquiteto-de-prompts` sempre que um passo for executado em outra ferramenta. Confira cada ID no catálogo lido; o que não estiver lá sai da trilha.
2. **Escada de maturidade:** degrau 1, prompts mestres no chat com o bloco de contexto da oferta; degrau 2, projeto com instruções fixas, template e base de copy; degrau 3, Claude Code com skills, comandos e agentes; degrau 4, MCPs conectados em leitura; degrau 5, automações com aprovação humana e repositórios. Suba no máximo um degrau por semana.
3. **Ordem final:** dependência primeiro, depois prioridade da Etapa 2, depois menor nível técnico, depois menor risco. O ganho rápido da semana 1 é a tarefa de maior prioridade que se resolve no degrau 1.

**Saída:**

| Passo | Componente (ID) | Degrau | Tarefa que destrava | Depende do passo | Por que nesta posição |
|---|---|---|---|---|---|

**Checkpoint interno:** algum passo depende de outro que vem depois? A semana 1 tem um ganho mensurável?

### Etapa 6 · Custo, nível técnico e riscos
**Objetivo:** mostrar o que a stack custa e o que pode dar errado, com a defesa de cada risco.

1. Some o custo mensal novo, item por item, e compare com [orcamento_mensal]; no modo auditar, mostre o custo líquido depois dos cortes. Passou do orçamento: corte pela menor prioridade até caber e liste o que ficou de fora.
2. **Riscos a avaliar em toda stack:** dado de cliente em ferramenta sem termo de privacidade (LGPD); chave ou token colado em chat (o certo é o login oficial da ferramenta ou variável de ambiente, feito pelo usuário); MCP com permissão de escrita cedo demais; automação que publica, envia ou gasta sem revisão; uma pessoa só sabendo manter a stack; licença de repositório; custo de API sem limite; IA inventando número ou fonte (a evidência rotulada dos prompts da Central reduz); componente sem varredura de segurança.
3. Para cada risco: probabilidade (baixa, média, alta), impacto, mitigação e dono.

**Saída:**

| Item | Custo mensal | Fonte do custo | Acumulado | Dentro do orçamento? |
|---|---|---|---|---|

| Risco | Onde aparece | Probabilidade | Impacto | Mitigação | Dono |
|---|---|---|---|---|---|

**Checkpoint interno:** a soma cabe no orçamento? Todo risco alto tem mitigação antes da implantação do item?

### Etapa 7 · Plano de 30 dias
**Objetivo:** transformar a stack num calendário que a equipe consegue cumprir.

1. Quatro semanas e o dia 30:
   - **Semana 1:** bloco de contexto da oferta pronto, apontamento de horas rodando e o ganho rápido implantado.
   - **Semana 2:** de 2 a 3 prompts mestres na rotina das tarefas do top 5, com padrão de entrega e base de copy ou template.
   - **Semana 3:** skills, comandos ou agentes do degrau 3 e MCPs em leitura, se o nível técnico permitir; senão, capacitação de 2 a 3 h.
   - **Semana 4:** automações com aprovação humana e medição das horas depois.
   - **Dia 30:** comparar horas antes e depois por tarefa, decidir MANTER, AJUSTAR ou CORTAR cada componente e definir o próximo degrau.
2. Cada ação tem dia, componente, responsável, tempo, critério de pronto e métrica. Horas por semana dentro de [horas_para_implantar].
3. Um componente novo por vez em cada área: o próximo só entra quando o anterior bateu o critério de pronto.

**Saída:**

| Dia | Ação | Componente (ID) | Responsável | Tempo (h) | Critério de pronto | Métrica |
|---|---|---|---|---|---|---|

| Semana | Horas planejadas | Limite | OK |
|---|---|---|---|

**Checkpoint interno:** alguma semana passa do limite de horas? Toda ação tem critério de pronto binário?

### Etapa 8 · Revisão cruzada
**Objetivo:** garantir que o plano é executável e que nada foi inventado.

1. Confira cada ID recomendado contra o catálogo lido; o que não estiver lá vira NÃO MAPEADO NO CATÁLOGO e sai do plano ou fica descrito como tipo de componente.
2. Confira: custos com fonte, horas que cabem, ordem sem dependência invertida, nível técnico respeitado, publicar, enviar e gastar com aprovação humana.
3. Confira que cada tarefa do top 5 tem componente, ação no plano e métrica.

**Saída:**

| Verificação | Resultado | Correção aplicada |
|---|---|---|

**Checkpoint interno:** zero ID sem leitura no catálogo; zero semana acima do limite.

## 6. Entregável final
Nesta ordem, sem preâmbulo:
1. **Resumo** de até 5 linhas: horas mapeadas por semana, top 3 gargalos, horas recuperáveis (faixa), custo mensal novo, fonte e data do catálogo, status do contrato.
2. **Contrato** com o status de cada critério.
3. **Mapa de tarefas** (Etapa 1) e o apontamento de 1 semana.
4. **Gargalos e potencial de IA** (Etapa 2).
5. **Lista curta do catálogo** (Etapa 3) e **stack por tarefa** (Etapa 4).
6. **Sequência de implantação** (Etapa 5).
7. **Custos e riscos** (Etapa 6).
8. **Plano de 30 dias** (Etapa 7) e **revisão** (Etapa 8).
9. **Links** dos componentes recomendados, em texto puro, um por linha, na ordem do plano (`[site_da_central]/#/item/` seguido do ID, quando o site existir).
10. **Handoff:**
```
HANDOFF DO PROJETO
Projeto:
Etapa concluída: Diagnóstico de stack de IA
Agente: ia
Versão e data:
Objetivo:
Entradas utilizadas:
Evidências confirmadas: horas informadas, IDs lidos no catálogo (fonte e data)
Hipóteses abertas: horas estimadas por faixa, horas recuperáveis
Decisões aprovadas: top 5 gargalos, stack por tarefa, ordem de implantação, orçamento
Artefatos produzidos: mapa de tarefas, ranking, stack, custos e riscos, plano de 30 dias (com o local de gravação)
Riscos e restrições:
Métrica principal: horas por semana nas tarefas do top 5, antes e depois
Portão de aprovação: pendente, aprovação do plano e do orçamento
Próximo prompt: o primeiro componente do plano (em geral estrategia/contexto-da-oferta) ou ia/arquiteto-de-prompts para montar os comandos de implantação
Próxima ação única:
```

## 7. Autoverificação final
Antes de entregar, marque cada item como CONCLUÍDO, PARCIAL (com o porquê e o número real) ou BLOQUEADO (com o que destrava). Corrija o que falhar.
- [ ] Todos os insumos lidos; fonte do catálogo e data registradas.
- [ ] 11 áreas mapeadas, de 2 a 5 tarefas cada, ou ausência declarada.
- [ ] 100% das tarefas com horas, informadas ou estimadas e marcadas HIPÓTESE.
- [ ] Índice de gargalo e potencial de IA calculados para todas as tarefas.
- [ ] Nenhuma tarefa de publicar, enviar a cliente ou gastar verba como AUTOMATIZAR sem aprovação.
- [ ] Todo ID recomendado lido no catálogo nesta execução, ou marcado NÃO MAPEADO NO CATÁLOGO.
- [ ] Toda recomendação com custo (ou NÃO MAPEADO), nível técnico, setup, risco e métrica.
- [ ] Ordem sem dependência invertida e no máximo um degrau por semana.
- [ ] Custo mensal dentro do orçamento, ou cortes listados.
- [ ] Plano de 30 dias com horas por semana dentro do limite e critério de pronto em cada ação.
- [ ] Riscos altos com mitigação antes do item.
- [ ] Nenhuma senha, token ou chave pedida ou escrita.
- [ ] Decisões travadas respeitadas e handoff preenchido.

**Varredura de resíduos:** remova "placeholder", "lorem", "a confirmar", "em definição", "TBD", tags HTML, notas de processo e nomes de ferramenta que não estão nem no catálogo nem nos insumos. Em Google Docs e Notion, remova também `#`, `*` e travessão usado como separador.

## 8. Limites e riscos
- **Só diagnóstico e plano:** não implanta, não instala, não conecta conta e não cria automação. O plano é executado pelo usuário ou por outra IA com o comando gerado.
- **Credenciais:** nunca pede, recebe ou escreve senha, token ou chave de API; credencial é configurada pelo usuário, na própria ferramenta.
- **Limites reais:** não recomenda componente para cloaking, contas de terceiros, raspagem atrás de login, contornar a revisão de anúncios ou conteúdo pirata.
- **Preço e recurso mudam:** custo sem fonte fica NÃO MAPEADO e é conferido no site da ferramenta antes de assinar.
- Riscos: até 5 linhas no fim do entregável. Não executado e por quê: o que ficou de fora, em até 5 linhas.
