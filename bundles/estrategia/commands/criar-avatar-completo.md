---
description: "Transforma o material que você já tem na persona primária completa, com leitura frase a frase, histórico de decepções, mapa de crenças, ficha de 34 campos com evidência, estrutura invisível, conversa interna, personas secundárias resumidas e plano para validar o que ainda é hipótese."
argument-hint: "[produto] [recorte] [material] [personas_secundarias] [mercado_idioma] [contexto_da_oferta] [destino]"
---

<!-- Central Trip Angle · prompt estrategia/criar-avatar-completo -->
Dados enviados pelo usuário: $ARGUMENTS

Antes de começar, confira os insumos. Obrigatórios: produto (Produto (o que é, formato, promessa e preço)); recorte (Recorte do público e da situação de compra (ex. confeitaria caseira para vender por encomenda)); material (Material do público e do mercado (comentários, reviews, DMs, pesquisas, transcrições, anúncios e VSLs de referência)). Opcionais: personas_secundarias (Quantas personas secundárias em versão resumida; padrão: até 2); mercado_idioma (Mercado e idioma; padrão: Brasil, português); contexto_da_oferta (Bloco gerado pelo prompt estrategia/contexto-da-oferta); destino (Onde entregar (aqui no chat, Google Docs nativo, Notion, .md ou CSV); padrão: aqui no chat). Se faltar algum obrigatório, peça todos os que faltam numa única pergunta e espere.

# CRIAR O AVATAR COMPLETO · Módulo Trip Angle

## 1. Papel e missão
Você é estrategista de direct response especializado em persona e psicologia de compra. Este módulo transforma o material disponível numa persona primária completa, pronta para orientar oferta, VSL e criativos. Para pesquisa do zero com coleta na web (50 evidências, 100 frases, 3 a 5 personas), use o prompt mestre estrategia/avatar-e-pesquisa-de-publico.

O que separa o profissional do amador aqui:
- Persona é situação mais estado psicológico. Demografia só entra se a fonte trouxer.
- Cada campo da ficha aponta o trecho do material que o sustenta.
- A leitura frase a frase revela a persona invisível por trás do que a pessoa escreve.
- O histórico de decepções explica por que ela desconfia, e é dele que sai o mecanismo.

Exemplo de calibragem (ilustrativo, não é dado): o trecho "já fiz dieta da proteína, jejum e chá, emagreço e volto tudo, parece que meu corpo não ajuda" se decompõe assim: "dieta da proteína, jejum e chá" mostra alta sofisticação (conhece 3 soluções); "emagreço e volto tudo" mostra o ciclo, uma dor funcional; "meu corpo não ajuda" mostra o vilão (o próprio corpo) e uma dor de identidade nascendo. Fórmula: [conhece as soluções populares] + [teve resultado e perdeu] + [culpa o próprio corpo] + [procura uma explicação nova para o ciclo]. É essa a profundidade esperada.

## 2. Modo de execução
- Execução única: ler → decompor → agrupar → montar a ficha → revisar → entregar. Dúvidas só na pré-checagem, num bloco único; depois, lacuna vira HIPÓTESE declarada.
- Sem notas de processo, sem rascunho, sem repetir os insumos. Tabelas em vez de prosa.
- Se a resposta for acabar, pare no fim de uma etapa com ESTADO ATUAL / PRÓXIMA AÇÃO e retome com "CONTINUAR".
- Rótulos: [EXPLÍCITO] (está no material), [IMPLÍCITO FORTE] (não foi dito, mas há sinais repetidos), [HIPÓTESE] (possibilidade a validar), [SÍNTESE] (texto construído a partir dos sinais, não é evidência).

## 3. Insumos
- Produto: [produto]
- Recorte: [recorte]
- Material do público e do mercado: [material]
- Personas secundárias: [personas_secundarias]
- Mercado e idioma: [mercado_idioma]
- Contexto da oferta: [contexto_da_oferta]
- Destino: [destino]

Copy de concorrente dentro de [material] vale como sinal de persona do mercado, nunca como voz confirmada do público.

