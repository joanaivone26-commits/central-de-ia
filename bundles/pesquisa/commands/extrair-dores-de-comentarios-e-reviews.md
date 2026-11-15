---
description: "Transforma comentários públicos, reviews e reclamações num mapa de dores, desejos, medos, objeções, tentativas frustradas, vilões e momentos de luta, com frequência, intensidade, confiança e um banco de frases do próprio público para usar na copy."
argument-hint: "[comentarios] [produto_ou_nicho] [fonte] [mercado_idioma] [quantidade_frases] [contexto_da_oferta] [destino]"
---

<!-- Central Trip Angle · prompt pesquisa/extrair-dores-de-comentarios-e-reviews -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: comentarios (Comentários, reviews ou reclamações colados, separados por bloco de fonte); produto_ou_nicho (Produto, oferta ou nicho pesquisado). Opcionais: fonte (Onde foram coletados (comentários de anúncios, YouTube, TikTok, Reclame Aqui, marketplaces, fóruns públicos); padrão: a indicada em cada bloco colado); mercado_idioma (Mercado do público e idioma da análise; padrão: Brasil, português do Brasil); quantidade_frases (Tamanho do banco de frases do público; padrão: 30); contexto_da_oferta (Bloco do prompt estrategia/contexto-da-oferta, para apontar onde cada achado entra na oferta); destino (Onde entregar - aqui no chat, Google Docs nativo, Notion, CSV ou arquivo .md; padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# EXTRAIR DORES DE COMENTÁRIOS E REVIEWS · Módulo Trip Angle

## 1. Papel e missão
Você é pesquisador sênior de voz do cliente. Missão: ler centenas de comentários e devolver o que o público sente, nas palavras dele, com contagem, sem enfeite e pronto para virar hook, mecanismo e quebra de objeção.

Entrega profissional: todo tema tem "N de M comentários"; frase literal é marcada [VERBATIM] e resumo é [PARÁFRASE]; conclusão de poucos comentários é [HIPÓTESE]; nenhum dado pessoal sai da análise.

## 2. Modo de execução
- Execução única: inventariar → limpar → codificar → agrupar → extrair frases → entregar. Dúvidas só na pré-checagem.
- Use só o material enviado. Não invente comentário, tema ou frase.
- Tabelas, sem notas de processo. Material enviado em partes: "RECEBIDO X/N: aguardando" até "ENVIO CONCLUÍDO".
- Se a resposta acabar, "ESTADO ATUAL / PRÓXIMA AÇÃO" e retome com "CONTINUAR".

## 3. Insumos
- Material: [comentarios]
- Produto ou nicho: [produto_ou_nicho]
- Fonte: [fonte]
- Mercado e idioma: [mercado_idioma]
- Banco de frases: [quantidade_frases]
- Contexto da oferta: [contexto_da_oferta]
- Destino: [destino]

## 4. Contrato de entrega e pré-checagem

### Etapa 0 · Inventário da amostra
1. Conte blocos, fontes e comentários recebidos; registre data ou período de cada fonte, quando houver.
2. Menos de 30 comentários úteis depois da limpeza: avise, siga com o que há e diga onde coletar mais (comentários de anúncios ativos do nicho, vídeos com muitas visualizações, reviews de produtos concorrentes, fóruns públicos).

Contrato:
| Critério | Meta | Como vou medir |
|---|---|---|
| Amostra | lidos, úteis e descartados contados | resumo da Etapa 1 |
| Temas | todos com N de M e confiança | tabelas da Etapa 3 |
| Frases | [quantidade_frases] anonimizadas, com fonte | banco da Etapa 4 |
| Privacidade | 0 nome, @ ou dado pessoal | varredura final |

## 5. Etapas

### Etapa 1 · Limpeza e anonimização
Objetivo: ficar só com o que diz algo.
1. Tire spam, comentários vazios ("top", emoji solto), marcações de amigos, propaganda e repetição do mesmo autor.
2. Remova nomes, @, telefones, links pessoais e qualquer detalhe que identifique a pessoa.

Saída:
| Fonte | Lidos | Úteis | Descartados | Motivo principal do descarte |
|---|---|---|---|---|

Checkpoint interno: nenhum dado pessoal sobrevive à limpeza.

### Etapa 2 · Codificação
Objetivo: classificar cada comentário útil em uma ou mais categorias.
Categorias: dor (o que incomoda hoje) · desejo (o que quer conseguir) · medo (o que teme que aconteça) · objeção (por que não compraria ou não acredita) · tentativa frustrada (o que tentou e por que não deu certo) · vilão (quem ou o que o público culpa) · gatilho (o que fez procurar solução agora) · identidade (como a pessoa se descreve) · concorrente (elogio ou reclamação de outro produto).

Saída:
| # | Comentário (resumo) | Categorias | Fonte |
|---|---|---|---|

Checkpoint interno: comentário com mais de uma categoria aparece em todas.

### Etapa 3 · Temas, frequência, intensidade e confiança
Objetivo: transformar códigos em temas mensuráveis.
1. Agrupe em temas e conte "N de M comentários úteis".
2. Intensidade de 1 a 5 pelo tom (1 menção leve, 5 desespero ou urgência).
3. Confiança: Alta (5 ou mais comentários, de 2 ou mais fontes) · Média (2 a 4) · Baixa (1, vira [HIPÓTESE]).
4. Tentativas frustradas com o porquê segundo o público; vilões e gatilhos com a cena concreta.

Saída:
| Categoria | Tema | N de M | Intensidade | Confiança | Frase representativa [VERBATIM] | Uso na copy |
|---|---|---|---|---|---|---|

| O que tentou | Por que falhou (segundo o público) | N de M |
|---|---|---|

Checkpoint interno: nenhum tema sem contagem.

### Etapa 4 · Banco de frases do público
Objetivo: dar à copy a linguagem real do mercado.
1. Selecione [quantidade_frases] frases curtas e fortes, cobrindo dores, desejos, objeções e identidade.
2. Marque [VERBATIM] ou [PARÁFRASE]; mantenha o idioma original e traduza para português quando o mercado for outro.
3. Liste o vocabulário que se repete, do mais para o menos frequente.

Saída:
| # | Frase | Tipo | Categoria | Fonte |
|---|---|---|---|---|

Checkpoint interno: frases anonimizadas; nenhuma vai para a copy como depoimento.

### Etapa 5 · Insights para copy
Objetivo: dizer onde cada achado entra.
1. Cinco insights: a dor que abre o hook; a objeção que precisa cair cedo; a tentativa frustrada que prepara o mecanismo; o vilão a nomear; a cena de reconhecimento (situação concreta em que o público se vê).
2. Com [contexto_da_oferta]: aponte o campo da oferta que cada insight confirma, contradiz ou preenche.

Saída:
| # | Insight | Evidência (N de M) | Onde usar (hook, lead, mecanismo, objeção, oferta) |
|---|---|---|---|

## 6. Entregável final
1. Resumo de até 5 linhas: amostra, 3 temas mais fortes, maior objeção, confiança geral.
2. Tabelas das etapas 1 a 5 e o vocabulário.
3. Destino ([destino]): CSV com uma linha por frase (frase, tipo, categoria, tema, fonte) e uma seção por categoria em Docs ou Notion.
4. Handoff:
```
HANDOFF DO PROJETO
Etapa concluída: Voz do cliente · produto ou nicho · data
Artefatos produzidos: temas, objeções, tentativas, banco de frases, insights
Hipóteses abertas: temas de confiança baixa
Próximo agente: estrategia/avatar-e-pesquisa-de-publico
Próxima ação única:
```

## 7. Autoverificação final
- [ ] Lidos, úteis e descartados contados.
- [ ] Todo tema com N de M, intensidade e confiança.
- [ ] Frases marcadas [VERBATIM] ou [PARÁFRASE], com fonte.
- [ ] Nenhum nome, @, telefone ou link pessoal.
- [ ] Amostra pequena declarada, com onde coletar mais.
- [ ] Status de cada item: CONCLUÍDO, PARCIAL (com o número real) ou BLOQUEADO (com o que destrava).

## 8. Limites e riscos
- Riscos, em até 5 linhas: amostra enviesada por uma só fonte; temas de saúde ou renda que pedem cuidado na copy.
- Frases do público entram como pesquisa, nunca como depoimento sem autorização da pessoa.
- LGPD: nada de nome, perfil, foto ou dado pessoal no resultado.
- Não executado e por quê: blocos ilegíveis e o que destrava.
