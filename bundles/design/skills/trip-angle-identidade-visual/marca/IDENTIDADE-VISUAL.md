# Identidade visual Trip Angle

![Prancha da identidade Trip Angle](imagens/prancha-identidade.png)

Este guia reúne o que define a cara da comunidade Trip Angle e como aplicar em documentos, thumbnails e vídeos. Ele foi montado a partir dos materiais oficiais já publicados (ícone de tripangle.com.br, artes "Call de hoje" e thumbnails "O novo nível da IA" e "Deixei a IA controlar meus ads").

**Essência:** preto profundo, vermelho de alerta e branco gelo. Visual de operação ao vivo: painéis, grades, pontos de status e títulos condensados em caixa alta.
**Assinatura:** *Mercado real. Execução real.* · **ALL DAY** · `[ COMUNIDADE TRIP ANGLE ]`
**Perfis:** @tripanglelucas · @trip.angle · tripangle.com.br

## Logotipo

| Arquivo | Uso |
|---|---|
| `logo/trip-angle-logo-horizontal-branco.svg` | Principal. Sobre preto ou fotos escuras. |
| `logo/trip-angle-logo-horizontal-preto.svg` | Sobre branco ou papel. |
| `logo/trip-angle-simbolo-branco.svg` | Símbolo isolado: avatar, marca d'água, favicon. |
| `logo/trip-angle-simbolo-vermelho.svg` | Símbolo como elemento gráfico sobre preto. |
| `logo/trip-angle-simbolo-preto.svg` | Símbolo sobre fundos claros. |
| `logo/trip-angle-icone.svg` | Ícone de app: símbolo branco sobre degradê vinho → vermelho. |

O símbolo são três barras inclinadas que formam um triângulo aberto. As coordenadas foram traçadas do ícone oficial publicado no site; se você tiver o arquivo vetorial original da marca, substitua os SVGs por ele.

- **Respiro mínimo:** a espessura de uma barra em volta de todo o logo.
- **Tamanho mínimo:** símbolo com 24 px de altura na tela; logo horizontal com 32 px.
- **Não faça:** esticar, girar, trocar a cor de uma barra só, contornar, aplicar sombra colorida, escrever "Triple Angle" ou "TripAngle" junto. O nome é **Trip Angle**, em duas palavras.

## Cores

| Nome | Hex | Uso |
|---|---|---|
| Preto base | `#050505` | Fundo principal de capas, telas e vídeos. |
| Grafite | `#111113` | Cartões, painéis, caixas sobre o preto. |
| Linha grafite | `#26262A` | Bordas, divisórias, grade HUD. |
| **Vermelho Trip** | `#CE0103` | Destaque: a palavra-chave do título, botões, marcadores. Amostrado das artes oficiais. |
| Vermelho neon | `#FF2B2B` | Brilho, pontos de status (●), realces pequenos. Nunca em áreas grandes. |
| Vinho Angle | `#6D0D0D` | Degradês e cor principal no tema claro do site. |
| Branco gelo | `#F5F5F5` | Texto principal sobre preto. |
| Cinza texto | `#A1A1A1` | Texto secundário, rodapés, legendas de tabela. |

Proporção recomendada: 70% preto/grafite, 20% branco, 10% vermelho. O vermelho funciona porque aparece pouco.

## Tipografia

| Papel | Fonte (Google Fonts, gratuita) | Alternativa já instalada | Estilo |
|---|---|---|---|
| Títulos | **Anton** | Impact | CAIXA ALTA, condensada, linhas curtas e empilhadas. |
| Selos e chamadas | **Barlow Condensed** 800 itálico | Arial Narrow Bold Italic | Dentro de paralelogramos: `AO VIVO`, `TESTE REAL`. |
| Texto | **Inter** | Helvetica Neue, Aptos, Arial | Parágrafos e tabelas. |
| Logotipo | Inter Bold | Helvetica Neue Bold | Só no "Trip / Angle" do logo. |
| Código | JetBrains Mono | Menlo, Consolas | Comandos e caminhos. |

Para os scripts usarem as fontes exatas, veja `fontes/LEIA-ME.md`.

## Elementos gráficos

1. **Colchetes vermelhos com texto espaçado:** `[ C O M U N I D A D E   T R I P   A N G L E ]`.
2. **Selos em paralelogramo** (inclinação de ~12°), borda vermelha, fundo vermelho translúcido e brilho suave.
3. **Título em blocos:** linhas brancas e uma linha (ou palavra) em vermelho. Ex.: `O NOVO NÍVEL` / `DA IA`.
4. **Grade HUD e triângulos de contorno** vermelhos ao fundo, com baixa opacidade.
5. **Pontos de status** vermelhos (●) para listas de etapas: Agente → Pesquisa → Execução → Análise → Resultado.
6. **Luz de recorte vermelha** nas fotos (rim light) e fundo escuro desfocado.

## Aplicação em vídeo

Use `ferramentas/trip_angle_marca.py` (Python + Pillow). Ele implementa tudo abaixo.

| Elemento | Função | Regra |
|---|---|---|
| Capa/thumbnail | `capa(l, a, linhas, destaque=1)` | Uma linha em vermelho; no máximo 3 linhas na vertical. |
| Legenda | `legenda_ass(palavras, l, a)` | CAIXA ALTA, 3 palavras por vez, palavra falada em vermelho, contorno preto. |
| Tarja de nome | `lower_third(l, a, nome, funcao)` | Paralelogramo preto com borda e barra vermelhas. |
| Marca d'água | `aplicar_marca_dagua(quadro)` | Canto inferior direito, 70% de opacidade, fora da área de interface. |
| Encerramento | `cartao_final(l, a)` | Logo, colchete, "Mercado real. **Execução real.**", perfis e ALL DAY. |

**Áreas seguras (9:16, 1080 × 1920):** deixe 220 px livres no topo, 420 px na base e 90 px nas laterais — é onde Reels, TikTok e Shorts colocam botões e descrição. As legendas ficam com a base em ~64% da altura; a tarja de nome logo abaixo, até 78%.

Teste tudo de uma vez:

```bash
python scripts/demo_identidade.py              # vertical
python scripts/demo_identidade.py --formato horizontal
```

## Aplicação em documentos

- **Capa:** fundo preto, logo branco, colchete, título em Anton com uma linha vermelha.
- **Páginas internas:** fundo branco para leitura e impressão; títulos em preto com marcador vermelho; tabelas com cabeçalho preto e linha vermelha.
- **Rodapé:** `@tripanglelucas | @trip.angle` à esquerda, *Mercado real. Execução real.* à direita.
- Tokens prontos para web: `tokens.css`. Tokens para qualquer linguagem: `tokens.json`.

## Tom de voz

Direto, prático e de quem testa antes de ensinar. Frases curtas, verbos de ação, números reais. Mostre o processo e o resultado; não prometa o que não foi testado. Separe sempre **o que foi usado** de **o que foi só avaliado** — como no guia de repositórios da aula.