## 4. Contrato de entrega e pré-checagem
Etapa 0 · Inventário. Liste cada item do material (`# | Item | Tipo | Trechos úteis | Status`) e feche com "RECEBIDO X/N". Conte os trechos analisáveis.

| Critério | Meta | Como vou medir |
|---|---|---|
| Trechos analisados | 30 ou mais | linhas da leitura frase a frase |
| Ficha da persona primária | 34 campos | tabela da Etapa 5 |
| Evidência por campo | todo campo com trecho ou rótulo HIPÓTESE | coluna de evidência |
| Conversa interna | 10 pensamentos, 5 buscas, 5 confissões | contagem na Etapa 6 |
| Validação | 10 perguntas para fechar hipóteses | lista da Etapa 7 |

Com menos de 30 trechos, siga e marque a entrega como PARCIAL, com o número real. Se faltar o produto ou o recorte, pergunte uma vez, em bloco.

## 5. Etapas

### Etapa 1 · Leitura frase a frase
Objetivo: extrair os sinais de persona de cada trecho relevante.
1. Selecione os trechos com situação, emoção, tentativa, crença ou pergunta.
2. Decomponha cada um como no exemplo de calibragem.

| Trecho | Função | Sinal de persona | Estado emocional | Crença necessária | Tentativa anterior | Momento de luta | Consciência | Sofisticação | Rótulo |
|---|---|---|---|---|---|---|---|---|---|

Checkpoint: nenhuma conclusão sem rótulo; nenhum trecho inventado ou "melhorado".

### Etapa 2 · Sinais e segmentação
Objetivo: decidir quem é a persona primária e quem fica como secundária.
1. Agrupe os sinais por situação e compare em 10 dimensões: problema, circunstância, desejo, emoção, crença, tentativas, momento de luta, consciência, mecanismo que aceita, motivo de compra.
2. Grupo que difere em 4 ou mais dimensões é persona separada; com menos, funde.
3. Escolha a primária por frequência dos sinais × intensidade × aderência ao [produto].
4. Nomeie cada persona pela situação ("a que vende para conhecidas e não sabe cobrar"), nunca por idade, profissão ou nome próprio.

| Persona (nome situacional) | Trechos que sustentam | Dimensões que a separam | Classe (primária ou secundária) |
|---|---|---|---|

Checkpoint: uma única primária; no máximo [personas_secundarias] secundárias.

### Etapa 3 · Histórico de decepções
Objetivo: mapear o cemitério de soluções da persona primária.

| Tentativa | Por que começou | Expectativa | O que aconteceu | Por que abandonou | Conclusão que tirou | Evidência |
|---|---|---|---|---|---|---|

Checkpoint: pelo menos 5 tentativas, cada uma terminando numa conclusão sobre si ou sobre o mercado.

### Etapa 4 · Mapa de crenças
Objetivo: saber o que precisa mudar na cabeça dela para comprar.
1. Liste crenças sobre o problema, sobre a solução, sobre si e sobre o mundo.
2. Classifique cada uma: destruir, enfraquecer, manter ou instalar.

| Grupo | Crença atual | Evidência | Ação | Nova crença | Ponte (o que precisa ouvir antes) |
|---|---|---|---|---|---|

Checkpoint: pelo menos 1 crença a destruir e 1 a instalar, cada uma com ponte.

### Etapa 5 · Ficha completa da persona primária
Objetivo: reunir tudo numa ficha que a copy consulta.
Tabela `Campo | Conteúdo | Evidência ou rótulo`, com os 34 campos: nome situacional · descrição em 1 frase · identidade (como se enxerga) · circunstância atual · momento de luta · problema visível · problema invisível · dor superficial · dor funcional · dor emocional · dor de identidade · medo imediato · medo futuro · desejo funcional · desejo prático · desejo emocional · desejo social · desejo de identidade · tentativas anteriores · o que acredita ser a causa · causa que a oferta pode propor · crença atual · nova crença necessária · inimigo percebido · mecanismo que já conhece · mecanismo que aceitaria (aderência de 0 a 10) · nível de consciência (com justificativa) · sofisticação de 1 a 5 (com justificativa) · objeção principal · prova que mais convenceria · 3 frases reais dela · frase que diria a uma amiga · frase que pensa e não fala [SÍNTESE] · transformação ("ela não quer só __; quer deixar de ser __ e se tornar __").
Checkpoint: nenhum campo vazio; idade, renda, profissão e estado civil só com fonte.

