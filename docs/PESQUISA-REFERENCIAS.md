# Pesquisa de referências para a Central de IA Trip Angle

Pesquisa feita em 15/11/2026 com busca na web e leitura das páginas (WebSearch e WebFetch). Cada referência traz uma coluna **Verificação**:

- **verificado**: a página foi aberta e lida nesta pesquisa;
- **parcial**: a página abriu, mas o conteúdo útil não carregou;
- **não verificado**: a página não abriu (bloqueio 403/429/504 ou 404). Nesses casos, as informações vêm de fontes secundárias e podem estar desatualizadas.

O Reddit bloqueia o agente de busca: nenhuma thread foi lida, e por isso não há referência do Reddit neste relatório. O Product Hunt foi usado para achar produtos, e duas páginas dele foram abertas.

---

## Resumo

1. O mercado tem três camadas que ainda não se falam: **bibliotecas de prompts** (comunidade e marketplace), **diretórios de componentes para agentes** (skills, plugins, MCPs: Glama indexa 121 mil servidores MCP, Claude Marketplaces lista 23 mil skills) e **ferramentas de inteligência criativa** (swipe file e espionagem de anúncios), que estão ganhando agentes de IA e MCP.
2. Não encontrei quem junte as três camadas para o direct response brasileiro. O que existe em português são packs em PDF na Hotmart, listas de prompts em blogs (gptprompts.ai, Stone) e extensões de Chrome de espionagem (Minera Ads, Swipe Offers Spy). Esse espaço está livre para a Central.
3. Volume não diferencia ninguém: quem tem 100 mil itens também tem lixo e duplicata. O que diferencia os melhores é **curadoria com selo** (Anthropic verified, notas de qualidade do Glama, "Control/Tested" do Swiped), **exemplo de saída junto do prompt**, **contexto do negócio salvo uma vez e reaproveitado** (NjectAI do God of Prompt, arquivo de contexto do marketingskills, Brand IQ do Jasper) e **navegação por tarefa ou etapa**, não por tipo técnico.
4. Os padrões que mais se repetem: rankings por janela de tempo (24h, semana, sempre), coleções e packs, configuração pronta para copiar por cliente, contadores sociais e catálogo legível por agentes (llms.txt, API, MCP).
5. Nas ferramentas de criativos, a taxonomia é a mesma em todas: **formato, gancho, ângulo, persona e mensagem**, com etiquetagem automática por IA (Motion, Swipekit, Atria). Vale adotar esses campos para uma futura "biblioteca de referências" da Central.
6. Há sinais de fragilidade: o MagicBrief fecha em 31/07/2026 (a equipe foi para o Canva), a Smithery foi incorporada à Arcade e desligou o proxy MCP, o PulseMCP pausou cadastros e o FlowGPT virou plataforma de personagens. Isso reforça a escolha da Central por um catálogo em arquivos, portátil e sem dependência de backend.
7. Ao todo foram verificadas **70 referências**: 42 sites e produtos mais 28 vídeos do YouTube. Outras 10 não puderam ser abertas e estão marcadas como "não verificado", e 1 abriu só parcialmente.

---

## Referências por família

Notas de relevância para a Central: 5 = copiar já, 1 = só curiosidade.

### 1. Bibliotecas e marketplaces de prompts

| Nome | URL | O que reúne | Como organiza | UX que vale copiar | Modelo de negócio | Nota | Verificação |
|---|---|---|---|---|---|---|---|
| Prompt library do Claude Code (Anthropic) | https://code.claude.com/docs/en/prompt-library | Prompts para copiar no Claude Code, tirados dos guias oficiais | Tags por tarefa e por função; cada cartão leva à fonte | Bloco expansível **"Why this works"** em cada prompt, que ensina o padrão por trás; seção de padrões (descreva o resultado, dê um jeito de conferir, aponte uma referência, diga o formato) | Grátis (documentação) | 5 | verificado. A antiga biblioteca de prompts da API (`platform.claude.com/.../prompt-library/library`) agora redireciona para "Prompting best practices" |
| prompts.chat (antigo Awesome ChatGPT Prompts) | https://prompts.chat | Prompts de texto, imagem e vídeo, skills, workflows e "bots" | Tipos (Text/Image/Video), tags por tema, Trending, Featured, "Today's Most Upvoted", Latest, páginas de autor | Votos, variáveis em bloco, CLI (`npx prompts.chat`), plugin do Claude Code, servidor MCP, opção de self-hosting (Next.js + Prisma), livro interativo em 17 idiomas | Grátis e open source, com patrocínio no GitHub e oferta para times; cerca de 178 mil estrelas | 5 | verificado (site e repositório) |
| PromptBase | https://promptbase.com | Marketplace de prompts pagos para texto e imagem | Por modelo e categoria | Exemplos de saída na página de venda, encomenda de prompt sob medida, link de indicação do vendedor | Comissão de cerca de 20% nas vendas do marketplace; 0% em vendas por link próprio (fontes secundárias) | 3 | **não verificado** (403) |
| PromptHero | https://prompthero.com | Prompts de imagem e vídeo com o resultado gerado | Abas Featured/Hot/New/Top/Video; filtros por modelo (Midjourney, FLUX, Veo, Sora, Nano Banana...) e categoria | **Cada prompt aparece com a imagem ou vídeo que ele gera**; clicar abre o gerador já preenchido com o prompt (remix) | Planos pagos, afiliados e anúncios | 4 (para criativos) | verificado |
| FlowGPT | https://flowgpt.com | Começou como biblioteca de prompts e virou loja de personagens e bots | Categorias e ranking de criadores | Leaderboard, recompensas para criadores | Freemium | 1 | **não verificado** (403). Fontes secundárias dizem que migrou para chat de personagens |
| God of Prompt | https://www.godofprompt.ai | Cerca de 7.800 prompts em 18 categorias, guias, GPTs prontos e automações n8n | Por categoria (Marketing, Vendas, SEO...), **por público ("para copywriters", "para agências")** e por modelo | Variáveis entre colchetes; **NjectAI**: guarda negócio, público e voz uma vez e preenche os prompts (também via extensão no ChatGPT/Claude/Gemini); gerador de prompts; diretórios de ferramentas, skills e MCPs | Bundle vitalício pago, Starter Pack de US$ 20 e newsletter (100 mil+) como funil | 5 | verificado |
| AIPRM | https://www.aiprm.com | Extensão com biblioteca de prompts da comunidade dentro do ChatGPT, Claude e Gemini | Caminho de categoria (ex.: Copywriting > Improve, SEO > Ideation) | Contadores de visualizações, votos e usos por prompt; prompts privados e de time | Freemium (planos Solo e Team) | 3 | verificado |
| Snack Prompt | https://snackprompt.com | Prompts, imagens, automações e agentes | Seções por tipo, tópicos (incluindo Marketing e Claude Code), itens "Prompt" ou "List" | Ordenar por "Mais usados" e "Mais novos"; filtros por plataforma de agente | Marketplace (menu "Create/Sell") | 2 | verificado |
| OpenAI Academy: Prompt Packs | https://academy.openai.com | Mais de 300 prompts organizados por função e setor (marketing, vendas, RH...) | Por função e caso de uso | Packs por cargo: o pack de marketing cobre planejamento de campanha, pesquisa de concorrente, desenvolvimento criativo e análise | Grátis | 3 | **não verificado** (404 e página só com navegação) |
| Vertex AI Prompt Gallery (Google Cloud) | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/prompt-gallery | Amostras oficiais de prompt e resposta para o Gemini | Por caso de uso: Answer Question, Classify, Code, Extract, Summarize, Transform, Write/Generate | Cada amostra traz **prompt + resposta de exemplo** e abre no console para testar; há amostras de marketing ("Ad copy", "Video Ad script writer") | Grátis (documentação) | 3 | verificado |
| gptprompts.ai: Prompts para marketing (BR) | https://gptprompts.ai/pt-br/prompts-para-marketing | Prompts de marketing em português para o Brasil | 4 blocos: Conteúdo e SEO, Anúncios pagos, E-mail marketing, Estratégia | Campos entre colchetes ([NICHO], [PRODUTO], [PERSONA]); seção "Como usar" com 3 dicas | Conteúdo para atrair público, monetizado com afiliados e anúncios | 3 | verificado |
| KissMySkills (PT) | https://kissmyskills.com/pt/pages/prompts-for-marketers | 10 prompts grátis para marketing e venda avulsa de skills e agentes | Por tarefa; tabela "tarefa → prompt ou ferramenta" | Tabela que liga cada tarefa ao prompt certo | Prompts grátis; skills a US$ 19, biblioteca a US$ 9, bundle a US$ 49 | 3 | verificado |
| Pack 70 Prompts para Marketing Digital (Hotmart) | https://hotmart.com/pt-br/marketplace/produtos/pack-70-prompts-prontos-para-marketing-digital/V100726956C | Pack em português: posts virais, e-mails, roteiros, carrosséis, atendimento | Por tipo de peça | Só como referência do formato vendido no Brasil (lista estática, sem variáveis nem exemplos) | Infoproduto de venda única | 2 | verificado |
| PromptHub | https://www.prompthub.us | Gestão de prompts para times, com biblioteca pública | Projetos, branches e biblioteca da comunidade | **Versionamento estilo git com diff**, **testes em lote comparando modelos**, encadeamento de prompts sem código, variáveis, **fork e estrelas** na biblioteca pública | Freemium com planos para times | 4 | verificado |
| Promptlyb | https://www.producthunt.com/products/promptlyb | Biblioteca de prompts para times | Pastas e tags | Templates com variáveis (nome, tom), histórico de versões com rollback, marketplace da comunidade | Grátis no lançamento | 3 | verificado (página no Product Hunt) |
| Jasper: biblioteca de agentes | https://www.jasper.ai/apps | Mais de 100 agentes de marketing (anúncio de busca, sequência de e-mail, landing page, briefing) | Filtros por função, por etapa de conteúdo (**Awareness/Consideration/Conversion**) e pipeline Plan, Create, Adapt, Activate, Optimize | "Brand IQ": voz da marca, guia de estilo e base de conhecimento aplicados a todos os agentes | SaaS pago (trial) | 4 | verificado |
| multiple.chat (PT) | https://multiple.chat/pt/biblioteca-de-prompts | Mais de 734 prompts em 63 categorias, incluindo copywriting | Por categoria profissional | — | Grátis | 2 | **não verificado** (403) |

