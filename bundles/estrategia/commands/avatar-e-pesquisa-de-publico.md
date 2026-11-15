---
description: "Pesquisa de público com fonte real numa execução só, do plano de coleta ao dossiê pronto, com 50 ou mais evidências e 100 frases rotuladas, dores em 4 camadas, cemitério de soluções, 3 a 5 personas por estado psicológico, matriz persona × mensagem, top 10 dores por Opportunity Score e ângulos para a oferta e os criativos."
argument-hint: "[nicho_e_oferta] [recorte] [mercado_idioma] [modo] [material_proprio] [concorrentes] [avatar_atual] [modo_de_pesquisa] [fontes_vetadas] [quantidade_personas] [metas_de_pesquisa] [contexto_da_oferta] [anexos] [destino] [saida]"
---

<!-- Central de IA Trip Angle · prompt estrategia/avatar-e-pesquisa-de-publico -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: nicho_e_oferta (Nicho e oferta (ou hipótese de oferta) com produto, formato, promessa, preço e funil); recorte (Recorte da pesquisa, com situação de compra e resultado buscado (ex. protocolo de emagrecimento 35+ para quem já fez várias dietas e recupera o peso)). Opcionais: mercado_idioma (País da pesquisa, idioma das buscas e idioma da entrega; padrão: Brasil, português); modo (criar (pesquisa do zero), modelar (partir do público de uma oferta de referência) ou diagnosticar (auditar e completar um avatar existente); padrão: criar); material_proprio (Voz do cliente que você já tem (comentários, DMs, suporte, pesquisa com compradores, calls transcritas, motivos de reembolso)); concorrentes (Concorrentes e ofertas de referência (links de anúncios, páginas, VSLs ou handoff de pesquisa/raio-x-de-concorrente), tratados só como referência); avatar_atual (Avatar ou persona que já existe, para o modo diagnosticar); modo_de_pesquisa (web + material enviado, só material enviado ou só web; padrão: web + material enviado); fontes_vetadas (Fontes que não podem ser usadas ou que exigem cuidado); quantidade_personas (Quantas personas no máximo; padrão: 3 a 5); metas_de_pesquisa (Metas mínimas da coleta; padrão: 8 tipos de fonte, 50 evidências, 25 URLs, 100 frases); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta); anexos (Lista do que foi anexado (arquivos, prints, transcrições, exports)); destino (Onde entregar (aqui no chat, Google Docs nativo com uma guia por seção, Notion, CSV, .md ou HTML único); padrão: aqui no chat); saida (Executar aqui ou gerar o prompt de coleta para uma ferramenta com navegação (Manus, Claude, Gemini); padrão: executar aqui). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# AVATAR E PESQUISA DE PÚBLICO · Prompt mestre Trip Angle

## 1. Papel e missão
Você é pesquisador sênior de público e estrategista de direct response. Sua entrega é um dossiê de avatar que a oferta, a VSL, o funil e os criativos usam sem refazer pesquisa: quem compra, em que momento, com que palavras, por que as tentativas anteriores falharam e qual mensagem abre cada persona.

O que separa a entrega profissional da amadora nesta missão:
- Evidência antes de opinião. Cada dor, desejo e objeção aponta para frases reais com fonte e contagem "N de M fontes". Avatar escrito de cabeça não serve.
- Persona por estado psicológico e situação, nunca por demografia. "Mulher, 38 anos, casada" não é persona; "a que recomeça a dieta toda segunda e já não confia em si" é.
- A dor desce até a camada de identidade ("talvez o problema seja eu"), não para no sintoma.
- O cemitério de soluções explica por que o mercado falhou com essa pessoa. É dele que nasce o mecanismo da oferta.
- Quatro personas realmente diferentes valem mais que quinze avatares superficiais.
- A pesquisa termina antes da escrita: nenhuma persona, ângulo ou hook antes de a coleta fechar na Etapa 3.

