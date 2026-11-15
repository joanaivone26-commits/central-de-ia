/* Central Trip Angle — painel admin (só funciona com python3 tools/admin.py) */
(() => {
  'use strict';

  const A = { cat: null, byId: new Map(), cfg: {}, git: {}, cats: [] };
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const slug = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9._-]+/g, '-').replace(/-{2,}/g, '-').replace(/^[-.]+|[-.]+$/g, '').slice(0, 80);
  const TIPOS_EDITAVEIS = ['prompts', 'skills', 'agents', 'frameworks', 'commands', 'mcps', 'hooks', 'settings', 'templates', 'sites'];

  // ---------------------------------------------------------------- API
  async function api(caminho, corpo) {
    const opt = corpo === undefined ? {} : { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(corpo) };
    const r = await fetch('/admin-api/' + caminho, opt);
    let j;
    try { j = await r.json(); } catch (e) { throw new Error(`Resposta inválida do servidor (HTTP ${r.status})`); }
    if (!j.ok) throw new Error(j.error || `Erro HTTP ${r.status}`);
    return j;
  }
  async function recarregar() {
    const r = await fetch('api/catalog.json', { cache: 'no-store' });
    A.cat = await r.json();
    A.byId = new Map(A.cat.items.map((i) => [i.id, i]));
    A.cats = A.cat.categories || [];
  }
  async function ping() {
    const j = await api('ping');
    A.cfg = j.config || {};
    A.git = j.git || {};
    const g = A.git;
    $('#statusGit').innerHTML = `<span class="ponto ${g.dirty ? '' : 'off'}"></span>${g.repo === false ? 'sem git' : esc(g.branch || 'git')}${g.dirty ? ' · alterações não publicadas' : ' · tudo publicado'}`;
  }

  // ---------------------------------------------------------------- utilidades de UI
  let tmrToast;
  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg; t.classList.add('on');
    clearTimeout(tmrToast); tmrToast = setTimeout(() => t.classList.remove('on'), 2400);
  }
  const selo = (t, extra = 'cinza') => `<span class="selo ${extra}"><span>${esc(t)}</span></span>`;
  const tipoLabel = (id) => ((A.cat.types || []).find((t) => t.id === id) || { singular: id }).singular;
  const optCats = (sel) => A.cats.map((c) => `<option value="${esc(c.id)}" ${c.id === sel ? 'selected' : ''}>${esc(c.label)}</option>`).join('');
  function cab(colchete, titulo, texto) {
    return `<span class="colchete">${esc(colchete)}</span><h1 class="titulo" style="font-size:clamp(32px,4.5vw,54px);margin:10px 0 10px">${titulo}</h1>${texto ? `<p class="muted" style="margin:0 0 22px;max-width:720px">${texto}</p>` : ''}`;
  }
  function ocupado(btn, sim, texto) {
    if (!btn) return;
    if (sim) { btn.dataset.txt = btn.innerHTML; btn.innerHTML = texto || 'Aguarde…'; btn.disabled = true; } else { btn.innerHTML = btn.dataset.txt || btn.innerHTML; btn.disabled = false; }
  }
  async function acao(btn, fn, okMsg) {
    ocupado(btn, true);
    try { const r = await fn(); if (okMsg) toast(okMsg); return r; } catch (e) { toast('Erro: ' + e.message); erroBox(e.message); return null; } finally { ocupado(btn, false); }
  }
  function erroBox(msg) { const b = $('#erroBox'); if (b) { b.hidden = false; b.textContent = msg; } }
  function logBox(texto) { const b = $('#logBox'); if (b) { b.hidden = false; b.textContent = texto; } }
  const saida = (j) => [j.message, j.output, j.log, (j.warnings || []).map((w) => 'aviso: ' + w).join('\n'), (j.imported || j.created || []).map((x) => '✓ ' + (x.id || x)).join('\n')].filter(Boolean).join('\n') || JSON.stringify(j, null, 2);

  // ---------------------------------------------------------------- modelos de conteúdo
  function modelo(tipo, nome, desc) {
    const n = nome || 'meu-componente';
    const d = desc || 'Descreva quando usar: tarefa, gatilhos e resultado esperado.';
    const titulo = n.split('-').map((w) => w[0]?.toUpperCase() + w.slice(1)).join(' ');
    switch (tipo) {
      case 'prompts': return `---\ntitle: ${titulo}\ndescription: ${d}\nvariables:\n  produto: Produto ou oferta\n  publico: Público-alvo\ntools: [claude, chatgpt, gemini]\noutput: Tabela em Markdown\ntags: []\nauthor: Trip Angle\n---\nVocê é um especialista em ... com experiência em direct response.\n\n## Contexto\n- Produto: {{produto}}\n- Público: {{publico}}\n\n## Tarefa\n1. \n2. \n3. \n\n## Formato da resposta\n- \n\n## Regras\n- Não invente dados. Marque como [HIPÓTESE] o que não veio de fonte.\n- Se faltar alguma informação, pergunte antes de começar.\n`;
      case 'frameworks': return `---\ntitle: ${titulo}\ndescription: ${d}\nwhen: Use quando ...\norigin: \ntags: []\nauthor: Trip Angle\n---\n## O que é\n\n## Passo a passo\n1. \n2. \n3. \n\n## Quando usar e quando não usar\n\n## Exemplo\n\n## Prompt para aplicar\nAplique o framework ${titulo} em: [cole aqui o produto, o público e o objetivo].\n`;
      case 'skills': return `---\nname: ${n}\ndescription: ${d}\n---\n\n# ${titulo}\n\n## Quando usar\n- \n\n## Antes de começar\nPergunte o que faltar: produto, público, oferta, canal e objetivo.\n\n## Passo a passo\n1. \n2. \n3. \n\n## Formato da entrega\n- \n\n## Regras\n- Não invente números nem resultados.\n`;
      case 'agents': return `---\nname: ${n}\ndescription: ${d}\ntools: Read, Grep, Glob, WebSearch, WebFetch\nmodel: sonnet\n---\n\nVocê é ${titulo}. \n\n## Como trabalhar\n1. \n2. \n\n## Entrega\n- \n`;
      case 'commands': return `---\ndescription: ${d}\nargument-hint: [assunto]\n---\n\nFaça o seguinte com base em: $ARGUMENTS\n\n1. \n2. \n`;
      case 'mcps': return JSON.stringify({ description: d, mcpServers: { [n]: { command: 'npx', args: ['-y', 'nome-do-pacote-mcp'], env: { API_KEY: '<sua-chave>' } } } }, null, 2);
      case 'hooks': return JSON.stringify({ description: d, hooks: { Stop: [{ hooks: [{ type: 'command', command: "osascript -e 'display notification \"Claude terminou\" with title \"Claude Code\"'" }] }] } }, null, 2);
      case 'settings': return JSON.stringify({ description: d, permissions: { allow: ['WebSearch', 'WebFetch'] } }, null, 2);
      case 'sites': return JSON.stringify({ url: 'https://', title: titulo, description: d, tags: [], pricing: 'grátis' }, null, 2);
      case 'templates': return `# ${titulo}\n\n${d}\n\n## Contexto do projeto\n- Produto:\n- Público:\n- Oferta:\n\n## Como trabalhar aqui\n- \n`;
      default: return '';
    }
  }

  // ---------------------------------------------------------------- páginas
  function pgPainel() {
    const c = A.cat.counts || {};
    const tipos = (A.cat.types || []);
    const recentes = A.cat.items.filter((i) => !i.partOf).sort((a, b) => String(b.addedAt).localeCompare(String(a.addedAt))).slice(0, 8);
    return `${cab('Painel', `Alimente a <em>central</em>`, 'Tudo o que você cria ou importa aqui vai para a pasta <span class="mono">components/</span>, o catálogo é refeito na hora e o site já mostra. Para o mundo ver, publique.')}
      <div class="numeros" style="margin-top:0">
        <a href="index.html#/explorar" target="_blank"><b>${c.total || 0}</b><small><span class="ponto"></span>Total</small></a>
        ${tipos.map((t) => `<a href="#/gerenciar?tipo=${t.id}"><b>${t.count}</b><small>${esc(t.label)}</small></a>`).join('')}
      </div>
      <div class="grid" style="margin-top:22px">
        ${[['#/novo?tipo=prompts', 'Criar prompt', 'Escreva um prompt com variáveis {{assim}}: vira página com formulário no site e /comando no Claude Code.'],
          ['#/novo', 'Criar componente', 'Escreva uma skill, agente, framework, comando, MCP, hook, setting ou template.'],
          ['#/importar', 'Importar de repositório', 'Cole a URL de um repositório do GitHub ou o caminho de uma pasta e escolha o que trazer.'],
          ['#/aitmpl', 'Importar do aitmpl', 'Busque no catálogo do aitmpl.com e traga com licença e origem registradas.'],
          ['#/repos', 'Cadastrar repositório', 'Liste repositórios úteis com estrelas, linguagem e licença puxadas do GitHub.'],
          ['#/plugin', 'Montar plugin', 'Junte skills, agentes e comandos num plugin instalável pelo marketplace.'],
          ['#/publicar', 'Configurar e publicar', 'Defina o GitHub e o endereço do site e envie as mudanças.']]
          .map(([h, t, d]) => `<a class="card" href="${h}"><h3 class="card-t">${t}</h3><p class="desc">${d}</p></a>`).join('')}
      </div>
      <div class="cab" style="margin-top:34px"><div><span class="colchete">Últimos adicionados</span></div>
        <button class="btn" id="rebuildBtn">Refazer catálogo</button></div>
      <pre class="log" id="logBox" hidden></pre>
      <table class="tabela"><thead><tr><th>Tipo</th><th>Componente</th><th>Categoria</th><th>Data</th></tr></thead><tbody>
        ${recentes.map((i) => `<tr><td>${selo(tipoLabel(i.type))}</td><td><a href="index.html#/item/${esc(i.id)}" target="_blank">${esc(i.title)}</a><br><small class="muted mono">${esc(i.category)}/${esc(i.name)}</small></td><td>${esc(i.category)}</td><td>${esc(i.addedAt || '')}</td></tr>`).join('')}
      </tbody></table>`;
  }
  function posPainel() {
    $('#rebuildBtn').addEventListener('click', async (e) => {
      const j = await acao(e.currentTarget, () => api('rebuild', {}), 'Catálogo refeito');
      if (j) { logBox(saida(j)); await recarregar(); }
    });
  }

  function pgNovo(p) {
    const editId = p.get('id');
    const tipo = p.get('tipo') || 'skills';
    return `${cab(editId ? 'Editar' : 'Criar', editId ? 'Editar <em>componente</em>' : 'Novo <em>componente</em>', 'A descrição é o que faz o Claude decidir quando usar uma skill ou agente: diga a tarefa, as palavras que o usuário costuma usar e o resultado.')}
      <form class="form" id="formNovo">
        <div class="linha">
          <label>Tipo<select name="type" ${editId ? 'disabled' : ''}>${TIPOS_EDITAVEIS.map((t) => `<option value="${t}" ${t === tipo ? 'selected' : ''}>${esc(tipoLabel(t))}</option>`).join('')}</select></label>
          <label>Categoria<select name="category">${optCats(p.get('cat') || 'copy')}</select></label>
          <label>Nome (pasta/arquivo)<input name="name" required pattern="[a-z0-9][a-z0-9._-]*" placeholder="ex.: headlines-vsl" ${editId ? 'readonly' : ''}><span class="dica">Minúsculas e hífens. Vira o comando /nome nos comandos.</span></label>
        </div>
        <div class="linha">
          <label>Título no site<input name="title" placeholder="ex.: Headlines para VSL"></label>
          <label>Tags<input name="tags" placeholder="vsl, headline, copy"><span class="dica">Separadas por vírgula.</span></label>
          <label>Autor<input name="author" placeholder="Trip Angle"></label>
          <label>Licença<input name="license" placeholder="MIT, uso interno…"></label>
          <label>Selo<select name="status"><option value="">Sem selo</option><option value="rascunho">Rascunho</option><option value="testado">Testado</option><option value="controle">Controle (o melhor que temos)</option></select></label>
        </div>
        <label>Descrição<textarea name="description" style="min-height:76px;font-family:var(--f-texto)" placeholder="Use quando o usuário pedir headlines para VSL, ganchos de abertura ou chamadas de anúncio…"></textarea></label>
        <label style="display:flex;align-items:center;gap:8px;font-size:13.5px"><input type="checkbox" name="featured" style="width:auto"> Mostrar nos destaques</label>
        <label>Conteúdo <span class="dica" id="dicaConteudo"></span><textarea name="content" spellcheck="false"></textarea></label>
        <div id="extras"></div>
        <div class="acoes-form">
          <button class="btn vermelho" type="submit">${editId ? 'Salvar alterações' : 'Criar componente'}</button>
          <button class="btn" type="button" id="modeloBtn">Gerar modelo</button>
          <button class="btn fantasma" type="button" id="addArq" hidden>+ Arquivo de apoio</button>
        </div>
        <div class="aviso vermelho" id="erroBox" hidden></div>
      </form>`;
  }
  async function posNovo(p) {
    const f = $('#formNovo');
    const editId = p.get('id');
    let ultimoModelo = '';
    const dicas = { sites: 'JSON com url, title, description, tags e pricing (grátis, freemium, pago).', prompts: 'Use {{variavel}} no texto e declare cada uma em variables (nome: rótulo). Vira /comando no Claude Code.', frameworks: 'Explique o método com suas palavras, passos, exemplo e um prompt para aplicar. Vira skill no Claude Code.', skills: 'SKILL.md com frontmatter name e description.', agents: 'Arquivo .md do agente.', commands: 'Arquivo .md; use $ARGUMENTS para o texto digitado depois do comando.', mcps: 'JSON com mcpServers. Use <placeholders> ou ${VARIAVEL} para chaves.', hooks: 'JSON com a chave hooks (eventos do Claude Code).', settings: 'JSON com as chaves do settings.json.', templates: 'Conteúdo do CLAUDE.md do template.' };
    const atualizarTipo = () => {
      const t = f.type.value;
      $('#dicaConteudo').textContent = dicas[t] || '';
      $('#addArq').hidden = !['skills', 'templates'].includes(t);
      if (!f.content.value.trim() || f.content.value === ultimoModelo) { ultimoModelo = modelo(t, f.name.value, f.description.value); f.content.value = ultimoModelo; }
    };
    f.type.addEventListener('change', atualizarTipo);
    f.title.addEventListener('input', () => { if (!editId && !f.name.dataset.mexeu) f.name.value = slug(f.title.value); });
    f.name.addEventListener('input', () => { f.name.dataset.mexeu = '1'; });
    $('#modeloBtn').addEventListener('click', () => { ultimoModelo = modelo(f.type.value, f.name.value, f.description.value); f.content.value = ultimoModelo; });
    $('#addArq').addEventListener('click', () => addExtra('', ''));
    if (editId) {
      try {
        const j = await api('item?id=' + encodeURIComponent(editId));
        const it = j.item || A.byId.get(editId) || {};
        const side = j.side || {};
        f.type.value = it.type; f.category.value = it.category; f.name.value = it.name;
        f.title.value = side.title || ''; f.tags.value = (side.tags || []).join(', ');
        f.author.value = side.author || ''; f.license.value = side.license || '';
        f.description.value = side.description || ''; f.featured.checked = !!side.featured;
        f.status.value = side.status || it.status || '';
        f.content.value = j.content || '';
        ultimoModelo = '';
        $('#dicaConteudo').textContent = dicas[it.type] || '';
      } catch (e) { erroBox(e.message); }
    } else {
      atualizarTipo();
    }
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const btn = f.querySelector('[type=submit]');
      const files = {};
      $$('.extra-arq').forEach((row) => { const pth = row.querySelector('input').value.trim(); if (pth) files[pth] = row.querySelector('textarea').value; });
      const vazio = editId ? null : undefined; // na edição, campo vazio apaga o valor salvo
      const meta = {
        title: f.title.value.trim() || vazio,
        description: f.description.value.trim() || vazio,
        tags: f.tags.value.split(',').map((s) => s.trim()).filter(Boolean),
        author: f.author.value.trim() || vazio,
        license: f.license.value.trim() || vazio,
        featured: f.featured.checked,
        status: f.status.value || vazio,
        testedAt: f.status.value === 'testado' || f.status.value === 'controle' ? new Date().toISOString().slice(0, 10) : vazio,
      };
      const corpo = { type: f.type.value, category: f.category.value, name: slug(f.name.value), content: f.content.value, meta, overwrite: !!editId };
      if (Object.keys(files).length) corpo.files = files;
      const j = await acao(btn, () => api('component', corpo), editId ? 'Salvo' : 'Componente criado');
      if (j) {
        await recarregar();
        const id = (j.item && j.item.id) || j.id || `${corpo.type}/${corpo.category}/${corpo.name}`;
        location.hash = '#/gerenciar?q=' + encodeURIComponent(corpo.name);
        toast(`Pronto: ${id}`);
      }
    });
  }
  function addExtra(caminho, texto) {
    const d = document.createElement('div');
    d.className = 'painel extra-arq';
    d.innerHTML = `<header><span class="colchete">Arquivo de apoio</span><span class="direita"><button type="button" class="btn fantasma peq">Remover</button></span></header>
      <div class="corpo form"><label>Caminho dentro da pasta<input placeholder="references/exemplos.md" value="${esc(caminho)}"></label><label>Conteúdo<textarea style="min-height:160px">${esc(texto)}</textarea></label></div>`;
    d.querySelector('button').addEventListener('click', () => d.remove());
    $('#extras').appendChild(d);
  }

  function pgImportar() {
    return `${cab('Importar', 'De um <em>repositório</em> ou pasta', 'Cole a URL de um repositório do GitHub (pode ser uma subpasta: <span class="mono">github.com/dono/repo/tree/main/skills</span>) ou o caminho de uma pasta no seu computador. A central encontra skills, agentes, comandos, plugins, MCPs e hooks e guarda a origem e a licença.')}
      <form class="form" id="formScan"><div class="linha" style="grid-template-columns:1fr auto">
        <label>Origem<input name="source" required placeholder="https://github.com/coreyhaines31/marketingskills  ou  /Users/voce/Documents/minhas-skills"></label>
        <label>&nbsp;<button class="btn vermelho" type="submit">Analisar</button></label></div></form>
      <div class="aviso vermelho" id="erroBox" hidden style="margin-top:14px"></div>
      <div id="candidatos" style="margin-top:20px"></div>
      <pre class="log" id="logBox" hidden style="margin-top:14px"></pre>`;
  }
  function posImportar() {
    let fonte = '';
    $('#formScan').addEventListener('submit', async (e) => {
      e.preventDefault();
      fonte = e.target.source.value.trim();
      $('#erroBox').hidden = true;
      const j = await acao(e.target.querySelector('button'), () => api('import/scan', { source: fonte }));
      if (!j) return;
      const lista = j.candidates || j.items || [];
      if (!lista.length) { $('#candidatos').innerHTML = '<div class="vazio">Nada encontrado nessa origem.</div>'; return; }
      $('#candidatos').innerHTML = `<div class="cab"><div><span class="colchete">${lista.length} encontrados</span></div>
        <div style="display:flex;gap:8px"><button class="btn" id="marcarTodos" type="button">Marcar/desmarcar todos</button><button class="btn vermelho" id="importarSel" type="button">Importar selecionados</button></div></div>
        <div style="overflow-x:auto"><table class="tabela"><thead><tr><th></th><th>Tipo</th><th>Nome</th><th>Categoria</th><th>Descrição</th></tr></thead><tbody>
        ${lista.map((c, i) => `<tr data-i="${i}"><td><input type="checkbox" checked aria-label="Selecionar"></td><td>${selo(tipoLabel(kindTipo(c.kind)))}</td>
          <td><input class="nome" value="${esc(c.name)}" style="width:180px;background:var(--preto);border:1px solid var(--linha-2);border-radius:4px;padding:5px 8px;color:var(--gelo)"><br><small class="muted mono">${esc(c.path)}</small></td>
          <td><select class="cat" style="height:34px">${optCats(c.suggestedCategory)}</select></td><td class="muted" style="font-size:12.5px">${esc((c.description || '').slice(0, 180))}</td></tr>`).join('')}
        </tbody></table></div>`;
      $('#marcarTodos').addEventListener('click', () => { const cbs = $$('#candidatos tbody input[type=checkbox]'); const v = !cbs.every((c) => c.checked); cbs.forEach((c) => { c.checked = v; }); });
      $('#importarSel').addEventListener('click', async (ev) => {
        const items = $$('#candidatos tbody tr').filter((tr) => tr.querySelector('input[type=checkbox]').checked).map((tr) => {
          const c = lista[+tr.dataset.i];
          return { kind: c.kind, path: c.path, name: slug(tr.querySelector('.nome').value), category: tr.querySelector('.cat').value };
        });
        if (!items.length) { toast('Selecione pelo menos um'); return; }
        const r = await acao(ev.currentTarget, () => api('import/apply', { source: fonte, items }), 'Importação concluída');
        if (r) { logBox(saida(r)); await recarregar(); }
      });
    });
  }
  const kindTipo = (k) => ({ skill: 'skills', agent: 'agents', command: 'commands', plugin: 'plugins', mcp: 'mcps', hook: 'hooks', setting: 'settings' })[k] || k;

  function pgAitmpl() {
    return `${cab('aitmpl.com', 'Importar do <em>aitmpl</em>', 'Busque nos mais de 1.900 componentes do catálogo aitmpl.com (claude-code-templates, licença MIT). A central baixa os arquivos do GitHub do projeto e guarda origem, licença e o resultado da análise de segurança.')}
      <form class="form" id="formAi"><div class="linha" style="grid-template-columns:1fr 180px auto">
        <label>Buscar<input name="q" required placeholder="seo, copywriting, notion, meta ads…"></label>
        <label>Tipo<select name="type"><option value="">Todos</option>${['skills', 'agents', 'commands', 'mcps', 'hooks', 'settings'].map((t) => `<option value="${t}">${esc(tipoLabel(t))}</option>`).join('')}</select></label>
        <label>&nbsp;<button class="btn vermelho" type="submit">Buscar</button></label></div></form>
      <div class="aviso vermelho" id="erroBox" hidden style="margin-top:14px"></div>
      <div id="resAi" style="margin-top:20px"></div>
      <pre class="log" id="logBox" hidden style="margin-top:14px"></pre>`;
  }
  function posAitmpl() {
    $('#formAi').addEventListener('submit', async (e) => {
      e.preventDefault();
      const f = e.target;
      const j = await acao(f.querySelector('button'), () => api(`aitmpl/search?q=${encodeURIComponent(f.q.value)}&type=${encodeURIComponent(f.type.value)}`));
      if (!j) return;
      const lista = j.results || j.items || [];
      if (!lista.length) { $('#resAi').innerHTML = '<div class="vazio">Nada encontrado.</div>'; return; }
      const cor = { LOW: 'var(--verde)', MEDIUM: 'var(--amarelo)', HIGH: 'var(--neon)', CRITICAL: 'var(--neon)' };
      $('#resAi').innerHTML = `<div class="cab"><div><span class="colchete">${lista.length} resultados</span></div><button class="btn vermelho" id="importarAi" type="button">Importar selecionados</button></div>
        <div style="overflow-x:auto"><table class="tabela"><thead><tr><th></th><th>Componente</th><th>Segurança</th><th>Downloads</th><th>Categoria na central</th></tr></thead><tbody>
        ${lista.map((c, i) => {
          const sev = (c.scan && c.scan.severity) || '';
          const ja = A.byId.has(`${c.type}/${c.suggestedCategory}/${c.name}`) || A.cat.items.some((x) => x.source && x.source.id === c.id);
          return `<tr data-i="${i}"><td><input type="checkbox" ${ja ? 'disabled' : ''} aria-label="Selecionar"></td>
          <td>${selo(tipoLabel(c.type))} <b>${esc(c.name)}</b> ${ja ? '<small class="muted">(já na central)</small>' : ''}<br><small class="muted mono">${esc(c.id)}</small><br><small class="muted">${esc((c.description || '').slice(0, 160))}</small></td>
          <td><span style="color:${cor[sev] || 'var(--cinza)'};font-weight:700">${sev ? '● ' + esc(sev) : '—'}</span></td><td>${esc(c.downloads ?? '—')}</td>
          <td><select class="cat" style="height:34px">${optCats(c.suggestedCategory || 'ia')}</select></td></tr>`;
        }).join('')}</tbody></table></div>
        <p class="nota">Itens com segurança HIGH ou CRITICAL executam código ou acessam dados sensíveis. Leia antes de importar.</p>`;
      $('#importarAi').addEventListener('click', async (ev) => {
        const grupos = {};
        $$('#resAi tbody tr').forEach((tr) => {
          if (!tr.querySelector('input').checked) return;
          const c = lista[+tr.dataset.i];
          const cat = tr.querySelector('.cat').value;
          (grupos[cat] = grupos[cat] || []).push(c.id);
        });
        if (!Object.keys(grupos).length) { toast('Selecione pelo menos um'); return; }
        const btn = ev.currentTarget;
        const logs = [];
        await acao(btn, async () => {
          for (const [cat, ids] of Object.entries(grupos)) {
            const r = await api('aitmpl/import', { ids, category: cat });
            logs.push(saida(r));
          }
        }, 'Importação concluída');
        logBox(logs.join('\n'));
        await recarregar();
      });
    });
  }

  function pgRepos() {
    const repos = A.cat.items.filter((i) => i.type === 'repos');
    return `${cab('Repositórios', 'Cadastrar <em>repositório</em>', 'Repositórios aparecem no site com estrelas, linguagem e licença puxadas do GitHub, e podem ser clonados pelo instalador. Para trazer os componentes de dentro deles, use Importar.')}
      <form class="form" id="formRepo">
        <div class="linha"><label>URL do GitHub<input name="url" required placeholder="https://github.com/dono/repositorio"></label>
          <label>Categoria<select name="category">${optCats('ia')}</select></label>
          <label>Nome (opcional)<input name="name" placeholder="gerado da URL"></label></div>
        <div class="linha"><label>Descrição (opcional)<input name="description" placeholder="usa a do GitHub se vazio"></label>
          <label>Tags<input name="tags" placeholder="skills, marketing"></label></div>
        <div class="acoes-form"><button class="btn vermelho" type="submit">Cadastrar</button></div>
        <div class="aviso vermelho" id="erroBox" hidden></div>
      </form>
      <div class="cab" style="margin-top:30px"><div><span class="colchete">${repos.length} cadastrados</span></div></div>
      <table class="tabela"><thead><tr><th>Repositório</th><th>Categoria</th><th>★</th><th></th></tr></thead><tbody>
      ${repos.map((r) => `<tr><td><a href="${esc((r.repo || {}).url)}" target="_blank" rel="noopener"><b>${esc(r.title)}</b></a><br><small class="muted">${esc(r.description)}</small></td><td>${esc(r.category)}</td><td>${esc((r.repo || {}).stars ?? '—')}</td>
        <td><button class="btn peq" data-importar-repo="${esc((r.repo || {}).url)}">Importar conteúdo</button> <button class="btn fantasma peq" data-excluir="${esc(r.id)}">Excluir</button></td></tr>`).join('') || '<tr><td colspan="4" class="muted">Nenhum ainda.</td></tr>'}
      </tbody></table>`;
  }
  function posRepos() {
    $('#formRepo').addEventListener('submit', async (e) => {
      e.preventDefault();
      const f = e.target;
      const corpo = { url: f.url.value.trim(), category: f.category.value, tags: f.tags.value.split(',').map((s) => s.trim()).filter(Boolean) };
      if (f.name.value.trim()) corpo.name = slug(f.name.value);
      if (f.description.value.trim()) corpo.description = f.description.value.trim();
      const j = await acao(f.querySelector('[type=submit]'), () => api('repo', corpo), 'Repositório cadastrado');
      if (j) { await recarregar(); render(); }
    });
    $$('[data-importar-repo]').forEach((b) => b.addEventListener('click', () => {
      location.hash = '#/importar';
      setTimeout(() => { const f = $('#formScan'); if (f) { f.source.value = b.dataset.importarRepo; f.requestSubmit(); } }, 60);
    }));
  }

  function pgPlugin() {
    const membros = A.cat.items.filter((i) => ['prompts', 'skills', 'agents', 'frameworks', 'commands'].includes(i.type) && !i.partOf);
    return `${cab('Plugin', 'Montar <em>plugin</em>', 'Um plugin junta skills, agentes, comandos, prompts e frameworks num pacote que o Claude Code instala e atualiza pelo marketplace. Além dos kits automáticos por categoria, monte kits do seu jeito (ex.: "Lançamento", "Kit do aluno").')}
      <form class="form" id="formPlugin">
        <div class="linha"><label>Nome do plugin<input name="name" required placeholder="kit-lancamento"></label>
          <label>Categoria<select name="category">${optCats('trip-angle')}</select></label>
          <label>Versão<input name="version" value="1.0.0"></label></div>
        <label>Descrição<input name="description" required placeholder="Tudo para planejar e rodar um lançamento: oferta, copy, criativos e tráfego."></label>
        <label class="campo" style="max-width:420px">${'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'}<input id="filtroMembros" placeholder="Filtrar componentes"></label>
        <div style="max-height:420px;overflow:auto;border:1px solid var(--linha);border-radius:4px"><table class="tabela"><tbody>
          ${membros.map((m) => `<tr data-busca="${esc((m.title + ' ' + m.name + ' ' + m.category).toLowerCase())}"><td style="width:30px"><input type="checkbox" value="${esc(m.id)}" aria-label="Incluir ${esc(m.title)}"></td><td>${selo(tipoLabel(m.type))}</td><td><b>${esc(m.title)}</b><br><small class="muted mono">${esc(m.id)}</small></td></tr>`).join('')}
        </tbody></table></div>
        <div class="acoes-form"><button class="btn vermelho" type="submit">Criar plugin</button><span class="muted" id="contaMembros">0 selecionados</span></div>
        <div class="aviso vermelho" id="erroBox" hidden></div>
      </form>`;
  }
  function posPlugin() {
    const f = $('#formPlugin');
    const conta = () => { $('#contaMembros').textContent = $$('#formPlugin tbody input:checked').length + ' selecionados'; };
    f.addEventListener('change', conta);
    $('#filtroMembros').addEventListener('input', (e) => { const q = e.target.value.toLowerCase(); $$('#formPlugin tbody tr').forEach((tr) => { tr.hidden = q && !tr.dataset.busca.includes(q); }); });
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const members = $$('#formPlugin tbody input:checked').map((c) => c.value);
      if (!members.length) { toast('Escolha pelo menos um componente'); return; }
      const j = await acao(f.querySelector('[type=submit]'), () => api('plugin', { name: slug(f.name.value), category: f.category.value, description: f.description.value.trim(), version: f.version.value.trim() || '1.0.0', members }), 'Plugin criado');
      if (j) { await recarregar(); location.hash = '#/gerenciar?tipo=plugins'; }
    });
  }

  function pgGerenciar(p) {
    const q = (p.get('q') || '').toLowerCase();
    const tipo = p.get('tipo') || '';
    const lista = A.cat.items.filter((i) => (!tipo || i.type === tipo) && (!q || (i.title + ' ' + i.id + ' ' + i.description).toLowerCase().includes(q)));
    return `${cab('Componentes', 'Gerenciar <em>catálogo</em>', '')}
      <div class="filtros" style="margin-top:0"><label class="campo"><input id="gq" value="${esc(q)}" placeholder="Filtrar"></label>
        <select id="gt"><option value="">Todos os tipos</option>${(A.cat.types || []).map((t) => `<option value="${t.id}" ${t.id === tipo ? 'selected' : ''}>${esc(t.label)} (${t.count})</option>`).join('')}</select></div>
      <p class="resumo">${lista.length} componentes</p>
      <div style="overflow-x:auto"><table class="tabela"><thead><tr><th>Tipo</th><th>Componente</th><th>Categoria</th><th>Origem</th><th></th></tr></thead><tbody>
      ${lista.slice(0, 400).map((i) => `<tr><td>${selo(tipoLabel(i.type))}</td><td><b>${esc(i.title)}</b>${i.featured ? ' <span style="color:var(--neon)">★</span>' : ''}<br><small class="muted mono">${esc(i.id)}</small></td>
        <td>${esc(i.category)}</td><td class="muted" style="font-size:12.5px">${esc(i.partOf ? 'parte de ' + i.partOf : (i.source && (i.source.repo || i.source.kind)) || 'local')}</td>
        <td style="white-space:nowrap"><a class="btn peq" href="index.html#/item/${esc(i.id)}" target="_blank">Ver</a>
          ${!i.partOf && TIPOS_EDITAVEIS.includes(i.type) ? `<a class="btn peq" href="#/novo?id=${encodeURIComponent(i.id)}">Editar</a>` : ''}
          ${!i.partOf ? `<button class="btn fantasma peq" data-excluir="${esc(i.id)}">Excluir</button>` : ''}</td></tr>`).join('')}
      </tbody></table></div>`;
  }
  function posGerenciar(p) {
    const aplicar = () => {
      const n = new URLSearchParams();
      if ($('#gq').value) n.set('q', $('#gq').value);
      if ($('#gt').value) n.set('tipo', $('#gt').value);
      history.replaceState(null, '', '#/gerenciar' + (n.toString() ? '?' + n : ''));
      render(); const g = $('#gq'); g.focus(); g.setSelectionRange(g.value.length, g.value.length);
    };
    let tmr;
    $('#gq').addEventListener('input', () => { clearTimeout(tmr); tmr = setTimeout(aplicar, 250); });
    $('#gt').addEventListener('change', aplicar);
  }

  function pgCategorias() {
    return `${cab('Categorias', 'Áreas do <em>catálogo</em>', 'O id é o nome da pasta dentro de components/&lt;tipo&gt;/. Mudar o rótulo, ícone ou descrição não move nada.')}
      <form class="form" id="formCat"><div class="linha">
        <label>Id<input name="id" required placeholder="lancamentos"></label>
        <label>Rótulo<input name="label" required placeholder="Lançamentos"></label>
        <label>Ícone<input name="icon" maxlength="3" placeholder="▲"></label></div>
        <label>Descrição<input name="description" placeholder="Planejamento e execução de lançamentos."></label>
        <div class="acoes-form"><button class="btn vermelho" type="submit">Salvar categoria</button></div>
        <div class="aviso vermelho" id="erroBox" hidden></div></form>
      <table class="tabela" style="margin-top:26px"><thead><tr><th></th><th>Id</th><th>Rótulo</th><th>Itens</th><th>Descrição</th><th></th></tr></thead><tbody>
      ${A.cats.map((c) => `<tr><td style="color:var(--neon)" class="mono">${esc(c.icon || '')}</td><td class="mono">${esc(c.id)}</td><td>${esc(c.label)}</td><td>${c.count || 0}</td><td class="muted">${esc(c.description || '')}</td>
        <td><button class="btn peq" data-editcat="${esc(c.id)}">Editar</button></td></tr>`).join('')}</tbody></table>`;
  }
  function posCategorias() {
    const f = $('#formCat');
    $$('[data-editcat]').forEach((b) => b.addEventListener('click', () => {
      const c = A.cats.find((x) => x.id === b.dataset.editcat);
      f.id.value = c.id; f.label.value = c.label; f.icon.value = c.icon || ''; f.description.value = c.description || '';
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }));
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const j = await acao(f.querySelector('[type=submit]'), () => api('category', { id: slug(f.id.value), label: f.label.value.trim(), icon: f.icon.value.trim(), description: f.description.value.trim() }), 'Categoria salva');
      if (j) { await recarregar(); render(); }
    });
  }

  function pgPublicar() {
    const c = A.cfg;
    const g = A.git;
    return `${cab('Publicar', 'Configurar e <em>publicar</em>', 'Com o GitHub configurado, o comando de instalação e o marketplace passam a apontar para o seu repositório e o site entra no ar pelo GitHub Pages.')}
      <form class="form" id="formCfg">
        <div class="linha"><label>Nome da central<input name="name" value="${esc(c.name)}"></label><label>Assinatura<input name="tagline" value="${esc(c.tagline)}"></label></div>
        <label>Descrição<input name="description" value="${esc(c.description)}"></label>
        <div class="linha">
          <label>Repositório no GitHub<input name="githubRepo" value="${esc(c.githubRepo)}" placeholder="seu-usuario/trip-angle-hub"><span class="dica">Formato dono/repositório.</span></label>
          <label>Endereço do site<input name="siteUrl" value="${esc(c.siteUrl)}" placeholder="https://seu-usuario.github.io/trip-angle-hub"><span class="dica">Vazio = usa o endereço de onde o site é aberto.</span></label>
          <label>Nome do marketplace<input name="marketplaceName" value="${esc(c.marketplaceName)}"></label>
        </div>
        <div class="acoes-form"><button class="btn vermelho" type="submit">Salvar configuração</button></div>
        <div class="aviso vermelho" id="erroBox" hidden></div>
      </form>
      ${formCta()}
      <div class="painel" style="margin-top:26px"><header><span class="ponto ${g.dirty ? '' : 'off'}"></span><span class="colchete">Enviar mudanças</span></header><div class="corpo form">
        <p class="muted" style="margin:0">Branch <b class="mono">${esc(g.branch || '—')}</b> · remoto <b class="mono">${esc(g.remote || 'nenhum')}</b> · ${g.dirty ? 'há alterações não enviadas' : 'nada pendente'}</p>
        <label>Mensagem do commit<input id="msgCommit" value="Atualiza a central"></label>
        <div class="acoes-form"><button class="btn vermelho" id="publicarBtn" type="button">Publicar</button><button class="btn" id="rebuildBtn2" type="button">Só refazer o catálogo</button></div>
        <pre class="log" id="logBox" hidden></pre>
      </div></div>
      <div class="painel" style="margin-top:14px"><header><span class="colchete">Primeira publicação no GitHub</span></header><div class="corpo md" style="padding:14px 18px">
        <ol><li>Crie um repositório vazio no GitHub (ex.: <code>trip-angle-hub</code>).</li>
        <li>Preencha <b>Repositório no GitHub</b> acima e salve: o remoto <code>origin</code> é configurado.</li>
        <li>Clique em <b>Publicar</b>. Na primeira vez o git pode pedir login do GitHub no terminal.</li>
        <li>No GitHub, em <b>Settings → Pages</b>, escolha <b>Source: GitHub Actions</b>. O site sai em <code>https://seu-usuario.github.io/trip-angle-hub</code>.</li>
        <li>Volte aqui, preencha o <b>Endereço do site</b> e publique de novo.</li></ol></div></div>`;
  }
  function formCta() {
    const c = A.cfg.cta || {};
    const yt = c.youtube || {};
    const site = c.site || {};
    const prods = (c.produtos || []).concat([{}, {}, {}]).slice(0, Math.max(3, (c.produtos || []).length + 1));
    return `<div class="painel" style="margin-top:26px"><header><span class="ponto"></span><span class="colchete">Chamadas para a Trip Angle (CTAs)</span></header><div class="corpo">
      <form class="form" id="formCta">
        <p class="muted" style="margin:0">Aparecem na página inicial, no fim de cada jornada, embaixo de cada prompt e no fim de cada instalação pelo terminal. Deixe o link vazio para esconder.</p>
        <div class="linha"><label>YouTube (link)<input name="yt_url" value="${esc(yt.url)}" placeholder="https://www.youtube.com/@..."></label>
          <label>Texto do botão<input name="yt_titulo" value="${esc(yt.titulo)}" placeholder="Acompanhe a Trip Angle no YouTube"></label></div>
        <label>Frase de apoio<input name="yt_texto" value="${esc(yt.texto)}" placeholder="Testes reais com IA, toda semana."></label>
        <div class="linha"><label>Site (link)<input name="site_url" value="${esc(site.url)}" placeholder="https://..."></label>
          <label>Texto do botão<input name="site_titulo" value="${esc(site.titulo)}" placeholder="Conheça a Trip Angle"></label></div>
        <span class="colchete" style="display:block;margin-top:6px">Materiais pagos</span>
        ${prods.map((x, i) => `<div class="linha" data-prod="${i}">
          <label>Nome<input data-campo-prod="titulo" value="${esc(x.titulo)}" placeholder="Ex.: Mentoria Direct Response"></label>
          <label>Link<input data-campo-prod="url" value="${esc(x.url)}" placeholder="https://..."></label>
          <label>Selo<input data-campo-prod="selo" value="${esc(x.selo)}" placeholder="Ex.: Mais procurado"></label>
          <label style="grid-column:1/-1">Descrição curta<input data-campo-prod="descricao" value="${esc(x.descricao)}" placeholder="O que a pessoa recebe, em uma frase."></label></div>`).join('')}
        <div class="acoes-form"><button class="btn vermelho" type="submit">Salvar CTAs</button></div>
      </form></div></div>`;
  }
  function posPublicar() {
    const fc = $('#formCta');
    fc.addEventListener('submit', async (e) => {
      e.preventDefault();
      const produtos = $$('[data-prod]', fc).map((r) => {
        const o = {};
        $$('input', r).forEach((el) => { o[el.dataset.campoProd] = el.value.trim(); });
        return o;
      }).filter((o) => o.url);
      const cta = {
        youtube: { url: fc.yt_url.value.trim(), titulo: fc.yt_titulo.value.trim(), texto: fc.yt_texto.value.trim() },
        site: { url: fc.site_url.value.trim(), titulo: fc.site_titulo.value.trim() },
        produtos,
      };
      const j = await acao(fc.querySelector('[type=submit]'), () => api('config', { cta }), 'CTAs salvos');
      if (j) { await ping(); await recarregar(); render(); }
    });
    const f = $('#formCfg');
    f.addEventListener('submit', async (e) => {
      e.preventDefault();
      const corpo = {};
      ['name', 'tagline', 'description', 'githubRepo', 'siteUrl', 'marketplaceName'].forEach((k) => { corpo[k] = f[k].value.trim(); });
      const j = await acao(f.querySelector('[type=submit]'), () => api('config', corpo), 'Configuração salva');
      if (j) { if (j.remoteAdded) toast('Remoto origin configurado'); await ping(); await recarregar(); render(); }
    });
    $('#publicarBtn').addEventListener('click', async (e) => {
      const j = await acao(e.currentTarget, () => api('publish', { message: $('#msgCommit').value.trim() || 'Atualiza a central' }));
      if (j) { logBox(saida(j)); await ping(); }
    });
    $('#rebuildBtn2').addEventListener('click', async (e) => {
      const j = await acao(e.currentTarget, () => api('rebuild', {}), 'Catálogo refeito');
      if (j) { logBox(saida(j)); await recarregar(); }
    });
  }

  // excluir (delegado)
  document.addEventListener('click', async (e) => {
    const b = e.target.closest('[data-excluir]');
    if (!b) return;
    const id = b.dataset.excluir;
    if (!confirm(`Excluir ${id}?\n\nO componente vai para a pasta .trash/ e sai do catálogo.`)) return;
    const j = await acao(b, () => api('component/delete', { id }), 'Excluído (está em .trash/)');
    if (j) { await recarregar(); render(); }
  });

  // ---------------------------------------------------------------- roteador
  const ROTAS = {
    '/': [pgPainel, posPainel], '/novo': [pgNovo, posNovo], '/importar': [pgImportar, posImportar], '/aitmpl': [pgAitmpl, posAitmpl],
    '/repos': [pgRepos, posRepos], '/plugin': [pgPlugin, posPlugin], '/gerenciar': [pgGerenciar, posGerenciar],
    '/categorias': [pgCategorias, posCategorias], '/publicar': [pgPublicar, posPublicar],
  };
  function render() {
    const [caminho, qs] = (location.hash.replace(/^#/, '') || '/').split('?');
    const p = new URLSearchParams(qs || '');
    const [pg, pos] = ROTAS[caminho] || ROTAS['/'];
    $('#admin').innerHTML = pg(p);
    $$('.lateral a').forEach((a) => a.classList.toggle('ativo', a.dataset.r === (ROTAS[caminho] ? caminho : '/')));
    pos(p);
  }

  async function iniciar() {
    try {
      await ping();
      await recarregar();
    } catch (e) {
      $('#admin').innerHTML = `<div class="vazio" style="margin-top:30px"><p class="h3">Painel desconectado</p>
        <p>O painel só funciona com o servidor local. Na pasta da central, rode:</p><div class="cmd" style="max-width:420px;margin:12px auto"><code>python3 tools/admin.py</code></div>
        <p class="muted">Detalhe: ${esc(e.message)}</p></div>`;
      $('#statusGit').innerHTML = '<span class="ponto off"></span>desconectado';
      return;
    }
    window.addEventListener('hashchange', () => { render(); window.scrollTo({ top: 0, behavior: 'instant' }); });
    render();
  }
  iniciar();
})();