### 2. Diretórios de skills, agentes e plugins (Claude Code, Cursor e outros)

| Nome | URL | O que reúne | Como organiza | UX que vale copiar | Modelo de negócio | Nota | Verificação |
|---|---|---|---|---|---|---|---|
| aitmpl.com (Claude Code Templates) | https://aitmpl.com | Mais de 1.990 componentes: skills, agentes, comandos, settings, hooks, MCPs, mods e plugins | Menu por tipo; caminho `categoria/nome` | Busca ⌘K, **Stack Builder** ("+" junta itens para instalar de uma vez), contadores de downloads, **llms.txt e API do catálogo para agentes** | Open source, com patrocinadores, vagas e certificações | 5 (a Central já importa dele) | verificado |
| Claude Marketplaces | https://claudemarketplaces.com | Cerca de 23.400 skills, 8.700 servidores MCP e 3.600 marketplaces | Páginas por tipo e categoria (ex.: Sales & Marketing); "Recently added" e "Popular" | **Ranking por instalações reais**; comando de instalação de uma linha; atualização diária a partir do GitHub com remoção de spam por um editor | Grátis, com patrocínio, anúncios e digest semanal | 4 | verificado |
| skills.sh (Vercel) | https://skills.sh | Leaderboard de skills de agentes (cerca de 1,4 milhão de instalações) | Abas **All Time / Trending (24h) / Hot**; seções Official, **Packs**, tópicos (inclui Marketing) e **Security audits** | `npx skills add <dono/repo>` com suporte a 20 agentes (Claude Code, Cursor, Codex...) | Grátis (CLI open source) | 4 | verificado |
| Marketplace oficial de plugins do Claude | https://claude.com/plugins | 531 plugins para Claude e Claude Code | Filtro "Works with" (Claude ou Claude Code) | **Selo "Anthropic verified"**, instalação com um clique, botão "Submit a plugin" | Grátis | 4 | verificado |
| Build with Claude | https://www.buildwithclaude.com | Plugins, skills, subagentes, comandos, hooks e temas | Por tipo | Seção **"Stories"** (autores contam como usam), página de contribuição, adicionado como marketplace do Claude Code | Open source (MIT) | 3 | verificado |
| Vibe Index | https://vibeindex.ai | Skills, MCPs, plugins, mods, "Picks" (vídeos curtos) e coleções | Rankings por tipo, "Rising", tags populares, coleções | **Status de scan de segurança** por item; skill e MCP próprios para buscar no índice; vídeos curtos de demonstração | Independente (sem modelo claro) | 3 | verificado |
| awesome-claude-code | https://github.com/hesreallyhim/awesome-claude-code | Lista curada de skills, agentes, status lines, ferramentas e plugins | Seções do README **geradas a partir de um CSV** por script | Fonte única em CSV que gera a página (o mesmo princípio do build.py da Central) | Grátis (cerca de 58 mil estrelas) | 3 | verificado |
| marketingskills | https://github.com/coreyhaines31/marketingskills | 53 skills de marketing (copywriting, CRO, ads, ad-creative, offers, pricing, customer-research, competitor-profiling...) | Categorias (Conversão, Conteúdo e copy, SEO, Pago, Medição, Retenção, Estratégia...) | **Skill de fundação com o contexto do produto**, que todas as outras leem antes; 9 formas de instalar | Grátis (MIT, cerca de 60 mil estrelas) | 5 | verificado |
| Knowledge Work Plugins (Anthropic) | https://github.com/anthropics/knowledge-work-plugins | 11 plugins por função, incluindo marketing e vendas | Um plugin por função, cada um com skills, comandos e `.mcp.json` | Estrutura modelo: skills automáticas + comandos explícitos + conectores; tudo em markdown e JSON, sem build | Grátis | 4 | verificado |
| SkillsMP | https://skillsmp.com | Índice de arquivos SKILL.md públicos do GitHub (de 170 mil a 1,6 milhão, conforme a fonte) | Categorias e busca | Busca semântica; páginas de criador | Grátis (comunitário) | 2 | **não verificado** (403) |
| cursor.directory | https://cursor.directory | Regras, MCPs e conteúdo da comunidade do Cursor | Por linguagem e framework | — | Grátis | 2 | **não verificado** (429) |

