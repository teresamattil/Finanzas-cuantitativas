import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read_md(rel, strip_fm=False, no_img=False):
    path = os.path.join(BASE, rel)
    with open(path, encoding='utf-8') as f:
        t = f.read()
    if strip_fm:
        t = re.sub(r'^---\s*\n[\s\S]*?\n---\s*\n', '', t)
    if no_img:
        t = re.sub(r'!\[.*?\]\([^)]*\)\n?', '', t)
    return t.strip()

contents = {
    'home':        read_md('Resumen- Cuatri.md'),
    'm7':          read_md('7 - Valoración de instrumentos financieros/resumen_modulo07.md', strip_fm=True),
    'm7-medicion': read_md('7 - Valoración de instrumentos financieros/temas 06 a 10 - Medición/Resumen_Temas_6-9.md'),
    'm7-markowitz':read_md('7 - Valoración de instrumentos financieros/temas 06 a 10 - Medición/Markowitz_CAL_Sharpe.md'),
    'm7-val1':     read_md('7 - Valoración de instrumentos financieros/temas 11 a 17 - Valoración I/resumen_temas_11_17_v2.md'),
    'm7-val2':     read_md('7 - Valoración de instrumentos financieros/temas 18 a 21 - Valoración II/resumen_temas_18_21.md', strip_fm=True),
    'm8':          read_md('8 - Gestión de carteras de inversión/resumen_modulo08.md', strip_fm=True),
    'm9':          read_md('9 - Gestión de riesgos/resumen_modulo09.md'),
    'm9-mates':    read_md('9 - Gestión de riesgos/mates_de_detras.md'),
    'm10':         read_md('10 - Teoría del valor extremo/resumen_modulo10.md'),
    'p001':        read_md('preguntas/respuesta_001.md', strip_fm=True),
    'p002':        read_md('preguntas/respuesta_002.md', strip_fm=True, no_img=True),
    'p003':        read_md('preguntas/respuesta_003.md', strip_fm=True, no_img=True),
    'p004':        read_md('preguntas/respuesta_004.md', strip_fm=True),
    'p005':        read_md('preguntas/respuesta_005.md', strip_fm=True),
    'p006':        read_md('preguntas/respuesta_006.md', strip_fm=True),
}

# Fix Markowitz: bare Python lines -> code block
old_py = ("# Expected portfolio return\n"
          "np.sum(weights * log_returns.mean())* 250\n"
          "# Expected Portfolio Variance\n"
          "np.dot(weights.T,np.dot(log_returns.cov()* 250,weights))\n"
          "# Expected Portfolio Volatility\n"
          "np.sqrt(np.dot(weights.T,np.dot(log_returns.cov()* 250,weights)))")
new_py = ("```python\n"
          "# Expected portfolio return\n"
          "np.sum(weights * log_returns.mean()) * 250\n"
          "# Expected Portfolio Variance\n"
          "np.dot(weights.T, np.dot(log_returns.cov() * 250, weights))\n"
          "# Expected Portfolio Volatility\n"
          "np.sqrt(np.dot(weights.T, np.dot(log_returns.cov() * 250, weights)))\n"
          "```")
contents['m7-markowitz'] = contents['m7-markowitz'].replace(old_py, new_py)

def script_blocks():
    return '\n'.join(
        f'<script type="text/markdown" id="c-{k}">\n{v}\n</script>'
        for k, v in contents.items()
    )

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Finanzas Cuantitativas M7–M10</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --sb:252px;
  --c7:#3b82f6;--c8:#8b5cf6;--c9:#10b981;--c10:#f59e0b;--cp:#ef4444;--ch:#60a5fa;
  --tx:#1e293b;--tm:#64748b;--bg:#f8fafc;--bdr:#e2e8f0;--card:#ffffff
}
body{font-family:system-ui,sans-serif;color:var(--tx);background:var(--bg);display:flex;min-height:100vh}

