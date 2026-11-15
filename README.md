# Central de IA Trip Angle

Tudo de IA que um projeto digital precisa, num lugar só, grátis e sem login: **prompts mestres**, **frameworks**, skills, agentes, comandos, servidores MCP, hooks, plugins, templates, **repositórios do GitHub** e ferramentas, organizados em **jornadas por objetivo** (direct response, e-commerce, pesquisa de público, base de copy, criativos e vídeo com IA, produto, conteúdo e YouTube, stack de IA). Tem site com a identidade Trip Angle, instalador de um comando, kits para o Claude Code, montador de prompt, painel admin para alimentar o catálogo e importadores de GitHub, pastas locais, aitmpl.com e da central de repositórios de IA.

*Mercado real. Execução real.*

## O que tem aqui

| Parte | Onde | Para quê |
|---|---|---|
| Componentes | `components/<tipo>/<categoria>/<nome>` | Fonte de verdade do catálogo |
| Site | `site/` → gerado em `dist/` | Explorar, buscar (⌘K), ver arquivos, montar stack e copiar comandos |
| Instalador | `tools/tahub.py` → publicado em `/tahub.py` | Instala qualquer componente no projeto, busca, diagnóstico e painéis locais |
| Marketplace | `.claude-plugin/marketplace.json` + `bundles/` | Kits por categoria e plugins instaláveis com `/plugin install` |
| Painel admin | `tools/admin.py` | Criar, importar, organizar e publicar |
| Importadores | `tools/importers.py` | GitHub, pasta local, aitmpl.com e cadastro de repositórios |
| Build | `tools/build.py` | Gera catálogo, kits, marketplace e o site em `dist/` |

Tudo roda com **Python 3.8+** e a biblioteca padrão. Não precisa de Node, pip nem build de front-end.

## Prompts mestres

A biblioteca segue o [padrão de prompt mestre Trip Angle](docs/PADRAO-PROMPT-MESTRE.md): cada prompt conduz uma missão inteira numa execução (ler → pesquisar → construir → revisar → entregar), pede todos os insumos de uma vez, abre com um contrato `Critério | Meta | Como vou medir`, segue etapas com checagem interna, fecha com status CONCLUÍDO/PARCIAL/BLOQUEADO e um bloco de passagem para a próxima missão. O padrão nasceu da análise dos prompts e tarefas reais da operação no ChatGPT e no Codex.

| Missão | Prompt mestre |
|---|---|
| Contexto | `estrategia/contexto-da-oferta` (Prompt Mestre 0: o bloco para colar em qualquer chat) |
| Pesquisa | `pesquisa/mineracao-de-ofertas`, `pesquisa/raio-x-de-concorrente` |
| Avatar e oferta | `estrategia/avatar-e-pesquisa-de-publico`, `estrategia/oferta-completa` |
| Copy e funil | `copy/vsl-do-zero`, `funil/pagina-advertorial-e-quiz` |
| Criativos | `criativos/criativos-em-escala`, `criativos/tiktok-shop` |
| Conteúdo | `conteudo/radar-viral-semanal`, `conteudo/pacote-de-publicacao` |
| Tráfego | `trafego/campanha-meta-ads` |
| Vendas | `vendas/esteira-e-pos-venda`, `vendas/campanha-na-comunidade` |
| Compliance | `compliance/revisao-de-compliance` |
| Produto | `produto/produto-digital-completo` |
| IA | `ia/arquiteto-de-prompts` (gera o comando completo para Lovable, Manus, Claude, Codex…) |

Os 33 módulos (partes de missão feitas sozinhas) seguem o mesmo esqueleto. `python3 tools/build.py` avisa se um prompt mestre ficar sem alguma das 8 seções, curto demais ou com insumo sem marcação `[obrigatório]`, `[opcional]` ou `[padrão = …]`; `python3 tools/check_conversao.py` garante que o comando gerado no Claude Code é o mesmo pelo instalador e pelo marketplace.

## Recursos do site