### 3. Registros de MCP

| Nome | URL | O que reúne | Como organiza | UX que vale copiar | Modelo de negócio | Nota | Verificação |
|---|---|---|---|---|---|---|---|
| mcp.so | https://mcp.so | Cerca de 20.500 servidores MCP (1.447 remotos), 395 clientes, 269 skills e 177 CLIs | Categorias, Featured, **Trending por instalações da semana**, New, rankings, tags e coleções; filtros por categoria, tag, runtime e integração | **Configuração pronta para copiar por cliente** (Claude, Cursor, VS Code, Codex); envio por URL com preenchimento automático e revisão antes de publicar | Grátis, com anúncios e parceiros | 4 | verificado |
| Glama MCP Servers | https://glama.ai/mcp/servers | 121.515 servidores (em 15/11/2026) | Filtros por linguagem, hospedagem (remoto, local, híbrido), capacidades, oficial ou reivindicado; cerca de 30 categorias | **Notas em letra para licença, qualidade e manutenção**; ordenação por uso recente, downloads e estrelas; Inspector para testar | Diretório grátis; gateway, hospedagem e API pagos | 4 | verificado |
| MCP Market | https://mcpmarket.com | 54.513 servidores (atualizado de hora em hora), clientes e skills | Cerca de 20 categorias; Official, Featured, Top, Latest; Top 100 diário | Rankings diários; vitrine "Sell Skills" | Patrocínio, anúncios, afiliados e venda de skills | 3 | verificado |
| Official MCP Registry | https://registry.modelcontextprotocol.io | Registro oficial e aberto de servidores MCP | Busca, filtro "só versões mais recentes", "Recently Updated" | API pública documentada, ambientes de produção e staging | Projeto aberto | 3 | verificado |
| Smithery | https://smithery.ai | Servidores MCP e toolkits (agora parte da Arcade) | Grade de cartões | Endpoints hospedados prontos | Em transição: o proxy MCP e a identidade gerenciada foram desligados em 31/10 | 2 | verificado |
| PulseMCP | https://www.pulsemcp.com | Servidores, clientes, casos de uso e newsletter sobre MCP | Seções por tipo de conteúdo | **"Use Cases"** (o que dá para fazer) ao lado do diretório | Newsletter; cadastros pausados para reestruturação | 2 | verificado |

### 4. Diretórios de ferramentas de IA e hubs "tudo de IA num lugar"

| Nome | URL | O que reúne | Como organiza | UX que vale copiar | Modelo de negócio | Nota | Verificação |
|---|---|---|---|---|---|---|---|
| There's An AI For That (TAAFT) | https://theresanaiforthat.com | Mais de 50 mil ferramentas, **11 mil tarefas e 5 mil cargos mapeados** | Por tarefa, por cargo e por preço; base de empresas, modelos e investimentos | **Busca pela tarefa ("quero fazer X")**; conta grátis salva ferramentas e coleções; servidor MCP do diretório | Listagem paga, patrocínio, anúncio por clique e venda de dados; newsletter com 1,8 milhão de assinantes | 3 | verificado (página "About"; a home deu 403) |
| Futurepedia | https://www.futurepedia.io | Diretório de ferramentas e plataforma de ensino | AI Directory, **Workflows** (playbooks por função), Learn | **"Smart Tool Stacks"** (combinações para um fluxo), questionário de onboarding que monta um plano pessoal, acompanhamento de progresso | Freemium e planos para empresas | 3 | verificado |
| Future Tools | https://futuretools.io | Mais de 4.500 ferramentas e notícias | Categorias; Top 20 por votos dos últimos 30 dias; "Newly Added"; escolhas do editor | Indicador de quantas posições a ferramenta subiu ou caiu desde ontem; newsletter com bônus | Newsletter (250 mil+) e destaques patrocinados | 2 | verificado |
| Toolify | https://www.toolify.ai | De 17 mil a 27 mil ferramentas, loja de GPTs e diretório de extensões | Rankings por visitas mensais, categoria, região e receita | Dados de tráfego por ferramenta | Listagem paga e anúncios | 2 | **não verificado** (403) |
| AI Second Brain Notion Template | https://www.producthunt.com/products/ai-second-brain-notion-template | Template de Notion com dashboard, biblioteca de 100 prompts, projetos, planner e "knowledge vault" | Banco de dados no Notion | Exemplo do formato "AI OS" vendido como template: biblioteca de prompts dentro de um painel de trabalho | Template pago (Gumroad) | 2 | verificado |
| AI Prompt Manager (template de Notion) | https://jackchalkley.com/templates/ai-prompt-manager | Banco de prompts no Notion | Propriedades por categoria e modelo | — | Template | 1 | **não verificado** (429) |

O God of Prompt (família 1) também é o melhor exemplo de comunidade que vende biblioteca: bundle vitalício, newsletter como funil e diretórios de ferramentas, skills e MCPs no mesmo site.

### 5. Ferramentas de marketing com IA para espionagem e criativos

