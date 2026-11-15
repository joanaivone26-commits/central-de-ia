# Arquitetura da Central Trip Angle

Referência técnica para quem mantém a Central. O guia de uso está no `README.md`.

## Pastas

```
trip-angle-hub/
├── hub.config.json          nome, URL do site, repositório GitHub, nome do marketplace
├── categories.json          categorias (id = nome da pasta), rótulo, ícone, descrição
├── components/<tipo>/<categoria>/<nome>   fonte de verdade de tudo que o catálogo mostra
├── bundles/                 GERADO: um plugin por categoria (ta-<categoria>) para o marketplace
├── .claude-plugin/marketplace.json   GERADO: marketplace do Claude Code
├── site/                    site estático (index.html, assets/), admin.html e assets/admin.js
├── dist/                    GERADO e ignorado no git: site + api/ + components/ + tahub.py
└── tools/
    ├── hubcore.py           tipos, leitura de componentes (usado por build/admin/importers)
    ├── build.py             gera catálogo, bundles, marketplace e dist/
    ├── tahub.py             instalador para usuários finais (um arquivo, só biblioteca padrão)
    ├── importers.py         importa de repositórios GitHub, pastas locais e do aitmpl.com
    └── admin.py             servidor local do painel admin (http://localhost:4545)
```

Tudo roda com Python 3.9+ e só a biblioteca padrão. Nada de pip, Node ou build de front-end.

## Tipos de componente

| Tipo (`type`) | Flag do CLI | Formato em `components/` | Onde o CLI instala (relativo ao projeto, `-d`) |
|---|---|---|---|
| prompts | `--prompts` | arquivo `<cat>/<nome>.md` com frontmatter e variáveis `{{nome}}` | convertido em comando: `.claude/commands/<nome>.md` (ver "Prompts e frameworks") |
| frameworks | `--framework` | arquivo `<cat>/<nome>.md` com frontmatter | convertido em skill: `.claude/skills/framework-<nome>/SKILL.md` |
| skills | `--skill` | pasta `<cat>/<nome>/` com `SKILL.md` e arquivos de apoio | `.claude/skills/<nome>/` (pasta inteira) |
| agents | `--agent` | arquivo `<cat>/<nome>.md` com frontmatter | `.claude/agents/<nome>.md` |
| commands | `--command` | arquivo `<cat>/<nome>.md` | `.claude/commands/<nome>.md` |
| mcps | `--mcp` | `<cat>/<nome>.json` com `mcpServers` | chaves de `mcpServers` mescladas em `.mcp.json` |
| hooks | `--hook` | `<cat>/<nome>.json` com `hooks` | chave `hooks` mesclada no arquivo de settings do escopo; scripts em `.claude/hooks/` |
| settings | `--setting` | `<cat>/<nome>.json` com chaves de settings | chaves mescladas no arquivo de settings do escopo; scripts em `.claude/scripts/` |
| plugins | `--plugin` | pasta de plugin com `.claude-plugin/plugin.json` | habilitado pelo marketplace (ver abaixo) |
| templates | `--template` | pasta com `CLAUDE.md` e arquivos iniciais | arquivos copiados na raiz do projeto (não sobrescreve sem `--force`) |
| repos | `--repo` | `<cat>/<nome>.json` com `url` | `git clone <url>` em `./<nome>` |

Regras:
- Nomes de pasta e arquivo em minúsculas com hífens (`^[a-z0-9][a-z0-9._-]*$`).
- Metadados extras da Central ficam num arquivo lateral que **nunca é instalado**: `<pasta>/.hub.json` para pastas e `<cat>/<nome>.hub.json` para arquivos. Campos aceitos: `title`, `description`, `tags`, `author`, `license`, `version`, `source`, `scan`, `featured`, `addedAt`, `notes`.
- Em hooks, MCPs e settings, as chaves `description`, `scripts` e `$schema` são da Central e não vão para a configuração do usuário.
- Scripts de apoio de hooks e settings: qualquer arquivo na mesma pasta com o mesmo nome base (ex.: `notificar.json` + `notificar.sh`) ou uma pasta `<cat>/<nome>/`. Viram `extras` no catálogo.
- Plugins têm os filhos (skills, agents, commands) listados como itens próprios com `partOf` apontando para o plugin. Instalar um filho com o CLI copia só ele.

