---
name: trip-angle-identidade-visual
description: Aplica a identidade visual da comunidade Trip Angle em páginas, landing pages, slides em HTML, documentos, capas, thumbnails e criativos - logo, cores preto/vermelho/branco gelo, títulos condensados em caixa alta, selos em paralelogramo, colchetes e pontos de status. Use quando pedirem algo "com a cara da Trip Angle", padronizar um material da marca ou criar peça para a comunidade.
license: Uso pela comunidade Trip Angle
metadata:
  autor: Trip Angle
  versao: "1.1"
---

# Identidade visual Trip Angle

Leia `marca/IDENTIDADE-VISUAL.md` antes de criar algo novo. Não invente cores, não redesenhe o logo e escreva sempre **Trip Angle**, em duas palavras.

## Arquivos desta skill

| Arquivo | Para quê |
|---|---|
| `marca/IDENTIDADE-VISUAL.md` | Guia completo: logo, cores, fontes, elementos, tom de voz |
| `marca/tokens.css` | Variáveis CSS e classes prontas (`.ta-colchete`, `.ta-selo`, `.ta-titulo`) |
| `marca/tokens.json` | Os mesmos tokens para qualquer linguagem |
| `marca/logo/*.svg` | Logo horizontal (branco/preto), símbolo (branco/preto/vermelho) e ícone |
| `marca/prancha-identidade.png` | Prancha de referência visual |

Copie os arquivos de `marca/` para o projeto antes de usar. Não aponte para o caminho da skill no HTML final.

## Páginas e HTML

1. Importe `tokens.css` (já carrega Anton, Barlow Condensed, Inter e JetBrains Mono do Google Fonts).
2. Fundo `--ta-preto`, cartões `--ta-grafite` com borda `--ta-linha`, texto `--ta-gelo`, secundário `--ta-cinza`.
3. Títulos com `.ta-titulo` e uma palavra em `<em>` (fica vermelha). Rótulos de seção com `.ta-colchete`. Chamadas curtas com `.ta-selo`.
4. Botão principal: fundo `--ta-vermelho`, texto branco, cantos retos ou 4 px. O neon `--ta-neon` só em brilho e pontos de status (●).
5. Fundo com grade HUD: linhas de 1 px em `rgba(255,255,255,.04)` a cada 48 px e um triângulo de contorno vermelho com baixa opacidade.

## Documentos e slides

- Capa: fundo preto, logo branco, colchete `[ COMUNIDADE TRIP ANGLE ]`, título em Anton com uma linha vermelha.
- Páginas internas: fundo branco, títulos pretos com marcador vermelho, tabelas com cabeçalho preto e linha vermelha.
- Rodapé: `@tripanglelucas | @trip.angle` à esquerda e *Mercado real. Execução real.* à direita.

## Criativos, capas e thumbnails

- 70% preto/grafite, 20% branco, 10% vermelho. Uma linha ou palavra vermelha por título.
- Títulos em CAIXA ALTA, no máximo 3 linhas no vertical.
- Área segura do 9:16 (1080 × 1920): 220 px livres no topo, 420 px na base e 90 px nas laterais.
- Etapas com pontos de status: ● AGENTE — ● PESQUISA — ● EXECUÇÃO — ● ANÁLISE — ● RESULTADO.
- Confira sempre abrindo o PNG ou a página gerada antes de entregar.

## Tom de voz

Direto, prático, de quem testa antes de ensinar. Frases curtas, verbos de ação, números reais. Separe o que foi usado do que foi só avaliado.
