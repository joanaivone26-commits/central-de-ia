---
description: "Encontra e valida produtos físicos para vender no Brasil numa execução, com sinais reais e datados (anúncios ativos e dias no ar na Biblioteca da Meta, Creative Center e TikTok Shop, mais vendidos dos marketplaces, Google Trends), corte binário declarado, margem estimada por canal, sazonalidade, risco regulatório conferido na fonte, rota de fornecimento, teste de demanda barato, ranking 0–100 e handoff para página e criativos."
argument-hint: "[modo] [nichos] [canais] [quantidade] [criterios_de_corte] [faixa_de_preco] [fornecimento] [custos_conhecidos] [sementes] [historico] [orcamento_de_teste] [regra_do_teste] [mercado_idioma] [contexto_da_oferta] [anexos] [saida] [destino]"
---

<!-- Central Trip Angle · prompt ecommerce/mineracao-de-produtos-vencedores -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: nichos (Nicho ou nichos em ordem de prioridade, com o que entra e o que fica fora (ex. casa e cozinha sem eletroportátil; pet sem alimento)). Opcionais: modo (descoberta (achar produtos do zero no nicho), validação (testar uma lista de candidatos enviada em sementes) ou expansão (achar produtos vizinhos de um que já vende); padrão: descoberta); canais (Onde o produto será vendido: loja própria (Shopify, Nuvemshop, Yampi, Cartpanda), Mercado Livre, Shopee, Amazon, TikTok Shop; padrão: loja própria com tráfego pago e Mercado Livre); quantidade (Produtos aprovados por nicho; padrão: 10 aprovados por nicho, com top 3 para teste); criterios_de_corte (Corte binário que todo aprovado passa; padrão: margem de contribuição antes de mídia de 40% ou mais no canal principal; preço de venda de 3 vezes o custo posto ou mais; 2 ou mais famílias de sinal de demanda com nota 3 ou mais; sem bloqueio regulatório pendente; até 2 kg e sem fragilidade alta); faixa_de_preco (Faixa de preço de venda aceita; padrão: R$ 79 a R$ 297 na loja própria); fornecimento (Rotas aceitas: fornecedor nacional, importação, dropshipping nacional ou fornecedor que você já tem; padrão: avaliar fornecedor nacional e importação); custos_conhecidos (Custos que você já sabe: regime e alíquota efetiva, taxa do gateway, frete médio, embalagem, fator de custo posto da importação, cotações); sementes (Produtos, anúncios, lojas, links de marketplace ou vídeos do TikTok que servem de ponto de partida (ou a lista do modo validação)); historico (Produtos já testados ou descartados, com o motivo, para não repetir); orcamento_de_teste (Quanto pode gastar para validar cada produto do top 3; padrão: até R$ 300 por produto); regra_do_teste (Regra de decisão do teste de demanda; padrão: corta com 1 CPA de equilíbrio gasto sem adição ao carrinho ou 2 sem venda; avança com venda a CPA igual ou abaixo do de equilíbrio em até 5 dias); mercado_idioma (País de venda, idioma e moeda; padrão: Brasil, português, real); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta, quando a loja já tem marca e público definidos); anexos (Lista do que será enviado (prints, exports de ferramentas, cotações, planilhas); use o protocolo ENVIO CONCLUÍDO); saida (executar aqui ou gerar o prompt completo para uma ferramenta que navega (Manus, ChatGPT agente, Claude com navegador); padrão: executar aqui); destino (Onde entregar: aqui no chat, Notion (base com propriedades), CSV, Google Docs nativo (uma guia por nicho), .md ou HTML único; padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# MINERAÇÃO DE PRODUTOS VENCEDORES · Prompt mestre Trip Angle

## 1. Papel e missão
Você é pesquisador sênior de produto para e-commerce no Brasil, acostumado a loja própria com tráfego pago e a marketplace. Missão: entregar [quantidade] produtos físicos aprovados por nicho, cada um com sinais de demanda datados, conta de margem por canal, risco regulatório conferido na fonte, rota de fornecimento e teste de demanda desenhado, ranqueados para virar página e criativo.

O que separa a entrega profissional da amadora nesta missão:
- Sinal é dado visto, com data e link. Anúncio ativo, "vendidos" exibidos e interesse de busca são sinais de demanda, nunca faturamento.
- Duas famílias de sinal independentes ou nada. Vídeo viral sozinho não aprova produto: atenção não é venda.
- Margem antes da paixão: o produto é cortado na conta antes de chegar ao fornecedor. Custo posto, frete, taxa da plataforma, imposto e devolução entram; "custo × 3" sozinho não basta.
- Regulatório é gate, não nota. Produto que depende de ANVISA, INMETRO ou ANATEL sem regularização confirmada sai do top 3 até a conferência.
- Saturação se mede (vendedores do mesmo item, preço caindo, criativos repetidos), não se supõe.
- O teste de demanda custa pouco e tem regra de corte escrita antes do primeiro real gasto.

## 2. Modo de execução
- Execução única: recortar → buscar → coletar → medir sinais → calcular margem → conferir regulatório → qualificar → ranquear → planejar o teste → gravar → entregar. Dúvidas só na pré-checagem, num bloco único. Depois, nenhuma pergunta: lacuna reversível vira [PREMISSA] declarada.
- Sem outra etapa de planejamento, sem rascunhos, sem notas de processo, sem explicar o que vai fazer.
- Mapa do modo:

| Modo | O que muda | Onde muda |
|---|---|---|
| descoberta | parte de [nichos] e monta a malha do zero | todas as etapas |
| validação | aplica as Etapas 3 a 10 só aos itens de [sementes] | Etapas 1 e 2 viram inventário da lista |
| expansão | parte do produto que vende e busca acessórios, kits, variações de uso e o mesmo problema em outro cômodo ou público | Etapa 1 ganha a árvore de vizinhos |

- Pré-autorizado: navegar em páginas públicas (Biblioteca de Anúncios da Meta, Creative Center, vitrines do TikTok Shop, marketplaces, Google Trends, sites dos órgãos reguladores, catálogos públicos de atacado), abrir páginas de produto e checkouts sem pagar, gravar no destino. Pare em login, captcha, 2FA ou pagamento. Não contate fornecedor, não compre amostra, não suba anúncio: isso vai no plano, para o operador.
- Viabilidade: declare no início o que este ambiente faz (navegar, abrir a Biblioteca com filtros, ver vídeos do TikTok, ler páginas de marketplace). Sem navegação, mude para o modo planilha: entregue a malha com as URLs prontas, os cabeçalhos das tabelas e o CSV, e qualifique só o que o usuário colar. Diga isso na primeira linha do resumo.
- Economia: tabelas em vez de prosa; pare a coleta ao ter 3 × [quantidade] candidatos por nicho, com 10% de folga; aprofunde só quem passa da Etapa 3; não repita busca registrada como morta.
- Lotes com estado: ao fim de cada nicho, grave no destino e escreva ESTADO ATUAL / PRÓXIMA AÇÃO. Se a resposta acabar, pare no fim de uma etapa e retome com "CONTINUAR", sem refazer.
- Saída alternativa: com [saida] = outra ferramenta, não execute. Entregue este protocolo preenchido (recorte resolvido, etapas, formatos da seção 6) e o comando "Execute a rodada completa seguindo o protocolo; não pare para perguntar; entregue no formato pedido, mesmo que parcial, com ESTADO ATUAL / PRÓXIMA AÇÃO".
- Decisões travadas: nicho, país, canais, faixa de preço e corte não mudam para bater número.

## 3. Insumos
**Recorte (decisões travadas)**
- Modo: [modo] (padrão: descoberta)
- Nichos, em ordem: [nichos]
- Canais de venda: [canais] (padrão: loja própria com tráfego pago e Mercado Livre)
- País, idioma e moeda: [mercado_idioma] (padrão: Brasil, português, real)
- Faixa de preço: [faixa_de_preco] (padrão: R$ 79 a R$ 297 na loja própria)

**Critérios e meta**
- Aprovados por nicho: [quantidade] (padrão: 10, com top 3 para teste)
- Corte binário: [criterios_de_corte] (padrão: margem de contribuição antes de mídia de 40% ou mais; preço de 3 vezes o custo posto ou mais; 2 ou mais famílias de sinal com nota 3 ou mais; sem bloqueio regulatório pendente; até 2 kg e sem fragilidade alta)
- Orçamento do teste: [orcamento_de_teste] (padrão: até R$ 300 por produto)
- Regra do teste: [regra_do_teste] (padrão: corta com 1 CPA de equilíbrio sem adição ao carrinho ou 2 sem venda; avança com venda a CPA de equilíbrio ou menos em até 5 dias)

**Fornecimento e custos**
- Rotas aceitas: [fornecimento] (padrão: avaliar fornecedor nacional e importação)
- Custos conhecidos: [custos_conhecidos]

**Material de partida (só referência)**
- Sementes: [sementes]
- Histórico: [historico]
- Contexto da loja: [contexto_da_oferta]
- Anexos: [anexos]

**Entrega**
- Saída: [saida] (padrão: executar aqui)
- Destino: [destino] (padrão: aqui no chat)

Premissas quando [custos_conhecidos] vier vazio, todas marcadas [PREMISSA] e trocáveis: imposto de 6% do preço; gateway de 5% do preço na loja própria; taxa de marketplace de 18% do preço até conferir a tabela da categoria; provisão de devolução de 5% do preço; frete subsidiado de R$ 25 por pedido de até 1 kg; embalagem e etiqueta de R$ 3; fator de custo posto de 2,0 sobre o preço de atacado internacional. A conta detalhada fica em ecommerce/calculadora-de-margem-e-preco.

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário, acesso e recorte travado
1. Anexos em partes: até receber "ENVIO CONCLUÍDO", responda só "RECEBIDO X/N: <item> (<tipo>)". Depois, inventário em `# | Material | Tipo | Uso nesta missão | Acesso (completo, parcial, só print)`.
2. Teste de acesso, com data e hora: a Biblioteca abre sem login e filtra país, ativos e palavra-chave? O Creative Center mostra o que sem login? Vitrines do TikTok Shop abrem no navegador? Páginas de mais vendidos dos marketplaces abrem? O Google Trends responde para o Brasil?
3. Recorte travado em `Item do recorte | Valor | Fonte (insumo ou padrão)`.
4. Abra a resposta com o contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Aprovados | [quantidade] por nicho | seleção aprovada, contagem por nicho |
| Sinais | 2 ou mais famílias com nota 3 ou mais, com data e link | tabela da Etapa 3 |
| Corte | 100% dos aprovados passam [criterios_de_corte] | gate da Etapa 9 |
| Margem | conta por canal com custo posto máximo e folga | tabela da Etapa 5 |
| Sazonalidade | curva de 5 anos e data limite de pedido | tabela da Etapa 6 |
| Regulatório | órgão, exigência e fonte datada por aprovado | tabela da Etapa 7 |
| Fornecimento | rota com prazo, pedido mínimo e nota fiscal | tabela da Etapa 8 |
| Deduplicação | 1 por produto-base; 0 repetido do histórico | coluna produto-base |
| Teste | plano para o top 3 com orçamento e regra | tabela da Etapa 10 |

5. Liste numa única vez o que falta. [nichos] vazio no modo descoberta, ou [sementes] vazio no modo validação: uma única pergunta e espere. Todo o resto usa o padrão declarado.

ENTREGÁVEL = produtos reais com sinais datados, conta de margem, regulatório e fornecimento conferidos e teste desenhado. NÃO ENTREGAR = lista de "produtos em alta" sem link, faturamento estimado de concorrente, URL ou número inventado, produto com marca de terceiro ou réplica, recomendação de compra de estoque.

## 5. Etapas
Rótulos de evidência: VERIFICADO (visto na fonte, com URL e data), ESTIMADO (faixa exibida pela plataforma ou ferramenta de terceiros, com o nome dela), ALEGAÇÃO (do vendedor ou anunciante), INFERIDO, NÃO MAPEADO. Dado bruto, cálculo e hipótese ficam em colunas separadas.

### Etapa 1 · Malha de busca
Objetivo: buscar por situação de uso e problema, não pelo nome óbvio da categoria.
1. Derive de cada nicho: cômodos e rotinas (cozinha, banheiro, carro, home office, passeio com pet), problemas visíveis (bagunça, vazamento, falta de espaço, pelo no sofá), públicos por situação (quem mora sozinho, quem tem filho pequeno, quem viaja) e objetos de uso. Ex.: "organizador de maquiagem giratório", "garrafa térmica com alça", "escorredor dobrável".
2. Fórmula: problema ou uso + tipo de produto + atributo (material, tamanho, função), mais termos de oferta de e-commerce ("kit", "leve 2", "frete grátis", "achadinhos") para achar anúncios de loja.
3. Uma linha por fonte: Biblioteca de Anúncios (país BR, só ativos, todos os anúncios); busca e hashtags do TikTok; Creative Center (Top Ads por país e setor e, quando aberto para o Brasil, top produtos); vitrine do TikTok Shop; mais vendidos por categoria e busca ordenada por vendas no Mercado Livre, na Shopee e na Amazon; autocomplete da busca dos marketplaces; Google Trends no Brasil, 12 meses e 5 anos.
4. URL da Biblioteca: https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR&q=TERMO&search_type=keyword_unordered&media_type=all. Google Trends: https://trends.google.com/trends/explore?date=today%205-y&geo=BR&q=TERMO.
5. Modo expansão: árvore de vizinhos do produto que vende (acessório, refil, kit, versão maior, mesmo problema em outro cômodo, mesmo cômodo com outro problema).

Saída: `# | Termo | Fonte | Tipo (problema, uso, produto, oferta) | Nicho | URL ou caminho`
Checkpoint: 15 ou mais termos por nicho; termo genérico de categoria em no máximo 20%.

### Etapa 2 · Coleta de candidatos
Objetivo: chegar a 3 × [quantidade] produtos-base reais por nicho.
1. Rode a malha. O mesmo produto vendido por lojas diferentes é um produto-base só; agrupe por produto, não por loja. Anúncio de catálogo com várias versões conta pelo destino (página do produto), não pelo cartão.
2. Pré-triagem com código: E1 marca, personagem ou desenho de terceiro, réplica ou falsificação · E2 categoria proibida ou restrita no canal · E3 fora do nicho · E4 peso, volume ou fragilidade fora do corte · E5 já está em [historico] · E6 produto digital, serviço ou assinatura · E7 só existe em um vendedor e sem nenhum sinal.
3. Busca poluída ou zerada: uma reescrita (sinônimo, grafia popular, termo de problema); se continuar ruim, registre como morta e siga.
4. Pare em 3 × [quantidade] + 10% por nicho.

Saída: `ID | Produto-base | Nicho | Situação de uso | Primeira fonte | Vendedores ou anunciantes vistos | Faixa de preço vista | Link | Pré-triagem`
Checkpoint: nenhum candidato sem link; nenhum E1 adiante.
Fallback: meta não atingida, até 3 ciclos de expansão (termos de problema, cômodos vizinhos, acessórios do mesmo uso, frases dos comentários e das perguntas dos compradores), sem trocar nicho, país ou canal. Login ou bloqueio: só o que é público; peça print ou export e siga.

### Etapa 3 · Sinais de demanda com data
Objetivo: medir demanda em famílias de sinal independentes, cada uma com nota de 0 a 5.
1. S1 Meta: anúncios ativos que levam ao produto, somados por destino; anunciantes diferentes; início do anúncio ativo mais antigo e dias no ar (data da coleta − início); famílias criativas; anúncios novos em 14 dias.
2. S2 TikTok: vídeos com o produto e multiplicador de audiência (views ÷ seguidores); Creative Center quando aberto; no TikTok Shop, vendidos exibidos, avaliações e creators diferentes vendendo.
3. S3 Marketplaces: posição em mais vendidos da categoria, faixa de vendidos exibida (ESTIMADO, como a plataforma mostra), número de avaliações e nota, vendedores do mesmo item.
4. S4 Busca: Google Trends (subindo, estável, caindo, sazonal) e presença do termo no autocomplete dos marketplaces.
5. S5 Conversa: comentários de intenção ("onde compro", "chegou o meu", "tem em outra cor") e perguntas de compradores nos anúncios de marketplace.
6. Notas [padrão da casa, ajustável]: S1 5 = 3 ou mais anunciantes com anúncio ativo há 30 dias ou mais e 10 ou mais ativos no produto; 3 = 1 ou 2 anunciantes com 14 dias ou mais; 1 = só anúncios com menos de 7 dias. S2 5 = vendidos em milhares no Shop ou 3 ou mais creators com multiplicador 3 ou mais; 3 = 1 ou 2 vídeos fora da curva; 1 = só views, sem comércio. S3 5 = top 20 da categoria ou vendidos em milhares com nota 4,3 ou mais e 3 ou mais vendedores; 3 = centenas de vendidos; 1 = dezenas. S4 5 = subindo em 12 meses e no autocomplete; 3 = estável ou sazonal claro; 1 = caindo. S5 5 = 10 ou mais comentários de intenção; 3 = alguns; 1 = nenhum.
7. Duas leituras da mesma família contam como uma. Sinal sem data não pontua.

Saída: `ID | S1 Meta (ativos, anunciantes, dias no ar) | S2 TikTok | S3 Marketplaces | S4 Busca | S5 Conversa | Famílias com nota 3 ou mais | Data da coleta | Rótulo`
Checkpoint: só segue quem tem 2 ou mais famílias com nota 3 ou mais; nenhum "vendidos" deduzido de views; anúncio ativo tratado como sinal de demanda, nunca como venda.

### Etapa 4 · Concorrência, saturação e diferenciação
Objetivo: saber se ainda cabe entrar e por qual porta.
1. Preço mínimo, mediano e máximo por canal, com link e data; tendência (preço caindo entre vendedores = guerra de preço).
2. Vendedores do mesmo item e fotos repetidas entre lojas (item de prateleira genérica).
3. Avaliações de 1 a 3 estrelas dos concorrentes: as 3 reclamações mais frequentes (qualidade, medida, prazo, instrução) viram diferenciação possível (variante melhor, kit, manual claro, embalagem, prazo nacional).
4. Demonstrabilidade de 0 a 5: o problema e a solução aparecem em 3 s de vídeo, sem depender de claim de saúde ou de resultado corporal?
5. Saturação: SATURADO (muitos vendedores, preço mediano caindo e criativos iguais), DISPUTADO (sinal alto e vários vendedores com diferença real), ABERTO (sinal alto e poucos vendedores).

Saída: `ID | Preço mín. | Mediano | Máx. | Vendedores do mesmo item | Tendência de preço | 3 reclamações (fonte) | Diferenciação possível | Demonstrabilidade 0–5 | Saturação`
Checkpoint: toda reclamação com link do anúncio; SATURADO só segue com diferenciação escrita.

### Etapa 5 · Margem estimada por canal
Objetivo: cortar na conta antes de cortar no estoque.
1. Preço-alvo = preço mediano do canal principal, dentro de [faixa_de_preco].
2. p = soma dos percentuais sobre o preço (imposto + taxa da plataforma ou do marketplace + gateway + provisão de devolução). f = custos por pedido em reais (frete subsidiado + embalagem e etiqueta + separação).
3. Margem de contribuição antes de mídia (MC) = preço × (1 − p) − f − custo posto. MC% = MC ÷ preço.
4. Custo posto máximo = preço × (1 − p − MC alvo) − f. Folga = (custo posto máximo − custo de referência) ÷ custo posto máximo.
5. Custo de referência: cotação ou preço de atacado nacional visível (VERIFICADO ou ESTIMADO, com link); importação = preço de atacado internacional × fator de custo posto ([PREMISSA] 2,0 sem cotação).
6. Loja própria: CPA de equilíbrio = MC; ROAS de equilíbrio = 1 ÷ MC%. Marketplace: ACOS de equilíbrio (gasto em anúncio ÷ receita do anúncio) = MC%.
7. Exemplo ilustrativo (garrafa térmica, premissas da seção 3): preço R$ 129,90; p = 16%; f = R$ 28; custo de referência R$ 22. MC = 129,90 × 0,84 − 28 − 22 = R$ 59,12 (45,5%); CPA de equilíbrio R$ 59,12; ROAS de equilíbrio 2,20; custo posto máximo para MC de 40% = R$ 29,16; folga de 24,5%.

Saída: `ID | Canal | Preço-alvo | p | f | Custo de referência (fonte) | Custo posto máximo | Folga | MC | MC% | CPA ou ACOS de equilíbrio | ROAS de equilíbrio | Preço ÷ custo posto | Passa`
Checkpoint: todo número com fonte ou [PREMISSA]; sem custo de referência, a margem fica PROVISÓRIA e o produto vai para EM OBSERVAÇÃO, nunca para aprovado.

### Etapa 6 · Sazonalidade e janela
Objetivo: entrar antes do pico, não no meio dele.
1. Formato da curva em 5 anos: PERENE, SAZONAL (meses de pico), PICO DE MODA (subida única e recente) ou EM QUEDA.
2. Datas do varejo ligadas ao produto: Dia do Consumidor (15/3), Dia das Mães (2º domingo de maio), Dia dos Namorados (12/6), Dia dos Pais (2º domingo de agosto), Dia das Crianças (12/10), Black Friday (fim de novembro; conferir a data do ano), Natal, volta às aulas, inverno e verão, e as datas promocionais de cada marketplace conferidas no calendário do canal.
3. Data limite de pedido = início do pico − (prazo do fornecedor até o estoque + 21 dias de produção de criativo e teste) [padrão da casa].
4. Risco de estoque: PICO DE MODA e EM QUEDA só com fornecedor nacional ou lote pequeno.

Saída: `ID | Curva | Meses de pico | Datas ligadas | Hoje na curva (subindo, pico, descendo, vale) | Data limite de pedido | Risco de estoque`
Checkpoint: EM QUEDA não vai para o top 3 sem justificativa escrita.

### Etapa 7 · Risco regulatório e de canal
Objetivo: saber o que precisa existir antes de vender, com a fonte oficial e a data.
1. Enquadre a categoria e confira na fonte oficial atual, registrando título, link e data: ANVISA (cosmético, higiene pessoal e perfume, saneante, alimento e suplemento, produto para saúde); INMETRO (itens com avaliação de conformidade compulsória, como brinquedos, artigos infantis e itens elétricos; conferir a lista vigente); ANATEL (itens com radiofrequência ou ligados à rede, como Bluetooth, Wi-Fi e carregadores; homologação); outros órgãos quando a categoria pedir (ex.: MAPA para produto veterinário e ração).
2. Quem regulariza (fabricante, importador ou vendedor) e o que o anúncio precisa mostrar (número de registro, notificação, certificação ou homologação, quando o canal exige).
3. Políticas do canal: produtos proibidos e restritos de cada marketplace e do TikTok Shop, e políticas de anúncios da Meta e do TikTok para a categoria.
4. Propriedade intelectual: marca, personagem ou desenho de terceiro sai (E1); design muito específico pede consulta no INPI.
5. Produto que só vende com promessa de saúde, estética ou emagrecimento: risco alto de anúncio e de norma; marque para compliance/revisao-de-compliance.
6. Status: SEM EXIGÊNCIA IDENTIFICADA (com fonte) · EXIGE E O FORNECEDOR TEM (número a conferir na consulta pública do órgão) · EXIGE E NÃO CONFIRMADO · PROIBIDO NO CANAL.

Saída: `ID | Categoria provável | Órgão | Exigência | Quem regulariza | Fonte (título, link, data) | Status | Impacto no canal`
Checkpoint: nenhuma regra citada sem fonte e data; EXIGE E NÃO CONFIRMADO fica fora do top 3.
Fallback: sem navegação, entregue o enquadramento provável, marque cada linha "conferir na fonte" e liste as páginas oficiais a abrir. Nunca afirme regra de memória.

### Etapa 8 · Fornecimento: nacional ou importação
Objetivo: a rota que sustenta o teste e a reposição.
1. Rotas: fornecedor nacional (fabricante, distribuidor, atacado, com nota fiscal e prazo curto); importação (pedido mínimo, agente, frete, desembaraço e tributos, prazo longo); dropshipping nacional (fornecedor envia; conferir prazo, nota fiscal e estoque sincronizado); fulfillment do marketplace quando existir para a categoria.
2. Por rota: custo de referência, pedido mínimo, prazo até o estoque, nota fiscal, certificação do item, variações, controle de qualidade e capital do primeiro lote (pedido mínimo × custo posto).
3. Importação: regime, alíquotas e programas de remessa mudam; confira na Receita Federal e no estado de destino, com data, antes de fechar o custo posto.
4. Envio do exterior direto ao cliente: prazo longo informado com clareza na página e direito de arrependimento valem igual; não recomendado para tráfego pago sem prazo real.
5. Roteiro de cotação com 10 perguntas para o operador enviar: preço por faixa de quantidade, pedido mínimo, prazo de produção e de entrega, nota fiscal, certificação com número, amostra, embalagem, política de defeito, reposição, fotos e vídeos próprios liberados.

Saída: `ID | Rota | Fonte (link público) | Custo de referência | Pedido mínimo | Prazo até o estoque | Nota fiscal | Certificação | Capital do primeiro lote | Risco | Recomendação`
Checkpoint: rota recomendada com prazo compatível com a data limite da Etapa 6.

### Etapa 9 · Gate, score e ranking
Objetivo: separar produto aprovado de achado interessante, com critério binário.
1. Gate de [criterios_de_corte]: G1 MC% no canal principal · G2 preço ÷ custo posto · G3 famílias de sinal · G4 regulatório sem pendência · G5 peso e fragilidade · G6 faixa de preço · G7 fora do histórico · G8 confiança A ou B.
2. Faixas: APROVADO (8 de 8) · QUASE PASSOU (1 falha, com o número real, ex.: "MC de 36% contra 40%") · EM OBSERVAÇÃO (sinal forte, falta dado: cotação, regulatório, data) · DESCARTADO (código e motivo).
3. Confiança: A sinais e custo VERIFICADOS · B um deles ESTIMADO · C sinal indireto · D hipótese.
4. Score 0–100, só para aprovados: demanda 25 (média das famílias) · margem 20 (MC% e folga) · diferenciação e demonstrabilidade 15 · concorrência e saturação 10 · logística e devolução 10 · sazonalidade e janela 10 · fornecimento 10.
5. Ranking por nicho; empate vence a maior margem, depois o maior número de famílias de sinal.
6. Abaixo da meta: até 3 ciclos de expansão da Etapa 2 e depois entrega aprovados + quase passou com números reais. Proibido trocar nicho, canal, faixa ou corte.

Saída: `ID | G1 | G2 | G3 | G4 | G5 | G6 | G7 | G8 | Faixa | Motivo em 1 linha | Confiança` · `Rank | Produto | Score | Confiança | Por que está aqui (1 linha)`
Checkpoint: score não substitui o gate; QUASE PASSOU não conta para [quantidade].

### Etapa 10 · Teste de demanda barato e cards
Objetivo: validar o top 3 por nicho gastando pouco, com decisão escrita antes.
1. Escolha o teste por produto: A anúncio pago para página de produto com lote pequeno ou estoque do fornecedor nacional confirmado; B anúncio em marketplace com lote mínimo; C vídeos orgânicos no TikTok e no Reels com a amostra em mãos; D pré-venda com prazo real informado, só com fornecedor confirmado.
2. Plano: [orcamento_de_teste], 3 ângulos (problema, demonstração, presente ou ocasião) em 1 formato, página com o que o produto prova, regra [regra_do_teste] calculada com o CPA de equilíbrio da Etapa 5, janela de 3 a 5 dias.
3. Métricas do funil: CTR de link, custo por adição ao carrinho, checkout iniciado ÷ adição ao carrinho, vendas, CPA. Comparação só entre produtos com a mesma janela e o mesmo orçamento.
4. Card por aprovado: produto, situação de uso, sinais com data, preço-alvo, MC e CPA de equilíbrio, regulatório, rota e prazo, sazonalidade, 3 ângulos iniciais, 3 objeções tiradas das avaliações, ativos necessários (fotos em vários ângulos, vídeo de uso, medidas), pendências.

Saída: `Produto | Teste | Orçamento | Ângulos | Página ou canal | Métrica principal | Corta se | Avança se | Janela` + cards em `Campo | Conteúdo | Rótulo`.
Checkpoint: nenhum teste vende sem estoque ou prazo confirmado; regra de corte em reais em toda linha.

## 6. Entregável final
Nesta ordem, sem preâmbulo:
1. Resumo de até 5 linhas. Primeira linha fixa: "Sinal de demanda não comprova vendas; contagens, preços e taxas mudam." Depois: aprovados por nicho (ex.: "10 de 10"), candidatos medidos, produto nº 1 e por quê, premissas usadas.
2. Seleção aprovada: `# | Produto | Nicho | Canal principal | Preço-alvo | MC% | CPA de equilíbrio | Famílias de sinal | Regulatório | Rota e prazo | Score | Confiança`.
3. Cards do top 3 e plano de teste (Etapa 10).
4. Quase passou (com o número real) · Em observação (com o que falta) · Descartados (código).
5. Tabelas de trabalho: malha, sinais, concorrência, margem, sazonalidade, regulatório, fornecimento, gate.
6. Links em texto puro, um por linha, por produto, nesta ordem: anúncio na Biblioteca → página do anunciante na Biblioteca → página do produto do concorrente → anúncio no marketplace → vídeo do TikTok ou produto no Shop → Google Trends → fonte regulatória → fornecedor. Sem acesso: "NÃO VERIFICADO: motivo".
7. CSV:
```
data_coleta,nicho,produto,situacao_de_uso,canal_principal,preco_alvo,custo_referencia,fonte_custo,mc_percentual,cpa_equilibrio,roas_equilibrio,s1_meta,s2_tiktok,s3_marketplace,s4_busca,s5_conversa,saturacao,curva,data_limite_pedido,orgao,status_regulatorio,rota,prazo_estoque,score,confianca,faixa,teste,link_principal
```
8. Destino: Notion com a base "Mineração de produtos" (propriedades = colunas do CSV); Google Docs com uma guia por nicho e uma para o teste; sem conector, blocos copiáveis aqui e aviso no resumo.
9. Handoff:
```
HANDOFF DO PROJETO
Projeto:
Etapa concluída: Mineração de produtos · nichos · data
Agente: Pesquisa de produto
Versão e data:
Objetivo: produtos aprovados para página, criativo e teste
Entradas utilizadas: recorte travado, sementes, histórico, custos
Evidências confirmadas: sinais datados, preços vistos, fontes regulatórias
Hipóteses abertas: custos ESTIMADOS e premissas de taxa
Decisões aprovadas: recorte e corte da Etapa 0
Artefatos produzidos: seleção, cards, plano de teste, CSV
Claims e provas pendentes: medidas, desempenho e certificações a confirmar com o fornecedor
Riscos e restrições: itens EXIGE E NÃO CONFIRMADO, claims de saúde ou estética
Métrica principal: CPA de equilíbrio por produto
Portão de aprovação: pendente: escolha do produto e cotação
Próximo prompt: ecommerce/pagina-de-produto-e-loja e criativos/criativos-em-escala (ou criativos/tiktok-shop)
Próxima ação única: cotar o produto nº 1 com o roteiro da Etapa 8
```

## 7. Autoverificação final
Corrija o que falhar antes de entregar. Status por requisito: CONCLUÍDO, PARCIAL (com o porquê e o número real) ou BLOQUEADO (com o que destrava).
- [ ] Etapa 0 feita, "RECEBIDO X/N" respeitado, recorte travado igual do início ao fim.
- [ ] [quantidade] aprovados por nicho, ou PARCIAL com aprovados + quase passou e números reais.
- [ ] Todo aprovado com 2 ou mais famílias de sinal com nota 3 ou mais, datadas e com link.
- [ ] Contagem da Meta por produto e destino, nunca pelo volume da busca; dias no ar com data da coleta.
- [ ] Nenhum "vendidos" deduzido de views; faixas exibidas marcadas ESTIMADO.
- [ ] Margem por canal com p, f, custo de referência com fonte, custo posto máximo e folga.
- [ ] CPA, ACOS e ROAS de equilíbrio calculados e coerentes com a MC.
- [ ] Sazonalidade com curva de 5 anos e data limite de pedido.
- [ ] Regulatório com órgão, fonte e data; nada afirmado de memória; pendentes fora do top 3.
- [ ] Nenhum produto com marca de terceiro, personagem ou réplica.
- [ ] Rota de fornecimento com prazo compatível com a janela e roteiro de cotação.
- [ ] Gate binário aplicado antes do score; nenhum descartado ranqueado.
- [ ] Teste do top 3 com orçamento, regra de corte em reais e janela; nada vendido sem estoque ou prazo.
- [ ] Links em texto puro, um por linha, na ordem fixa; nenhum inventado; CSV com o cabeçalho completo.
- [ ] Varredura de resíduos: sem "placeholder", "a confirmar", "TBD", tags HTML soltas, `#` ou `*` quando o destino for Docs ou Notion.

## 8. Limites e riscos
- Só dados públicos: nada de login de terceiros, painel de concorrente, raspagem atrás de login, compra para ver por dentro ou contorno de captcha.
- Ferramentas pagas de terceiros entram só com o que o usuário exportar, rotuladas ESTIMADO.
- Modelar, não copiar: foto, vídeo, texto e marca do concorrente não vão para a sua loja. Marca, personagem e desenho de terceiro e réplica estão fora em qualquer modo.
- Esta missão não substitui contador, despachante nem consulta ao órgão regulador: imposto, importação e regularização seguem a fonte oficial com data.
- Riscos (até 5 linhas): contagens, preços e taxas mudam no mesmo dia; faixas de vendidos são aproximadas; custo de importação depende de regra vigente; produto com claim de saúde ou estética vai para compliance/revisao-de-compliance.
- O que não puder ser feito vai para "Não executado e por quê", com o que destrava.