### Escopo de settings e hooks (`--scope`)

| Escopo | Arquivo |
|---|---|
| `local` (padrão, e sempre com `--yes`) | `.claude/settings.local.json` |
| `project` | `.claude/settings.json` |
| `user` | `~/.claude/settings.json` |

### Plugins e marketplace

`build.py` gera `.claude-plugin/marketplace.json` com:
- cada plugin de `components/plugins/<cat>/<nome>` (source `./components/plugins/<cat>/<nome>`);
- um pacote por categoria em `bundles/<cat>` chamado `ta-<cat>` com todas as skills, agentes e comandos soltos da categoria.

No Claude Code, com o repositório publicado no GitHub:
```
/plugin marketplace add <dono>/<repo>
/plugin install ta-copy@trip-angle
```
O `--plugin` do CLI faz o mesmo: se o comando `claude` existir, roda `claude plugin marketplace add` e `claude plugin install`; senão escreve no settings do escopo:
```json
{
  "extraKnownMarketplaces": { "trip-angle": { "source": { "source": "github", "repo": "<dono>/<repo>" } } },
  "enabledPlugins": { "<plugin>@trip-angle": true }
}
```

## Catálogo (`dist/api/catalog.json`)

```json
{
  "schemaVersion": 1,
  "generatedAt": "2026-11-15T12:00:00+00:00",
  "hub": { "name", "shortName", "tagline", "description", "siteUrl", "githubRepo", "branch", "marketplaceName", "owner", "socials" },
  "types": [{ "id": "skills", "label": "Skills", "singular": "Skill", "flag": "--skill", "kind": "dir", "count": 12 }],
  "categories": [{ "id": "copy", "label": "Copywriting", "icon": "✎", "description": "...", "order": 2, "count": 9 }],
  "counts": { "skills": 12, "...": 0, "total": 40 },
  "bundles": [{ "name": "ta-copy", "category": "copy", "label": "...", "description": "...", "source": "./bundles/copy", "skills": 3, "agents": 1, "commands": 0, "members": ["skills/copy/copywriting"] }],
  "items": [ITEM]
}
```

ITEM:
```json
{
  "id": "skills/copy/copywriting",          // <type>/<category>/<name>
  "type": "skills", "category": "copy", "name": "copywriting",
  "title": "Copywriting", "description": "...", "tags": [], "author": null, "license": "MIT", "version": null,
  "kind": "dir",                              // "dir" ou "file"
  "base": "components/skills/copy/copywriting",   // pasta (dir) ou arquivo (file), relativo à raiz do dist
  "main": "SKILL.md",                         // arquivo principal, relativo a base (para file: nome do arquivo)
  "files": ["components/skills/copy/copywriting/SKILL.md", "..."],   // TODOS os arquivos a instalar, relativos à raiz do dist
  "extras": [],                               // scripts de apoio (hooks/settings), relativos à raiz do dist
  "partOf": null,                             // id do plugin quando é filho de plugin
  "children": [],                             // ids dos filhos (só plugins)
  "source": { "kind": "github", "repo": "dono/repo", "path": "skills/x", "commit": "sha", "url": "https://..." },
  "scan": null, "featured": false, "addedAt": "2026-11-15", "size": 12345,
  "bundle": "ta-copy",                        // plugin do marketplace que contém o item
  // só alguns tipos:
  "servers": ["notion"], "requires": ["NOTION_TOKEN"],   // mcps
  "events": ["Stop"],                                     // hooks
  "pluginName": "kit-lancamento", "marketplaceName": "kit-lancamento",   // plugins
  "repo": { "url": "https://github.com/...", "stars": 100, "language": "Python", "license": "MIT" },  // repos
  "model": "opus", "tools": "Read, Grep",                 // agents
  "argumentHint": "[assunto]"                             // commands
}
```