- **Comece aqui: jornadas por objetivo** (`#/jornadas`, dados em `journeys.json`): 8 jornadas com a sequência certa de passos. Cada passo traz o prompt principal, o apoio (frameworks, skills, MCPs, repositórios e ferramentas), a entrega e o que levar ao passo seguinte. Progresso salvo no navegador e botão para pôr a jornada inteira na stack.
- **Central de repositórios de IA**: cerca de 360 repositórios do GitHub (vídeo, áudio e voz, lip sync e avatares, MCPs) com ficha técnica completa (função, melhor uso, roda no Mac, hardware, licenças, uso comercial, status) e filtros por subcategoria, Mac e uso comercial, mais as ferramentas comerciais equivalentes. Atualize com `python3 tools/importar_catalogo_repos.py <pasta-dados>`.
- **Montador de prompt mestre** (`#/montador`): o membro preenche missão, insumos e etapas e o prompt sai no padrão da Central, com o guia "como formular prompts" ao lado. Copia ou baixa o `.md`.
- **Favoritos** (`#/favoritos`): estrela em qualquer item, lista própria e botão para pôr tudo na stack.
- **CTAs da Trip Angle**: YouTube, site e materiais pagos na página inicial, no fim das jornadas, embaixo de cada prompt e no fim de cada instalação pelo terminal. Edite em **Configurar e publicar** no admin (`cta` no `hub.config.json`).
- **Biblioteca de prompts** (`#/prompts`): filtros por etapa e por ferramenta; em cada prompt, formulário com as variáveis, texto final ao vivo, **Copiar**, **Abrir no Claude** e **Abrir no ChatGPT**.
- **Meu perfil da oferta** (`#/perfil`): produto, nicho, avatar, promessa, mecanismo, preço… preenchidos uma vez e usados em todos os prompts. Exporta `oferta.md` para o projeto.
- **Trilha DR** (`#/trilha`): as 10 etapas do trabalho de resposta direta com o que usar em cada uma.
- **Frameworks**: AIDA, PAS, BAB, 4Ps, Hook-Story-Offer, estrutura de VSL, níveis de consciência, sofisticação de mercado, equação de valor, big idea, JTBD, matriz de ângulos, hook-corpo-CTA e funil de conteúdo.
- **Kits curados** (`collections.json`): seleções por missão (espionagem, avatar e oferta, VSL, criativos, orgânico, tráfego) que entram inteiras na stack.
- **Ferramentas & Sites**: referências externas (Biblioteca de Anúncios, TikTok Creative Center, Foreplay, Atria, Glama, prompts.chat…).
- **Selo de maturidade**: rascunho, testado ou controle, definido no admin.
- **Novidades em RSS** (`feed.xml`) e catálogo para agentes (`llms.txt`, `api/*.json` e a skill `central-trip-angle`).

A pesquisa de referências que orientou esses recursos está em [docs/PESQUISA-REFERENCIAS.md](docs/PESQUISA-REFERENCIAS.md).

## Usar no dia a dia (dono da central)

```bash
python3 tools/admin.py
```

Abre `http://localhost:4545/admin`. Lá você:
- **cria** skills, agentes, comandos, MCPs, hooks, settings e templates com modelos prontos;
- **importa** de qualquer repositório do GitHub (inteiro ou uma subpasta) ou de uma pasta do computador, escolhendo item por item e a categoria;
- **traz do aitmpl.com** com a licença, a origem e o resultado da análise de segurança registrados;
- **cadastra repositórios** (estrelas, linguagem e licença vêm do GitHub);
- **monta plugins** juntando componentes;
- **organiza** categorias, edita e exclui (vai para `.trash/`, nada é apagado de vez);
- **publica** (commit e push).

O site público fica em `http://localhost:4545/` enquanto o admin roda.

Pelo terminal:

```bash
python3 tools/importers.py scan https://github.com/dono/repositorio
python3 tools/importers.py apply https://github.com/dono/repositorio --all --category copy
python3 tools/importers.py aitmpl search "seo"
python3 tools/importers.py aitmpl import skills/business-marketing/seo-optimizer --category seo
python3 tools/importers.py repo https://github.com/dono/repositorio --category ia
python3 tools/build.py
```

## Usar como aluno ou cliente da central

No site, cada componente mostra o comando. O formato:

