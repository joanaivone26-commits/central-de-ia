# Guia de contribuição: como escrever prompts para a Central de IA Trip Angle

Este guia vale para quem cria ou revisa prompts da Central, seja pelo painel admin, seja direto nos arquivos.

## Antes de escrever

1. Leia o [padrão de prompt mestre](PADRAO-PROMPT-MESTRE.md). Ele é obrigatório.
2. Leia dois prompts mestres prontos como régua de profundidade, por exemplo `components/prompts/copy/vsl-do-zero.md` e `components/prompts/estrategia/avatar-e-pesquisa-de-publico.md`.
3. Veja o que já existe na área (`components/prompts/<categoria>/`) para não duplicar, e os frameworks relacionados em `components/frameworks/`.

## Formato

- Arquivo `components/prompts/<categoria>/<nome>.md`, nome em minúsculas com hífens.
- Frontmatter: `title`, `description` (1–2 frases dizendo o que entrega), `level` (`mestre` ou `modulo`), `stage`, `etapas`, `tempo`, `variables`, `tools`, `output`, `next`, `tags`, `author: Trip Angle`.
- Cada rótulo de variável começa com `[obrigatório]`, `[opcional]` ou `[padrão = X]`, entre aspas duplas. Variáveis em snake_case sem acento, usadas no texto como `{{nome}}`; toda variável usada precisa estar declarada.
- Corpo com as 8 seções, títulos exatamente assim: `## 1. Papel e missão`, `## 2. Modo de execução`, `## 3. Insumos`, `## 4. Contrato de entrega e pré-checagem`, `## 5. Etapas`, `## 6. Entregável final`, `## 7. Autoverificação final`, `## 8. Limites e riscos`. Etapas como `### Etapa N · Nome`; a Etapa 0 (inventário "RECEBIDO X/N") fica na seção 4.
- Prompt mestre: 220 a 500 linhas. Módulo: 100 a 220 linhas.
- Campos padrão em toda missão: `destino` (`[padrão = aqui no chat]`), `mercado_idioma`, `contexto_da_oferta` (`[opcional]`, bloco do prompt `estrategia/contexto-da-oferta`), `saida` (`[padrão = executar aqui]` ou gerar prompt para outra ferramenta) e `modo` quando a missão admite criar, modelar ou diagnosticar.
- Na seção 3, ao lado de cada insumo com padrão, repita "(padrão: X)" para o prompt funcionar mesmo colado sem preencher.

## Conteúdo

- Português do Brasil, tom Trip Angle: direto, verbos de ação, critérios mensuráveis, números da casa.
- Cada etapa: objetivo, passos numerados, saída com formato exato (cabeçalhos de tabela escritos) e checkpoint interno.
- Fallback real: fonte inacessível, meta não atingida, ferramenta sem acesso à web.
- No corpo, prefira "análise de concorrência", "mineração", "pesquisa de mercado".

## Limites

- Conteúdo público: nada de dados pessoais, nomes de alunos, clientes ou pessoas reais, credenciais, links privados, nomes de ofertas privadas. Exemplos sempre genéricos ou de nicho.
- Não reproduza trechos de livros: métodos com palavras próprias e crédito ao autor.
- Nada de cloaking, contas de terceiros, burlar revisão de anúncios, raspagem atrás de login ou conteúdo pirata.
- Copy com força e sem avisos legais dentro das peças, mas sem inventar depoimento, prova, número ou resultado: o que depende de prova fica `[PROVA A INSERIR]` e os riscos vão na seção 8.

## Validação

```bash
python3 tools/build.py --check      # nenhum aviso dos seus arquivos
python3 tools/check_conversao.py    # diferenças: 0
```