/* SIDEBAR */
.sb{width:var(--sb);background:#1e1e2e;color:#cbd5e1;position:fixed;top:0;left:0;bottom:0;overflow-y:auto;display:flex;flex-direction:column}
.sb-logo{padding:1.4rem 1.25rem;border-bottom:1px solid #2d3748}
.sb-logo-main{font-size:.88rem;font-weight:700;color:#f1f5f9}
.sb-logo-sub{font-size:.7rem;color:#475569;margin-top:.2rem}
.sb-sec{padding-top:1.2rem}
.sb-lbl{padding:.2rem 1.25rem .45rem;font-size:.6rem;text-transform:uppercase;letter-spacing:.1em;color:#475569;font-weight:700}
.sb-a{display:block;padding:.52rem 1.25rem;font-size:.86rem;color:#94a3b8;cursor:pointer;border-left:3px solid transparent;transition:all .12s;user-select:none}
.sb-a:hover{color:#e2e8f0;background:rgba(255,255,255,.04)}
.sb-a.on{color:#f1f5f9;font-weight:600;background:rgba(255,255,255,.07)}
.sb-a.on[data-id=home]{border-color:var(--ch)}
.sb-a.on[data-mod=m7]{border-color:var(--c7)}
.sb-a.on[data-mod=m8]{border-color:var(--c8)}
.sb-a.on[data-mod=m9]{border-color:var(--c9)}
.sb-a.on[data-mod=m10]{border-color:var(--c10)}
.sb-a.on[data-mod=p]{border-color:var(--cp)}

/* MAIN */
.main{margin-left:var(--sb);flex:1;padding:2.25rem 3.5rem 5rem;min-width:0}

/* BREADCRUMB */
.bc{display:flex;align-items:center;gap:.4rem;font-size:.78rem;color:var(--tm);margin-bottom:1.75rem;flex-wrap:wrap}
.bc span{cursor:pointer}
.bc span:hover{text-decoration:underline;color:var(--tx)}
.bc span.cur{color:var(--tx);font-weight:500;cursor:default}
.bc span.cur:hover{text-decoration:none}
.bc-sep{color:#cbd5e1;cursor:default!important}

/* MODULE CARDS (landing) */
.mod-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.9rem;margin-bottom:2.5rem}
.mc{background:var(--card);border:1px solid var(--bdr);border-radius:10px;border-top:4px solid;padding:1.1rem 1.25rem;cursor:pointer;transition:all .14s}
.mc:hover{box-shadow:0 6px 18px rgba(0,0,0,.1);transform:translateY(-2px)}
.mc.m7{border-top-color:var(--c7)}.mc.m8{border-top-color:var(--c8)}
.mc.m9{border-top-color:var(--c9)}.mc.m10{border-top-color:var(--c10)}
.mc-id{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;margin-bottom:.35rem}
.mc.m7 .mc-id{color:var(--c7)}.mc.m8 .mc-id{color:var(--c8)}
.mc.m9 .mc-id{color:var(--c9)}.mc.m10 .mc-id{color:var(--c10)}
.mc-t{font-size:.93rem;font-weight:600;margin-bottom:.25rem}
.mc-d{font-size:.73rem;color:var(--tm)}

/* DETAIL CARDS (level 1 -> 2) */
.det-wrap{margin-bottom:2rem}
.det-lbl{font-size:.65rem;text-transform:uppercase;letter-spacing:.09em;color:var(--tm);font-weight:700;margin-bottom:.6rem}
.det-row{display:flex;flex-wrap:wrap;gap:.65rem}
.dc{background:var(--card);border:1px solid var(--bdr);border-radius:8px;padding:.8rem 1.1rem;cursor:pointer;transition:all .12s;flex:1;min-width:155px}
.dc:hover{box-shadow:0 3px 10px rgba(0,0,0,.1);transform:translateY(-1px)}
.dc-t{font-size:.88rem;font-weight:600;margin-bottom:.2rem}
.dc-s{font-size:.73rem;color:var(--tm)}
.dc.m7 .dc-t{color:var(--c7)}.dc.m8 .dc-t{color:var(--c8)}
.dc.m9 .dc-t{color:var(--c9)}.dc.m10 .dc-t{color:var(--c10)}

/* QUESTION CARDS */
.q-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1rem;margin-top:1.5rem}
.qc{background:var(--card);border:1px solid var(--bdr);border-radius:10px;padding:1.25rem;cursor:pointer;transition:all .14s}
.qc:hover{border-color:var(--cp);box-shadow:0 4px 14px rgba(0,0,0,.1);transform:translateY(-2px)}
.qc-n{font-size:.65rem;font-weight:800;text-transform:uppercase;letter-spacing:.1em;color:var(--cp);margin-bottom:.5rem}
.qc-t{font-size:.93rem;font-weight:600;line-height:1.4}

/* MARKDOWN CONTENT */
#content{max-width:820px;line-height:1.75}
#content h1{font-size:1.85rem;font-weight:800;margin-bottom:1rem;color:#0f172a;line-height:1.25}
#content h2{font-size:1.3rem;font-weight:700;margin:2.25rem 0 .7rem;color:#0f172a;border-bottom:2px solid var(--bdr);padding-bottom:.35rem}
#content h3{font-size:1.05rem;font-weight:700;margin:1.75rem 0 .5rem;color:#1e293b}
#content h4{font-size:.95rem;font-weight:700;margin:1.25rem 0 .4rem;color:#334155}
#content p{margin-bottom:.9rem}
#content ul,#content ol{margin:.5rem 0 .9rem 1.6rem}
#content li{margin-bottom:.3rem}
#content table{border-collapse:collapse;width:100%;margin:1.1rem 0;font-size:.88rem}
#content th{background:#f1f5f9;padding:.55rem .85rem;text-align:left;font-weight:700;border:1px solid var(--bdr)}
#content td{padding:.45rem .85rem;border:1px solid var(--bdr)}
#content tr:nth-child(even) td{background:#f8fafc}
#content code{font-family:Consolas,Monaco,monospace;background:#f1f5f9;padding:.15em .4em;border-radius:3px;font-size:.86em;color:#c7254e}
#content pre{background:#1e293b;color:#e2e8f0;border-radius:8px;padding:1.25rem;overflow-x:auto;margin:1rem 0;font-size:.85rem;line-height:1.65}
#content pre code{background:none;padding:0;color:inherit;font-size:inherit}
#content blockquote{border-left:4px solid var(--c7);background:#eff6ff;padding:.85rem 1.1rem;margin:1rem 0;border-radius:0 6px 6px 0;color:#1e40af}
#content blockquote p{margin:0}
#content hr{border:none;border-top:1px solid var(--bdr);margin:2rem 0}
#content strong{font-weight:700}
.mjx-container{overflow-x:auto}
</style>
</head>
<body>

<aside class="sb">
  <div class="sb-logo">
    <div class="sb-logo-main">Finanzas Cuantitativas</div>
    <div class="sb-logo-sub">Máster · Módulos 7–10</div>
  </div>
  <div class="sb-sec">
    <div class="sb-lbl">General</div>
    <div class="sb-a" data-id="home" onclick="nav('home')">Vista General</div>
  </div>
  <div class="sb-sec">
    <div class="sb-lbl">Módulos</div>
    <div class="sb-a" data-id="m7" data-mod="m7" onclick="nav('m7')">M7 — Valoración</div>
    <div class="sb-a" data-id="m8" data-mod="m8" onclick="nav('m8')">M8 — Carteras</div>
    <div class="sb-a" data-id="m9" data-mod="m9" onclick="nav('m9')">M9 — Riesgos</div>
    <div class="sb-a" data-id="m10" data-mod="m10" onclick="nav('m10')">M10 — Valor Extremo</div>
  </div>
  <div class="sb-sec">
    <div class="sb-lbl">Examen</div>
    <div class="sb-a" data-id="preguntas" data-mod="p" onclick="nav('preguntas')">Preguntas de Examen</div>
  </div>
</aside>

<div class="main">
  <div id="bc" class="bc"></div>
  <div id="top"></div>
  <div id="content"></div>
</div>

""" + script_blocks() + r"""

<script src="https://cdn.jsdelivr.net/npm/marked@9/marked.min.js"></script>
<script>
window.MathJax={tex:{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre']}};
</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" async></script>
<script>
const CFG={
  home:{bc:[{l:'Vista General',id:'home'}],cid:'c-home',top:'modules',mod:'home'},
  m7:{bc:[{l:'Vista General',id:'home'},{l:'M7 — Valoración',id:'m7'}],cid:'c-m7',top:'detail',mod:'m7',
    cards:[
      {t:'Medición (T6–9)',s:'Retornos, riesgo, distribuciones, diversificación',id:'m7-medicion'},
      {t:'Markowitz, CAL y Sharpe',s:'Frontera eficiente y portfolio tangente',id:'m7-markowitz'},
      {t:'Valoración I (T11–17)',s:'Bonos, acciones, CAPM, APT, Fama-French',id:'m7-val1'},
      {t:'Valoración II (T18–21)',s:'Derivados, Black-Scholes, Monte Carlo, Euler',id:'m7-val2'},
    ]},
  'm7-medicion':{bc:[{l:'Vista General',id:'home'},{l:'M7 — Valoración',id:'m7'},{l:'Medición (T6–9)',id:'m7-medicion'}],cid:'c-m7-medicion',top:null,mod:'m7'},
  'm7-markowitz':{bc:[{l:'Vista General',id:'home'},{l:'M7 — Valoración',id:'m7'},{l:'Markowitz, CAL y Sharpe',id:'m7-markowitz'}],cid:'c-m7-markowitz',top:null,mod:'m7'},
  'm7-val1':{bc:[{l:'Vista General',id:'home'},{l:'M7 — Valoración',id:'m7'},{l:'Valoración I (T11–17)',id:'m7-val1'}],cid:'c-m7-val1',top:null,mod:'m7'},
  'm7-val2':{bc:[{l:'Vista General',id:'home'},{l:'M7 — Valoración',id:'m7'},{l:'Valoración II (T18–21)',id:'m7-val2'}],cid:'c-m7-val2',top:null,mod:'m7'},
  m8:{bc:[{l:'Vista General',id:'home'},{l:'M8 — Carteras',id:'m8'}],cid:'c-m8',top:null,mod:'m8'},
  m9:{bc:[{l:'Vista General',id:'home'},{l:'M9 — Riesgos',id:'m9'}],cid:'c-m9',top:'detail',mod:'m9',
    cards:[{t:'Fundamentos matemáticos (T1–12)',s:'Probabilidad, distribuciones, series temporales, GARCH',id:'m9-mates'}]},
  'm9-mates':{bc:[{l:'Vista General',id:'home'},{l:'M9 — Riesgos',id:'m9'},{l:'Fundamentos matemáticos',id:'m9-mates'}],cid:'c-m9-mates',top:null,mod:'m9'},
  m10:{bc:[{l:'Vista General',id:'home'},{l:'M10 — Valor Extremo',id:'m10'}],cid:'c-m10',top:null,mod:'m10'},
  preguntas:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas de Examen',id:'preguntas'}],cid:null,top:'questions',mod:'p'},
  p001:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas',id:'preguntas'},{l:'001 — Normal vs t-Student',id:'p001'}],cid:'c-p001',top:null,mod:'p'},
  p002:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas',id:'preguntas'},{l:'002 — Rasgos diagnósticos',id:'p002'}],cid:'c-p002',top:null,mod:'p'},
  p003:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas',id:'preguntas'},{l:'003 — Cálculo del VaR',id:'p003'}],cid:'c-p003',top:null,mod:'p'},
  p004:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas',id:'preguntas'},{l:'004 — Escalado con √n',id:'p004'}],cid:'c-p004',top:null,mod:'p'},
  p005:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas',id:'preguntas'},{l:'005 — Utilidad media-varianza',id:'p005'}],cid:'c-p005',top:null,mod:'p'},
  p006:{bc:[{l:'Vista General',id:'home'},{l:'Preguntas',id:'preguntas'},{l:'006 — Transaction costs en Markowitz',id:'p006'}],cid:'c-p006',top:null,mod:'p'},
};

function parseMd(text){
  const saved=[];
  text=text.replace(/\$\$([\s\S]*?)\$\$/g,(_,m)=>{saved.push('<div style="overflow-x:auto;padding:.5rem 0">\\['+m+'\\]</div>');return'@@M'+(saved.length-1)+'@@';});
  text=text.replace(/\$([^\n$]{1,300}?)\$/g,(_,m)=>{saved.push('\\('+m+'\\)');return'@@M'+(saved.length-1)+'@@';});
  let h=marked.parse(text);
  saved.forEach((s,i)=>{h=h.split('@@M'+i+'@@').join(s);});
  return h;
}

function nav(id){
  const c=CFG[id]; if(!c) return;
  // breadcrumb
  document.getElementById('bc').innerHTML=c.bc.map((b,i)=>{
    const last=i===c.bc.length-1;
    return last?`<span class="cur">${b.l}</span>`:`<span onclick="nav('${b.id}')">${b.l}</span><span class="bc-sep">›</span>`;
  }).join(' ');
  // sidebar
  document.querySelectorAll('.sb-a').forEach(el=>el.classList.remove('on'));
  const modMap={home:'home',m7:'m7',m8:'m8',m9:'m9',m10:'m10',p:'preguntas'};
  const sbEl=document.querySelector(`.sb-a[data-id="${modMap[c.mod]||c.mod}"]`);
  if(sbEl) sbEl.classList.add('on');
  // top area
  const topEl=document.getElementById('top');
  const modCls=c.mod==='home'?'':(c.mod==='p'?'':c.mod);
  if(c.top==='modules'){
    topEl.innerHTML=`<div class="mod-grid">
      <div class="mc m7" onclick="nav('m7')"><div class="mc-id">M7</div><div class="mc-t">Valoración de Instrumentos</div><div class="mc-d">Medición, bonos, acciones, Black-Scholes</div></div>
      <div class="mc m8" onclick="nav('m8')"><div class="mc-id">M8</div><div class="mc-t">Gestión de Carteras</div><div class="mc-d">Delta hedging, volatilidad, gestión activa</div></div>
      <div class="mc m9" onclick="nav('m9')"><div class="mc-id">M9</div><div class="mc-t">Gestión de Riesgos</div><div class="mc-d">VaR, ES, crédito, liquidez, Basilea</div></div>
      <div class="mc m10" onclick="nav('m10')"><div class="mc-id">M10</div><div class="mc-t">Valor Extremo</div><div class="mc-d">EVT, GEV, GPD, POT, Hill</div></div>
    </div>`;
  } else if(c.top==='detail'&&c.cards){
    const cls=c.mod;
    topEl.innerHTML=`<div class="det-wrap"><div class="det-lbl">Ir al detalle</div><div class="det-row">${
      c.cards.map(d=>`<div class="dc ${cls}" onclick="nav('${d.id}')"><div class="dc-t">${d.t}</div><div class="dc-s">${d.s}</div></div>`).join('')
    }</div></div>`;
  } else if(c.top==='questions'){
    topEl.innerHTML='';
  } else {
    topEl.innerHTML='';
  }
  // content
  const el=document.getElementById('content');
  if(c.top==='questions'){
    el.innerHTML=`<h1>Preguntas de Examen</h1>
<p style="color:var(--tm);margin:.75rem 0 0">Registro de preguntas trabajadas sobre los módulos 7–10.</p>
<div class="q-grid">
  <div class="qc" onclick="nav('p001')"><div class="qc-n">Pregunta 001</div><div class="qc-t">¿Por qué importa elegir Normal vs t-Student para retornos diarios? ¿Cuándo es óptima cada una?</div></div>
  <div class="qc" onclick="nav('p002')"><div class="qc-n">Pregunta 002</div><div class="qc-t">¿Qué rasgos teórico-matemáticos delatan si los datos siguen una Normal o una t-Student?</div></div>
  <div class="qc" onclick="nav('p003')"><div class="qc-n">Pregunta 003</div><div class="qc-t">¿Cómo se calcula el VaR? Cuatro métodos: paramétrico, histórico, Monte Carlo y EVT.</div></div>
  <div class="qc" onclick="nav('p004')"><div class="qc-n">Pregunta 004</div><div class="qc-t">¿Cuál es la intuición detrás de escalar el VaR con √n al cambiar el horizonte temporal?</div></div>
  <div class="qc" onclick="nav('p005')"><div class="qc-n">Pregunta 005</div><div class="qc-t">¿Qué es la utilidad media-varianza (mean-variance utility)? ¿Por qué importa?</div></div>
  <div class="qc" onclick="nav('p006')"><div class="qc-n">Pregunta 006</div><div class="qc-t">¿Qué son los transaction costs en Markowitz? ¿Por qué importan?</div></div>
</div>`;
  } else if(c.cid){
    el.innerHTML=parseMd(document.getElementById(c.cid).textContent);
  } else {
    el.innerHTML='';
  }
  window.scrollTo(0,0);
  if(window.MathJax&&MathJax.typesetPromise) MathJax.typesetPromise();
}

document.addEventListener('DOMContentLoaded',()=>nav('home'));
</script>
</body>
</html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"Generado: {out} ({os.path.getsize(out)//1024} KB)")