Para skills (`kind: dir`) o destino de cada arquivo é `.claude/skills/<name>/` + o caminho do arquivo relativo a `base`.

Também gerados: `api/<tipo>.json` (`{type, count, items}`), `api/version.json`, `llms.txt`, `marketplace.json`, `tahub.py`.

## Origem dos arquivos para o CLI

`tahub.py` lê o catálogo e os arquivos de uma ORIGEM:
1. `--source <url-ou-pasta>` ou variável `TAHUB_SOURCE`;
2. senão, a constante `DEFAULT_SOURCE` (o build troca `__TAHUB_DEFAULT_SOURCE__` pelo `siteUrl`; o admin troca pela própria URL ao servir `/tahub.py`);
3. senão, se existir `../dist/api/catalog.json` ao lado do script (rodando de dentro do repositório), usa essa pasta.

Catálogo: `<origem>/api/catalog.json`. Arquivo: `<origem>/<caminho de files[]>`. Uma origem que é pasta local é lida direto do disco.

Comando que o site mostra:
```
python3 <(curl -fsSL https://SITE/tahub.py) --skill copy/copywriting
```

## API do painel admin (só em `tools/admin.py`, escuta 127.0.0.1)

Todas as respostas são JSON `{ "ok": true, ... }` ou `{ "ok": false, "error": "mensagem" }`. Toda escrita reconstrói o catálogo no fim (`build.build(quiet=True)`).

| Método e rota | Corpo / parâmetros | Faz |
|---|---|---|
| GET `/admin-api/ping` | | `{ok, config, root, git: {repo, remote, branch, dirty}}` |
| GET `/admin-api/item?id=` | | item do catálogo + `content` (texto do arquivo principal) + `side` (.hub.json) |
| POST `/admin-api/component` | `{type, category, name, content, meta?, overwrite?}` | cria ou atualiza. Para skills `content` é o SKILL.md; para JSON é o texto JSON (validado) |
| POST `/admin-api/component/delete` | `{id}` | move para `.trash/<data>/...` (não apaga de vez) |
| POST `/admin-api/category` | `{id, label, icon?, description?}` | cria ou atualiza em `categories.json` |
| POST `/admin-api/repo` | `{url, category, name?, description?, tags?}` | cria `components/repos/<cat>/<nome>.json` com metadados do GitHub (descrição, estrelas, linguagem, licença) |
| POST `/admin-api/import/scan` | `{source}` (URL GitHub ou caminho local) | lista candidatos `[{kind, path, name, description, suggestedCategory}]` |
| POST `/admin-api/import/apply` | `{source, items:[{kind, path, name?, category}]}` | importa os escolhidos com `source` registrado no `.hub.json` |
| GET `/admin-api/aitmpl/search?q=&type=` | | busca no catálogo do aitmpl.com (cache local de 1 dia) |
| POST `/admin-api/aitmpl/import` | `{ids:[...], category}` | baixa do GitHub do projeto e grava com atribuição e licença |
| POST `/admin-api/rebuild` | | roda o build |
| POST `/admin-api/publish` | `{message}` | `git add -A`, `git commit`, `git push` se houver remoto |

## Importadores

Detecção (igual para GitHub e pasta local):
- `**/SKILL.md` → skill (a pasta que contém o arquivo);
- `**/.claude-plugin/plugin.json` → plugin (a pasta acima de `.claude-plugin`); os filhos não viram itens soltos;
- `**/agents/*.md` → agente; `**/commands/*.md` → comando (fora de plugins detectados);
- `.mcp.json` ou `**/*.json` com chave `mcpServers` → MCP;
- `hooks/hooks.json` ou JSON com chave `hooks` de eventos do Claude Code → hook.

GitHub: `GET https://api.github.com/repos/<dono>/<repo>` (branch padrão, licença) e `.../git/trees/<branch>?recursive=1`; arquivos via `https://raw.githubusercontent.com/<dono>/<repo>/<commit>/<caminho>`. Usa `GITHUB_TOKEN` se existir. Grava `source: {kind:"github", repo, path, commit, url}`.