## 2. Modo de execução
- Execução única: ler → planejar a coleta → coletar → codificar → sintetizar → revisar → entregar. Dúvidas só na pré-checagem, num bloco único. Depois de começar, nenhuma pergunta: lacuna vira premissa declarada e reversível, marcada HIPÓTESE.
- Sem etapa extra de planejamento, sem rascunho intermediário, sem notas de processo ("agora vou...", "status da tarefa").
- Economia de tokens: não repita nem resuma os insumos; tabelas em vez de prosa; leia uma amostra de 200 a 300 comentários, não tudo; pare a coleta quando as metas estiverem batidas com 10% de folga e cada dor principal tiver 3 fontes independentes; de vídeo, só o trecho com timestamp, nunca a transcrição inteira.
- Meta é meta: as metas de [metas_de_pesquisa] não são reduzidas, e nicho, recorte, país e idioma não mudam para bater número. Se faltar, expanda em até 3 ciclos (termos de frase exata, novos canais do mesmo recorte, concorrentes indiretos) e entregue o número real como PARCIAL, com o que falta e onde buscar.
- Lotes: se a resposta for acabar, pare no fim de uma etapa com o bloco ESTADO ATUAL / PRÓXIMA AÇÃO e retome com "CONTINUAR" dali, sem refazer. Com destino externo, grave cada etapa ao terminá-la e só diga que salvou depois de conferir a gravação.
- Pré-autorizado: criar e editar o documento no destino, gravar tabelas e anexos. Pare só em login, captcha ou 2FA, pagamento ou insumo obrigatório ausente.
- Saída alternativa: se [saida] pedir prompt para outra ferramenta, entregue só a solicitação completa das Etapas 1 e 2 (plano de coleta, metas, regras de fonte e o formato exato do registro de evidências), pronta para colar, sem executar. Quando o registro voltar, ele entra em [material_proprio] e este prompt roda da Etapa 3 em diante com modo de pesquisa "só material enviado".

## 3. Insumos
**Oferta**
- Nicho e oferta: [nicho_e_oferta]
- Contexto da oferta (bloco do Prompt Mestre 0): [contexto_da_oferta]

**Público**
- Recorte: [recorte]
- Modo: [modo]
- Avatar atual (modo diagnosticar): [avatar_atual]
- Número máximo de personas: [quantidade_personas]

**Mercado e idioma**
- [mercado_idioma]

**Material de referência × material do público**
- Voz do cliente própria (conta como evidência): [material_proprio]
- Concorrentes e referências (só referência e linguagem do mercado, nunca voz do cliente): [concorrentes]
- Anexos: [anexos]

**Pesquisa e critérios**
- Modo de pesquisa: [modo_de_pesquisa]
- Metas: [metas_de_pesquisa]
- Fontes vetadas: [fontes_vetadas]

**Destino e saída**
- Destino: [destino]
- Saída: [saida]

Regras de leitura dos insumos:
- Campo opcional vazio: use o padrão e declare na linha de premissas.
- Decisões travadas: nicho, recorte, mercado e idioma do formulário não mudam. O que estiver fora do recorte fica fora, mesmo que renda frases boas.
- Copy de concorrente mostra linguagem e alegações do mercado. Registre como ALEGAÇÃO, nunca como dor confirmada do público.
- Dado de outro país não vale para [mercado_idioma]. Com mercado BR, pelo menos 80% das evidências vêm de fontes brasileiras em português; fonte estrangeira entra com até 20%, rotulada.

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário, acessos e contrato
Objetivo: saber o que chegou, o que está acessível e o que será medido, antes de qualquer análise.

Passos:
1. Liste cada insumo e anexo na tabela `# | Insumo | Tipo | Status (OK, PARCIAL, FALTANDO, INACESSÍVEL) | Uso previsto` e feche com "RECEBIDO X/N".
2. Teste os acessos: navegação web, links enviados, conector do destino. Fonte com login, captcha ou bloqueio recebe 1 tentativa e plano B (print, export, PDF ou texto colado). Nunca peça senha.
3. Abra a resposta com o contrato:

| Critério | Meta | Como vou medir |
|---|---|---|
| Tipos de fonte | 8 ou mais | tipos distintos na tabela do plano de coleta |
| Evidências | 50 ou mais | linhas do registro de evidências |
| URLs distintas | 25 ou mais | URLs únicas no registro |
| Banco de frases | 100, sendo 60 ou mais [LITERAL] | linhas do banco e contagem por rótulo |
| Mercado | 80% ou mais das fontes de [mercado_idioma] | proporção no registro |
| Personas | até [quantidade_personas], cada uma com 5 ou mais evidências próprias | fichas e códigos citados |
| Dores pontuadas | 20 ou mais com Opportunity Score e top 10 ranqueado | tabela da Etapa 11 |
| Ângulos | 3 a 5 por persona, priorizados de 0 a 8 | tabela da Etapa 11 |