```bash
python3 <(curl -fsSL https://tripangledigitalltda-star.github.io/central-de-ia/tahub.py) --skill copy/copywriting
```

No Windows (PowerShell ou Prompt de Comando), que não tem `<(...)`:

```
py -c "import urllib.request as u;exec(u.urlopen('https://tripangledigitalltda-star.github.io/central-de-ia/tahub.py').read())" --skill copy/copywriting
```

Rode dentro da pasta do projeto. Na pasta pessoal (`~`) o instalador para e avisa, para não deixar tudo global sem querer.

Vários de uma vez (é o que o botão **Stack** do site monta):

```bash
python3 <(curl -fsSL https://tripangledigitalltda-star.github.io/central-de-ia/tahub.py) --skill copy/copywriting,estrategia/offers --agent conteudo/content-marketer --command copy/hooks-anuncio
```

Prompts viram comandos e frameworks viram skills: `--prompts estrategia/criar-avatar-completo`, `--framework copy/pas`. Para ver um prompt preenchido no terminal: `--show prompts/estrategia/big-idea --var produto="Curso X"`. Outras opções: `--search`, `--list`, `--info`, `--dry-run`, `--yes`, `--scope local|project|user`, `-d <pasta>`, `--prompt`, `--health-check`, `--analytics`, `--chats`. Sem argumentos abre um menu interativo. A lista completa está em **Como usar** no site.

Kits pelo marketplace, dentro do Claude Code:

```
/plugin marketplace add tripangledigitalltda-star/central-de-ia
/plugin install ta-copy@trip-angle
```

Para os kits se atualizarem sozinhos, ative a atualização automática em `/plugin` → Marketplaces → trip-angle, ou rode `/plugin marketplace update trip-angle` de vez em quando. O `/plugin marketplace add` precisa do git instalado.

Componentes de terceiros (MIT e Apache-2.0) são redistribuídos com os avisos de licença em [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) e dentro de cada kit.

## Publicar

1. Crie um repositório vazio no GitHub.
2. No admin, em **Configurar e publicar**, preencha `dono/repositorio` e salve (o remoto `origin` é configurado).
3. Clique em **Publicar**.
4. No GitHub: **Settings → Pages → Source: GitHub Actions**. O workflow `.github/workflows/pages.yml` gera o site a cada push e já preenche o endereço e o repositório no catálogo.

Repositório privado: o GitHub Pages exige plano pago para repositório privado, e o marketplace e o instalador vão precisar de acesso ao repositório. Para uso só da equipe, dá para rodar o admin localmente ou publicar em outro serviço estático (Vercel, Netlify, Cloudflare Pages) servindo a pasta `dist/`.

## Conteúdo inicial

- **20 skills de marketing** curadas pela Trip Angle a partir de `coreyhaines31/marketingskills` (MIT, licença incluída em cada pasta).
- **Identidade Visual Trip Angle**: skill com o guia de marca, tokens e logos.
- **Templates** de operação de oferta DR e de lançamento, **comandos** de hooks de anúncio, briefing de oferta, plano de campanha no Meta, espionagem de oferta e revisão de claims, um hook de notificação e um setting de pesquisa web.
- **Curadoria do aitmpl.com** com componentes de marketing, documentos, design e automação, cada um com a origem e a licença.
- **Central de repositórios de IA** para vídeo, áudio, lip sync e avatares, com as ferramentas comerciais equivalentes.
- **Guia de contribuição** para quem escreve prompts: [docs/GUIA-DE-CONTRIBUICAO.md](docs/GUIA-DE-CONTRIBUICAO.md).

## Regras para componentes

- Nomes de pastas e arquivos em minúsculas com hífens.
- A descrição decide quando o Claude usa uma skill ou agente: diga a tarefa, as palavras que o usuário usa e o resultado.
- Chaves de API nunca vão no catálogo: em MCPs use `<placeholder>` ou `${VARIAVEL}`.
- Metadados da central (título, tags, origem, licença, destaque) ficam no arquivo lateral `.hub.json`, que nunca é instalado.

Detalhes técnicos: [docs/ARQUITETURA.md](docs/ARQUITETURA.md).
