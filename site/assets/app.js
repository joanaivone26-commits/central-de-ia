/* Central Trip Angle — site do catálogo (sem framework, roteamento por hash) */
(() => {
  'use strict';

  const S = { cat: null, items: [], byId: new Map(), types: {}, cats: {}, stack: [], origin: '', limite: 60 };
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const norm = (s) => String(s ?? '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* sem armazenamento */ } },
  };

  const I = {
    copiar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="11" height="11" rx="1"/><path d="M5 15V5a1 1 0 0 1 1-1h10"/></svg>',
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m5 12 5 5 9-10"/></svg>',
    mais: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>',
    lixo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>',
    link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>',
    baixar: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 4v11m0 0-4-4m4 4 4-4M5 20h14"/></svg>',
    busca: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    ext: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 5h5v5M19 5l-8 8M18 14v5H5V6h5"/></svg>',
    estrela: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9L12 3Z"/></svg>',
    estrelaCheia: '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2"><path d="m12 3 2.8 5.7 6.2.9-4.5 4.4 1 6.2L12 17.3 6.5 20.2l1-6.2L3 9.6l6.2-.9L12 3Z"/></svg>',
    play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>',
  };
  const TRI = '<svg class="tri" viewBox="190 190 710 612" aria-hidden="true"><g fill="none" stroke="#CE0103" stroke-width="3"><polygon points="543,211 736,548 673,664 478,325"/><polygon points="406,434 532,434 334,782 210,782"/><polygon points="411,671 815,671 880,783 474,783"/></g></svg>';

  // ---------------------------------------------------------------- dados
  async function carregar() {
    const r = await fetch('api/catalog.json', { cache: 'no-cache' });
    if (!r.ok) throw new Error('HTTP ' + r.status);
    S.cat = await r.json();
    S.items = S.cat.items || [];
    S.items.forEach((it) => {
      S.byId.set(it.id, it);
      it._busca = norm([it.title, it.name, it.description, (it.tags || []).join(' '), it.category, it.author,
        it.source && it.source.repo].join(' '));
      it._titulo = norm(it.title + ' ' + it.name);
    });
    (S.cat.types || []).forEach((t) => { S.types[t.id] = t; });
    (S.cat.categories || []).forEach((c) => { S.cats[c.id] = c; });
    const hub = S.cat.hub || {};
    S.origin = (hub.siteUrl || (location.origin + location.pathname.replace(/[^/]*$/, ''))).replace(/\/+$/, '');
    S.stack = store.get('ta-stack', []).filter((id) => S.byId.has(id));
  }

  const tipo = (id) => S.types[id] || { label: id, singular: id, flag: '--' + id };
  const catInfo = (id) => S.cats[id] || { id, label: id, icon: '•' };
  const ref = (it) => `${it.category}/${it.name}`;
  const pyCmd = () => `python3 <(curl -fsSL ${S.origin}/tahub.py)`;
  const cmdItem = (it) => (it.type === 'sites' ? ((it.site || {}).url || '') : `${pyCmd()} ${tipo(it.type).flag} ${ref(it)}`);
  const instalavel = (it) => it.type !== 'sites';
  function seloStatus(it) {
    const st = it.status;
    if (!st) return '';
    const cfg = { testado: ['Testado', 'status-testado'], controle: ['Controle', 'cheio brilho'], rascunho: ['Rascunho', 'cinza'] }[st];
    return cfg ? `<span class="selo ${cfg[1]}" title="${esc(it.testedAt ? 'Testado em ' + it.testedAt : '')}"><span>${cfg[0]}</span></span>` : '';
  }
  const urlItem = (it) => `#/item/${it.id}`;
  const hub = () => (S.cat && S.cat.hub) || {};
  const mpNome = () => hub().marketplaceName || 'trip-angle';
  const mpAdd = () => (hub().githubRepo ? `/plugin marketplace add ${hub().githubRepo}` : null);
  const fmtBytes = (n) => (n > 1048576 ? (n / 1048576).toFixed(1) + ' MB' : n > 1024 ? Math.round(n / 1024) + ' KB' : (n || 0) + ' B');
  const fmtData = (d) => { if (!d) return '—'; const [y, m, dd] = d.split('-'); return `${dd}/${m}/${y}`; };

  function origemTexto(it) {
    const s = it.source || {};
    if (s.kind === 'github' && s.repo) return s.repo;
    if (s.kind === 'aitmpl') return 'via aitmpl.com';
    return it.author || 'Trip Angle';
  }
  function origemUrl(it) {
    const s = it.source || {};
    if (s.url) return s.url;
    if (s.repo) return `https://github.com/${s.repo}`;
    return null;
  }

  // ---------------------------------------------------------------- busca
  function buscar(q, base) {
    const termos = norm(q).split(/\s+/).filter(Boolean);
    const lista = base || S.items;
    if (!termos.length) return lista.slice();
    const out = [];
    for (const it of lista) {
      let pts = 0;
      let ok = true;
      for (const t of termos) {
        if (!it._busca.includes(t)) { ok = false; break; }
        if (it._titulo.includes(t)) pts += 10;
        if (norm(it.name) === t) pts += 20;
        if ((it.tags || []).some((g) => norm(g).includes(t))) pts += 4;
      }
      if (ok) { if (it.featured) pts += 2; out.push([pts, it]); }
    }
    out.sort((a, b) => b[0] - a[0] || a[1].title.localeCompare(b[1].title));
    return out.map((x) => x[1]);
  }

  function ordenar(lista, ordem) {
    const l = lista.slice();
    if (ordem === 'az') l.sort((a, b) => a.title.localeCompare(b.title, 'pt'));
    else if (ordem === 'recentes') l.sort((a, b) => String(b.addedAt).localeCompare(String(a.addedAt)) || a.title.localeCompare(b.title));
    else l.sort((a, b) => ((b.level === 'mestre') - (a.level === 'mestre')) || (b.featured - a.featured) || (a.partOf ? 1 : 0) - (b.partOf ? 1 : 0) || a.title.localeCompare(b.title, 'pt'));
    return l;
  }

  // ---------------------------------------------------------------- stack
  function salvarStack() {
    store.set('ta-stack', S.stack);
    const b = $('#stackBadge');
    b.dataset.n = S.stack.length;
    b.textContent = S.stack.length || '';
    $$('[data-stack]').forEach((el) => marcarBotao(el));
    if ($('#gaveta').classList.contains('aberta')) desenharStack();
  }
  function marcarBotao(el) {
    const on = S.stack.includes(el.dataset.stack);
    el.classList.toggle('na-stack', on);
    el.innerHTML = on ? I.ok : I.mais;
    el.setAttribute('aria-label', on ? 'Remover da stack' : 'Adicionar à stack');
    el.title = on ? 'Na sua stack (clique para remover)' : 'Adicionar à stack';
  }
  function alternarStack(id) {
    const i = S.stack.indexOf(id);
    if (i >= 0) { S.stack.splice(i, 1); toast('Removido da stack'); } else { S.stack.push(id); toast('Adicionado à stack'); }
    salvarStack();
  }
  function cmdStack(ids) {
    const porFlag = {};
    ids.map((id) => S.byId.get(id)).filter((it) => it && instalavel(it)).forEach((it) => {
      const f = tipo(it.type).flag;
      (porFlag[f] = porFlag[f] || []).push(ref(it));
    });
    const partes = Object.entries(porFlag).map(([f, v]) => `  ${f} ${v.join(',')}`);
    return partes.length ? `${pyCmd()} \\\n${partes.join(' \\\n')}` : '';
  }
  function desenharStack() {
    const lista = $('#stackLista');
    const rod = $('#stackRodape');
    if (!S.stack.length) {
      lista.innerHTML = `<div class="vazio" style="margin-top:12px"><p class="h3">Stack vazia</p><p>Clique no <b>+</b> dos componentes para juntar tudo num comando só.</p></div>`;
      rod.innerHTML = `<a class="btn" href="#/explorar">Explorar componentes</a>`;
      return;
    }
    lista.innerHTML = S.stack.map((id) => {
      const it = S.byId.get(id);
      return `<div class="linha-stack">
        <span class="selo cinza"><span>${esc(tipo(it.type).singular)}</span></span>
        <div><b><a href="${urlItem(it)}">${esc(it.title)}</a></b><small>${esc(ref(it))}</small></div>
        <button class="btn fantasma peq icone" data-remover="${esc(id)}" aria-label="Remover ${esc(it.title)}">${I.lixo}</button>
      </div>`;
    }).join('');
    const cmd = cmdStack(S.stack);
    rod.innerHTML = `
      <span class="colchete">${S.stack.length} componente${S.stack.length > 1 ? 's' : ''}</span>
      ${blocoCmd(cmd)}
      <p class="nota">Rode na pasta do projeto. O instalador mostra o que vai gravar e pede confirmação.</p>
      <div class="linha-btns">
        <button class="btn vermelho" data-copiar="${esc(cmd)}">${I.copiar} Copiar comando</button>
        <button class="btn" id="compartilharStack">${I.link} Link</button>
        <button class="btn fantasma" id="limparStack">Limpar</button>
      </div>`;
  }
  function abrirGaveta(abrir) {
    const g = $('#gaveta');
    g.classList.toggle('aberta', abrir);
    g.setAttribute('aria-hidden', String(!abrir));
    $('#veu').classList.toggle('aberto', abrir);
    if (abrir) desenharStack();
  }

  // ---------------------------------------------------------------- componentes de UI
  function blocoCmd(texto, prompt = true) {
    const linhas = esc(texto).replace(/(^|\s)(--?[a-z][a-z-]*)/g, '$1<span class="fl">$2</span>');
    return `<div class="cmd"><code>${prompt && !texto.startsWith('/') ? '<span class="p">$ </span>' : ''}${linhas}</code>
      <button class="btn fantasma peq icone" data-copiar="${esc(texto)}" aria-label="Copiar comando">${I.copiar}</button></div>`;
  }
  function selo(texto, extra = '') { return `<span class="selo ${extra}"><span>${esc(texto)}</span></span>`; }

  function card(it) {
    const c = catInfo(it.category);
    const tags = (it.tags || []).slice(0, 3).map((t) => `<span class="tag-x">${esc(t)}</span>`).join('');
    return `<article class="card ${it.featured ? 'destaque' : ''}">
      <div class="topo-card">${it.level === 'mestre' ? selo('Prompt mestre', 'cheio brilho') : selo(tipo(it.type).singular, it.featured ? 'cheio' : 'cinza')}${seloStatus(it)}<span class="cat">${esc(c.label)}</span></div>
      ${it.level === 'mestre' && (it.etapas || it.tempo) ? `<div class="meta-mestre">${it.etapas ? `<span><b>${it.etapas}</b> etapas</span>` : ''}${it.tempo ? `<span>${esc(it.tempo)}</span>` : ''}${(it.variables || []).length ? `<span><b>${it.variables.length}</b> insumos</span>` : ''}</div>` : ''}
      <h3 class="card-t"><a href="${urlItem(it)}">${esc(it.title)}</a></h3>
      <p class="desc">${esc(it.description || 'Sem descrição.')}</p>
      ${it.type === 'prompts' && it.preview ? `<p class="previa">${esc(it.preview)}</p>` : ''}
      ${it.type === 'prompts' ? `<div class="tags">${(it.variables || []).slice(0, 4).map((v) => `<span class="tag-x var">{{${esc(v.name)}}}</span>`).join('')}${(it.tools || []).slice(0, 3).map((t) => `<span class="tag-x ferr">${esc(nomeFerr(t))}</span>`).join('')}</div>`
        : it.type === 'repos' && it.detalhes ? `<div class="tags">${chipsRepo(it)}</div>` : tags ? `<div class="tags">${tags}</div>` : ''}
      <div class="rodape-card">
        <span class="orig">${it.partOf ? '<span class="ponto off"></span>parte de ' + esc(S.byId.get(it.partOf)?.title || 'plugin') : esc(origemTexto(it))}</span>
        <span class="btns">${instalavel(it) ? `
          <button class="btn peq icone" data-copiar="${esc(cmdItem(it))}" aria-label="Copiar comando de instalação" title="Copiar comando de instalação">${I.copiar}</button>
          <button class="btn peq icone" data-stack="${esc(it.id)}"></button>` : `
          <a class="btn peq" href="${esc(cmdItem(it))}" target="_blank" rel="noopener" style="position:relative;z-index:1">Abrir ${I.ext}</a>`}
          <button class="btn peq icone" data-fav="${esc(it.id)}"></button>
        </span>
      </div>
    </article>`;
  }

  function contar(tipoId) { return (S.cat.counts || {})[tipoId] || 0; }

  // ---------------------------------------------------------------- prompts
  const FERRAMENTAS = { claude: 'Claude', chatgpt: 'ChatGPT', gemini: 'Gemini', midjourney: 'Midjourney', ideogram: 'Ideogram',
    'gpt-image': 'GPT Image', veo: 'Veo', kling: 'Kling', runway: 'Runway', suno: 'Suno', elevenlabs: 'ElevenLabs', perplexity: 'Perplexity',
    manus: 'Manus', lovable: 'Lovable', codex: 'Codex', notion: 'Notion', heygen: 'HeyGen', capcut: 'CapCut' };
  const nomeFerr = (t) => FERRAMENTAS[String(t).toLowerCase()] || t;
  const LONGO = /transcri|texto|copy|coment|review|pagina|página|conteudo|conteúdo|roteiro|descri|lista|anuncio|anúncio|dados|metricas|métricas|historia|história|briefing|swipe|exemplo/i;
  const promptCache = new Map();
  async function textoPrompt(it) {
    if (promptCache.has(it.id)) return promptCache.get(it.id);
    const r = await fetch(it.base);
    if (!r.ok) throw new Error('HTTP ' + r.status);
    const bruto = await r.text();
    const m = bruto.match(/^---\s*\n[\s\S]*?\n---\s*\n?/);
    const corpo = (m ? bruto.slice(m[0].length) : bruto).trim();
    promptCache.set(it.id, corpo);
    return corpo;
  }
  function preencher(corpo, valores, vars) {
    const info = {};
    (vars || []).forEach((v) => { info[v.name] = v; });
    return corpo.replace(/\{\{\s*([A-Za-z0-9_]+)\s*\}\}/g, (todo, nome) => {
      const val = valores[nome] && valores[nome].trim();
      if (val) return val;
      const v = info[nome];
      if (v && v.default) return `${v.default} (padrão)`;
      if (v && v.required === false) return '(não informado)';
      return todo;
    });
  }
  function painelPrompt(it) {
    const vars = it.variables || [];
    const salvo = store.get('ta-vars-' + it.id, {});
    return `<div class="painel usar-prompt" style="margin-top:18px">
      <header><span class="ponto"></span><span class="colchete">Usar este prompt</span><a class="btn fantasma peq" href="#/perfil" title="Campos como produto, nicho e avatar vêm do seu perfil">Meu perfil</a>
        <span class="direita">${(it.tools || []).map((t) => `<span class="tag-x ferr">${esc(nomeFerr(t))}</span>`).join(' ')}</span></header>
      <div class="corpo">
        ${vars.length ? `<form class="form" id="formVars">${vars.map((v) => {
          const longo = LONGO.test(v.name + ' ' + v.label) || v.name === 'sua_oferta';
          const doPerfil = !salvo[v.name] && perfilValor(v.name);
          const val = esc(salvo[v.name] || perfilValor(v.name) || '');
          return `<label>${v.required ? '<span class="obrig" title="Obrigatório">●</span> ' : ''}${esc(v.label)}${v.required === false ? ` <span class="dica">(${v.default ? 'padrão: ' + esc(v.default) : 'opcional'})</span>` : ''} <span class="dica mono">{{${esc(v.name)}}}${doPerfil ? ' · <span style="color:var(--verde)">do seu perfil</span>' : ''}</span>${longo
            ? `<textarea name="${esc(v.name)}" rows="4" style="min-height:96px;font-family:var(--f-texto)">${val}</textarea>`
            : `<input name="${esc(v.name)}" value="${val}" autocomplete="off">`}</label>`;
        }).join('')}</form>` : '<p class="nota" style="margin-top:0">Este prompt não tem variáveis: é só copiar e usar.</p>'}
        ${it.output ? `<p class="nota"><b>Entrega:</b> ${esc(it.output)}</p>` : ''}
        <div class="previa-prompt"><pre id="promptFinal" class="cru">Carregando o prompt…</pre></div>
        <div class="acoes-prompt">
          <button class="btn vermelho" id="copiarPrompt">${I.copiar} Copiar prompt</button>
          <a class="btn" id="abrirClaude" target="_blank" rel="noopener">Abrir no Claude ${I.ext}</a>
          <a class="btn" id="abrirChatgpt" target="_blank" rel="noopener">Abrir no ChatGPT ${I.ext}</a>
          ${vars.length ? '<button class="btn fantasma" id="limparVars" type="button">Limpar campos</button>' : ''}
        </div>
        <p class="nota" id="notaFaltando"></p>
        ${ctaLinha()}
      </div>
    </div>`;
  }
  async function ligarPrompt(it) {
    const pre = $('#promptFinal');
    if (!pre) return;
    let corpo;
    try { corpo = await textoPrompt(it); } catch (e) { pre.textContent = 'Não consegui carregar o prompt (' + e.message + ').'; return; }
    const form = $('#formVars');
    const valores = () => { const v = {}; if (form) $$('input, textarea', form).forEach((el) => { v[el.name] = el.value; }); return v; };
    const atualizar = () => {
      const v = valores();
      const final = preencher(corpo, v, it.variables);
      pre.textContent = final;
      const faltam = (it.variables || []).filter((x) => x.required !== false && !(v[x.name] || '').trim()).map((x) => x.label);
      $('#notaFaltando').innerHTML = faltam.length ? `Faltam ${faltam.length} obrigatório(s): ${faltam.map(esc).join(', ')}. Você pode copiar assim mesmo: o modelo pede o que faltar numa única pergunta. Campos opcionais vazios usam o padrão.` : '<span style="color:var(--verde)">● Obrigatórios preenchidos. Opcionais vazios usam o padrão.</span>';
      const q = encodeURIComponent(final);
      const longo = q.length > 7500;
      [['#abrirClaude', 'https://claude.ai/new?q='], ['#abrirChatgpt', 'https://chatgpt.com/?q=']].forEach(([sel, base]) => {
        const a = $(sel);
        if (longo) { a.removeAttribute('href'); a.setAttribute('aria-disabled', 'true'); a.title = 'Texto longo demais para abrir pelo link: copie e cole.'; a.classList.add('desab'); }
        else { a.href = base + q; a.removeAttribute('aria-disabled'); a.title = ''; a.classList.remove('desab'); }
      });
      if (longo) $('#notaFaltando').innerHTML += ' Texto longo: use <b>Copiar prompt</b> e cole no chat.';
      store.set('ta-vars-' + it.id, v);
      return final;
    };
    if (form) form.addEventListener('input', atualizar);
    $('#copiarPrompt').addEventListener('click', (e) => copiar(atualizar(), e.currentTarget));
    const lv = $('#limparVars');
    if (lv) lv.addEventListener('click', () => { $$('input, textarea', form).forEach((el) => { el.value = ''; }); atualizar(); });
    atualizar();
  }

  function paginaPrompts(p) {
    const etapa = p.get('cat') || '';
    const ferr = p.get('ferramenta') || '';
    const q = p.get('q') || '';
    const todos = S.items.filter((i) => i.type === 'prompts');
    const porCat = {};
    todos.forEach((i) => { porCat[i.category] = (porCat[i.category] || 0) + 1; });
    const ferrs = {};
    todos.forEach((i) => (i.tools || []).forEach((t) => { ferrs[t] = (ferrs[t] || 0) + 1; }));
    let lista = todos.filter((i) => (!etapa || i.category === etapa) && (!ferr || (i.tools || []).includes(ferr)));
    lista = q ? buscar(q, lista) : ordenar(lista, 'destaque');
    const link = (o) => {
      const n = new URLSearchParams();
      Object.entries(Object.assign({ cat: etapa, ferramenta: ferr, q }, o)).forEach(([k, v]) => { if (v) n.set(k, v); });
      return '#/prompts' + (n.toString() ? '?' + n : '');
    };
    const ordemCats = (S.cat.categories || []).filter((c) => porCat[c.id]);
    const frameworks = S.items.filter((i) => i.type === 'frameworks');
    return `<section class="hero" style="padding-bottom:10px">${TRI}<div class="wrap">
        <span class="colchete">Biblioteca de prompts</span>
        <h1 class="titulo" style="font-size:clamp(40px,6vw,76px)">Prompts prontos<br>para <em>o digital</em></h1>
        <p class="lead">Espionagem, extração de copy, avatar, oferta, criativos e formatos. Preencha os campos, copie ou abra direto no Claude ou no ChatGPT. No Claude Code, cada prompt vira um <b>/comando</b>.</p>
      </div></section>
      <div class="wrap" style="position:relative;z-index:1;padding-bottom:60px">
        <div class="chips-cat" style="display:flex;flex-wrap:wrap">
          <a href="${link({ cat: '' })}" class="${!etapa ? 'ativo' : ''}">Todas as etapas · ${todos.length}</a>
          ${ordemCats.map((c) => `<a href="${link({ cat: c.id })}" class="${etapa === c.id ? 'ativo' : ''}">${esc(c.icon || '')} ${esc(c.label)} · ${porCat[c.id]}</a>`).join('')}
        </div>
        <div class="filtros">
          <label class="campo">${I.busca}<input id="filtroPrompts" type="search" value="${esc(q)}" placeholder="Buscar prompt: VSL, avatar, UGC, Biblioteca de Anúncios…" aria-label="Buscar prompt"></label>
          <select id="filtroFerr" aria-label="Ferramenta"><option value="">Qualquer ferramenta</option>${Object.keys(ferrs).sort().map((t) => `<option value="${esc(t)}" ${t === ferr ? 'selected' : ''}>${esc(nomeFerr(t))} (${ferrs[t]})</option>`).join('')}</select>
        </div>
        <p class="resumo">${lista.length} prompt${lista.length === 1 ? '' : 's'}${q ? ` para “${esc(q)}”` : ''}</p>
        ${(() => {
          const mestres = lista.filter((i) => i.level === 'mestre');
          const modulos = lista.filter((i) => i.level !== 'mestre');
          if (!lista.length) return `<div class="vazio"><p class="h3">Nenhum prompt aqui ainda</p><p>Cadastre pelo painel admin em <b>Criar prompt</b>.</p></div>`;
          return (mestres.length ? `<div class="cab" style="margin-top:8px"><div><span class="colchete">Prompts mestres</span><h2 class="h2">Uma missão <em>inteira</em> por prompt</h2>
              <p>Pedem todos os insumos de uma vez, executam as etapas em sequência, se revisam e entregam o resultado final. Menos idas e vindas, menos créditos gastos.</p></div></div>
              <div class="grid">${mestres.map(card).join('')}</div>` : '')
            + (modulos.length ? `${mestres.length ? '<div class="cab" style="margin-top:36px"><div><span class="colchete">Módulos</span><h2 class="h2">Partes da missão <em>sob medida</em></h2><p>Para quando você precisa de uma etapa específica.</p></div></div>' : ''}
              <div class="grid">${modulos.map(card).join('')}</div>` : '');
        })()}
        ${frameworks.length ? `<div class="cab" style="margin-top:44px"><div><span class="colchete">Frameworks</span><h2 class="h2">Os métodos <em>por trás</em></h2>
          <p>Estruturas de copy, oferta e criativos explicadas com exemplo e prompt para aplicar. No Claude Code, cada framework vira uma skill.</p></div>
          <a class="btn" href="#/explorar?tipo=frameworks">Ver todos</a></div>
          <div class="grid">${ordenar(frameworks, 'destaque').slice(0, 6).map(card).join('')}</div>` : ''}
      </div>`;
  }

  // ---------------------------------------------------------------- perfil da oferta
  const PERFIL = [
    ['produto', 'Produto ou oferta', 'Ex.: Curso Seca Barriga 30D', ['produto', 'produto_ou_oferta', 'nome_do_produto', 'oferta']],
    ['nicho', 'Nicho e subnicho', 'Ex.: emagrecimento para mulheres 35+', ['nicho', 'seu_nicho', 'produto_ou_nicho', 'subnicho']],
    ['avatar', 'Avatar: quem compra', 'Idade, momento de vida, o que já tentou, nível de consciência', ['avatar', 'publico', 'publico_alvo', 'persona']],
    ['promessa', 'Promessa principal', 'Ex.: perder a barriga em 30 dias sem academia', ['promessa', 'promessa_principal']],
    ['mecanismo', 'Mecanismo único', 'O porquê de funcionar: o problema real e a solução', ['mecanismo', 'mecanismo_unico', 'como_funciona']],
    ['preco', 'Preço e condições', 'Ex.: R$ 197 ou 12x de R$ 19,70, Pix e boleto', ['preco', 'preco_e_condicoes']],
    ['provas', 'Provas disponíveis', 'Depoimentos autorizados, números, estudos, autoridade', ['provas']],
    ['objecoes', 'Objeções principais', 'Ex.: falta de tempo, já tentei de tudo, é caro', ['objecoes']],
    ['mercado', 'Mercado', 'Brasil, EUA, LATAM…', ['mercado', 'pais']],
    ['tom', 'Tom de voz', 'Ex.: próximo, direto, sem jargão', ['tom', 'tom_de_voz']],
    ['plataformas', 'Canais e plataformas', 'Ex.: Meta Ads, Instagram, TikTok, WhatsApp', ['plataformas', 'plataforma', 'canais']],
  ];
  const perfil = () => store.get('ta-perfil', {});
  function perfilValor(nome) {
    const pf = perfil();
    if (nome === 'sua_oferta') {
      const partes = [['Produto', pf.produto], ['Nicho', pf.nicho], ['Público', pf.avatar], ['Promessa', pf.promessa], ['Mecanismo', pf.mecanismo], ['Preço', pf.preco]]
        .filter(([, v]) => v && v.trim()).map(([k, v]) => `${k}: ${v.trim()}`);
      return partes.join('\n');
    }
    const campo = PERFIL.find(([, , , al]) => al.includes(nome));
    return campo ? (pf[campo[0]] || '') : '';
  }
  function perfilMd() {
    const pf = perfil();
    return '# Perfil da oferta\n\n' + PERFIL.map(([k, l]) => `- **${l}:** ${(pf[k] || '').trim() || '—'}`).join('\n')
      + '\n\nGerado na Central Trip Angle. Coloque em `.claude/oferta.md` no projeto e peça ao Claude para ler antes de cada tarefa.\n';
  }
  function paginaPerfil() {
    const pf = perfil();
    const n = PERFIL.filter(([k]) => (pf[k] || '').trim()).length;
    return `<section class="bloco"><div class="wrap" style="max-width:860px">
      <span class="colchete">Meu perfil</span>
      <h1 class="titulo" style="font-size:clamp(36px,5vw,64px);margin:10px 0 12px">Sua oferta <em>uma vez só</em></h1>
      <p class="muted" style="margin:0 0 22px">Preencha os dados da oferta que você está trabalhando. Todo prompt da biblioteca que pedir esses campos já vem preenchido. Fica salvo só neste navegador; nada é enviado.</p>
      <form class="form" id="formPerfil">
        ${PERFIL.map(([k, l, ph]) => {
          const longo = ['avatar', 'mecanismo', 'provas', 'objecoes'].includes(k);
          return `<label>${esc(l)}${longo ? `<textarea name="${k}" rows="3" style="min-height:84px;font-family:var(--f-texto)" placeholder="${esc(ph)}">${esc(pf[k] || '')}</textarea>`
            : `<input name="${k}" value="${esc(pf[k] || '')}" placeholder="${esc(ph)}" autocomplete="off">`}</label>`;
        }).join('')}
        <div class="acoes-form">
          <button class="btn vermelho" type="button" id="baixarPerfil">${I.baixar} Baixar oferta.md</button>
          <button class="btn" type="button" id="copiarPerfil">${I.copiar} Copiar como texto</button>
          <button class="btn fantasma" type="button" id="limparPerfil">Limpar perfil</button>
          <span class="muted" id="perfilStatus">${n} de ${PERFIL.length} campos preenchidos</span>
        </div>
      </form>
      <div class="painel" style="margin-top:24px"><header><span class="colchete">Usar no Claude Code</span></header><div class="corpo">
        <p class="nota" style="margin-top:0">Baixe o <b>oferta.md</b>, coloque em <b class="mono">.claude/oferta.md</b> no projeto e acrescente no <b class="mono">CLAUDE.md</b>: “Antes de qualquer tarefa de marketing, leia .claude/oferta.md”. Os prompts instalados como comandos e as skills passam a usar esse contexto.</p>
      </div></div>
    </div></section>`;
  }
  function ligarPerfil() {
    const f = $('#formPerfil');
    if (!f) return;
    f.addEventListener('input', () => {
      const v = {};
      PERFIL.forEach(([k]) => { v[k] = f[k].value; });
      store.set('ta-perfil', v);
      $('#perfilStatus').textContent = `${PERFIL.filter(([k]) => (v[k] || '').trim()).length} de ${PERFIL.length} campos preenchidos · salvo`;
    });
    $('#baixarPerfil').addEventListener('click', () => {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([perfilMd()], { type: 'text/markdown' }));
      a.download = 'oferta.md'; document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    });
    $('#copiarPerfil').addEventListener('click', (e) => copiar(perfilMd(), e.currentTarget));
    $('#limparPerfil').addEventListener('click', () => { if (confirm('Apagar o perfil salvo neste navegador?')) { store.set('ta-perfil', {}); rota(); } });
  }

  // ---------------------------------------------------------------- trilha DR
  const TRILHA = [
    ['Pesquisa e espionagem', ['pesquisa'], 'Minere ofertas, mapeie funis e anúncios dos concorrentes e colete a linguagem do público.'],
    ['Avatar e oferta', ['estrategia'], 'Defina quem compra, a promessa, o mecanismo e a oferta.'],
    ['Copy', ['copy'], 'Leads, VSL, página de vendas e revisão.'],
    ['Criativos', ['criativos'], 'Hooks, ângulos, roteiros, storyboards e prompts de imagem e vídeo.'],
    ['Formatos e conteúdo', ['conteudo', 'seo'], 'Formatos virais, calendário, orgânico e busca.'],
    ['Funil e páginas', ['funil', 'cro', 'design', 'dev'], 'Quiz, páginas, checkout e conversão.'],
    ['Tráfego e tracking', ['trafego', 'analytics'], 'Campanhas, métricas, atribuição e escala.'],
    ['Pós-venda', ['vendas', 'email-whatsapp'], 'Recuperação, upsell, retenção e relacionamento.'],
    ['Produto', ['produto', 'documentos'], 'Entregáveis, bônus e materiais.'],
    ['Compliance', ['compliance'], 'Claims, políticas de anúncio e versão segura antes de publicar.'],
  ];
  const ORDEM_TIPO = ['prompts', 'frameworks', 'skills', 'agents', 'commands', 'mcps', 'templates', 'sites'];
  function paginaTrilha() {
    return `<section class="hero" style="padding-bottom:10px">${TRI}<div class="wrap">
        <span class="colchete">Trilha DR</span>
        <h1 class="titulo" style="font-size:clamp(40px,6vw,76px)">Da pesquisa<br>à <em>escala</em></h1>
        <p class="lead">A ordem do trabalho de resposta direta, com os prompts, frameworks, skills e agentes de cada etapa.</p>
      </div></section>
      <div class="wrap trilha-dr" style="position:relative;z-index:1;padding-bottom:60px">
      ${TRILHA.map(([titulo, cats, desc], n) => {
        const itens = S.items.filter((i) => cats.includes(i.category) && !i.partOf && i.type !== 'repos');
        const porTipo = {};
        itens.forEach((i) => { porTipo[i.type] = (porTipo[i.type] || 0) + 1; });
        const top = itens.slice().sort((a, b) => ((b.level === 'mestre') - (a.level === 'mestre')) || (ORDEM_TIPO.indexOf(a.type) - ORDEM_TIPO.indexOf(b.type)) || (b.featured - a.featured) || a.title.localeCompare(b.title, 'pt')).slice(0, 8);
        return `<article class="etapa">
          <div class="num">${String(n + 1).padStart(2, '0')}</div>
          <div class="conteudo-etapa">
            <h2 class="h3" style="font-size:28px">${esc(titulo)}</h2>
            <p class="muted" style="margin:4px 0 10px">${esc(desc)}</p>
            <div class="tags" style="margin-bottom:12px">${ORDEM_TIPO.filter((t) => porTipo[t]).map((t) => `<a class="tag-x" href="#/explorar?cat=${cats[0]}&tipo=${t}">${porTipo[t]} ${esc(tipo(t).label.toLowerCase())}</a>`).join('')}</div>
            ${top.length ? `<div class="filhos">${top.map((f) => `<a href="${urlItem(f)}">${f.level === 'mestre' ? selo('Mestre', 'cheio') : selo(tipo(f.type).singular, 'cinza')}<span>${esc(f.title)}</span></a>`).join('')}</div>` : '<p class="muted">Nada nesta etapa ainda.</p>'}
            ${itens.length > top.length ? `<p class="nota"><a href="#/explorar?cat=${cats[0]}" style="color:var(--neon)">Ver os ${itens.length} itens da etapa →</a></p>` : ''}
          </div>
        </article>`;
      }).join('')}
      </div>`;
  }

  // ---------------------------------------------------------------- kits curados
  function colecaoCard(col) {
    const itens = col.items.map((id) => S.byId.get(id)).filter(Boolean);
    return `<article class="kit">
      <div class="topo-card" style="display:flex;gap:8px;align-items:center">${selo('Kit curado', 'cheio brilho')}<span class="mono muted" style="font-size:12px">${itens.length} itens</span></div>
      <h3 class="h3">${esc(col.title)}</h3>
      <p>${esc(col.description || '')}</p>
      <div class="filhos" style="grid-template-columns:1fr">${itens.slice(0, 7).map((f) => `<a href="${urlItem(f)}">${selo(tipo(f.type).singular, 'cinza')}<span>${esc(f.title)}</span></a>`).join('')}</div>
      ${itens.length > 7 ? `<p class="nota" style="margin:0">+ ${itens.length - 7} itens</p>` : ''}
      <button class="btn vermelho" data-kit="${esc(col.id)}">${I.mais} Adicionar kit à stack</button>
    </article>`;
  }

  // ---------------------------------------------------------------- favoritos
  const favs = () => store.get('ta-favs', []);
  function alternarFav(id) {
    let f = favs();
    const tinha = f.includes(id);
    f = tinha ? f.filter((x) => x !== id) : f.concat(id);
    store.set('ta-favs', f);
    atualizarFavs();
    toast(tinha ? 'Removido dos favoritos' : 'Salvo nos favoritos');
  }
  function marcarFav(el) {
    const on = favs().includes(el.dataset.fav);
    el.classList.toggle('fav-on', on);
    el.innerHTML = on ? I.estrelaCheia : I.estrela;
    el.title = on ? 'Nos seus favoritos (clique para tirar)' : 'Salvar nos favoritos';
    el.setAttribute('aria-label', el.title);
  }
  function atualizarFavs() {
    const n = favs().filter((id) => S.byId.has(id)).length;
    const b = $('#favBadge');
    if (b) { b.dataset.n = n; b.textContent = n || ''; }
    $$('[data-fav]').forEach(marcarFav);
  }
  function paginaFavoritos() {
    const lista = favs().map((id) => S.byId.get(id)).filter(Boolean);
    const instalaveis = lista.filter(instalavel);
    return `<section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Meus favoritos</span><h1 class="titulo" style="font-size:clamp(36px,5vw,64px);margin:10px 0 8px">O seu <em>arsenal</em></h1>
        <p>Salvos só neste navegador. Clique na estrela de qualquer item para guardar aqui.</p></div>
        ${instalaveis.length ? `<button class="btn vermelho" data-favs-stack>${I.mais} Pôr os ${instalaveis.length} na stack</button>` : ''}</div>
      ${lista.length ? `<div class="grid">${lista.map(card).join('')}</div>` : '<div class="vazio"><p class="h3">Nenhum favorito ainda</p><p>Explore os <a href="#/prompts" style="color:var(--neon)">prompts</a> e as <a href="#/jornadas" style="color:var(--neon)">jornadas</a> e salve o que for usar.</p></div>'}
    </div></section>`;
  }

  // ---------------------------------------------------------------- repositórios: ficha técnica
  const urlSegura = (u) => (/^https?:\/\//i.test(String(u || '')) ? String(u) : '');
  function fichaTecnica(it) {
    const d = it.detalhes || {};
    const fontes = (it.fontes || []).map(urlSegura).filter(Boolean);
    return `<div class="painel" style="margin-top:18px"><header><span class="colchete">Ficha técnica</span>${it.subcategoria ? `<span class="direita"><span class="tag-x">${esc(it.subcategoria)}</span></span>` : ''}</header>
      <div class="corpo"><dl class="meta ficha">${Object.entries(d).map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl>
      ${fontes.length ? `<p class="nota">Fontes conferidas: ${fontes.map((u) => `<a href="${esc(u)}" target="_blank" rel="noopener" style="color:var(--neon)">${esc(u.replace(/^https?:\/\//, '').slice(0, 54))}</a>`).join(' · ')}</p>` : ''}
      <p class="nota">Estrelas, datas e licenças mudam. Confira o README e o LICENSE antes de usar em projeto comercial.</p></div></div>`;
  }
  const chipsRepo = (it) => {
    const d = it.detalhes || {};
    const mac = d['Roda no Mac'];
    const com = d['Uso comercial'];
    const cor = (v) => (/^sim/i.test(v || '') ? 'ok' : /^n[ãa]o/i.test(v || '') ? 'nao' : 'talvez');
    return `${it.subcategoria ? `<span class="tag-x">${esc(it.subcategoria)}</span>` : ''}${mac ? `<span class="tag-x chip-${cor(mac)}">Mac: ${esc(mac)}</span>` : ''}${com ? `<span class="tag-x chip-${cor(com)}">Comercial: ${esc(com)}</span>` : ''}`;
  };

  // ---------------------------------------------------------------- CTAs
  function ctaCfg() { return hub().cta || {}; }
  function ctaBloco(titulo) {
    const c = ctaCfg();
    const yt = c.youtube && urlSegura(c.youtube.url) ? c.youtube : null;
    const site = c.site && urlSegura(c.site.url) ? c.site : null;
    const prods = (c.produtos || []).filter((p) => urlSegura(p.url));
    if (!yt && !site && !prods.length) return '';
    return `<section class="bloco cta-bloco"><div class="wrap">
      <div class="cta">
        <div><span class="colchete">Vá além</span><h2 class="h2">${titulo || 'Aprenda com quem <em>testa na prática</em>'}</h2>
          <p>${esc((yt && yt.texto) || 'Conteúdo novo toda semana sobre IA aplicada ao digital.')}</p></div>
        <div class="cta-acoes">
          ${yt ? `<a class="btn vermelho" href="${esc(yt.url)}" target="_blank" rel="noopener">${I.play} ${esc(yt.titulo || 'YouTube')}</a>` : ''}
          ${site ? `<a class="btn" href="${esc(site.url)}" target="_blank" rel="noopener">${esc(site.titulo || 'Site')} ${I.ext}</a>` : ''}
        </div>
      </div>
      ${prods.length ? `<div class="grid kits" style="margin-top:16px">${prods.map((p) => `<a class="kit produto" href="${esc(p.url)}" target="_blank" rel="noopener">
          ${p.selo ? `<div>${selo(p.selo, 'cheio brilho')}</div>` : ''}<h3 class="h3">${esc(p.titulo)}</h3><p>${esc(p.descricao || '')}</p>
          <span class="btn vermelho peq" style="align-self:flex-start">Conhecer ${I.ext}</span></a>`).join('')}</div>` : ''}
    </div></section>`;
  }
  function ctaLinha() {
    const c = ctaCfg();
    const yt = c.youtube && urlSegura(c.youtube.url) ? c.youtube : null;
    const p = (c.produtos || []).find((x) => urlSegura(x.url));
    if (!yt && !p) return '';
    return `<p class="nota cta-linha"><span style="color:var(--neon)">▲</span> Gostou? ${yt ? `<a href="${esc(yt.url)}" target="_blank" rel="noopener">${esc(yt.titulo || 'YouTube da Trip Angle')}</a>` : ''}${yt && p ? ' · ' : ''}${p ? `<a href="${esc(p.url)}" target="_blank" rel="noopener">${esc(p.titulo)}</a>` : ''}</p>`;
  }

  // ---------------------------------------------------------------- jornadas
  const jornadas = () => S.cat.journeys || [];
  const progresso = (id) => store.get('ta-jornada-' + id, []);
  function jornadaCard(j) {
    const n = (j.passos || []).length;
    const feitos = progresso(j.id).length;
    return `<a class="kit jornada-card" href="#/jornada/${esc(j.id)}">
      <div style="display:flex;gap:8px;align-items:center">${selo(`${n} passos`, feitos ? 'cheio' : '')}${feitos ? `<span class="mono muted" style="font-size:12px">${feitos}/${n} feitos</span>` : ''}</div>
      <span class="ic-grande" aria-hidden="true">${esc(j.icone || '▲')}</span>
      <h3 class="h3">${esc(j.titulo)}</h3>
      <p style="color:var(--gelo);font-weight:600">${esc(j.subtitulo || '')}</p>
      <p>${esc(j.para || '')}</p>
    </a>`;
  }
  function paginaJornadas() {
    return `<section class="hero" style="padding-bottom:10px">${TRI}<div class="wrap">
        <span class="colchete">Comece aqui</span>
        <h1 class="titulo" style="font-size:clamp(40px,6vw,76px)">Qual é o seu<br><em>objetivo</em>?</h1>
        <p class="lead">Escolha a jornada e siga os passos na ordem. Cada passo diz qual prompt usar, o que dá apoio (frameworks, skills, MCPs e repositórios), o que você entrega e o que levar para o passo seguinte.</p>
      </div></section>
      <div class="wrap" style="position:relative;z-index:1;padding-bottom:30px">
        <div class="grid kits">${jornadas().map(jornadaCard).join('')}</div>
        <p class="nota" style="margin-top:18px">Prefere ver por etapa do trabalho? Abra a <a href="#/trilha" style="color:var(--neon)">Trilha DR</a>. Quer criar o seu próprio prompt? Use o <a href="#/montador" style="color:var(--neon)">montador</a>.</p>
      </div>${ctaBloco()}`;
  }
  function paginaJornada(id) {
    const j = jornadas().find((x) => x.id === id);
    if (!j) return '<div class="wrap" style="padding:60px 0"><div class="vazio"><p class="h3">Jornada não encontrada</p><p><a href="#/jornadas" style="color:var(--neon)">Ver todas</a></p></div></div>';
    const feitos = progresso(j.id);
    const n = j.passos.length;
    const pct = Math.round((feitos.length / Math.max(n, 1)) * 100);
    const mini = (it) => `<a class="principal" href="${urlItem(it)}">${it.level === 'mestre' ? selo('Prompt mestre', 'cheio') : selo(tipo(it.type).singular, 'cinza')}<span><b>${esc(it.title)}</b><small>${esc(it.description || '')}</small></span><span class="abrir">Abrir →</span></a>`;
    return `<section class="hero" style="padding-bottom:16px">${TRI}<div class="wrap">
        <nav class="trilha" aria-label="Trilha"><a href="#/jornadas">Jornadas</a><i>/</i><span>${esc(j.titulo)}</span></nav>
        <span class="colchete">Jornada · ${n} passos</span>
        <h1 class="titulo" style="font-size:clamp(38px,6vw,72px);margin:12px 0 12px">${esc(j.titulo)}</h1>
        <div class="jornada-info"><div><b>Para quem</b><p>${esc(j.para || '')}</p></div><div><b>Resultado</b><p>${esc(j.resultado || '')}</p></div></div>
        <div class="barra-progresso" role="progressbar" aria-valuenow="${pct}" aria-valuemin="0" aria-valuemax="100"><span style="width:${pct}%"></span></div>
        <p class="nota">${feitos.length} de ${n} passos concluídos · salvo neste navegador</p>
        <div class="acoes-prompt"><button class="btn vermelho" data-jornada-stack="${esc(j.id)}">${I.mais} Pôr a jornada inteira na stack</button>
          ${feitos.length ? `<button class="btn fantasma" data-jornada-reset="${esc(j.id)}">Recomeçar</button>` : ''}</div>
      </div></section>
      <div class="wrap jornada" style="position:relative;z-index:1">
      ${j.passos.map((ps, i) => {
        const it = ps.principal ? S.byId.get(ps.principal) : null;
        const apoio = (ps.apoio || []).map((x) => S.byId.get(x)).filter(Boolean);
        const ok = feitos.includes(i);
        return `<article class="passo ${ok ? 'feito' : ''}">
          <div class="num">${String(i + 1).padStart(2, '0')}</div>
          <div class="conteudo-passo">
            <div class="passo-topo"><h2 class="h3">${esc(ps.titulo)}</h2>
              <label class="check"><input type="checkbox" data-passo="${i}" data-jornada="${esc(j.id)}" ${ok ? 'checked' : ''}> Concluído</label></div>
            <p class="muted" style="margin:4px 0 12px">${esc(ps.objetivo || '')}</p>
            ${it ? mini(it) : '<p class="nota">Item em preparação.</p>'}
            ${apoio.length ? `<div class="apoio"><span class="rotulo">Apoio</span>${apoio.map((a) => `<a class="tag-x" href="${urlItem(a)}">${esc(tipo(a.type).singular)} · ${esc(a.title)}</a>`).join('')}</div>` : ''}
            <dl class="meta" style="margin-top:12px"><dt>Entrega</dt><dd>${esc(ps.entrega || '')}</dd><dt>Leve adiante</dt><dd>${esc(ps.leve || '')}</dd></dl>
          </div>
        </article>`;
      }).join('')}
      </div>${ctaBloco('Quer acelerar essa jornada?')}`;
  }

  // ---------------------------------------------------------------- montador de prompt mestre
  const MONTADOR_PADRAO = {
    titulo: '', resultado: '', papel: '', nivel: 'mestre', etapaTrilha: '', tempo: '15-30 min', criterios: '',
    insumos: [{ nome: 'produto', rotulo: 'Produto ou oferta', tipo: 'obrigatorio', padrao: '' }, { nome: 'publico', rotulo: 'Público-alvo', tipo: 'obrigatorio', padrao: '' }, { nome: 'destino', rotulo: 'Onde entregar', tipo: 'padrao', padrao: 'aqui no chat' }],
    etapas: [{ nome: '', objetivo: '', passos: '', saida: '' }],
    entregavel: '', naoEntregar: '', checklist: '', limites: '',
  };
  const montador = () => Object.assign({}, MONTADOR_PADRAO, store.get('ta-montador', {}));
  const snake = (s) => String(s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_+|_+$/g, '').slice(0, 40);
  const linhas = (s) => String(s || '').split('\n').map((x) => x.trim()).filter(Boolean);
  function gerarPrompt(d) {
    const ins = d.insumos.filter((x) => x.nome || x.rotulo).map((x) => Object.assign({}, x, { nome: snake(x.nome || x.rotulo) }));
    const rot = (x) => (x.tipo === 'obrigatorio' ? '[obrigatório] ' : x.tipo === 'padrao' && x.padrao ? `[padrão = ${x.padrao}] ` : '[opcional] ') + (x.rotulo || x.nome);
    const etapas = d.etapas.filter((e) => e.nome || e.objetivo || e.passos);
    const titulo = d.titulo || 'Meu prompt';
    const fm = ['---', `title: ${titulo}`, `description: ${(d.resultado || '').replace(/\n/g, ' ')}`, `level: ${d.nivel}`, `stage: ${d.etapaTrilha || 'geral'}`,
      `etapas: ${etapas.length}`, `tempo: ${d.tempo}`, 'variables:', ...ins.map((x) => `  ${x.nome}: "${rot(x).replace(/"/g, "'")}"`),
      'tools: [claude, chatgpt, gemini]', `output: ${(d.entregavel || '').split('\n')[0]}`, 'tags: []', 'author: Trip Angle', '---', ''];
    const crit = linhas(d.criterios);
    const corpo = [
      `# ${titulo} · ${d.nivel === 'mestre' ? 'Prompt mestre' : 'Módulo'}`, '',
      '## 1. Papel e missão', `Você é ${d.papel || '[papel sênior]'}. Sua missão é entregar, nesta execução, ${d.resultado || '[resultado]'}.`, '',
      ...(crit.length ? ['O que separa a entrega profissional da amadora nesta missão:', ...crit.map((c) => `- ${c}`), ''] : []),
      '## 2. Modo de execução',
      '- Execução única: ler → pesquisar → construir → revisar → entregar. Dúvidas só na pré-checagem (seção 4), num bloco único. Depois de começar, nenhuma pergunta: lacuna vira premissa marcada [PREMISSA].',
      '- Sem planejamento extra, sem rascunhos intermediários e sem notas de processo. A entrega começa pelo contrato.',
      `- Entregar: ${d.entregavel ? d.entregavel.split('\n')[0] : '[o artefato exato]'}.${d.naoEntregar ? ` Não entregar: ${d.naoEntregar}.` : ''}`,
      '- Economia: não repita nem resuma os insumos; tabelas em vez de prosa; alternativas só onde decidem resultado.',
      '- Se a resposta acabar, pare no fim de uma etapa, escreva ESTADO ATUAL / PRÓXIMA AÇÃO e retome quando o usuário escrever CONTINUAR.',
      '- Evidência rotulada: FATO (com fonte), ALEGAÇÃO, HIPÓTESE, NÃO MAPEADO. Nunca invente URL, número ou depoimento.', '',
      '## 3. Insumos', ...ins.map((x) => `- ${x.rotulo || x.nome}: {{${x.nome}}}${x.tipo === 'padrao' && x.padrao ? ` (padrão: ${x.padrao})` : ''}`),
      'Campo vazio ou ainda entre chaves duplas usa o padrão; opcional vazio fica de fora.', '',
      '## 4. Contrato de entrega e pré-checagem',
      '### Etapa 0 · Inventário', '1. Liste o que recebeu ("RECEBIDO X/N"): anexos, links, transcrições.', '2. Se faltar insumo obrigatório, peça TODOS os que faltam numa única pergunta e pare.', '3. Abra a resposta com a tabela:', '',
      '| Critério | Meta | Como vou medir |', '|---|---|---|', ...(crit.length ? crit.map((c) => `| ${c} | | |`) : ['| | | |']), '',
      '## 5. Etapas',
      ...etapas.flatMap((e, i) => [`### Etapa ${i + 1} · ${e.nome || 'Etapa'}`, `**Objetivo:** ${e.objetivo || ''}`, ...linhas(e.passos).map((p, k) => `${k + 1}. ${p.replace(/^\d+[.)]\s*/, '')}`),
        `**Saída:** ${e.saida || ''}`, '**Checkpoint:** confira a saída contra o critério desta etapa antes de seguir; não pergunte, corrija.', '']),
      '## 6. Entregável final', ...linhas(d.entregavel).map((l) => `- ${l}`),
      '- Resumo de até 5 linhas com o status do contrato.', '- Handoff: os dados mínimos para a próxima missão e a próxima ação única.', '',
      '## 7. Autoverificação final', ...(linhas(d.checklist).length ? linhas(d.checklist) : ['Todos os insumos obrigatórios foram usados', 'Cada etapa entregou a saída no formato pedido']).map((c) => `- [ ] ${c}`),
      '- [ ] Varredura: nenhum resíduo de processo ("status", "versão", "placeholder", "a confirmar").',
      'Status por requisito: CONCLUÍDO, PARCIAL (com o número real) ou BLOQUEADO (com o que destrava). Corrija o que falhar antes de entregar.', '',
      '## 8. Limites e riscos', ...(linhas(d.limites).length ? linhas(d.limites).map((l) => `- ${l}`) : []),
      '- Não invente depoimento, prova, número ou resultado: o que precisa de prova fica [PROVA A INSERIR].',
      '- Sem avisos legais dentro das peças; riscos numa seção separada de até 5 linhas.',
    ];
    return fm.join('\n') + corpo.join('\n') + '\n';
  }
  function linhaInsumo(x, i) {
    return `<div class="linha-montador" data-insumo="${i}">
      <input data-campo="rotulo" value="${esc(x.rotulo)}" placeholder="Rótulo (ex.: Produto ou oferta)" aria-label="Rótulo do insumo">
      <select data-campo="tipo" aria-label="Tipo"><option value="obrigatorio" ${x.tipo === 'obrigatorio' ? 'selected' : ''}>Obrigatório</option><option value="opcional" ${x.tipo === 'opcional' ? 'selected' : ''}>Opcional</option><option value="padrao" ${x.tipo === 'padrao' ? 'selected' : ''}>Com padrão</option></select>
      <input data-campo="padrao" value="${esc(x.padrao)}" placeholder="Valor padrão" aria-label="Valor padrão" ${x.tipo === 'padrao' ? '' : 'hidden'}>
      <button type="button" class="btn fantasma peq icone" data-remover-insumo="${i}" aria-label="Remover insumo">${I.lixo}</button></div>`;
  }
  function blocoEtapa(e, i) {
    return `<div class="painel etapa-montador" data-etapa="${i}"><header><span class="colchete">Etapa ${i + 1}</span><span class="direita"><button type="button" class="btn fantasma peq" data-remover-etapa="${i}">Remover</button></span></header>
      <div class="corpo form"><div class="linha"><label>Nome<input data-campo="nome" value="${esc(e.nome)}" placeholder="Ex.: Diagnóstico"></label><label>Objetivo<input data-campo="objetivo" value="${esc(e.objetivo)}" placeholder="Uma linha"></label></div>
      <label>Passos (um por linha)<textarea data-campo="passos" style="min-height:96px;font-family:var(--f-texto)">${esc(e.passos)}</textarea></label>
      <label>Saída (formato exato)<input data-campo="saida" value="${esc(e.saida)}" placeholder="Ex.: tabela Dor | Frase real | Fonte"></label></div></div>`;
  }
  function paginaMontador() {
    const d = montador();
    const regras = [
      ['Execução única', 'Peça todos os insumos de uma vez e execute tudo numa resposta: ler, pesquisar, construir, revisar, entregar.'],
      ['Meta é meta', 'Números claros (quantidade, corte, duração). O modelo não pode reduzir nem trocar o recorte para bater a meta.'],
      ['Entregar X, não Y', 'Diga o artefato exato e o que é proibido entregar no lugar (ex.: o prompt, não a imagem).'],
      ['Etapas com checkpoint', 'Cada etapa tem objetivo, passos, saída em formato fechado e uma autoavaliação, nunca uma pergunta.'],
      ['Evidência rotulada', 'FATO, ALEGAÇÃO, HIPÓTESE. Nada de link, número ou depoimento inventado.'],
      ['Contrato e status', 'Abra com Critério | Meta | Como vou medir e feche com CONCLUÍDO, PARCIAL ou BLOQUEADO.'],
      ['Economia de tokens', 'Sem introdução, sem repetir insumos, tabelas em vez de prosa, alternativas só onde decidem.'],
      ['Handoff', 'Termine com o que a próxima etapa precisa, para não refazer pesquisa.'],
    ];
    return `<div class="wrap montador">
      <div>
        <span class="colchete">Montador de prompt</span>
        <h1 class="titulo" style="font-size:clamp(34px,5vw,60px);margin:10px 0 12px">Crie o seu <em>prompt mestre</em></h1>
        <p class="muted" style="margin:0 0 20px">Preencha os campos e o prompt sai no padrão da Central, com as 8 seções. O rascunho fica salvo neste navegador.</p>
        <form class="form" id="formMontador">
          <div class="linha"><label>Nome do prompt<input name="titulo" value="${esc(d.titulo)}" placeholder="Ex.: Roteiro de anúncio para nutra"></label>
            <label>Nível<select name="nivel"><option value="mestre" ${d.nivel === 'mestre' ? 'selected' : ''}>Prompt mestre (missão inteira)</option><option value="modulo" ${d.nivel === 'modulo' ? 'selected' : ''}>Módulo (uma parte)</option></select></label></div>
          <label>Resultado que ele entrega<textarea name="resultado" style="min-height:70px;font-family:var(--f-texto)" placeholder="Ex.: 10 roteiros de anúncio prontos para gravar, com hook, corpo e CTA, testáveis por ângulo">${esc(d.resultado)}</textarea></label>
          <div class="linha"><label>Papel do modelo<input name="papel" value="${esc(d.papel)}" placeholder="Ex.: estrategista sênior de criativos de direct response"></label>
            <label>Etapa da trilha<input name="etapaTrilha" value="${esc(d.etapaTrilha)}" placeholder="Ex.: criativos"></label>
            <label>Tempo típico<input name="tempo" value="${esc(d.tempo)}"></label></div>
          <label>O que separa o profissional do amador (um por linha)<textarea name="criterios" style="min-height:84px;font-family:var(--f-texto)" placeholder="Ex.: 30 hooks pontuados, só os 18+ entram">${esc(d.criterios)}</textarea></label>
          <div class="painel"><header><span class="colchete">Insumos</span><span class="direita"><button type="button" class="btn peq" id="addInsumo">+ Insumo</button></span></header>
            <div class="corpo" id="insumos">${d.insumos.map(linhaInsumo).join('')}</div></div>
          <div id="etapas">${d.etapas.map(blocoEtapa).join('')}</div>
          <button type="button" class="btn" id="addEtapa">+ Etapa</button>
          <label>Entregável final (um item por linha)<textarea name="entregavel" style="min-height:84px;font-family:var(--f-texto)">${esc(d.entregavel)}</textarea></label>
          <div class="linha"><label>Não entregar no lugar<input name="naoEntregar" value="${esc(d.naoEntregar)}" placeholder="Ex.: esqueleto vazio, resumo, exemplos genéricos"></label></div>
          <label>Checklist de qualidade (um por linha)<textarea name="checklist" style="min-height:84px;font-family:var(--f-texto)">${esc(d.checklist)}</textarea></label>
          <label>Limites e riscos (um por linha)<textarea name="limites" style="min-height:70px;font-family:var(--f-texto)">${esc(d.limites)}</textarea></label>
        </form>
      </div>
      <aside class="lado">
        <div class="painel"><header><span class="ponto"></span><span class="colchete">Seu prompt</span></header><div class="corpo">
          <div class="acoes-prompt" style="margin-top:0"><button class="btn vermelho" id="copiarMontado">${I.copiar} Copiar</button><button class="btn" id="baixarMontado">${I.baixar} Baixar .md</button><button class="btn fantasma" id="limparMontador">Limpar</button></div>
          <div class="previa-prompt"><pre class="cru" id="previaMontador" style="max-height:52vh"></pre></div>
          <p class="nota">Quer publicar na Central? Leve o .md para o painel admin, em <b>Criar prompt</b>.</p></div></div>
        <div class="painel"><header><span class="colchete">Como formular prompts</span></header><div class="corpo">
          <dl class="meta">${regras.map(([a, b]) => `<dt>${a}</dt><dd>${b}</dd>`).join('')}</dl>
          <p class="nota">O padrão completo está em <a href="#/como-usar" style="color:var(--neon)">Como usar</a>. Veja um exemplo pronto: <a href="#/item/prompts/copy/vsl-do-zero" style="color:var(--neon)">VSL do zero</a>.</p></div></div>
      </aside>
    </div>`;
  }
  function ligarMontador() {
    const f = $('#formMontador');
    if (!f) return;
    const ler = () => {
      const d = montador();
      ['titulo', 'resultado', 'papel', 'nivel', 'etapaTrilha', 'tempo', 'criterios', 'entregavel', 'naoEntregar', 'checklist', 'limites'].forEach((k) => { d[k] = f[k].value; });
      d.insumos = $$('[data-insumo]').map((r) => ({ rotulo: r.querySelector('[data-campo=rotulo]').value, nome: r.querySelector('[data-campo=rotulo]').value, tipo: r.querySelector('[data-campo=tipo]').value, padrao: r.querySelector('[data-campo=padrao]').value }));
      d.etapas = $$('[data-etapa]').map((r) => ({ nome: r.querySelector('[data-campo=nome]').value, objetivo: r.querySelector('[data-campo=objetivo]').value, passos: r.querySelector('[data-campo=passos]').value, saida: r.querySelector('[data-campo=saida]').value }));
      return d;
    };
    const atualizar = () => { const d = ler(); store.set('ta-montador', d); $('#previaMontador').textContent = gerarPrompt(d); };
    const redesenhar = (d) => { store.set('ta-montador', d); const y = window.scrollY; rota(); window.scrollTo(0, y); };
    f.addEventListener('input', (e) => {
      if (e.target.matches('[data-campo=tipo]')) { const pd = e.target.parentElement.querySelector('[data-campo=padrao]'); pd.hidden = e.target.value !== 'padrao'; }
      atualizar();
    });
    f.addEventListener('change', atualizar);
    $('#addInsumo').addEventListener('click', () => { const d = ler(); d.insumos.push({ nome: '', rotulo: '', tipo: 'opcional', padrao: '' }); redesenhar(d); });
    $('#addEtapa').addEventListener('click', () => { const d = ler(); d.etapas.push({ nome: '', objetivo: '', passos: '', saida: '' }); redesenhar(d); });
    f.addEventListener('click', (e) => {
      const ri = e.target.closest('[data-remover-insumo]');
      const re = e.target.closest('[data-remover-etapa]');
      if (ri) { const d = ler(); d.insumos.splice(+ri.dataset.removerInsumo, 1); redesenhar(d); }
      if (re) { const d = ler(); d.etapas.splice(+re.dataset.removerEtapa, 1); if (!d.etapas.length) d.etapas.push({ nome: '', objetivo: '', passos: '', saida: '' }); redesenhar(d); }
    });
    $('#copiarMontado').addEventListener('click', (e) => copiar(gerarPrompt(ler()), e.currentTarget));
    $('#baixarMontado').addEventListener('click', () => {
      const d = ler();
      const a = document.createElement('a');
      a.href = URL.createObjectURL(new Blob([gerarPrompt(d)], { type: 'text/markdown' }));
      a.download = (snake(d.titulo).replace(/_/g, '-') || 'meu-prompt') + '.md';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    });
    $('#limparMontador').addEventListener('click', () => { if (confirm('Apagar o rascunho do montador?')) { store.set('ta-montador', {}); rota(); } });
    atualizar();
  }

  // ---------------------------------------------------------------- páginas
  function paginaInicio() {
    const h = hub();
    const tipos = (S.cat.types || []).filter((t) => t.count > 0);
    const destaques = ordenar(S.items.filter((i) => i.featured), 'destaque').slice(0, 8);
    const recentes = ordenar(S.items.filter((i) => !i.partOf), 'recentes').slice(0, 8);
    const kits = kitsLista().slice(0, 6);
    const cats = (S.cat.categories || []).filter((c) => c.count > 0);
    const prompts = ordenar(S.items.filter((i) => i.type === 'prompts'), 'destaque').slice(0, 6);
    return `
    <section class="hero">${TRI}
      <div class="wrap">
        <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap"><span class="colchete">Central de IA Trip Angle</span>${selo('Grátis · sem login', 'cheio brilho')}</div>
        <h1 class="titulo">Toda a IA que o seu<br><em>projeto digital</em> precisa</h1>
        <p class="lead">${esc(h.description || '')} Siga a jornada do seu objetivo, copie o prompt, instale no Claude Code e execute.</p>
        <form class="hero-busca" id="heroBusca" role="search">
          ${I.busca}
          <input name="q" type="search" placeholder="Ex.: copy de VSL, Meta Ads, tracking, thumbnail…" aria-label="Buscar no catálogo">
          <button class="btn vermelho" type="submit">Buscar</button>
        </form>
        <div class="etapas" aria-hidden="true"><span><b class="ponto"></b>Escolha</span><i></i><span><b class="ponto"></b>Combine</span><i></i><span><b class="ponto"></b>Instale</span><i></i><span><b class="ponto"></b>Execute</span></div>
        <div class="numeros">
          <a href="#/explorar"><b>${S.cat.counts.total}</b><small><span class="ponto"></span>Componentes</small></a>
          ${tipos.map((t) => `<a href="#/explorar?tipo=${t.id}"><b>${t.count}</b><small>${esc(t.label)}</small></a>`).join('')}
          <a href="#/kits"><b>${(S.cat.bundles || []).length}</b><small>Kits</small></a>
        </div>
      </div>
    </section>

    <section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Começo rápido</span><h2 class="h2">Um comando, <em>tudo instalado</em></h2>
        <p>Rode na pasta do projeto. Precisa só do Python 3 e do Claude Code. Depois é abrir o Claude ali mesmo.</p></div>
        <a class="btn" href="#/como-usar">Guia completo</a></div>
      <div class="terminal"><div class="barra"><i></i><i></i><i></i><span>terminal</span></div>
        ${blocoCmd(`${pyCmd()}`)}
        ${destaques[0] ? blocoCmd(cmdItem(destaques.find((d) => d.type === 'skills') || destaques[0])) : ''}
        ${blocoCmd(`${pyCmd()} --search "meta ads"`)}
      </div>
    </div></section>

    ${jornadas().length ? `<section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Comece aqui</span><h2 class="h2">Qual é o seu <em>objetivo</em>?</h2>
        <p>Cada jornada mostra a sequência certa: o prompt de cada passo, o que usar de apoio e o que levar para o passo seguinte.</p></div>
        <a class="btn" href="#/jornadas">Ver jornadas</a></div>
      <div class="grid kits">${jornadas().map(jornadaCard).join('')}</div>
    </div></section>` : ''}

    ${prompts.length ? `<section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Biblioteca de prompts</span><h2 class="h2">O prompt certo para <em>cada etapa</em></h2>
        <p>Espionagem, avatar, oferta, copy, criativos e formatos. Preencha os campos e abra no Claude ou no ChatGPT.</p></div>
        <a class="btn vermelho" href="#/prompts">Abrir a biblioteca</a></div>
      <div class="grid">${prompts.map(card).join('')}</div>
    </div></section>` : ''}

    ${kits.length ? `<section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Kits prontos</span><h2 class="h2">Instale uma <em>área inteira</em></h2>
        <p>Cada kit é um plugin do Claude Code com as skills, agentes e comandos de uma área. Instala pelo marketplace e atualiza sozinho.</p></div>
        <a class="btn" href="#/kits">Ver todos</a></div>
      <div class="grid kits">${kits.map(kitCard).join('')}</div>
    </div></section>` : ''}

    ${destaques.length ? `<section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Destaques</span><h2 class="h2">Testados na <em>operação</em></h2></div>
        <a class="btn" href="#/explorar">Explorar tudo</a></div>
      <div class="grid">${destaques.map(card).join('')}</div>
    </div></section>` : ''}

    <section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Categorias</span><h2 class="h2">Por <em>área</em> do digital</h2></div></div>
      <div class="grid cats">${cats.map((c) => `<a class="cat-card" href="#/explorar?cat=${c.id}"><span class="ic">${esc(c.icon || '•')}</span><span><b>${esc(c.label)}</b><small>${c.count} componente${c.count > 1 ? 's' : ''}</small></span></a>`).join('')}</div>
    </div></section>

    ${ctaBloco()}

    <section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Novidades</span><h2 class="h2">Adicionados <em>recentemente</em></h2></div></div>
      <div class="grid">${recentes.map(card).join('')}</div>
    </div></section>`;
  }

  function kitsLista() {
    const plugins = S.items.filter((i) => i.type === 'plugins').map((p) => ({
      nome: p.marketplaceName || p.pluginName || p.name, titulo: p.title, desc: p.description, plugin: p,
      skills: (p.children || []).filter((c) => c.startsWith('skills/')).length,
      agents: (p.children || []).filter((c) => c.startsWith('agents/')).length,
      commands: (p.children || []).filter((c) => c.startsWith('commands/')).length,
      link: urlItem(p), destaque: p.featured,
    }));
    const bundles = (S.cat.bundles || []).map((b) => ({
      nome: b.name, titulo: b.label, desc: catInfo(b.category).description || b.description, bundle: b,
      skills: b.skills, agents: b.agents, commands: b.commands, prompts: b.prompts || 0, frameworks: b.frameworks || 0, link: `#/explorar?cat=${b.category}`, destaque: false,
    }));
    const tot = (k) => k.skills + k.agents + k.commands + (k.prompts || 0) + (k.frameworks || 0);
    return plugins.sort((a, b) => b.destaque - a.destaque).concat(bundles.sort((a, b) => tot(b) - tot(a)));
  }

  function kitCard(k) {
    const inst = `/plugin install ${k.nome}@${mpNome()}`;
    return `<article class="kit">
      <div class="topo-card" style="display:flex;gap:8px;align-items:center">${selo(k.plugin ? 'Plugin' : 'Kit', k.destaque ? 'cheio brilho' : '')}<span class="mono muted" style="font-size:12px">${esc(k.nome)}</span></div>
      <h3 class="h3"><a href="${k.link}">${esc(k.titulo)}</a></h3>
      <p>${esc(k.desc || '')}</p>
      <div class="conta"><span><b>${k.skills}</b>skills</span><span><b>${k.agents}</b>agentes</span><span><b>${k.commands}</b>comandos</span>${k.prompts ? `<span><b>${k.prompts}</b>prompts</span>` : ''}${k.frameworks ? `<span><b>${k.frameworks}</b>frameworks</span>` : ''}</div>
      ${blocoCmd(inst)}
    </article>`;
  }

  function paginaKits() {
    const kits = kitsLista();
    const add = mpAdd();
    return `<section class="bloco"><div class="wrap">
      <div class="cab"><div><span class="colchete">Kits &amp; Plugins</span><h1 class="titulo" style="font-size:clamp(36px,5vw,64px)">Instale direto no <em>Claude Code</em></h1>
      <p>Cada kit junta os prompts, skills, agentes e frameworks de uma área. Adicione a Central uma vez no Claude Code e instale quantos kits quiser; eles se atualizam sozinhos.</p></div></div>
      <div class="painel" style="margin-bottom:24px"><header><span class="ponto"></span><span class="colchete">Passo 1 · adicionar o marketplace</span></header>
        <div class="corpo">${add ? blocoCmd(add) : `<div class="aviso">A central ainda não foi publicada no GitHub. Depois de publicar, este passo vira <b class="mono">/plugin marketplace add dono/repositorio</b>. Para testar no seu computador, use o caminho da pasta: <b class="mono">/plugin marketplace add /caminho/para/trip-angle-hub</b>.</div>`}
        <p class="nota">Digite dentro do Claude Code. Depois, <b>/plugin</b> mostra tudo o que está instalado.</p></div></div>
      ${(S.cat.collections || []).length ? `<div class="cab" style="margin-top:6px"><div><span class="colchete">Kits curados</span><h2 class="h2">Montados para <em>uma missão</em></h2>
        <p>Seleções prontas de prompts, frameworks, skills e agentes. Adicione à stack e instale tudo com um comando.</p></div></div>
        <div class="grid kits" style="margin-bottom:36px">${S.cat.collections.map(colecaoCard).join('')}</div>` : ''}
      <span class="colchete" style="display:block;margin-bottom:12px">Passo 2 · instalar o kit do marketplace</span>
      <div class="grid kits">${kits.map(kitCard).join('') || '<div class="vazio">Nenhum kit ainda.</div>'}</div>
      <p class="nota" style="margin-top:18px">Prefere sem marketplace? O instalador também aceita kits: <span class="mono">${esc(pyCmd())} --plugin ta-copy</span></p>
    </div></section>`;
  }

  function paginaExplorar(p) {
    const tipoSel = p.get('tipo') || '';
    const catSel = p.get('cat') || '';
    const q = p.get('q') || '';
    const ordem = p.get('ordem') || 'destaque';
    let base = S.items.filter((i) => (!tipoSel || i.type === tipoSel));
    const porCat = {};
    base.forEach((i) => { porCat[i.category] = (porCat[i.category] || 0) + 1; });
    base = base.filter((i) => !catSel || i.category === catSel);
    const subSel = p.get('sub') || '';
    const macSel = p.get('mac') || '';
    const comSel = p.get('com') || '';
    const doRepo = (i, k) => ((i.detalhes || {})[k] || '').split(/[ ,(]/)[0].toLowerCase();
    const opcoes = (fn) => [...new Set(base.map(fn).filter(Boolean))].sort();
    const filtrosRepo = tipoSel === 'repos' ? { sub: opcoes((i) => i.subcategoria), mac: opcoes((i) => doRepo(i, 'Roda no Mac')), com: opcoes((i) => doRepo(i, 'Uso comercial')) } : null;
    if (filtrosRepo) base = base.filter((i) => (!subSel || i.subcategoria === subSel) && (!macSel || doRepo(i, 'Roda no Mac') === macSel) && (!comSel || doRepo(i, 'Uso comercial') === comSel));
    let lista = q ? buscar(q, base) : ordenar(base, ordem);
    if (q && ordem !== 'destaque') lista = ordenar(lista, ordem);
    const link = (o) => {
      const n = new URLSearchParams();
      const v = Object.assign({ tipo: tipoSel, cat: catSel, q, ordem: ordem === 'destaque' ? '' : ordem }, o);
      Object.entries(v).forEach(([k, val]) => { if (val) n.set(k, val); });
      const s = n.toString();
      return '#/explorar' + (s ? '?' + s : '');
    };
    const cats = (S.cat.categories || []).filter((c) => porCat[c.id]);
    const total = S.items.filter((i) => !catSel || i.category === catSel);
    const titulo = catSel ? catInfo(catSel).label : tipoSel ? tipo(tipoSel).label : 'Todo o catálogo';
    return `<div class="wrap explorar">
      <aside class="lateral" aria-label="Categorias">
        <h4>Categorias</h4>
        <a href="${link({ cat: '' })}" class="${!catSel ? 'ativo' : ''}"><span class="ic">◆</span><span>Todas</span><span class="n">${Object.values(porCat).reduce((a, b) => a + b, 0)}</span></a>
        ${cats.map((c) => `<a href="${link({ cat: c.id })}" class="${catSel === c.id ? 'ativo' : ''}"><span class="ic">${esc(c.icon || '•')}</span><span>${esc(c.label)}</span><span class="n">${porCat[c.id]}</span></a>`).join('')}
      </aside>
      <div>
        <span class="colchete">Explorar</span>
        <h1 class="titulo" style="font-size:clamp(34px,5vw,58px);margin:10px 0 18px">${esc(titulo)}</h1>
        <nav class="abas" aria-label="Tipos">
          <a href="${link({ tipo: '' })}" class="${!tipoSel ? 'ativo' : ''}">Tudo <small>${total.length}</small></a>
          ${(S.cat.types || []).map((t) => { const n = total.filter((i) => i.type === t.id).length; return n ? `<a href="${link({ tipo: t.id })}" class="${tipoSel === t.id ? 'ativo' : ''}">${esc(t.label)} <small>${n}</small></a>` : ''; }).join('')}
        </nav>
        <div class="chips-cat"><a href="${link({ cat: '' })}" class="${!catSel ? 'ativo' : ''}">Todas</a>${cats.map((c) => `<a href="${link({ cat: c.id })}" class="${catSel === c.id ? 'ativo' : ''}">${esc(c.label)} · ${porCat[c.id]}</a>`).join('')}</div>
        <div class="filtros">
          <label class="campo">${I.busca}<input id="filtroQ" type="search" value="${esc(q)}" placeholder="Filtrar por nome, descrição ou tag" aria-label="Filtrar"></label>
          <select id="filtroOrdem" aria-label="Ordenar">
            <option value="destaque" ${ordem === 'destaque' ? 'selected' : ''}>${q ? 'Mais relevantes' : 'Destaques primeiro'}</option>
            <option value="az" ${ordem === 'az' ? 'selected' : ''}>A → Z</option>
            <option value="recentes" ${ordem === 'recentes' ? 'selected' : ''}>Mais recentes</option>
          </select>
          ${filtrosRepo ? `<select data-param="sub" aria-label="Subcategoria"><option value="">Toda subcategoria</option>${filtrosRepo.sub.map((v) => `<option ${v === subSel ? 'selected' : ''}>${esc(v)}</option>`).join('')}</select>
            <select data-param="mac" aria-label="Roda no Mac"><option value="">Mac: qualquer</option>${filtrosRepo.mac.map((v) => `<option value="${esc(v)}" ${v === macSel ? 'selected' : ''}>Mac: ${esc(v)}</option>`).join('')}</select>
            <select data-param="com" aria-label="Uso comercial"><option value="">Comercial: qualquer</option>${filtrosRepo.com.map((v) => `<option value="${esc(v)}" ${v === comSel ? 'selected' : ''}>Comercial: ${esc(v)}</option>`).join('')}</select>` : ''}
        </div>
        <p class="resumo">${lista.length} resultado${lista.length === 1 ? '' : 's'}${q ? ` para “${esc(q)}”` : ''}</p>
        ${lista.length ? `<div class="grid" id="gridItens">${lista.slice(0, S.limite).map(card).join('')}</div>
          ${lista.length > S.limite ? `<div class="mais"><button class="btn" id="maisBtn">Mostrar mais (${lista.length - S.limite})</button></div>` : ''}`
        : `<div class="vazio"><p class="h3">Nada encontrado</p><p>Tente outra palavra ou <a href="#/explorar" style="color:var(--neon)">limpe os filtros</a>.</p></div>`}
      </div>
    </div>`;
  }

  function paginaItem(id) {
    const it = S.byId.get(id);
    if (!it) return `<div class="wrap" style="padding:60px 0"><div class="vazio"><p class="h3">Componente não encontrado</p><p><a href="#/explorar" style="color:var(--neon)">Voltar ao catálogo</a></p></div></div>`;
    const t = tipo(it.type);
    const c = catInfo(it.category);
    const pai = it.partOf ? S.byId.get(it.partOf) : null;
    const url = origemUrl(it);
    const scan = it.scan && it.scan.severity;
    const corScan = { LOW: 'var(--verde)', MEDIUM: 'var(--amarelo)', HIGH: 'var(--neon)', CRITICAL: 'var(--neon)' }[scan] || 'var(--cinza)';
    const plugNome = it.type === 'plugins' ? (it.marketplaceName || it.pluginName || it.name) : (pai ? (pai.marketplaceName || pai.name) : it.bundle);
    const avisos = [];
    if (scan === 'HIGH' || scan === 'CRITICAL') avisos.push(`<div class="aviso vermelho">Análise de segurança: <b>${scan}</b> (nota ${it.scan.score}). Leia todos os arquivos antes de instalar.</div>`);
    if (it.type === 'hooks') avisos.push('<div class="aviso">Hooks executam comandos na sua máquina em eventos do Claude Code. Leia o arquivo antes de instalar.</div>');
    if (it.type === 'mcps' && (it.requires || []).length) avisos.push(`<div class="aviso">Depois de instalar, preencha no <b class="mono">.mcp.json</b>: ${it.requires.map((r) => `<b class="mono">${esc(r)}</b>`).join(', ')}. Use variáveis de ambiente para chaves.</div>`);

    let instalar;
    if (it.type === 'sites') {
      instalar = `<a class="btn vermelho" style="width:100%" href="${esc((it.site || {}).url)}" target="_blank" rel="noopener">Abrir o site ${I.ext}</a>
        ${blocoCmd((it.site || {}).url || '', false)}${(it.site || {}).pricing ? `<p class="nota">Preço: <b>${esc(it.site.pricing)}</b></p>` : ''}`;
    } else if (it.type === 'repos') {
      instalar = blocoCmd(`git clone ${(it.repo || {}).url || ''}`) + blocoCmd(cmdItem(it));
    } else {
      const abas = [['cli', 'Instalador'], ...(plugNome ? [['mp', 'Marketplace']] : []), ['manual', 'Manual']];
      instalar = `<div class="seg" role="tablist">${abas.map(([k, l], i) => `<button role="tab" data-aba="${k}" class="${i === 0 ? 'ativo' : ''}">${l}</button>`).join('')}</div>
        <div data-painel="cli">${blocoCmd(cmdItem(it))}<p class="nota">Rode na pasta do projeto. ${destinoTexto(it)}</p></div>
        ${plugNome ? `<div data-painel="mp" hidden>${mpAdd() ? blocoCmd(mpAdd()) : '<p class="nota">Publique a central no GitHub para usar o marketplace.</p>'}${blocoCmd(`/plugin install ${plugNome}@${mpNome()}`)}
          <p class="nota">Dentro do Claude Code. ${it.type === 'plugins' ? 'Instala o plugin inteiro.' : `Instala o ${pai ? 'plugin' : 'kit'} <b>${esc(plugNome)}</b>, que inclui este componente.`}</p></div>` : ''}
        <div data-painel="manual" hidden><p class="nota" style="margin-top:0">Baixe os arquivos abaixo e coloque em <b class="mono">${esc(destinoManual(it))}</b>.</p></div>`;
    }

    const filhos = (it.children || []).map((cid) => S.byId.get(cid)).filter(Boolean);
    const arquivos = it.files || [];
    return `<div class="wrap detalhe">
      <div>
        <nav class="trilha" aria-label="Trilha"><a href="#/explorar">Catálogo</a><i>/</i><a href="#/explorar?tipo=${it.type}">${esc(t.label)}</a><i>/</i><a href="#/explorar?cat=${it.category}">${esc(c.label)}</a></nav>
        <div style="display:flex;gap:8px;flex-wrap:wrap">${selo(t.singular, 'cheio')}${seloStatus(it)}${it.featured ? selo('Destaque', 'brilho') : ''}${pai ? `<a href="${urlItem(pai)}">${selo('Parte de ' + pai.title, 'cinza')}</a>` : ''}</div>
        <h1 class="titulo">${esc(it.title)}</h1>
        <p class="lead">${esc(it.description || 'Sem descrição.')}</p>
        ${(it.tags || []).length ? `<div class="tags" style="margin-bottom:18px">${it.tags.map((g) => `<a class="tag-x" href="#/explorar?q=${encodeURIComponent(g)}">${esc(g)}</a>`).join('')}</div>` : ''}
        ${avisos.join('')}
        ${it.type === 'prompts' ? painelPrompt(it) : ''}
        ${it.type === 'repos' && it.detalhes ? fichaTecnica(it) : ''}
        ${(it.next || []).length ? `<div class="painel" style="margin-top:14px"><header><span class="colchete">Próximo passo</span></header><div class="corpo filhos">${it.next.map((n) => S.byId.get('prompts/' + n) || S.byId.get(n)).filter(Boolean).map((f) => `<a href="${urlItem(f)}">${selo(f.level === 'mestre' ? 'Mestre' : tipo(f.type).singular, 'cinza')}<span>${esc(f.title)}</span></a>`).join('')}</div></div>` : ''}
        ${it.type === 'frameworks' && it.when ? `<div class="aviso" style="border-color:var(--linha-2);background:rgba(255,255,255,.03);color:var(--cinza)"><b style="color:var(--gelo)">Quando usar:</b> ${esc(it.when)}</div>` : ''}
        ${filhos.length ? `<div class="painel" style="margin-top:18px"><header><span class="colchete">Inclui ${filhos.length} componentes</span></header><div class="corpo filhos">
          ${filhos.map((f) => `<a href="${urlItem(f)}">${selo(tipo(f.type).singular, 'cinza')}<span>${esc(f.title)}</span></a>`).join('')}</div></div>` : ''}
        ${arquivos.length ? `<div class="painel" style="margin-top:18px">
          <header><span class="colchete">Arquivos</span><span class="direita"><a class="btn peq" id="baixarArq" href="#" download>${I.baixar} Baixar</a></span></header>
          <div class="arquivos" id="listaArq">${arquivos.map((f, i) => `<button data-arq="${esc(f)}" class="${i === principal(it) ? 'ativo' : ''}"><span>${esc(relArq(it, f))}</span></button>`).join('')}</div>
        </div>
        <div class="painel viewer" id="viewer" style="margin-top:14px"><div class="esqueleto" style="margin:14px"></div></div>` : ''}
      </div>
      <aside class="lado">
        <div class="painel"><header><span class="ponto"></span><span class="colchete">${instalavel(it) ? 'Instalar' : 'Acessar'}</span><span class="direita"><button class="btn peq icone" data-fav="${esc(it.id)}"></button>${instalavel(it) ? `<button class="btn peq icone" data-stack="${esc(it.id)}"></button>` : ''}</span></header>
          <div class="corpo">${instalar}</div></div>
        <div class="painel"><header><span class="colchete">Detalhes</span></header><div class="corpo">
          <dl class="meta">
            <dt>ID</dt><dd class="mono" style="font-size:12px">${esc(ref(it))}</dd>
            <dt>Categoria</dt><dd><a href="#/explorar?cat=${it.category}">${esc(c.label)}</a></dd>
            <dt>Origem</dt><dd>${url ? `<a href="${esc(url)}" target="_blank" rel="noopener">${esc(origemTexto(it))}</a>` : esc(origemTexto(it))}</dd>
            ${it.author ? `<dt>Autor</dt><dd>${esc(it.author)}</dd>` : ''}
            <dt>Licença</dt><dd>${esc(it.license || '—')}</dd>
            ${it.version ? `<dt>Versão</dt><dd>${esc(it.version)}</dd>` : ''}
            ${it.model ? `<dt>Modelo</dt><dd>${esc(it.model)}</dd>` : ''}
            ${it.type === 'prompts' ? `<dt>Nível</dt><dd>${it.level === 'mestre' ? 'Prompt mestre' : 'Módulo'}</dd>` : ''}
            ${it.etapas ? `<dt>Etapas</dt><dd>${it.etapas}</dd>` : ''}
            ${it.tempo ? `<dt>Tempo</dt><dd>${esc(it.tempo)}</dd>` : ''}
            ${it.type === 'prompts' ? `<dt>Insumos</dt><dd>${(it.variables || []).filter((v) => v.required).length} obrigatórios · ${(it.variables || []).length} no total</dd>` : ''}
            ${it.origin ? `<dt>Crédito</dt><dd>${esc(it.origin)}</dd>` : ''}
            ${it.events && it.events.length ? `<dt>Eventos</dt><dd>${esc(it.events.join(', '))}</dd>` : ''}
            ${it.servers && it.servers.length ? `<dt>Servidores</dt><dd class="mono">${esc(it.servers.join(', '))}</dd>` : ''}
            ${it.repo ? `<dt>GitHub</dt><dd><a href="${esc(it.repo.url)}" target="_blank" rel="noopener">${esc((it.repo.url || '').replace('https://github.com/', ''))}</a></dd>
              ${it.repo.stars != null ? `<dt>Estrelas</dt><dd>★ ${Number(it.repo.stars).toLocaleString('pt-BR')}</dd>` : ''}
              ${it.repo.language ? `<dt>Linguagem</dt><dd>${esc(it.repo.language)}</dd>` : ''}` : ''}
            ${scan ? `<dt>Segurança</dt><dd><span style="color:${corScan};font-weight:700">● ${esc(scan)}</span> <span class="muted">(${esc(it.scan.tool || 'scan')} ${esc(it.scan.score)})</span></dd>` : ''}
            ${arquivos.length ? `<dt>Arquivos</dt><dd>${arquivos.length} · ${fmtBytes(it.size)}</dd>` : ''}
            <dt>Adicionado</dt><dd>${fmtData(it.addedAt)}</dd>
          </dl></div></div>
      </aside>
    </div>`;
  }

  function principal(it) {
    const alvo = it.kind === 'dir' ? `${it.base}/${it.main}` : it.base;
    const i = (it.files || []).indexOf(alvo);
    return i >= 0 ? i : 0;
  }
  function relArq(it, f) { return it.kind === 'dir' && f.startsWith(it.base + '/') ? f.slice(it.base.length + 1) : f.split('/').pop(); }
  function destinoManual(it) {
    return ({
      skills: `.claude/skills/${it.name}/`, agents: '.claude/agents/', commands: '.claude/commands/', mcps: '.mcp.json (mesclar mcpServers)',
      hooks: '.claude/settings.json (mesclar hooks)', settings: '.claude/settings.json (mesclar)', templates: 'raiz do projeto',
      plugins: '~/.claude/plugins (use o marketplace)', repos: 'qualquer pasta',
      prompts: '.claude/commands/ (o instalador converte em comando)', frameworks: '.claude/skills/ (o instalador converte em skill)',
    })[it.type] || '.claude/';
  }
  function destinoTexto(it) {
    return ({
      skills: `Vai para <b class="mono">.claude/skills/${esc(it.name)}/</b> e carrega sozinha quando a tarefa combina.`,
      agents: `Vai para <b class="mono">.claude/agents/${esc(it.name)}.md</b> e aparece em <b>/agents</b>.`,
      commands: `Vai para <b class="mono">.claude/commands/${esc(it.name)}.md</b> e vira <b>/${esc(it.name)}</b>.`,
      mcps: 'Mescla o servidor no <b class="mono">.mcp.json</b>. Reinicie o Claude Code e confira em <b>/mcp</b>.',
      hooks: 'Mescla no settings do escopo escolhido (padrão <b class="mono">.claude/settings.local.json</b>). Confira em <b>/hooks</b>.',
      settings: 'Mescla no settings do escopo escolhido (padrão <b class="mono">.claude/settings.local.json</b>).',
      plugins: 'Habilita o plugin pelo marketplace no settings do escopo.',
      templates: 'Copia os arquivos para a raiz do projeto sem sobrescrever os que já existem.',
      prompts: `Vira o comando <b>/${esc(it.name)}</b> em <b class="mono">.claude/commands/</b>: digite /${esc(it.name)} e os dados.`,
      frameworks: `Vira a skill <b class="mono">.claude/skills/${esc(String(it.name).startsWith('framework-') ? it.name : 'framework-' + it.name)}/</b> e o Claude aplica o método quando a tarefa pede.`,
    })[it.type] || '';
  }

  async function abrirArquivo(it, caminho) {
    const v = $('#viewer');
    if (!v) return;
    $$('#listaArq button').forEach((b) => b.classList.toggle('ativo', b.dataset.arq === caminho));
    const bx = $('#baixarArq');
    if (bx) { bx.href = caminho; bx.setAttribute('download', caminho.split('/').pop()); }
    if (/\.(png|jpe?g|gif|webp|svg)$/i.test(caminho)) {
      v.innerHTML = `<div class="corpo"><img src="${esc(caminho)}" alt="${esc(caminho.split('/').pop())}" style="max-height:60vh;margin:auto"></div>`;
      return;
    }
    v.innerHTML = '<div class="esqueleto" style="margin:14px"></div>';
    try {
      const r = await fetch(caminho);
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const txt = await r.text();
      if (/\.md$/i.test(caminho)) {
        const m = txt.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
        let fm = '';
        let corpo = txt;
        if (m) {
          corpo = txt.slice(m[0].length);
          const linhas = m[1].split('\n').filter((l) => /^[A-Za-z0-9_-]+:/.test(l));
          fm = `<dl class="fm">${linhas.map((l) => { const i = l.indexOf(':'); return `<dt>${esc(l.slice(0, i))}</dt><dd>${esc(l.slice(i + 1).trim().replace(/^["']|["']$/g, ''))}</dd>`; }).join('')}</dl>`;
        }
        v.innerHTML = fm + `<div class="md">${md(corpo)}</div>`;
      } else if (/\.json$/i.test(caminho)) {
        let bonito = txt;
        try { bonito = JSON.stringify(JSON.parse(txt), null, 2); } catch (e) { /* mantém */ }
        v.innerHTML = `<pre class="cru">${esc(bonito)}</pre>`;
      } else {
        v.innerHTML = `<pre class="cru">${esc(txt)}</pre>`;
      }
    } catch (e) {
      v.innerHTML = `<div class="corpo"><div class="aviso">Não consegui abrir o arquivo (${esc(e.message)}).</div></div>`;
    }
  }
  function md(texto) {
    if (window.marked && window.DOMPurify) {
      try { return window.DOMPurify.sanitize(window.marked.parse(texto, { gfm: true })); } catch (e) { /* cai no texto puro */ }
    }
    return `<pre class="cru" style="padding:0">${esc(texto)}</pre>`;
  }

  function paginaDocs() {
    const h = hub();
    const py = pyCmd();
    const add = mpAdd() || '/plugin marketplace add /caminho/para/trip-angle-hub';
    const tiposLinhas = (S.cat.types || []).map((t) => `<tr><td class="mono">${esc(t.flag)}</td><td>${esc(t.label)}</td><td>${destinoTexto({ type: t.id, name: '<nome>' })}</td></tr>`).join('');
    const secoes = [
      ['comece', 'Comece aqui'], ['requisitos', 'Requisitos'], ['instalar', 'Instalar'], ['stack', 'Montar uma stack'], ['prompts', 'Prompts e frameworks'],
      ['marketplace', 'Kits pelo marketplace'], ['destinos', 'Onde cada coisa fica'], ['flags', 'Opções do instalador'],
      ['ferramentas', 'Painéis locais'], ['alimentar', 'Alimentar a central'], ['publicar', 'Publicar'], ['api', 'API'],
    ];
    return `<div class="wrap docs">
      <nav class="lateral" aria-label="Seções"><h4>Como usar</h4>${secoes.map(([id, l]) => `<a href="#/como-usar" data-ancora="${id}">${l}</a>`).join('')}</nav>
      <article class="md">
        <span class="colchete">Guia</span>
        <h1 class="titulo" style="font-size:clamp(36px,5vw,64px);margin:10px 0 24px">Como usar a <em>central</em></h1>

        <h2 id="comece">Comece aqui</h2>
        <p>A ${esc(h.name || 'Central Trip Angle')} reúne componentes prontos para o <b>Claude Code</b>: skills, agentes, comandos, servidores MCP, hooks, configurações, plugins, templates e repositórios, organizados por área do mercado digital. Você escolhe no site, copia um comando e roda na pasta do projeto. Depois é só abrir o Claude Code ali.</p>
        <p><b>O caminho mais rápido:</b> abra <a href="#/jornadas">Comece aqui</a>, escolha o seu objetivo e siga os passos na ordem. Cada passo diz qual prompt mestre usar, o que dá apoio e o que levar para o passo seguinte. Os prompts funcionam em qualquer IA (Claude, ChatGPT, Gemini): é só preencher os campos e copiar. Para criar os seus próprios prompts no mesmo padrão, use o <a href="#/montador">montador</a>.</p>
        <p>Sem argumentos, o instalador abre um menu para escolher pelo terminal:</p>
        ${blocoCmd(py)}

        <h2 id="requisitos">Requisitos</h2>
        <ul><li><b>Python 3.9 ou mais novo</b> (já vem no macOS com as ferramentas de linha de comando; no Windows use o WSL ou instale o Python).</li>
        <li><b>Claude Code</b> instalado (terminal, app desktop ou extensão).</li>
        <li>Nada é instalado no sistema: o comando baixa o instalador a cada uso.</li></ul>

        <h2 id="instalar">Instalar um componente</h2>
        <p>Cada página de componente mostra o comando pronto. O formato é sempre <code>tipo categoria/nome</code>:</p>
        ${blocoCmd(`${py} --skill copy/copywriting`)}
        ${blocoCmd(`${py} --agent conteudo/content-marketer`)}
        <p>Use <code>--dry-run</code> para ver o que seria gravado sem mudar nada, e <code>--yes</code> para pular a confirmação. Buscar pelo terminal:</p>
        ${blocoCmd(`${py} --search "meta ads"`)}

        <h2 id="stack">Montar uma stack</h2>
        <p>Clique no <b>+</b> dos componentes. O botão <b>Stack</b> no topo junta tudo num comando só, com as vírgulas e flags certas. O botão <b>Link</b> copia um endereço para compartilhar a mesma stack com a equipe.</p>

        <h2 id="prompts">Prompts e frameworks</h2>
        <p>Na <a href="#/prompts">Biblioteca de prompts</a>, cada prompt tem um formulário com os campos que ele precisa. O texto final aparece na hora: copie ou abra direto no Claude ou no ChatGPT. Os campos ficam guardados no seu navegador.</p>
        <p>No Claude Code, o instalador transforma o prompt em comando e o framework em skill:</p>
        ${blocoCmd(`${py} --prompts estrategia/criar-avatar-completo`)}
        ${blocoCmd(`${py} --framework copy/pas`)}
        <p>Depois é só digitar <code>/criar-avatar-completo</code> com os dados. Para ver um prompt no terminal: <code>--show prompts/estrategia/criar-avatar-completo --var produto="Curso X"</code>.</p>

        <h2 id="marketplace">Kits pelo marketplace</h2>
        <p>Cada categoria vira um kit (<code>ta-copy</code>, <code>ta-trafego</code>…), e os plugins que você montar no admin também ficam no marketplace. Dentro do Claude Code:</p>
        ${blocoCmd(add)}
        ${blocoCmd(`/plugin install ta-copy@${mpNome()}`)}
        <p>Os plugins ficam em <code>~/.claude/plugins</code> e são gerenciados pelo comando <code>/plugin</code>.</p>

        <h2 id="destinos">Onde cada coisa fica</h2>
        <table><thead><tr><th>Flag</th><th>Tipo</th><th>Destino</th></tr></thead><tbody>${tiposLinhas}</tbody></table>
        <p>Antes de alterar qualquer JSON existente, o instalador guarda uma cópia em <code>.claude/.tahub-backups/</code>. Configurações são mescladas, nunca substituídas.</p>
        <table><thead><tr><th>Escopo (<code>--scope</code>)</th><th>Arquivo</th><th>Uso</th></tr></thead><tbody>
          <tr><td><code>local</code> (padrão)</td><td><code>.claude/settings.local.json</code></td><td>Só você, fora do git</td></tr>
          <tr><td><code>project</code></td><td><code>.claude/settings.json</code></td><td>Compartilhado com a equipe</td></tr>
          <tr><td><code>user</code></td><td><code>~/.claude/settings.json</code></td><td>Todos os seus projetos</td></tr></tbody></table>

        <h2 id="flags">Opções do instalador</h2>
        <table><thead><tr><th>Opção</th><th>O que faz</th></tr></thead><tbody>
          <tr><td><code>--prompts --skill --agent --framework --command --mcp --hook --setting --plugin --template --repo</code></td><td>Instala componentes (vários separados por vírgula)</td></tr>
          <tr><td><code>-d, --directory &lt;pasta&gt;</code></td><td>Instala em outra pasta</td></tr>
          <tr><td><code>--scope local|project|user</code></td><td>Arquivo de settings usado por hooks, settings e plugins</td></tr>
          <tr><td><code>-y, --yes</code></td><td>Não pergunta nada</td></tr>
          <tr><td><code>--dry-run</code></td><td>Mostra o plano sem gravar</td></tr>
          <tr><td><code>--force</code></td><td>Sobrescreve arquivos existentes</td></tr>
          <tr><td><code>--search "termos"</code></td><td>Busca no catálogo</td></tr>
          <tr><td><code>--list [tipo]</code> e <code>--info tipo/categoria/nome</code></td><td>Lista e detalha componentes</td></tr>
          <tr><td><code>--show tipo/categoria/nome --var nome=valor</code></td><td>Mostra o texto de um prompt, com as variáveis preenchidas</td></tr>
          <tr><td><code>--prompt "texto"</code></td><td>Abre o Claude Code com esse pedido depois de instalar</td></tr>
          <tr><td><code>--health-check</code></td><td>Diagnóstico do Claude Code e do projeto</td></tr>
          <tr><td><code>--analytics</code> / <code>--chats</code></td><td>Painéis locais de uso e de conversas</td></tr></tbody></table>

        <h2 id="ferramentas">Painéis locais</h2>
        ${blocoCmd(`${py} --analytics`)}
        <p>Abre <code>http://localhost:3333</code> com sessões, tokens por modelo e atividade por dia, lidos de <code>~/.claude/projects</code>.</p>
        ${blocoCmd(`${py} --chats`)}
        <p>Abre <code>http://localhost:9876</code> para ler e buscar suas conversas antigas. Os dois só escutam no seu computador e não enviam nada para fora.</p>
        ${blocoCmd(`${py} --health-check`)}

        <h2 id="alimentar">Alimentar a central</h2>
        <p>Na pasta do repositório da central, abra o painel admin:</p>
        ${blocoCmd('python3 tools/admin.py')}
        <p>Em <code>http://localhost:4545/admin</code> você cria componentes à mão, importa skills, agentes, plugins e MCPs de qualquer repositório do GitHub ou pasta do computador, traz itens do catálogo do aitmpl.com com a licença e a origem registradas, cadastra repositórios, monta plugins e publica. Pelo terminal:</p>
        ${blocoCmd('python3 tools/importers.py scan https://github.com/dono/repositorio')}
        ${blocoCmd('python3 tools/importers.py aitmpl import skills/business-marketing/seo-optimizer --category seo')}
        ${blocoCmd('python3 tools/build.py')}

        <h2 id="publicar">Publicar</h2>
        <ol><li>Crie um repositório no GitHub e envie esta pasta (<code>git push</code>).</li>
        <li>Em <b>Settings → Pages</b>, escolha <b>GitHub Actions</b>. O workflow incluído gera o site a cada push.</li>
        <li>Preencha <code>siteUrl</code> e <code>githubRepo</code> no <code>hub.config.json</code>. O comando do instalador e o marketplace passam a apontar para lá.</li></ol>

        <h2 id="api">API</h2>
        <p>Tudo é estático e público: <a href="api/catalog.json">api/catalog.json</a> (catálogo completo), <code>api/&lt;tipo&gt;.json</code>, <a href="api/version.json">api/version.json</a>, <a href="llms.txt">llms.txt</a> e <a href="marketplace.json">marketplace.json</a>.</p>
      </article>
    </div>`;
  }

  // ---------------------------------------------------------------- roteador
  function rota() {
    const hash = location.hash.replace(/^#/, '') || '/';
    const [caminho, qs] = hash.split('?');
    const p = new URLSearchParams(qs || '');
    const app = $('#app');
    let html;
    let ativo = '';
    if (caminho.startsWith('/item/')) {
      html = paginaItem(decodeURIComponent(caminho.slice(6)));
    } else if (caminho === '/explorar') {
      html = paginaExplorar(p); ativo = p.get('tipo') ? 'tipo:' + p.get('tipo') : 'explorar';
    } else if (caminho === '/jornadas') {
      html = paginaJornadas(); ativo = 'jornadas';
    } else if (caminho.startsWith('/jornada/')) {
      html = paginaJornada(decodeURIComponent(caminho.slice(9))); ativo = 'jornadas';
    } else if (caminho === '/favoritos') {
      html = paginaFavoritos();
    } else if (caminho === '/montador') {
      html = paginaMontador(); ativo = 'montador';
    } else if (caminho === '/trilha') {
      html = paginaTrilha(); ativo = 'trilha';
    } else if (caminho === '/perfil') {
      html = paginaPerfil(); ativo = 'perfil';
    } else if (caminho === '/prompts') {
      html = paginaPrompts(p); ativo = 'prompts';
    } else if (caminho === '/kits') {
      html = paginaKits(); ativo = 'kits';
    } else if (caminho === '/como-usar') {
      html = paginaDocs(); ativo = 'como-usar';
    } else if (caminho === '/stack') {
      const ids = (p.get('ids') || '').split(',').filter((id) => S.byId.has(id));
      ids.forEach((id) => { if (!S.stack.includes(id)) S.stack.push(id); });
      salvarStack();
      history.replaceState(null, '', '#/');
      html = paginaInicio();
      setTimeout(() => { abrirGaveta(true); if (ids.length) toast(`${ids.length} componentes adicionados à stack`); }, 50);
    } else {
      html = paginaInicio();
    }
    app.innerHTML = html;
    $$('#nav a').forEach((a) => {
      const on = (a.dataset.rota && a.dataset.rota === ativo) || (a.dataset.tipo && 'tipo:' + a.dataset.tipo === ativo);
      a.classList.toggle('ativo', !!on);
    });
    $('#nav').classList.remove('aberta');
    $$('[data-stack]', app).forEach(marcarBotao);
    $$('[data-fav]', app).forEach(marcarFav);
    pos(caminho, p);
    if (!(caminho.startsWith('/explorar') || caminho.startsWith('/prompts')) || !p.toString()) window.scrollTo({ top: 0, behavior: 'instant' });
    const t = caminho.startsWith('/item/') ? (S.byId.get(decodeURIComponent(caminho.slice(6))) || {}).title : null;
    document.title = (t ? t + ' · ' : '') + (hub().name || 'Central Trip Angle');
  }

  function pos(caminho, p) {
    if (caminho.startsWith('/item/')) {
      const it = S.byId.get(decodeURIComponent(caminho.slice(6)));
      if (it && (it.files || []).length) abrirArquivo(it, it.files[principal(it)]);
      if (it && it.type === 'prompts') ligarPrompt(it);
      $$('[data-aba]').forEach((b) => b.addEventListener('click', () => {
        $$('[data-aba]').forEach((x) => x.classList.toggle('ativo', x === b));
        $$('[data-painel]').forEach((pn) => { pn.hidden = pn.dataset.painel !== b.dataset.aba; });
      }));
      $$('#listaArq button').forEach((b) => b.addEventListener('click', () => abrirArquivo(it, b.dataset.arq)));
    }
    const fp = $('#filtroPrompts');
    if (fp) {
      let tp;
      const aplicarP = () => {
        const n = new URLSearchParams(p);
        if (fp.value.trim()) n.set('q', fp.value.trim()); else n.delete('q');
        if ($('#filtroFerr').value) n.set('ferramenta', $('#filtroFerr').value); else n.delete('ferramenta');
        const novo = '#/prompts' + (n.toString() ? '?' + n : '');
        if (novo !== location.hash) { history.replaceState(null, '', novo); const y = window.scrollY; rota(); window.scrollTo(0, y); const f = $('#filtroPrompts'); f.focus(); f.setSelectionRange(f.value.length, f.value.length); }
      };
      fp.addEventListener('input', () => { clearTimeout(tp); tp = setTimeout(aplicarP, 220); });
      $('#filtroFerr').addEventListener('change', aplicarP);
    }
    if (caminho === '/perfil') ligarPerfil();
    if (caminho === '/montador') ligarMontador();
    $$('select[data-param]').forEach((sel) => sel.addEventListener('change', () => {
      const n = new URLSearchParams(p);
      if (sel.value) n.set(sel.dataset.param, sel.value); else n.delete(sel.dataset.param);
      location.hash = '#/explorar?' + n;
    }));
    const hb = $('#heroBusca');
    if (hb) hb.addEventListener('submit', (e) => { e.preventDefault(); const q = hb.q.value.trim(); location.hash = '#/explorar' + (q ? '?q=' + encodeURIComponent(q) : ''); });
    const fq = $('#filtroQ');
    if (fq) {
      let tmr;
      const aplicar = () => {
        const n = new URLSearchParams(p);
        if (fq.value.trim()) n.set('q', fq.value.trim()); else n.delete('q');
        const o = $('#filtroOrdem').value;
        if (o && o !== 'destaque') n.set('ordem', o); else n.delete('ordem');
        S.limite = 60;
        const novo = '#/explorar' + (n.toString() ? '?' + n : '');
        if (novo !== location.hash) { history.replaceState(null, '', novo); rota(); const f = $('#filtroQ'); f.focus(); f.setSelectionRange(f.value.length, f.value.length); }
      };
      fq.addEventListener('input', () => { clearTimeout(tmr); tmr = setTimeout(aplicar, 220); });
      $('#filtroOrdem').addEventListener('change', aplicar);
      const mb = $('#maisBtn');
      if (mb) mb.addEventListener('click', () => { S.limite += 60; const y = window.scrollY; rota(); window.scrollTo(0, y); });
    }
    $$('[data-ancora]').forEach((a) => a.addEventListener('click', (e) => { e.preventDefault(); const el = document.getElementById(a.dataset.ancora); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }));
  }

  // ---------------------------------------------------------------- paleta ⌘K
  let selPaleta = 0;
  let resPaleta = [];
  function abrirPaleta(abrir) {
    const pl = $('#paleta');
    pl.classList.toggle('aberta', abrir);
    if (abrir) { const i = $('#paletaInput'); i.value = ''; desenharPaleta(''); setTimeout(() => i.focus(), 10); }
  }
  function desenharPaleta(q) {
    resPaleta = (q ? buscar(q) : ordenar(S.items.filter((i) => i.featured), 'destaque')).slice(0, 30);
    selPaleta = 0;
    $('#paletaLista').innerHTML = resPaleta.length ? resPaleta.map((it, i) => `<li class="${i === 0 ? 'sel' : ''}" role="option"><a href="${urlItem(it)}" data-i="${i}">
      ${selo(tipo(it.type).singular, 'cinza')}<div><b>${esc(it.title)}</b><small>${esc(catInfo(it.category).label)} · ${esc(it.description)}</small></div></a></li>`).join('')
      : '<li style="padding:18px;color:var(--cinza)">Nada encontrado.</li>';
  }
  function moverPaleta(d) {
    const lis = $$('#paletaLista li');
    if (!lis.length || !resPaleta.length) return;
    lis[selPaleta]?.classList.remove('sel');
    selPaleta = (selPaleta + d + resPaleta.length) % resPaleta.length;
    lis[selPaleta].classList.add('sel');
    lis[selPaleta].scrollIntoView({ block: 'nearest' });
  }

  // ---------------------------------------------------------------- utilidades
  let tmrToast;
  function toast(msg) {
    const t = $('#toast');
    t.textContent = msg;
    t.classList.add('on');
    clearTimeout(tmrToast);
    tmrToast = setTimeout(() => t.classList.remove('on'), 1800);
  }
  async function copiar(texto, btn) {
    try {
      await navigator.clipboard.writeText(texto);
    } catch (e) {
      const ta = document.createElement('textarea');
      ta.value = texto; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (e2) { /* sem cópia */ }
      ta.remove();
    }
    toast('Copiado');
    if (btn) { btn.classList.add('ok'); setTimeout(() => btn.classList.remove('ok'), 1200); }
  }

  function ligar() {
    document.addEventListener('click', (e) => {
      const c = e.target.closest('[data-copiar]');
      if (c) { e.preventDefault(); copiar(c.dataset.copiar, c); return; }
      const s = e.target.closest('[data-stack]');
      if (s) { e.preventDefault(); alternarStack(s.dataset.stack); return; }
      const fv = e.target.closest('[data-fav]');
      if (fv) { e.preventDefault(); alternarFav(fv.dataset.fav); return; }
      const js = e.target.closest('[data-jornada-stack]');
      if (js) {
        const j = jornadas().find((x) => x.id === js.dataset.jornadaStack);
        const ids = j ? j.passos.flatMap((ps) => [ps.principal].concat(ps.apoio || [])).filter((id) => id && S.byId.has(id) && instalavel(S.byId.get(id)) && !S.stack.includes(id)) : [];
        S.stack.push(...ids); salvarStack(); toast(`${ids.length} itens adicionados à stack`); abrirGaveta(true);
        return;
      }
      const jr = e.target.closest('[data-jornada-reset]');
      if (jr) { if (confirm('Recomeçar o progresso desta jornada?')) { store.set('ta-jornada-' + jr.dataset.jornadaReset, []); rota(); } return; }
      if (e.target.closest('[data-favs-stack]')) {
        const ids = favs().filter((id) => S.byId.has(id) && instalavel(S.byId.get(id)) && !S.stack.includes(id));
        S.stack.push(...ids); salvarStack(); toast(`${ids.length} itens adicionados à stack`); abrirGaveta(true);
        return;
      }
      const k = e.target.closest('[data-kit]');
      if (k) {
        const col = (S.cat.collections || []).find((c) => c.id === k.dataset.kit);
        const novos = (col ? col.items : []).filter((id) => S.byId.has(id) && instalavel(S.byId.get(id)) && !S.stack.includes(id));
        S.stack.push(...novos); salvarStack(); toast(`${novos.length} itens adicionados à stack`); abrirGaveta(true);
        return;
      }
      const r = e.target.closest('[data-remover]');
      if (r) { alternarStack(r.dataset.remover); return; }
      if (e.target.closest('#limparStack')) { S.stack = []; salvarStack(); return; }
      if (e.target.closest('#compartilharStack')) {
        copiar(location.origin + location.pathname + '#/stack?ids=' + S.stack.map(encodeURIComponent).join(','));
        return;
      }
      if (e.target.closest('#gaveta a')) abrirGaveta(false);
      if (e.target.closest('#paletaLista a')) abrirPaleta(false);
    });
    $('#stackBtn').addEventListener('click', () => abrirGaveta(true));
    document.addEventListener('change', (e) => {
      const cb = e.target.closest('input[data-passo]');
      if (!cb) return;
      const id = cb.dataset.jornada;
      const i = +cb.dataset.passo;
      const atual = new Set(progresso(id));
      if (cb.checked) atual.add(i); else atual.delete(i);
      store.set('ta-jornada-' + id, [...atual]);
      const y = window.scrollY; rota(); window.scrollTo(0, y);
      if (cb.checked) toast('Passo concluído');
    });
    $('#fecharGaveta').addEventListener('click', () => abrirGaveta(false));
    $('#veu').addEventListener('click', () => abrirGaveta(false));
    $('#buscaBtn').addEventListener('click', () => abrirPaleta(true));
    $('#paleta').addEventListener('click', (e) => { if (e.target.id === 'paleta') abrirPaleta(false); });
    $('#menuBtn').addEventListener('click', () => {
      const n = $('#nav');
      n.classList.toggle('aberta');
      $('#menuBtn').setAttribute('aria-expanded', String(n.classList.contains('aberta')));
    });
    $('#paletaInput').addEventListener('input', (e) => desenharPaleta(e.target.value));
    $('#paletaInput').addEventListener('keydown', (e) => {
      if (e.key === 'ArrowDown') { e.preventDefault(); moverPaleta(1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); moverPaleta(-1); }
      else if (e.key === 'Enter') {
        e.preventDefault();
        const it = resPaleta[selPaleta];
        if (!it) return;
        if (e.shiftKey) { alternarStack(it.id); return; }
        abrirPaleta(false); location.hash = urlItem(it);
      }
    });
    document.addEventListener('keydown', (e) => {
      const emCampo = /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '');
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') { e.preventDefault(); abrirPaleta(!$('#paleta').classList.contains('aberta')); }
      else if (e.key === '/' && !emCampo) { e.preventDefault(); abrirPaleta(true); }
      else if (e.key === 'Escape') { abrirPaleta(false); abrirGaveta(false); }
    });
    window.addEventListener('hashchange', () => { S.limite = 60; rota(); });
  }

  async function iniciar() {
    try {
      await carregar();
    } catch (e) {
      $('#app').innerHTML = `<div class="wrap" style="padding:80px 0"><div class="vazio"><p class="h3">Não consegui carregar o catálogo</p>
        <p>${location.protocol === 'file:' ? 'Abra a central por um servidor: <span class="mono">python3 tools/admin.py</span> ou <span class="mono">python3 -m http.server -d dist</span>.' : esc(e.message)}</p></div></div>`;
      return;
    }
    const h = hub();
    $('#socials').textContent = (h.socials || []).join(' · ');
    if (h.githubRepo) { const rl = $('#repoLink'); rl.hidden = false; rl.href = `https://github.com/${h.githubRepo}`; rl.target = '_blank'; rl.rel = 'noopener'; }
    const yt = (h.cta || {}).youtube;
    if (yt && urlSegura(yt.url)) { const yl = $('#ytLink'); yl.hidden = false; yl.href = yt.url; }
    atualizarFavs();
    ligar();
    salvarStack();
    rota();
  }
  iniciar();
})();