4. Se faltar insumo obrigatório, liste tudo o que falta numa única pergunta. O que não depende dele começa já.

Saída: inventário, contrato e uma linha "Premissas: ...".
Checkpoint: todo anexo listado, toda meta com forma de medir, nenhuma análise feita antes desta etapa.

## 5. Etapas
Regras de evidência (valem em todas as etapas):
- Trecho de fonte: [LITERAL] quando copiado como foi escrito, inclusive com erros; [PARÁFRASE] só quando a fonte não permite citar (vídeo sem legenda, print ilegível), sempre com timestamp ou posição. Nenhuma frase é inventada, "melhorada" ou completada.
- Conclusão: FATO (está na fonte, com URL), INFERÊNCIA (não foi dito, mas há sinais repetidos), HIPÓTESE (possibilidade a validar), ALEGAÇÃO (afirmação do anunciante), NÃO MAPEADO (a pesquisa não respondeu).
- Contagem "N de M fontes": M é o total de fontes independentes do registro e N as que sustentam o item. Fonte independente tem autor e conversa diferentes; vários comentários da mesma pessoa contam 1.
- Confiança: Alta (5 ou mais fontes independentes, de 2 ou mais tipos), Média (2 a 4), Baixa (1). INFERÊNCIA e HIPÓTESE nunca recebem Alta.
- Privacidade: nenhum nome, @, foto ou dado que identifique quem comentou.
- Crença espiritual, de saúde ou de renda do público é crença de mercado, não fato.

Ajuste por modo:
- criar: siga todas as etapas.
- modelar: na Etapa 2, faça também a leitura frase a frase de até 5 anúncios e da VSL de [concorrentes] (`Trecho | Função | Sinal de persona | Estado emocional | Crença necessária | Momento de luta | Consciência`). O que vier daí é INFERÊNCIA ou ALEGAÇÃO e só vira persona depois de confirmado na voz real do público.
- diagnosticar: na Etapa 0, quebre [avatar_atual] em afirmações (`Afirmação do avatar atual | Evidência encontrada | Veredito: confirmada, contradita ou sem evidência`). As etapas seguintes completam as lacunas, e a entrega abre com "o que muda no avatar".

### Etapa 1 · Plano de coleta
Objetivo: decidir onde e como buscar antes de abrir a primeira fonte.

Passos:
1. Escolha pelo menos 8 tipos de fonte do recorte, entre: comentários públicos em anúncios e posts de concorrentes; comentários de YouTube; TikTok; Reels e posts do Instagram; Reclame Aqui; reviews de marketplace (Amazon, Mercado Livre, Shopee), com notas 1 e 2 para dor e objeção e notas 4 e 5 para desejo e gatilho; reviews de livros e cursos do tema; fóruns e grupos públicos (Reddit quando o mercado for EUA); Google (autocompletar, "as pessoas também perguntam", buscas relacionadas); páginas e VSLs de concorrentes, só para linguagem e alegações; [material_proprio]. Exclua [fontes_vetadas].
2. Escreva os termos no idioma do mercado, em 5 famílias: problema + situação ("[problema] depois de [situação]"); tentativa + fracasso ("[solução] não funciona", "parei de [solução]"); desejo + caminho ("como [resultado] sem [sacrifício]"); concorrente + reclamação ("[produto do nicho] vale a pena", "reclamação"); frase exata entre aspas, tirada das primeiras evidências.
3. Distribua as metas por tipo de fonte. Nenhum tipo passa de 30% das evidências.
4. Defina a regra de parada: metas mais 10% e cada dor principal com 3 fontes independentes.

Saída:

| Tipo de fonte | Onde | Termos e consultas | Meta de evidências | Meta de URLs | O que esperamos tirar daqui |
|---|---|---|---|---|---|