| Nome | URL | O que reúne | Como organiza | UX que vale copiar | Modelo de negócio | Nota | Verificação |
|---|---|---|---|---|---|---|---|
| Foreplay | https://www.foreplay.co | Swipe File, Discovery (mais de 100 milhões de anúncios), Spyder (monitora concorrente), Lens (analytics) e Briefs | Boards e mood boards; filtros avançados | Extensão de Chrome que salva anúncio da Meta, TikTok e LinkedIn; **transcrição automática**; brief modular com storyboard e roteiro; um brief enviado para vários criadores | Assinatura (trial de 7 dias) | 4 | verificado |
| Atria | https://www.tryatria.com | Biblioteca de mais de 100 milhões de anúncios da Meta e TikTok e o agente "Raya" | Boards por conceito, campanha ou cliente | O agente **identifica personas, ganchos e mensagens-chave que performam**, dá nota a cada anúncio, gera briefs; MCP para levar os dados ao Claude e ao ChatGPT | Plano grátis com 1.000 créditos; pago a partir de US$ 129/mês | 4 | verificado |
| Motion | https://motionapp.com | Analytics de criativos para Meta, TikTok, YouTube e LinkedIn | **A IA etiqueta cada criativo por tipo, formato visual, gancho e ângulo**; filtros por convenção de nomes e mais de 200 métricas | Relatórios comparativos de formatos, mensagens e tipo de talento; "momentum" semanal; agentes que revisam anúncio antes de subir | SaaS (trial) | 4 | verificado |
| Swipekit | https://swipekit.app/swipefile | Swipe file de anúncios (Meta, TikTok, LinkedIn) e uploads próprios | **Boards dentro de pastas; tags próprias com editor em massa e gerenciador de tags** | O anúncio continua salvo depois que sai do ar; detecção de gancho e idioma; compartilhar board por link; MCP e API | Assinatura (a partir de cerca de US$ 26/mês, segundo fonte secundária) | 4 | verificado |
| GetHookd | https://www.gethookd.ai | Mais de 22 milhões de anúncios ativos de Facebook e Instagram | Filtros por nicho, formato, tempo rodando e performance | "Clone Ads" (variações a partir de um anúncio vencedor), transcrição e roteiro, alerta quando o concorrente sobe anúncio novo, acesso via Claude e ChatGPT | US$ 29 a US$ 129/mês por créditos | 3 | verificado |
| Swiped.co | https://swiped.co | Swipe file clássico de direct response: mala direta, advertoriais, cartas de vendas | Nichos com contagem, tipo de peça, **status "Control" ou "Tested"**, era (moderna ou clássica), coleções públicas e privadas | **"Swipe Study"**: análise de por que a peça funciona | Newsletter e membros | 4 | verificado |
| TikTok Creative Center (Top Ads) | https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en | Anúncios de alta performance do TikTok | Filtros por região, objetivo, idioma, formato e curtidas; ordenar por For You, Reach ou CTR | Ordenar por CTR | Grátis (oficial) | 4 | verificado |
| Minera Ads (MineraROI) | https://chromewebstore.google.com/detail/minera-ads/bhkmpbjlggghmgknebaonpnbdbljfpcn | Extensão brasileira para minerar ofertas escaladas na Biblioteca de Anúncios | Envia produtos para a plataforma MineraROI | Exemplo do fluxo BR "biblioteca → painel de ofertas" | SaaS brasileiro; cerca de 4 mil usuários | 3 | verificado |
| Swipe Offers Spy | https://chromewebstore.google.com/detail/swipe-offers-spy/ihegoljlcpaeefpdeblkokdgafkcckci | Extensão brasileira para analisar a Biblioteca de Anúncios com **transcrição de vídeo** | Salvar e analisar anúncios | Transcrição direto na Biblioteca | Ferramenta BR; cerca de 1 mil usuários; também mantém um canal no YouTube | 3 | verificado |
| MagicBrief | https://magicbrief.com | Era biblioteca de anúncios com etiquetas e briefs | — | Lição de risco: **fecha em 31/07/2026**; a equipe foi para o Canva e criou o "Canva Grow" | Encerrado | 1 | verificado (aviso de encerramento) |
| Biblioteca de Anúncios da Meta | https://www.facebook.com/ads/library/ | Fonte oficial de anúncios ativos da Meta | País, categoria, plataforma, tipo de mídia, datas | Não mostra métricas de performance, por isso existem as ferramentas de terceiros | Grátis (oficial) | 5 | **não verificado** (403) |
| Google Ads Transparency Center | https://adstransparency.google.com | Anúncios do Google por anunciante ou domínio | Região, formato e data | — | Grátis (oficial) | 3 | **parcial** (só a navegação carregou) |
| Adligator | https://adligator.com/pt | Biblioteca de anúncios do Facebook com ordenação por "em exibição há mais tempo" | Filtros por geo, idioma e dias rodando | Ordenar por tempo rodando, que a Biblioteca da Meta não oferece | Assinatura | 2 | **não verificado** (504) |

---

## Vídeos do YouTube

Títulos e canais conferidos nas páginas dos vídeos (oEmbed e página). Os vídeos não foram assistidos. A linha "o que ensina" se baseia no título e no trecho da descrição que a busca mostrou.

### Biblioteca de prompts e organização