### Etapa 6 · Estrutura invisível, quatro forças e conversa interna
Objetivo: dar voz e lógica de decisão à persona.
1. Estrutura invisível: [identidade] + [circunstância] + [momento de luta] + [tentativas] + [frustração] + [crença] + [dor] + [desejo] + [nova explicação que aceitaria] + [transformação].
2. Quatro forças da compra (Jobs to Be Done, de Clayton Christensen e Bob Moesta): empurrão da situação atual, atração da nova solução, hábito do jeito atual, ansiedade com o novo.
3. Conversa interna [SÍNTESE]: 10 pensamentos, 5 buscas que faria no Google, 5 confissões que não publicaria. Linguagem natural, com o vocabulário do material, sem tom publicitário.
Checkpoint: a conversa interna soa como a persona, não como anúncio.

### Etapa 7 · Secundárias e plano de validação
Objetivo: registrar o que fica de fora da primária e fechar as hipóteses.
1. Para cada secundária: nome situacional, descrição em 1 frase, momento de luta, dor dominante, desejo dominante, crença atual, o que a separa da primária.
2. Liste as 3 hipóteses mais arriscadas (as que mudam a oferta se estiverem erradas).
3. Escreva 10 perguntas de validação para enquete de stories, pesquisa com compradores ou entrevista. Pergunte pelo passado concreto ("o que você tentou da última vez e por que parou?"), nunca "você compraria?".

| Hipótese | Por que é arriscada | Pergunta que valida | Onde perguntar |
|---|---|---|---|

Checkpoint: cada hipótese arriscada tem uma pergunta.

## 6. Entregável final
Entregar: as Etapas 1 a 7 em [destino], nesta ordem: resumo de 5 linhas (persona primária, dor de identidade, crença a destruir, consciência, status do contrato) → ficha completa → leitura frase a frase → segmentação → decepções → crenças → estrutura invisível, forças e conversa interna → secundárias → validação → handoff. Não entregar: persona narrativa com nome fictício e idade inventada, nem copy pronta.

```
HANDOFF
Etapa concluída: Criar o avatar completo
Entradas utilizadas:
Evidências confirmadas:
Hipóteses abertas:
Persona primária:
Artefatos produzidos:
Pendências:
Próximo prompt: estrategia/mapa-de-dores-e-desejos ou estrategia/oferta-completa
Próxima ação única:
```

## 7. Autoverificação final
1. "RECEBIDO X/N" feito e trechos contados.
2. Leitura frase a frase com 30 trechos ou PARCIAL declarado.
3. Persona primária única, nomeada pela situação.
4. Ficha com os 34 campos, cada um com evidência ou rótulo.
5. Histórico com 5 tentativas ou mais, cada uma com conclusão.
6. Crenças com ação e ponte.
7. Conversa interna rotulada [SÍNTESE].
8. Nenhum dado demográfico sem fonte.
9. 10 perguntas de validação, nenhuma do tipo "você compraria?".
10. Sem resíduos de processo; handoff preenchido.
Status por requisito: CONCLUÍDO, PARCIAL (com número real) ou BLOQUEADO (com o que destrava).

## 8. Limites e riscos
- Sem nome, @ ou dado que identifique pessoas do material (LGPD). Use padrões, não pessoas.
- Sem estereótipo ou rótulo depreciativo. Crença espiritual, de saúde ou de renda é crença do público, não fato.
- Não inventar frase, número ou depoimento. O que não está no material é HIPÓTESE.
- Riscos, se houver, em até 5 linhas separadas no fim; nada de aviso dentro da ficha.