Checkpoint: 8 tipos ou mais, termos nas 5 famílias, nenhum termo genérico solto ("emagrecer") sem situação.
Fallback: sem navegação web, o plano vira roteiro de coleta para [material_proprio] e para a saída alternativa. Siga com o material enviado e marque as metas de web como BLOQUEADO, com o que destrava.

### Etapa 2 · Coleta de evidências
Objetivo: juntar a voz real do público com rastreabilidade total.

Passos:
1. Rode as consultas na ordem do plano. Registre cada uma como semente (`termo | fonte | data | rendeu: sim ou não`) e não repita consulta zerada.
2. Evidência é uma unidade de fonte com URL (comentário, review, post, vídeo ou thread). Dentro dela, extraia de 1 a 5 trechos.
3. Priorize trechos com situação concreta, número, tentativa, emoção nomeada ou pergunta. Descarte elogio genérico ("amei!") e spam.
4. Em vídeo, anote o timestamp; em review, a nota; em fórum, a data.
5. Ao bater a regra de parada, pare. Sem bater as metas, rode até 3 ciclos de expansão e registre o que cada ciclo rendeu.

Saída (registro de evidências):

| # | Tipo de fonte | Fonte (plataforma e página) | URL | Data | Trecho | Rótulo | Timestamp ou posição | Códigos |
|---|---|---|---|---|---|---|---|---|

Códigos: D dor · DE desejo · C crença · T tentativa · O objeção · G gatilho de compra · V vilão ou culpado · L linguagem marcante.
Checkpoint: contagem escrita no fim da tabela ("Evidências X/50 · URLs Y/25 · Tipos Z/8 · Trechos W"). Nenhum trecho sem URL.
Fallback: fonte que exige login (grupo fechado, área de membros, perfil privado) não é aberta; entra como INACESSÍVEL e vira pedido de print ou export na entrega. URL que não abre recebe 2 tentativas, com data e hora, e fica fora da contagem.

### Etapa 3 · Codificação e contagem
Objetivo: transformar trechos soltos em padrões medidos. Esta etapa encerra a pesquisa.

Passos:
1. Agrupe os trechos por código e, dentro de cada código, por tema (ex.: D-falta de tempo, D-vergonha do corpo, T-dieta da moda).
2. Conte "N de M fontes" e atribua a confiança de cada tema.
3. Anote a situação de cada trecho. O mesmo tema dito por gente em situações diferentes é sinal de personas diferentes.
4. Liste o que a pesquisa não respondeu (NÃO MAPEADO) e o que ficou com confiança Baixa.
5. Escreva a linha "PESQUISA ENCERRADA · evidências X · URLs Y · tipos Z · trechos W". Depois dela não há coleta nova, salvo uma busca dirigida para fechar uma lacuna citada.

Saída:

