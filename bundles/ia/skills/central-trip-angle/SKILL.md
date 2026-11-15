---
name: central-trip-angle
description: Busca e instala componentes da Central de IA Trip Angle (prompts, skills, agentes, frameworks, comandos, MCPs, hooks, plugins e kits para o mercado digital). Use quando o usuário pedir um prompt, skill, agente ou MCP para uma tarefa de marketing digital (espionagem, avatar, oferta, copy, VSL, criativos, formatos, funil, tráfego, pós-venda, compliance), quiser saber "o que existe na central" ou pedir para instalar algo dela.
---

# Central de IA Trip Angle

A Central é um catálogo estático. Tudo o que você precisa está em JSON e Markdown no endereço da Central (a URL do site). Se não souber o endereço, pergunte ao usuário ou procure `siteUrl` no `hub.config.json` do repositório da Central.

## Onde buscar

| O quê | Endereço |
|---|---|
| Catálogo completo | `<site>/api/catalog.json` |
| Só um tipo | `<site>/api/prompts.json`, `skills.json`, `agents.json`, `frameworks.json`, `mcps.json`… |
| Lista curta para leitura | `<site>/llms.txt` |
| Arquivo de um componente | `<site>/<files[0]>` (caminhos do campo `files` de cada item) |

Cada item tem `id` (`tipo/categoria/nome`), `title`, `description`, `tags`, `category`, `files` e, nos prompts, `variables` (nome e rótulo de cada campo a preencher), `tools` e `output`.

## Como responder

1. Entenda a tarefa e a etapa (pesquisa, avatar e oferta, copy, criativos, formatos, funil, tráfego, pós-venda, produto, compliance).
2. Leia `llms.txt` ou o JSON do tipo certo com WebFetch e escolha de 1 a 5 itens que resolvem a tarefa. Prefira prompts e frameworks para tarefas pontuais e skills ou agentes para trabalho recorrente.
3. Mostre ao usuário: título, o que entrega, o que ele precisa ter em mãos (as `variables` do prompt) e o link `<site>/#/item/<id>`.
4. Para usar um prompt agora, baixe o arquivo, troque cada `{{variavel}}` pelos dados do usuário (pergunte o que faltar) e execute a tarefa.
5. Para instalar no projeto, rode na pasta do projeto, com a confirmação do usuário:

```bash
python3 <(curl -fsSL <site>/tahub.py) --prompts estrategia/criar-avatar-completo --skill copy/copywriting
```

Flags por tipo: `--prompts`, `--skill`, `--agent`, `--framework`, `--command`, `--mcp`, `--hook`, `--setting`, `--plugin`, `--template`. Vários itens do mesmo tipo vão separados por vírgula. Use `--dry-run` para mostrar o que seria gravado antes de instalar.

## Regras

- Não invente itens: só recomende o que existe no catálogo.
- MCPs, hooks e settings mexem na configuração do Claude Code e podem rodar código. Mostre o que vai mudar e peça confirmação antes de instalar.
- Se existir `.claude/oferta.md` no projeto (perfil da oferta exportado do site), use esses dados para preencher as variáveis dos prompts.