aitmpl.com: catálogo em `https://www.aitmpl.com/api/v1/catalog.json`; arquivos de cada componente via `https://www.aitmpl.com/component-content/<id>.json` (`meta.files[].path`) e `https://raw.githubusercontent.com/davila7/claude-code-templates/main/cli-tool/components/<type>/<category>/<name>...`. Grava `source: {kind:"aitmpl", id, url, repo:"davila7/claude-code-templates"}`, `scan` e `license`.

## Prompts e frameworks

### Formato do prompt (`components/prompts/<cat>/<nome>.md`)

```markdown
---
title: Extrair a estrutura de uma VSL
description: Destrincha a transcrição de uma VSL em blocos e mostra o que modelar.
variables:
  transcricao: Transcrição completa da VSL
  nicho: Nicho da oferta
tools: [claude, chatgpt, gemini]
output: Tabela em Markdown + lista de ângulos
tags: [vsl, extração de copy]
---
Texto do prompt usando {{transcricao}} e {{nicho}}.
```

- `variables` é um mapa nome → rótulo (o que a pessoa precisa preencher). Variáveis usadas no texto e não declaradas também são detectadas.
- `tools` (opcional): onde o prompt funciona bem: `claude`, `chatgpt`, `gemini`, `midjourney`, `veo`, `kling`, `suno`…
- No catálogo o item ganha `variables: [{name, label}]`, `tools`, `output` e `preview` (começo do texto).

Conversão em comando (`--prompts`, e nos kits do marketplace):

```markdown
---
description: "<description>"
argument-hint: "[transcricao] [nicho]"
---

<!-- Central Trip Angle · prompt <cat>/<nome> -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira se você tem: transcricao (Transcrição completa da VSL); nicho (Nicho da oferta). Se faltar algum, pergunte ao usuário.

<texto do prompt com cada {{variavel}} trocada por [variavel]>
```
(Sem variáveis, a linha "Antes de começar…" não aparece.) O comando fica em `.claude/commands/<nome>.md` e é chamado como `/<nome> dados…`.

### Formato do framework (`components/frameworks/<cat>/<nome>.md`)

```markdown
---
title: PAS (Problema, Agitação, Solução)
description: Estrutura de copy em três movimentos para textos curtos e anúncios.
when: Use para anúncios, e-mails e leads quando o público já sente a dor.
origin: Clássico da resposta direta
tags: [copy, estrutura]
---
Explicação, passos, exemplo e um prompt para aplicar.
```

Conversão em skill (`--framework`, e nos kits): pasta `.claude/skills/framework-<nome>/` (sem duplicar o prefixo se o nome já começar com `framework-`) com `SKILL.md`:

```markdown
---
name: framework-<nome>
description: "Framework <title>: <description> <when>"
---

# <title>

<corpo do framework>
```

As funções de referência são `prompt_to_command` e `framework_to_skill` em `tools/hubcore.py`; o `tahub.py` tem cópia própria com o mesmo resultado.

## Ferramentas & Sites, kits curados, selos e feed

- **sites** (`components/sites/<cat>/<nome>.json`): `{url, title, description, tags, pricing, lang}`. Não são instaláveis: o site mostra "Abrir o site" e o instalador ignora o tipo.
- **Kits curados** (`collections.json` na raiz): lista de `{id, title, description, items: [ids]}`. O build avisa sobre ids que não existem e publica em `catalog.collections`. No site, "Adicionar kit à stack".
- **Selo de maturidade**: `status` (`rascunho`, `testado` ou `controle`), `testedWith` e `testedAt` no `.hub.json` ou no frontmatter. O build avisa sobre valores fora da lista.
- **feed.xml**: RSS 2.0 com os 50 componentes mais recentes, gerado pelo build.
- **Perfil da oferta**: só no navegador (`localStorage`, chave `ta-perfil`). Os apelidos de variáveis ficam em `PERFIL` no `site/assets/app.js`.
