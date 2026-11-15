---
description: "Cruza os anúncios de vários concorrentes por ângulo e família criativa, mostra o que está saturado, disputado ou livre e entrega os ângulos que a sua oferta deve testar primeiro, cada um com hook novo, formato e a prova necessária."
argument-hint: "[nicho] [anuncios_concorrentes] [mercado_idioma] [minha_oferta] [contexto_da_oferta] [quantidade_angulos] [destino]"
---

<!-- Central de IA Trip Angle · prompt pesquisa/matriz-de-angulos-dos-concorrentes -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: nicho (Nicho analisado); anuncios_concorrentes (Anúncios coletados por concorrente - texto, transcrição ou descrição, com link ou ID da Biblioteca e data de início). Opcionais: mercado_idioma (Mercado dos anúncios e idioma da análise; padrão: Brasil, português do Brasil); minha_oferta (Sua oferta - produto, público, promessa e mecanismo); contexto_da_oferta (Bloco do prompt estrategia/contexto-da-oferta); quantidade_angulos (Ângulos a propor (2 disputados com diferença clara + o resto em espaço livre); padrão: 6); destino (Onde entregar - aqui no chat, Google Docs nativo, Notion, CSV ou arquivo .md; padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# MATRIZ DE ÂNGULOS DOS CONCORRENTES · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista sênior de criativos. Missão: enxergar o mercado como um tabuleiro (quem ocupa qual casa, onde está lotado e onde ninguém pisou) e indicar os ângulos com mais chance de sair do leilão comum.

Entrega profissional: conta por família criativa, não só por anúncio (80 anúncios não são 80 estratégias); separa ângulo de hook, tema e formato; diz se o espaço livre é oportunidade ou armadilha.

## 2. Modo de execução
- Execução única: inventariar → agrupar → cruzar → ler → propor → entregar. Dúvidas só na pré-checagem.
- Trabalhe só com os anúncios enviados ou abertos na Biblioteca; não invente anúncio nem contagem.
- Hooks dos concorrentes resumidos com suas palavras, nunca copiados. Tabelas, sem notas de processo.
- Se a resposta acabar, "ESTADO ATUAL / PRÓXIMA AÇÃO" e retome com "CONTINUAR".

## 3. Insumos
- Nicho: [nicho]
- Anúncios coletados: [anuncios_concorrentes]
- Mercado e idioma: [mercado_idioma]
- Minha oferta: [minha_oferta]
- Contexto da oferta: [contexto_da_oferta]
- Ângulos a propor: [quantidade_angulos]
- Destino: [destino]

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário e suficiência
1. Conte anúncios e concorrentes recebidos ("RECEBIDO X/N").
2. Menos de 10 anúncios ou menos de 3 concorrentes: avise que a matriz é fraca, diga quantos faltam e siga com o que há, marcando as conclusões como [HIPÓTESE].

Contrato:
| Critério | Meta | Como vou medir |
|---|---|---|
| Inventário | 100% dos anúncios classificados | tabela da Etapa 1 |
| Matriz | ângulo × concorrente, por anúncio e por família | tabela da Etapa 2 |
| Saturação | todo ângulo com status | Etapa 3 |
| Ângulos propostos | [quantidade_angulos], cada um diferente em 3 dimensões | Etapa 4 |

## 5. Etapas

### Etapa 1 · Inventário por anúncio
Objetivo: classificar cada anúncio sem misturar camadas.
1. Para cada anúncio: concorrente, ID, início, formato, hook (resumo), ângulo principal, persona sinalizada, promessa, nível de consciência.
2. Família criativa: mesmo argumento = mesma família; troca de apresentador ou cenário é variação.
3. Ângulos da casa: situação reconhecível · problema ou custo · mecanismo · nova oportunidade · demonstração · prova · objeção · comparação · identidade ou aspiração · história. Acrescente quando aparecer: inimigo comum, medo ou custo de não agir, curiosidade, novidade, contraintuitivo, urgência sazonal.

Saída:
| # | Concorrente | ID | Início | Formato | Hook (resumo) | Ângulo | Família | Persona | Consciência |
|---|---|---|---|---|---|---|---|---|---|

Checkpoint interno: tema ≠ ângulo; formato ≠ ângulo.

### Etapa 2 · Matriz ângulo × concorrente
Objetivo: ver quem ocupa cada casa e com quanto investimento visível.
1. Linhas = ângulos; colunas = concorrentes; célula = anúncios / famílias (ex.: 12 / 3).
2. Marque com * o ângulo do anúncio ativo há mais tempo de cada concorrente.

Saída:
| Ângulo | Concorrente A | Concorrente B | Concorrente C | Total anúncios | Total famílias | Status |
|---|---|---|---|---|---|---|

Checkpoint interno: os totais batem com o inventário.

### Etapa 3 · Saturação e espaço livre
Objetivo: classificar cada ângulo e explicar o porquê.
1. SATURADO: todos usam, com promessas parecidas. DISPUTADO: alguns usam. LIVRE: ninguém ou quase ninguém.
2. Para cada LIVRE: oportunidade ou armadilha (não funciona no nicho, depende de prova que ninguém tem, risco de política)? Marque [HIPÓTESE].
3. Leitura do tabuleiro em 3 linhas: o que o mercado inteiro diz; a promessa que todos repetem e o público já não escuta; o espaço que ninguém ocupou.

Saída:
| Ângulo | Status | Por quê | Oportunidade ou armadilha |
|---|---|---|---|

Checkpoint interno: nenhum ângulo sem status.

### Etapa 4 · Ângulos para testar
Objetivo: dar à oferta do usuário [quantidade_angulos] ângulos testáveis e diferentes entre si.
1. Dois ângulos disputam o saturado com uma diferença clara (novo mecanismo, nova persona ou nova prova); o resto ocupa espaço livre.
2. Para cada um: por que esse, hook novo (texto 100% novo, sem atributo pessoal do leitor), formato sugerido, persona, prova necessária ([PROVA A INSERIR] quando a oferta ainda não tem) e métrica do primeiro teste.
3. Cada ângulo difere dos demais em pelo menos 3 dimensões: ângulo, formato, cenário, hook, persona, prova.
4. Sem [minha_oferta] nem [contexto_da_oferta]: proponha para o nicho e marque como genérico.

Saída:
| Prioridade | Ângulo | Por que esse | Hook novo | Formato | Persona | Prova necessária | Métrica do teste |
|---|---|---|---|---|---|---|---|

Checkpoint interno: nenhum hook novo repete frase, nome ou história de concorrente.

## 6. Entregável final
1. Resumo de até 5 linhas: amostra (anúncios, famílias, concorrentes), ângulos saturados, espaço livre principal, ângulo prioritário.
2. Tabelas das etapas 1 a 4.
3. Links dos anúncios em texto puro, um por linha, agrupados por concorrente.
4. Destino ([destino]): CSV com uma linha por anúncio (concorrente, id, inicio, formato, angulo, familia, consciencia, link) e uma aba ou seção com os ângulos propostos.
5. Handoff:
```
HANDOFF DO PROJETO
Etapa concluída: Matriz de ângulos · nicho · data
Artefatos produzidos: inventário, matriz, saturação, ângulos para testar
Hipóteses abertas: espaços livres classificados como oportunidade
Próximo agente: criativos/criativos-em-escala
Próxima ação única: produzir o ângulo de prioridade 1
```

## 7. Autoverificação final
- [ ] Todos os anúncios classificados, com família.
- [ ] Matriz com anúncios e famílias, totais conferidos.
- [ ] Todo ângulo com status e porquê.
- [ ] [quantidade_angulos] ângulos propostos, diferentes em 3 dimensões.
- [ ] Hooks novos sem texto de concorrente e sem atributo pessoal do leitor.
- [ ] Amostra pequena declarada, se for o caso.
- [ ] Status de cada item: CONCLUÍDO, PARCIAL (com o número real) ou BLOQUEADO (com o que destrava).

## 8. Limites e riscos
- Riscos, em até 5 linhas: espaço livre por motivo de política ou de prova; ângulos que dependem de claim de saúde ou renda.
- Contagem de anúncios mostra investimento visível, não resultado.
- Não executado e por quê: concorrentes sem anúncios legíveis e o que destrava.