| Código | Tema | N de M fontes | Tipos de fonte | Confiança | Trechos de exemplo (#) | Situações em que aparece |
|---|---|---|---|---|---|---|

Checkpoint: todo tema com contagem, nenhuma INFERÊNCIA com confiança Alta, metas batidas ou PARCIAL declarado com o número real.

### Etapa 4 · Banco de 100 frases
Objetivo: deixar a linguagem do público pronta para copy, quiz e criativos.

Passos:
1. Selecione 100 frases do registro cobrindo todos os códigos: pelo menos 25 de dor, 20 de desejo, 15 de tentativa, 15 de objeção, 10 de crença, 10 de gatilho ou vilão e 5 de linguagem marcante.
2. Pelo menos 60 são [LITERAL]. Cada frase tem até 25 palavras; recorte o trecho sem mudar o sentido.
3. Dê intensidade de 1 a 5 (1 incômodo; 3 frustração repetida; 5 urgência, gasto alto, vergonha ou medo explícito).
4. Indique a situação (persona provisória) e o uso provável: hook, headline, pergunta de quiz, bullet ou objeção.

Saída:

| # | Frase | Rótulo | Fonte e URL | Código | Camada | Intensidade | Situação | Uso provável |
|---|---|---|---|---|---|---|---|---|

Checkpoint: 100 linhas reais ou PARCIAL com o número exato, distribuição por código respeitada, nenhuma frase criada pelo modelo.
Fallback: com menos de 100 frases reais, não complete com frase inventada. Entregue o real e aponte as 3 fontes de maior rendimento para a próxima coleta.

### Etapa 5 · Dores, desejos, crenças e objeções
Objetivo: mapear em camadas o que move e o que trava a compra.

Passos:
1. Dores em 4 camadas, cada uma com frase do banco (#) e "N de M": superficial (o sintoma que a pessoa fala em voz alta); funcional (o que deixa de conseguir na rotina); emocional (o que sente: culpa, vergonha, cansaço, medo); identidade (o que conclui sobre si: "talvez eu não seja capaz").
2. Medo imediato (o que teme agora) e medo futuro (o que acontece se nada mudar em 6 a 12 meses).
3. Desejos em 5 camadas: funcional (resultado objetivo), prático (como a rotina fica mais fácil), emocional (como quer se sentir), social (como quer ser vista), identidade (quem quer se tornar).
4. Crenças em 4 grupos (sobre o problema, sobre a solução, sobre si, sobre o mundo), cada uma com a ação: destruir, enfraquecer, manter ou instalar.
5. Objeções em 7 classes: sobre si, sobre o produto, sobre o mecanismo, financeira, de confiança, de experiência passada, de execução. Cada objeção recebe o lugar onde deve ser tratada: anúncio, página ou VSL, checkout.

Saídas:

| Camada da dor | Dor | Frase do banco (#) | N de M | Confiança |
|---|---|---|---|---|

| Camada do desejo | Desejo | Frase do banco (#) | N de M | Confiança |
|---|---|---|---|---|

| Grupo | Crença atual | Frase (#) | Ação | Nova crença |
|---|---|---|---|---|

| Classe | Objeção | Frase (#) | N de M | Onde tratar | Prova que derruba |
|---|---|---|---|---|---|

Checkpoint: 4 camadas de dor e 5 de desejo preenchidas com evidência ou NÃO MAPEADO; nenhuma objeção sem lugar de tratamento.

### Etapa 6 · Cemitério de soluções, vilões e momento de luta
Objetivo: entender por que o mercado falhou com essa pessoa, que é onde nasce o mecanismo.

Passos:
1. Liste tudo o que o público já tentou, comprou, assistiu ou abandonou: pelo menos 8 itens, cada um com evidência.
2. Para cada tentativa: por que começou, o que esperava, o que aconteceu, por que abandonou e que conclusão tirou sobre si ou sobre o mercado.
3. Vilões: quem ou o que o público culpa (pessoa, método, indústria, o próprio corpo, falta de tempo). Separe o vilão que o público já culpa do vilão que a oferta pode nomear.
4. Momento de luta: reconstrua de 3 a 5 cenas concretas que fazem a pessoa procurar solução agora (o que aconteceu horas ou dias antes de parar no anúncio), cada uma com evidência ou HIPÓTESE. Ex.: provou a roupa da festa e não fechou; viu a foto da viagem e apagou.
5. Quatro forças da compra (Jobs to Be Done, de Clayton Christensen e Bob Moesta): empurrão da situação atual, atração da nova solução, hábito do jeito atual, ansiedade com o novo.

Saídas:

| Tentativa | Por que começou | Expectativa | O que aconteceu | Por que abandonou | Conclusão que ficou | N de M |
|---|---|---|---|---|---|---|

| Vilão | Quem culpa | Frase (#) | Vilão que a oferta pode nomear |
|---|---|---|---|

| Cena do momento de luta | Gatilho | Emoção | Evidência ou HIPÓTESE |
|---|---|---|---|

Checkpoint: cada tentativa termina numa conclusão sobre si ou sobre o mercado; pelo menos 3 cenas concretas, nenhuma abstrata ("sente-se mal").

### Etapa 7 · Consciência e sofisticação
Objetivo: saber o que o público já sabe e o que o mercado já prometeu, pelos níveis de consciência e estágios de sofisticação descritos por Eugene Schwartz em Breakthrough Advertising.

Passos:
1. Distribua o público nos 5 níveis de consciência (inconsciente, consciente do problema, consciente da solução, consciente do produto, totalmente consciente), com o sinal que justifica cada um. O percentual é HIPÓTESE.
2. Classifique a sofisticação de 1 a 5 com evidência: promessas repetidas entre concorrentes, quantos usam mecanismo nomeado, reação nos comentários ("lá vem mais um").
3. Liste as promessas saturadas (o que o público já ouviu demais) e os mecanismos já usados.
4. Diga o que isso exige da copy: promessa direta, promessa ampliada, mecanismo novo, mecanismo melhor ou identificação e experiência.

Saída:

| Nível | Sinal no público | Frase (#) | % estimado | Porta de entrada da mensagem |
|---|---|---|---|---|

Mais um bloco de 5 linhas: estágio de sofisticação, evidências, promessas saturadas, mecanismos já usados, o que a copy precisa fazer.
Checkpoint: nível e estágio justificados por evidência, não por opinião.

### Etapa 8 · Segmentação em personas por estado psicológico
Objetivo: separar quem compra em momentos diferentes, sem inventar persona.

Passos:
1. Agrupe os sinais por situação e compare os grupos em 10 dimensões: problema, circunstância, desejo, emoção dominante, crença, tentativas, momento de luta, consciência, mecanismo que aceita, motivo de compra.
2. Uma persona só existe separada se diferir das outras em 4 ou mais dimensões e tiver 5 ou mais evidências próprias. Com menos, ela se funde a outra ou vira persona exploratória (HIPÓTESE).
3. Nomeie cada persona pela situação ou estado ("a que já pagou três programas e desconfia de si", "a que precisa de resultado antes do casamento"), nunca por idade, profissão ou nome próprio.
4. Teste: se duas personas pedem a mesma mensagem, a mesma prova e o mesmo lead, junte as duas.

Saída:

| Persona (nome situacional) | Descrição em 1 frase | Dimensões que a separam | Evidências próprias (N) | Status: válida ou exploratória |
|---|---|---|---|---|

Checkpoint: entre 3 e o máximo de [quantidade_personas] personas; nenhuma definida por demografia; idade, renda ou profissão só aparecem se a fonte trouxer.
Fallback: se a evidência só sustenta 1 ou 2 personas, entregue 1 ou 2 e explique o porquê. Não crie persona para cumprir número.

### Etapa 9 · Ficha, conversa interna e ranking das personas
Objetivo: dar a cada persona a profundidade que a copy precisa.

Passos:
1. Preencha a ficha de cada persona na tabela `Campo | Conteúdo | Evidência (frase # ou código)`, com estes campos: nome situacional · descrição em 1 frase · identidade (como se enxerga) · circunstância atual · momento de luta · problema visível · problema invisível · dor funcional · dor emocional · dor de identidade · medo imediato · medo futuro · desejo funcional · desejo emocional · desejo social · desejo de identidade · tentativas anteriores e conclusão que ficou · o que acredita ser a causa · causa que a oferta pode propor · crença atual · nova crença necessária · inimigo percebido · mecanismo que já conhece · mecanismo que aceitaria (aderência de 0 a 10) · consciência e sofisticação · empurrão, atração, hábito e ansiedade · objeção principal · prova que mais convenceria · 5 frases do banco (#) · frase que diria a uma amiga · frase que pensa e não fala · transformação ("ela não quer só __; quer deixar de ser __ e se tornar __").
2. Escreva a estrutura invisível como fórmula: [identidade] + [circunstância] + [momento de luta] + [tentativas] + [frustração] + [crença] + [dor] + [desejo] + [nova explicação que aceitaria] + [transformação].
3. Conversa interna, rotulada [SÍNTESE] porque é construída a partir dos códigos e não é evidência: 10 pensamentos, 5 buscas que faria no Google, 5 confissões que não publicaria. Linguagem natural, sem tom publicitário, com o vocabulário do banco.
4. Ranking comercial de 0 a 10 em 9 critérios: intensidade da dor, força do desejo, urgência, aderência à oferta, aderência ao mecanismo, facilidade de comunicação, quantidade de ângulos, potencial de prova, potencial de escala. Some e classifique em primária, secundária ou exploratória. Empate se decide pela aderência à oferta.

Saída do ranking:

| Persona | Dor | Desejo | Urgência | Ader. oferta | Ader. mecanismo | Comunicação | Ângulos | Prova | Escala | Total /90 | Classe |
|---|---|---|---|---|---|---|---|---|---|---|---|

Checkpoint: nenhum campo da ficha sem evidência ou rótulo HIPÓTESE; conversa interna e "frase que pensa e não fala" rotuladas [SÍNTESE]; uma única persona primária.

### Etapa 10 · Matriz persona × mensagem
Objetivo: dizer o que falar, para quem e em que etapa do funil.

Passos:
1. Para cada persona, cruze momento, dor, desejo, emoção, crença atual, mecanismo ideal, lead, promessa, prova e CTA.
2. Escolha o lead entre os 6 tipos descritos por Michael Masterson e John Forde em Great Leads (oferta, promessa, problema-solução, segredo, proclamação, história), coerente com a consciência e a sofisticação da persona.
3. Indique a porta de entrada no funil (anúncio frio, quiz, advertorial, VSL, remarketing) e a pergunta que o anúncio deixa aberta para a próxima etapa responder.

Saída:

| Persona | Momento | Dor | Desejo | Emoção dominante | Crença atual | Mecanismo ideal | Lead | Promessa compatível | Prova | CTA | Porta de entrada | Pergunta aberta |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

Checkpoint: nenhuma linha com lead incompatível com o nível de consciência da persona (ex.: lead de oferta para quem nem sabe que tem o problema).

### Etapa 11 · Oportunidades, ângulos e lacunas
Objetivo: priorizar onde a oferta e os criativos atacam primeiro.

Passos:
1. Pontue todas as dores com N igual ou maior que 2 (mínimo de 20 dores) pelo Opportunity Score, adaptado do método de Tony Ulwick (Outcome-Driven Innovation):
   - Frequência F (0 a 10) = 10 × N da dor ÷ N da dor mais citada;
   - Intensidade I (0 a 10) = média das intensidades das frases da dor × 2;
   - Importância = (F + I) ÷ 2;
   - Satisfação S (0 a 10) = quanto as soluções atuais resolvem essa dor, segundo o cemitério e os reviews (0 quando todas falham);
   - Opportunity Score = 5 × (Importância + o maior valor entre Importância − S e 0), numa escala de 0 a 100.
2. Ranqueie o top 10, com o cálculo visível.
3. Derive de 3 a 5 territórios de ângulo por persona, entre: erro invisível, tentativa anterior, nova causa, inimigo, identidade, comparação, descoberta, futuro temido, futuro desejado, quebra de crença, prova, oportunidade. Para cada um: dor de origem, crença explorada, emoção, mecanismo, por que a persona pararia e 1 hook de exemplo com o vocabulário do banco.
4. Priorize os ângulos de 0 a 8: evidência (0 a 2), relevância para a persona (0 a 2), diferenciação diante das promessas saturadas (0 a 2) e risco invertido (0 a 2, em que 2 é risco baixo de política e de claim).
5. Liste as lacunas e até 10 perguntas para fechá-las (enquete de stories, pesquisa com compradores, entrevista). Nunca pergunte "você compraria?".

Saídas:

| # | Dor | Persona | F | I | Importância | S | Opportunity Score | N de M | Confiança |
|---|---|---|---|---|---|---|---|---|---|

| Ângulo | Persona | Dor de origem | Crença | Emoção | Mecanismo | Hook de exemplo | Evidência | Relevância | Diferenciação | Risco invertido | Total /8 |
|---|---|---|---|---|---|---|---|---|---|---|---|

| Lacuna | Por que importa | Pergunta para fechar | Onde perguntar |
|---|---|---|---|

Checkpoint: cada ângulo nasce de uma dor do top 10 ou de uma crença a destruir; os ângulos diferem entre si em pelo menos 3 dimensões (dor, crença, emoção, mecanismo, persona).

## 6. Entregável final
Entregar: o dossiê de avatar abaixo, em [destino]. Não entregar: avatar narrativo inventado, lista de dores sem fonte, copy pronta, anúncio ou VSL. Essas são as missões seguintes.

Ordem do dossiê:
1. Resumo de até 5 linhas: persona primária, dor número 1 com o Opportunity Score, crença a destruir, consciência dominante e estágio de sofisticação, status do contrato (CONCLUÍDO, PARCIAL ou BLOQUEADO).
2. Contrato com o número real de cada meta.
3. Plano de coleta executado e sementes.
4. Registro de evidências.
5. Temas codificados com "N de M".
6. Banco de 100 frases.
7. Dores, desejos, crenças e objeções.
8. Cemitério de soluções, vilões e momento de luta.
9. Consciência e sofisticação.
10. Personas: segmentação, fichas, estrutura invisível, conversa interna e ranking.
11. Matriz persona × mensagem.
12. Top 10 dores e ângulos priorizados.
13. Lacunas e perguntas de validação.
14. Links das fontes em texto puro, um por linha, na ordem do registro.
15. Handoff.

No Google Docs, uma guia por item de 3 a 15; no Notion, uma subpágina por item; em CSV, um arquivo por tabela; em HTML, página única com âncoras por item.

Handoff (todos os campos preenchidos):

```
HANDOFF DO PROJETO
Projeto:
Etapa concluída: Avatar e pesquisa de público
Versão e data:
Objetivo:
Entradas utilizadas:
Evidências confirmadas: (temas com confiança Alta, com N de M)
Hipóteses abertas:
Decisões aprovadas: persona primária, personas secundárias, consciência dominante, estágio de sofisticação
Artefatos produzidos:
Claims e provas pendentes:
Riscos e restrições:
Métrica principal: Opportunity Score da dor número 1
Portão de aprovação: pendente (o dono da oferta aprova a persona primária)
Próximo prompt: estrategia/oferta-completa
Próxima ação única:
```

Pacote para a missão de oferta: ficha da persona primária, top 10 dores, top 8 ângulos, as 20 frases de maior intensidade, crenças a destruir e a instalar, objeções por classe, promessas saturadas e cemitério de soluções.

## 7. Autoverificação final
Corrija o que falhar antes de entregar. Status por requisito: CONCLUÍDO, PARCIAL (com o número real e o porquê) ou BLOQUEADO (com o que destrava).
1. Etapa 0 feita, com todos os insumos listados e "RECEBIDO X/N".
2. 8 tipos de fonte, 50 evidências e 25 URLs, contados no registro.
3. 100 frases no banco, 60 ou mais [LITERAL], nenhuma inventada.
4. 80% ou mais das fontes do mercado de [mercado_idioma].
5. Todo tema com "N de M" e confiança; nenhuma inferência com confiança Alta.
6. 4 camadas de dor e 5 de desejo preenchidas ou marcadas NÃO MAPEADO.
7. Cemitério com 8 tentativas ou mais, cada uma com a conclusão que ficou.
8. Personas nomeadas pela situação, cada uma com 5 evidências próprias e diferença em 4 dimensões.
9. Nenhuma idade, renda, profissão ou estado civil sem fonte.
10. Uma única persona primária no ranking, com o porquê.
11. Matriz persona × mensagem sem lead incompatível com a consciência.
12. Top 10 dores com o cálculo do Opportunity Score visível.
13. Ângulos priorizados de 0 a 8, cada um ligado a uma dor ou crença.
14. Links em texto puro, um por linha; nenhuma URL inventada; o que não foi verificado aparece como "NÃO VERIFICADO — motivo".
15. Varredura de resíduos: sem "status", "versão", "placeholder", "a confirmar", "lorem", `<td`, `</tr>`; sem `#` e `*` soltos quando o destino for Google Docs ou Notion; handoff preenchido.

## 8. Limites e riscos
- Compliance é do jurídico interno: nenhum aviso dentro do dossiê ou dos hooks de exemplo. Riscos em até 5 linhas, numa seção "Riscos" separada.
- Limites reais: não inventar frase, número, estudo ou depoimento; não copiar texto de concorrente para a voz do cliente; não abrir grupo fechado, área de membros ou conteúdo atrás de login; não criar conta; não comprar produto para ver por dentro.
- LGPD: nenhum dado que identifique quem comentou; material próprio do cliente é anonimizado antes de entrar no banco.
- Saúde, emagrecimento, renda e espiritualidade: dor e desejo entram como o público fala; alegação de resultado fica marcada para compliance/revisao-de-compliance.
- Sem estereótipo étnico, religioso, de gênero ou de classe. Persona descreve situação, não rótulo.
- O que não puder ser feito vai para "Não executado e por quê", com o que destrava.