| Vídeo | Canal | Idioma | O que ensina |
|---|---|---|---|
| [Criando um sistema de BIBLIOTECA de PROMPTS IA do ZERO no NOTION - #1](https://www.youtube.com/watch?v=XEhrdeNxVbs) | Pedro Peev | PT | Live que monta do zero, no Notion, um sistema para guardar, organizar e planejar prompts |
| [Create your own AI prompt library](https://www.youtube.com/watch?v=UHUzVw7JRPQ) | JuMo | EN | Tutorial rápido de banco de dados no Notion para deixar prompts prontos para uso |
| [From Chaos to System: How I Organize All My AI Prompts using Notion](https://www.youtube.com/watch?v=8d3uTEvCXAo) | Aynur Science | EN | Sistema de 3 passos que transforma prompts soltos num fluxo de trabalho |
| [Stop Rewriting the Same Prompts: Reusable AI Prompt Templates with Variables](https://www.youtube.com/watch?v=PedyNAG5OcY) | Delos | EN | Prompt escrito uma vez com variáveis e reaproveitado como template |
| [Claude Code: Prompts That Anthropic Teams Use](https://www.youtube.com/watch?v=BgaTxlK4MBg) | AI Coding Daily | EN | Passeio pela prompt library oficial do Claude Code (um comentário critica os prompts por serem genéricos) |

### "AI OS", central de skills e agentes

| Vídeo | Canal | Idioma | O que ensina |
|---|---|---|---|
| [How to Build Your Own AI Operating System. For Hermes, OpenClaw, Claude Code etc](https://www.youtube.com/watch?v=GzMUHyvOyAs) | (canal não exibido) | EN | Sistema em arquivos que dá à IA contexto persistente, skills reaproveitáveis e acesso a ferramentas |
| [Build & Sell Your Own AI OS With Claude Code (Free Full Build)](https://www.youtube.com/watch?v=iuZeXR6bgGc) | Shreyas Raj | EN | Montar e vender um "AI OS" (segundo cérebro que lembra e roda agentes) |
| [Claude Code Skills just Built me an AI Agent Team (2026 Guide)](https://www.youtube.com/watch?v=OdtGN27LchE) | Riley Brown | EN | Usar skills para montar um time de agentes para um negócio |
| [Turn Claude Code and OpenCode into Your Marketing Department (Free Skills)](https://www.youtube.com/watch?v=pUBALmdA33I) | AI Stack Engineer | EN | Coleção open source de skills de marketing instaláveis em agentes de código |
| [Agentes de IA são FIRULA? Mostrei como eu rodo o MARKETING inteiro no Claude Code com SKILLS](https://www.youtube.com/watch?v=5LyNOEOsVcU) | Ratos de IA | PT | Claude Code como sistema operacional do marketing, com skills por tarefa |
| [CRIE AGENTES, SUB AGENTES, SKILLS PASSO A PASSO](https://www.youtube.com/watch?v=dWbbEroOFf4) | Kacio Design | PT | Conceitos e passo a passo de agentes, subagentes e skills num projeto |
| [Agent Skills: o novo padrão da Anthropic que todo dev precisa dominar](https://www.youtube.com/watch?v=WrMGIHg28Y4) | Emilio Heinzmann | PT | Visão geral do padrão aberto de Agent Skills |
| [Claude Skills: O que é e Como Criar a Sua](https://www.youtube.com/watch?v=kxekBXyPEKc) | Matheus Santos | PT | Introdução a skills e criação da primeira |
| [As 18 SKILLS Obrigatórias para você usar no CLAUDE CODE](https://www.youtube.com/watch?v=f_HyJkUsbg0) | NoCode StartUp | PT | Curadoria comentada de skills, bom modelo de "lista curada com contexto" |

### Copy, espionagem e criativos

| Vídeo | Canal | Idioma | O que ensina |
|---|---|---|---|
| [Como Usar a melhor Skill de Copy pra ADS no Claude em menos de 5 minutos (COPY PRO com IA #01)](https://www.youtube.com/watch?v=7IZhb7jlpXo) | (canal não exibido) | PT | Skill que analisa a estrutura psicológica de um anúncio e gera variações |
| [Copywriter + Claude Skills - com Derick Carneiro](https://www.youtube.com/watch?v=JKSUMpOnVaU) | Swipe Offers | PT | Persona, ângulo, formato e mensagem como base de anúncios de resposta direta, usando skills |
| [SKILL no Claude que Cria COPY para SITES e LPs](https://www.youtube.com/watch?v=TOIIQHjMZ_M) | (canal não exibido) | PT | Skill de copy para landing page com briefing automático em blocos |
| [I used Claude Skill to write all my Ad Copy in 2 Minutes](https://www.youtube.com/watch?v=e163vxzqnQU) | Infrasity | EN | Skill de ad copy em uso real |
| [4 Ferramentas GRATUITAS Para Fazer Espionagem de OFERTAS ESCALADAS](https://www.youtube.com/watch?v=zOuJAfobidA) | (canal não exibido) | PT | Ferramentas grátis para achar ofertas escaladas na Biblioteca de Anúncios |
| [Como Analisar Anúncios que DÃO CERTO (e aplicar no seu negócio)](https://www.youtube.com/watch?v=4oOBRYt9hdM) | Grupo DPG | PT | Usar a Biblioteca de Anúncios para analisar a concorrência e extrair padrões |
| [Clone any ad in 6 minutes with AI](https://www.youtube.com/watch?v=IBV6Gu1f78Y) | Matt Clark | EN | Prompt que quebra um anúncio em vídeo num storyboard simplificado para recriar |
| [Meta Ads Library + Claude = Anuncios Ganadores ILIMITADOS](https://www.youtube.com/watch?v=qeScb6xtW88) | Julián Romero, Ecommerce | ES | Fluxo Biblioteca da Meta → Claude para analisar concorrentes e gerar anúncios |
| [Claude Code + Meta Ads Manager = Media Buyer](https://www.youtube.com/watch?v=mfk82SbXgGo) | Benjamín Cordero | ES | Claude Code operando o Gerenciador de Anúncios como gestor de tráfego |
| [How to Install the OFFICIAL META ADS MCP in CLAUDE (Full Tutorial)](https://www.youtube.com/watch?v=m3ozKloLTko) | Porter Metrics | EN | Instalar o MCP oficial da Meta Ads no Claude e ler a conta de anúncios |
| [Criei um Acervo de Prompts GRÁTIS para Vídeos UGC com IA](https://www.youtube.com/watch?v=mnlCkbL4dK8) | Nespol | PT | Acervo de prompts para UGC com IA, um exemplo brasileiro de biblioteca de prompts de criativo |
| [How to Create UNLIMITED Image Ads with AI (Nano Banana 2)](https://www.youtube.com/watch?v=ibzfKRRSHhU) | Alex Cooper | EN | Documento de prompts para anúncios estáticos gerados com Nano Banana 2 |

### Avatar e persona

| Vídeo | Canal | Idioma | O que ensina |
|---|---|---|---|
| [How To Create A Persona For Market Testing Your Niche In AI using ChatGPT](https://www.youtube.com/watch?v=F2CuDSPlIv0) | Ed Dale's AI 30 Day Challenge | EN | "Super prompt" que gera três personas ("market avatar") para testar um nicho |
| [Como criar personas com o ChatGPT](https://www.youtube.com/watch?v=xNEYX6WYt2o) | Betminds | PT | Criação de personas com ChatGPT (o trecho da busca não detalha o método) |

---

## Padrões que se repetem

1. **Dois eixos de navegação: tipo e tarefa.** Os diretórios técnicos navegam por tipo (skill, MCP, plugin). Os que atendem gente de negócio navegam pela tarefa ou pelo cargo: TAAFT tem 11 mil tarefas e 5 mil cargos, God of Prompt tem páginas "para copywriters", a OpenAI organiza packs por função e o Jasper filtra por etapa do funil. A Central já tem os tipos; falta o eixo "etapa do trabalho de DR".
2. **Exemplo de saída ao lado do prompt.** PromptHero (imagem gerada), PromptBase (exemplos na página de venda), Vertex (prompt + resposta) e Swiped.co (Swipe Study) mostram o resultado antes de a pessoa usar. Isso reduz abandono e ensina o padrão.
3. **"Por que funciona" explícito.** A prompt library do Claude Code tem "Why this works" em cada cartão, e o Swiped.co analisa cada peça. Explicar o mecanismo transforma a biblioteca em material de formação.
4. **Contexto salvo uma vez e reaproveitado.** NjectAI (God of Prompt), a skill de fundação do marketingskills e o Brand IQ do Jasper resolvem o mesmo problema: não digitar produto, público e voz em todo prompt.
5. **Rankings por janela de tempo e contadores sociais.** skills.sh (All Time / 24h / Hot), mcp.so (instalações da semana), Future Tools (votos de 30 dias e posição de ontem), AIPRM (visualizações, votos e usos).
6. **Coleções, packs e boards.** skills.sh Packs, coleções do mcp.so e do Vibe Index, boards do Foreplay, Atria e Swipekit, Smart Tool Stacks do Futurepedia. A curadoria vira produto.
7. **Selos de confiança.** "Anthropic verified", "Official" e "Claimed" (Glama), notas em letra de qualidade e manutenção, scan de segurança (Vibe Index, skills.sh), "Control/Tested" (Swiped.co).
8. **Instalação ou uso em um passo, por cliente.** Configuração do mcp.so por cliente (Claude, Cursor, VS Code, Codex), `npx skills add`, comando de uma linha do Claude Marketplaces, remix do PromptHero que abre o gerador preenchido.
9. **Catálogo legível por agentes.** llms.txt e API do aitmpl, MCP do TAAFT, skill e MCP do Vibe Index, MCP do prompts.chat, MCP do Atria, do Swipekit e do GetHookd. O catálogo deixou de ser só para humanos.
10. **Taxonomia de criativos padronizada.** Formato, gancho, ângulo, persona e mensagem aparecem no Motion, na Atria e no Swipekit, quase sempre com etiquetagem automática por IA.
11. **Ingestão automática com moderação.** Claude Marketplaces atualiza do GitHub todo dia com um editor removendo spam; mcp.so preenche o cadastro a partir da URL e revisa antes de publicar. É o mesmo desenho do painel admin da Central.
12. **Modelo de negócio.** Diretórios vivem de patrocínio e destaque pago (TAAFT, Claude Marketplaces, MCP Market); bibliotecas vendem bundle vitalício com newsletter como funil (God of Prompt); ferramentas de criativo cobram assinatura por créditos (Atria, GetHookd).
13. **Fragilidade de plataformas centralizadas.** MagicBrief fechou, Smithery mudou de dono e desligou serviços, PulseMCP pausou cadastros e FlowGPT mudou de foco. Catálogo em arquivos e Git sobrevive a isso.

---

## Top 12 recursos para a Central

Ordenados por valor dividido por esforço. Todos cabem no desenho atual: componentes em arquivos, `build.py` gerando o site estático e `tahub.py` só com a biblioteca padrão do Python.

### 1. Exemplo de saída e "Por que funciona" em cada prompt
Inspiração: PromptHero, Vertex Prompt Gallery, Swiped.co, prompt library do Claude Code.
- **Como fazer:** arquivo irmão `<nome>.exemplo.md`, que nunca é instalado, com as variáveis usadas no exemplo (`example_vars` no frontmatter) e a saída real de um modelo. No corpo do prompt, uma seção opcional `## Por que funciona`.
- **build.py:** lê os dois e põe `example` e `why` no JSON do catálogo.
- **Site:** abas "Prompt | Exemplo | Por que funciona" na página do componente.
- **Esforço:** baixo. **Valor:** muito alto. É o que mais reduz o "não sei se isso serve para mim".

### 2. Perfil da oferta: contexto salvo uma vez e reaproveitado
Inspiração: NjectAI do God of Prompt, contexto de produto do marketingskills, Brand IQ do Jasper.
- **Site:** painel "Meu perfil" com campos padrão (produto, nicho, avatar, promessa, mecanismo, preço, mercado BR ou global, tom). Salva em `localStorage` (com try/catch). Quando um prompt tem variável com o mesmo nome, ou um apelido definido em `hub.config.json` (ex.: `"profileAliases": {"nicho": ["seu_nicho", "nicho_publico"]}`), o campo já vem preenchido.
- **Exportar:** botão "Baixar perfil como .md" gera `oferta.md`. O comando `tahub.py --perfil oferta.md` copia o arquivo para `.claude/` e as skills e agentes leem antes de começar.
- **Esforço:** baixo a médio. **Valor:** muito alto.

### 3. Trilha por etapa do trabalho de DR
Inspiração: pipeline Plan, Create, Adapt, Activate, Optimize do Jasper; tarefas do TAAFT; packs por função da OpenAI.
- **Como fazer:** campos `stage` (lista fechada da taxonomia abaixo) e `order` no frontmatter ou no `.hub.json`.
- **build.py:** valida o valor e gera `api/trilha.json`.
- **Site:** página "Trilha DR" com as 10 etapas em colunas e o filtro "etapa" também no ⌘K.
- **Esforço:** baixo. **Valor:** alto. Dá ao iniciante a ordem do trabalho.

### 4. Kits curados (coleções públicas)
Inspiração: Packs do skills.sh, coleções do mcp.so e do Vibe Index, boards do Swipekit.
- **Como fazer:** `collections/<id>.json` com `title`, `description`, `items: ["prompts/pesquisa/minerar-ofertas", ...]` e `order`.
- **build.py:** valida os caminhos e gera a página `/kit/<id>`.
- **Site:** botão "Adicionar kit ao stack", que reaproveita o stack que já existe.
- **Exemplos:** "Kit Espionagem", "Kit VSL do zero", "Kit Criativos UGC".
- **Esforço:** baixo. **Valor:** alto.

### 5. Selo de maturidade e data do teste
Inspiração: "Control/Tested" do Swiped.co, "Anthropic verified", notas do Glama.
- **Como fazer:** no `.hub.json`, os campos `status: rascunho | testado | controle`, `testedWith: ["claude-opus-5.5", "gpt-5"]` e `testedAt`.
- **build.py:** gera o selo e recusa `controle` sem exemplo de saída.
- **Site:** filtro "só testados".
- **Esforço:** baixo. **Valor:** alto. É a forma de competir com bibliotecas de 7 mil prompts.

### 6. Catálogo legível por agentes: llms.txt, JSON e skill de busca
Inspiração: llms.txt e API do aitmpl, MCP do TAAFT, skill e MCP do Vibe Index, MCP do prompts.chat.
- **build.py:** escreve `dist/llms.txt` (um item por linha com título, descrição e URL do arquivo bruto) e `dist/api/search.json` (índice leve).
- **Skill `central-trip-angle`:** ensina o Claude a buscar no JSON com WebFetch e a instalar com o tahub.
- **Depois, opcional:** servidor MCP mínimo em Python puro (stdio) com `search` e `get`.
- **Esforço:** baixo (llms.txt e skill) a médio (MCP). **Valor:** alto. Os agentes de DR da comunidade passam a usar a Central sozinhos.

### 7. Favoritos, histórico de variáveis e "minha versão"
Inspiração: fork do PromptHub, remix do PromptHero, templates do Promptlyb.
- **Site:** estrela ★ e últimos valores usados por prompt, salvos em `localStorage`.
- **Minha versão:** botão "Editar minha versão" abre o `.md` numa caixa de texto e baixa o arquivo no formato da Central (frontmatter preservado), pronto para importar no admin ou abrir um pull request.
- **Esforço:** baixo. **Valor:** médio a alto.

### 8. Feedback sem backend
Inspiração: votos do AIPRM e do prompts.chat.
- **Site:** botões "Funcionou", "Não funcionou" e "Sugerir melhoria" abrem uma issue no GitHub já preenchida (`/issues/new?template=feedback.yml&title=[prompt] <slug>`). Só o slug vai na URL, nunca dado pessoal.
- **admin.py:** lista as issues abertas por item, usando `gh api` ou a API pública.
- **Esforço:** baixo. **Valor:** médio. Alimenta o selo do item 5.

### 9. Receitas encadeadas (prompt chaining)
Inspiração: chains do PromptHub e pipeline do Jasper.
- **Como fazer:** campo `next: [slug]` no prompt e `components/recipes/<nome>.json` com os passos em ordem e a regra de passagem (ex.: "use a saída do passo 1 como {{dores}} no passo 2").
- **Site:** passo a passo com "copiar este passo" e "copiar receita inteira".
- **CLI:** `tahub.py --recipe espionagem-completa` instala os prompts como comandos e cria um comando que orquestra a sequência.
- **Exemplo:** minerar oferta → mapear funil → extrair copy → avatar → ângulos → hooks → roteiro.
- **Esforço:** médio. **Valor:** alto.

### 10. Novidades, RSS e destaques
Inspiração: "Newly Added" do Future Tools, Trending do skills.sh, "Recently added" do Claude Marketplaces.
- **build.py:** ordena por `addedAt`, cria a seção "Novos na semana" e gera `feed.xml` (RSS 2.0 com `xml.etree`) e `api/novidades.json` para newsletter ou WhatsApp.
- **Destaques:** "Em alta" vem da curadoria manual (`featured`). Contagem de instalações só se um dia houver um ping opcional e anônimo.
- **Esforço:** baixo. **Valor:** médio (retenção da comunidade).

### 11. Biblioteca de referências anotadas (novo tipo `swipes`)
Inspiração: Swipe Study do Swiped.co, boards e tags do Foreplay e do Swipekit, taxonomia do Motion.
- **Formato:** `components/swipes/<cat>/<nome>.md`. Frontmatter com `link` (Biblioteca de Anúncios ou página), `formato`, `gancho`, `angulo`, `consciencia` (1 a 5), `mecanismo`, `nicho`, `mercado`, `dias_rodando`, `anuncios_ativos`, `capturado_em` e `status`. O corpo traz a análise "por que funciona" e uma transcrição curta.
- **Site:** filtros por gancho, ângulo e formato. Botão "Usar como referência" preenche `{{referencia}}` nos prompts de modelagem.
- **Cuidado:** guardar só o link, a análise própria e trechos curtos. Não hospedar vídeo nem imagem de terceiros.
- **Esforço:** médio. **Valor:** muito alto para DR, mas exige curadoria contínua.

### 12. Versões e histórico de mudanças
Inspiração: versionamento git do PromptHub e rollback do Snippets AI e do Promptlyb.
- **Como fazer:** `version` no frontmatter.
- **build.py:** roda `git log --follow --format=...` por arquivo e gera a seção "Histórico" (data, versão, mensagem) com link para o arquivo daquele commit.
- **Esforço:** baixo a médio. **Valor:** médio. Ganha importância quando a comunidade começa a contribuir.

**Extras baratos que não entraram no top 12:**
- Botões "Abrir no Gemini" e "Abrir no Perplexity".
- Campo `risco` (saúde, renda, antes e depois) que adiciona automaticamente um rodapé de compliance aos prompts de copy.
- Página "Para quem" (afiliado, produtor, copywriter, gestor de tráfego, editor), no estilo das páginas "for" do God of Prompt.

---

## Taxonomia sugerida para prompts de mercado digital

### Eixo principal: etapa (`stage`)

A coluna "Categoria atual" indica onde cada etapa se encaixa no `categories.json` que já existe. Assim, a etapa vira um campo novo sem mexer nas pastas.

| `stage` | Rótulo | Categoria atual | Subetapas (`substage`) | Tags sugeridas |
|---|---|---|---|---|
| `pesquisa` | Pesquisa e espionagem | `pesquisa` | mineração de ofertas, análise de funil, análise de anúncio, tendências, mineração de comentários e reviews | `biblioteca-de-anuncios`, `oferta-escalada`, `clones`, `anuncios-ativos`, `funil-concorrente`, `transcricao`, `google-trends`, `review-mining`, `comentarios`, `foruns`, `tiktok-creative-center` |
| `avatar` | Avatar e persona | `pesquisa` | perfil, dores e desejos, objeções, linguagem do cliente, jornada, crenças | `persona`, `dores`, `desejos`, `objecoes`, `linguagem-do-cliente`, `inimigo-comum`, `crencas`, `nivel-de-consciencia`, `sofisticacao` |
| `oferta` | Oferta e posicionamento | `estrategia` | promessa, mecanismo, big idea, stack de valor, preço, garantia, nome | `promessa`, `mecanismo-unico`, `big-idea`, `nome-da-oferta`, `stack-de-valor`, `bonus`, `garantia`, `preco`, `ancoragem`, `escassez`, `modelagem` |
| `copy` | Copy | `copy` | headline, lead, VSL, carta de vendas, advertorial, e-mail, revisão | `headline`, `lead`, `vsl`, `carta-de-vendas`, `advertorial`, `bullets`, `prova`, `fechamento`, `cta`, `revisao-de-copy`, `extracao-de-copy` |
| `criativos` | Criativos | `criativos` | hooks, ângulos, roteiro, storyboard, prompts de imagem e vídeo, variações | `hook`, `angulo`, `ugc`, `estatico`, `video-curto`, `roteiro`, `storyboard`, `prompt-imagem`, `prompt-video`, `variacoes`, `b-roll`, `clonar-anuncio` |
| `formatos` | Formatos de conteúdo | `conteudo` | formato viral, banco de formatos, calendário, reaproveitamento | `formato-viral`, `reels`, `tiktok`, `shorts`, `carrossel`, `pov`, `lista`, `mito-verdade`, `bastidores`, `estudo-de-caso`, `calendario` |
| `funil` | Funil e páginas | `funil` | pré-lander, advertorial, quiz, página de VSL, checkout, bump e upsell, obrigado | `pre-lander`, `quiz`, `pagina-vsl`, `pagina-de-vendas`, `checkout`, `order-bump`, `upsell`, `downsell`, `pagina-obrigado`, `cro` |
| `trafego` | Tráfego | `trafego` | estrutura de campanha, públicos, teste de criativo, leitura de métricas, escala, tracking | `meta-ads`, `google-ads`, `tiktok-ads`, `estrutura-de-campanha`, `publicos`, `teste-de-criativos`, `escala`, `metricas`, `utm`, `pixel-capi` |
| `pos-venda` | Pós-venda e backend | `vendas` / `email-whatsapp` | onboarding, recuperação, Pix e boleto, reembolso, ascensão, retenção | `onboarding`, `recuperacao-carrinho`, `pix-boleto`, `reducao-reembolso`, `ascensao`, `whatsapp`, `email`, `upsell-pos-compra`, `depoimentos` |
| `compliance` | Compliance | `compliance` | políticas de anúncio, claims, LGPD, versão segura | `politicas-meta`, `cdc`, `conar`, `anvisa`, `lgpd`, `claims`, `disclaimer`, `versao-segura`, `antes-depois` |

### Eixos secundários (facetas para filtro e ⌘K)

| Campo | Valores sugeridos | Para que serve |
|---|---|---|
| `canal` | meta, instagram, facebook, tiktok, youtube, google, whatsapp, email, telegram | Filtrar pelo lugar onde a peça vai rodar |
| `formato` | vsl, advertorial, quiz, ugc, estatico, carrossel, reels, live, webinar, carta | Cruzar com criativos e funil |
| `consciencia` | 1-inconsciente, 2-consciente-do-problema, 3-consciente-da-solucao, 4-consciente-do-produto, 5-totalmente-consciente | Liga o prompt ao framework de níveis de consciência que já existe |
| `sofisticacao` | 1 a 5 | Estágio de sofisticação do mercado |
| `nicho` | saude, emagrecimento, renda-extra, financas, relacionamento, beleza, pets, espiritualidade, educacao, ecommerce | Os nichos DR mais comuns no Brasil |
| `mercado` | br, latam, global-en, global-es | Modelagem de oferta gringa e adaptação para o Brasil |
| `framework` | aida, pas, bab, 4p, hook-story-offer, star-story-solution, 4u | Liga o prompt aos frameworks da Central |
| `insumo` | link-anuncio, transcricao-vsl, url-pagina, prints, metricas, comentarios, nenhum | Diz o que a pessoa precisa ter em mãos antes de usar |
| `saida` | lista, tabela, roteiro, analise, copy-pronta, plano, checklist | Mostra o tipo de entrega |
| `nivel` | iniciante, intermediario, avancado | Trilha de aprendizado |
| `risco` | baixo, medio, alto (com motivo: saude, renda, antes-depois, garantia) | Dispara o rodapé de compliance |
| `status` | rascunho, testado, controle | Selo de maturidade (Top 12, item 5) |
| `tools` | claude, chatgpt, gemini, perplexity | Já existe: botões "abrir no modelo" |

Regras práticas:
- Tags em minúsculas e com hífen, como os nomes de arquivo.
- Uma lista fechada de `stage` validada no `build.py`. Tags livres são aceitas, mas o build avisa quando uma tag aparece só uma vez (provável erro de digitação).
- No ⌘K, aceitar sinônimos em português (ex.: "espionar" → `pesquisa`, "hook" → `gancho`) num arquivo `synonyms.json`.

---

## 20 links externos para cadastrar na Central

Somente sites, sem repositórios do GitHub. Os IDs de categoria são os do `categories.json` atual.

| # | Nome | URL | Categoria sugerida | Por que cadastrar | Verificação |
|---|---|---|---|---|---|
| 1 | Biblioteca de Anúncios da Meta | https://www.facebook.com/ads/library/ | `pesquisa` | Fonte oficial para minerar ofertas e anúncios ativos | não verificado (403) |
| 2 | TikTok Creative Center: Top Ads | https://ads.tiktok.com/business/creativecenter/inspiration/topads/pc/en | `criativos` | Anúncios de alta performance com ordenação por CTR | verificado |
| 3 | Google Ads Transparency Center | https://adstransparency.google.com | `pesquisa` | Anúncios do Google por anunciante ou domínio | parcial |
| 4 | Swiped.co | https://swiped.co | `copy` | Swipe file clássico de DR com análise de cada peça | verificado |
| 5 | Foreplay | https://www.foreplay.co | `criativos` | Swipe file, descoberta de anúncios e briefs | verificado |
| 6 | Atria | https://www.tryatria.com | `criativos` | Biblioteca de anúncios com agente que aponta personas e ganchos que performam | verificado |
| 7 | Swipekit | https://swipekit.app/swipefile | `criativos` | Boards e tags para organizar referências de anúncio | verificado |
| 8 | GetHookd | https://www.gethookd.ai | `pesquisa` | Anúncios ativos filtráveis por tempo rodando e alerta de concorrente | verificado |
| 9 | Motion | https://motionapp.com | `analytics` | Analytics de criativo por gancho, formato e ângulo | verificado |
| 10 | Swipe Offers Spy (extensão) | https://chromewebstore.google.com/detail/swipe-offers-spy/ihegoljlcpaeefpdeblkokdgafkcckci | `pesquisa` | Ferramenta BR: transcrição de vídeo na Biblioteca de Anúncios (revisar permissões antes de instalar) | verificado |
| 11 | Minera Ads (extensão) | https://chromewebstore.google.com/detail/minera-ads/bhkmpbjlggghmgknebaonpnbdbljfpcn | `pesquisa` | Ferramenta BR de mineração de ofertas escaladas (revisar permissões antes de instalar) | verificado |
| 12 | Prompt library do Claude Code | https://code.claude.com/docs/en/prompt-library | `ia` | Prompts oficiais com explicação de "por que funciona" | verificado |
| 13 | prompts.chat | https://prompts.chat | `ia` | Maior biblioteca aberta de prompts, com CLI e MCP | verificado |
| 14 | gptprompts.ai: Prompts para marketing | https://gptprompts.ai/pt-br/prompts-para-marketing | `trafego` | Prompts em português para Meta Ads, Google Ads, e-mail e estratégia | verificado |
| 15 | skills.sh | https://skills.sh | `ia` | Ranking de skills de agentes, com tópico Marketing e packs | verificado |
| 16 | Marketplace de plugins do Claude | https://claude.com/plugins | `produtividade` | Plugins oficiais e verificados (inclui o de marketing) | verificado |
| 17 | Claude Marketplaces | https://claudemarketplaces.com | `produtividade` | Diretório de skills, MCPs e marketplaces ordenado por instalações | verificado |
| 18 | Glama: MCP Servers | https://glama.ai/mcp/servers | `automacao` | Maior índice de MCP, com notas de qualidade e filtro por categoria | verificado |
| 19 | mcp.so | https://mcp.so | `automacao` | Servidores MCP com configuração pronta por cliente | verificado |
| 20 | There's An AI For That | https://theresanaiforthat.com | `ia` | Busca de ferramentas de IA pela tarefa | verificado (página "About") |

Alternativas se algum link sair: Futurepedia (`ia`), Vertex AI Prompt Gallery (`ia`), Official MCP Registry (`automacao`), Future Tools (`ia`), PromptHero (`criativos`).

---

## Não verificado (consolidado)

| Referência | Motivo |
|---|---|
| PromptBase | 403 |
| FlowGPT | 403 |
| OpenAI Academy Prompt Packs | 404 e página só com navegação |
| multiple.chat | 403 |
| SkillsMP | 403 |
| cursor.directory | 429 (limite de requisições) |
| Toolify | 403 |
| AI Prompt Manager (template de Notion) | 429 |
| Biblioteca de Anúncios da Meta | 403 |
| Adligator | 504 |
| Google Ads Transparency Center | parcial (só a navegação carregou) |
| Reddit (todas as threads) | domínio bloqueado para o agente de busca |
