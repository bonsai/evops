#!/usr/bin/env python3
"""Generate papers.html from papers.json (1 paper = 1 sheet page)."""
import json, os

D = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(D, "papers.json")
html_path = os.path.join(D, "papers.html")

c = json.load(open(json_path, encoding="utf-8"))
papers = c["papers"]
synthesis = c["synthesis"]

CSS = """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SSSS Papers - Papers Database</title>
<style>
@page { size: A4 landscape; margin: 0; }
:root{--pw:297mm;--ph:210mm;--ink:#16191d;--ink2:#464d55;--ink3:#7b838c;--rule:#d5dae0;--rule2:#eceef1;--paper:#fff;--screen:#23262b;--c-plan:#b45309;--c-plan-bg:#fdf5ea;--c-deliver:#1d4ed8;--c-deliver-bg:#eef3fe;--c-present:#047857;--c-present-bg:#e9faf3;--f-ja:"Noto Sans JP","Noto Sans CJK JP","Hiragino Kaku Gothic ProN","Yu Gothic UI",system-ui,sans-serif;--f-la:"Inter","Helvetica Neue","Segoe UI",system-ui,sans-serif;--f-mono:"SFMono-Regular","Cascadia Mono","Consolas",ui-monospace,monospace;}
*{box-sizing:border-box}html,body{margin:0;padding:0;background:var(--screen)}body{font-family:var(--f-la),var(--f-ja);color:var(--ink);-webkit-font-smoothing:antialiased}
.stage{transform-origin:top center}
.sheet{position:relative;width:var(--pw);height:var(--ph);background:var(--paper);overflow:hidden;margin:0 auto;box-shadow:0 6px 28px rgba(0,0,0,.45);padding:13mm 15mm 12mm;display:flex;flex-direction:column;font-size:9.4pt;line-height:1.68;--accent:var(--c-plan);--accent-bg:var(--c-plan-bg)}
.cat-paper{--accent:var(--c-plan);--accent-bg:var(--c-plan-bg)}
.cat-vlm{--accent:var(--c-deliver);--accent-bg:var(--c-deliver-bg)}
.cat-3d{--accent:var(--c-present);--accent-bg:var(--c-present-bg)}
.sheet+.sheet{margin-top:8mm}
.sheet::before{content:"";position:absolute;left:0;right:0;top:0;height:2.2mm;background:var(--accent)}
.hd{display:flex;align-items:flex-end;gap:6mm;padding-bottom:2.2mm;border-bottom:.4mm solid var(--rule);flex:0 0 auto}
.hd-kicker{font-size:8.2pt;font-weight:800;letter-spacing:.13em;color:var(--accent);background:var(--accent-bg);padding:1mm 2.8mm;border-radius:1mm;white-space:nowrap}
.hd-title{font-size:12.8pt;font-weight:800;letter-spacing:.01em;line-height:1.26;flex:1 1 auto;margin:0}
.hd-title small{display:block;font-size:8.4pt;font-weight:500;color:var(--ink3);margin-top:.75mm}
.hd-meta{font-family:var(--f-mono);font-size:8.4pt;color:var(--ink3)}
.hd-no{font-family:var(--f-mono);font-size:9pt;color:var(--ink3);white-space:nowrap}
.body{flex:1 1 auto;padding-top:3.8mm;min-height:0}
.cover{padding:0}
.cover-in{height:100%;display:flex;flex-direction:column;justify-content:center;padding:0 24mm;position:relative}
.cover-in::before{content:"";position:absolute;left:0;top:0;bottom:0;width:14mm;background:var(--accent)}
.cover-label{font-size:9.5pt;letter-spacing:.28em;color:var(--accent);font-weight:800;margin-bottom:6mm}
.cover-h1{font-size:28pt;font-weight:800;line-height:1.28;margin:0 0 5mm}
.cover-sub{font-size:10.5pt;color:var(--ink2);margin:0 0 15mm;line-height:1.6}
.cover-meta{display:flex;gap:11mm;border-top:.4mm solid var(--rule);padding-top:6mm;font-size:9.8pt}
.cover-meta>div{min-width:32mm}
.cover-meta .k{font-size:7.8pt;letter-spacing:.14em;color:var(--ink3);display:block;margin-bottom:1.2mm}
.cover-meta .v{font-weight:700}
.card{border:.35mm solid var(--rule);border-radius:1.2mm;padding:2.8mm 3.4mm;background:#fff}
.card-h{font-size:8.6pt;font-weight:800;letter-spacing:.04em;color:var(--accent);display:flex;align-items:center;gap:2.2mm;margin-bottom:1.8mm}
.card-h .no{font-family:var(--f-mono);font-size:7.4pt;background:var(--accent);color:#fff;border-radius:1mm;padding:.5mm 1.6mm;letter-spacing:0}
.lead{font-size:10.2pt;line-height:1.75}
p{margin:0 0 2mm}p:last-child{margin-bottom:0}
small{font-size:8.2pt;color:var(--ink3)}
.meta-row{display:grid;grid-template-columns:auto 1fr;gap:1.1mm 4mm;font-size:8.8pt;margin:2.3mm 0}
.meta-row dt{font-weight:800;color:var(--ink2);white-space:nowrap}
.tags{display:flex;flex-wrap:wrap;gap:2.8mm;margin:2.2mm 0}
.tag{font-size:7.5pt;padding:.5mm 1.3mm;border-radius:.8mm;background:var(--accent-bg);color:var(--accent);font-weight:700;white-space:nowrap}
.note{border-left:.9mm solid var(--accent);background:var(--accent-bg);padding:2.3mm 3mm;font-size:9pt;border-radius:0 1mm 1mm 0}
.note b{color:var(--accent)}
.footer{display:flex;justify-content:space-between;padding-top:3mm;border-top:.3mm solid var(--rule2);font-size:7.7pt;color:var(--ink3);margin-top:3mm}
.syn-list{margin:0;padding-left:0;list-style:none}
.syn-list li{display:flex;gap:3mm;margin-bottom:1.8mm}
.syn-list .n{font-family:var(--f-mono);font-size:7.6pt;color:var(--accent);min-width:20mm}
.syn-list .t{flex:1}
.syn-list .t b{color:var(--ink2)}
.nav{position:fixed;left:50%;bottom:5mm;transform:translateX(-50%);display:flex;align-items:center;gap:1.6mm;background:rgba(20,22,26,.92);border:1px solid rgba(255,255,255,.14);border-radius:999px;padding:1.5mm 2.2mm;z-index:50;color:#e8ecf1;box-shadow:0 6px 20px rgba(0,0,0,.45)}
.nav button{all:unset;cursor:pointer;padding:1.1mm 2.6mm;border-radius:999px;color:#cfd6de;font-size:11px}
.nav button:hover{background:rgba(255,255,255,.14);color:#fff}
.nav .cur{font-family:var(--f-mono);font-size:11px;padding:0 1.6mm;min-width:22mm;text-align:center;color:#fff;font-variant-numeric:tabular-nums}
.nav .cur em{color:#7f8b98;font-style:normal}
.nav .sep{width:1px;height:14px;background:rgba(255,255,255,.16)}
.nav .ttl{font-size:10.4px;padding:0 1mm;color:#9aa5b1;max-width:40mm;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.toc{display:grid;grid-template-columns:repeat(3,1fr);gap:4mm 5mm}
.toc-sec{border-top:.9mm solid var(--accent);padding-top:2.2mm}
.toc-sec h4{margin:0 0 2mm;font-size:9.8pt;font-weight:800;color:var(--accent);letter-spacing:.03em}
.toc-sec ol{list-style:none;margin:0;padding:0}
.toc li{display:flex;gap:2mm;align-items:baseline;margin-bottom:1.2mm;font-size:8.3pt;cursor:pointer}
.toc li:hover{color:var(--accent)}
.toc li .pg{font-family:var(--f-mono);font-size:7.6pt;color:var(--ink3);min-width:9mm;text-align:right}
.toc li .txt{flex:1}
</style>
</head>
<body>
<div class="stage" id="stage">
<div class="stage-inner" id="sheets">
"""

def render_paper(p, idx, total):
    cat = p.get("categories", [])
    if "3d" in cat or "generation" in cat:
        catclass = "cat-3d"
    elif "v lm" in cat:
        catclass = "cat-vlm"
    else:
        catclass = "cat-paper"
    tags = "".join('<span class="tag">' + t + '</span>' for t in cat)
    next_txt = (papers[idx + 1]["title"][:50] if idx + 1 < total else "To Contents")
    prev_txt = (papers[idx - 1]["title"][:50] if idx > 0 else "")
    prev_attr = 'data-go="%d"' % (idx - 1) if idx > 0 else 'disabled'
    next_attr = 'data-go="%d"' % (idx + 2) if idx + 1 < total else 'disabled'
    return '''
<section class="sheet ''' + catclass + '''" data-t="''' + p["title"][:60] + '''">
  <div class="hd">
    <span class="hd-kicker">PAPER ''' + str(idx + 1).zfill(2) + '''</span>
    <h2 class="hd-title">''' + p["title"] + '''<small>''' + p.get("short", "") + '''</small></h2>
    <span class="hd-meta">''' + p["venue"] + ''' / ''' + str(p["year"]) + '''</span>
    <span class="hd-no">''' + str(idx + 2).zfill(2) + '''</span>
  </div>
  <div class="body">
    <div class="card">
      <div class="card-h"><span class="no">01</span>Summary</div>
      <p class="lead">''' + p["body"] + '''</p>
    </div>
    <div class="meta-row" style="margin-top:3mm">
      <dt>Relevance to theme</dt>
      <dd><p style="margin:0">''' + p["relevance"] + '''</p></dd>
    </div>
    <div class="tags">''' + tags + '''</div>
    <div class="footer">
      <span><button ''' + prev_attr + ''' class="navbutton" style="all:unset;cursor:inherit;color:var(--ink3);background:none;border:none;padding:0;font-size:8.2pt;margin-right:4px;">&larr; Prev</button>''' + prev_txt + '''</span>
      <span>''' + next_txt + ''' <button ''' + next_attr + ''' class="navbutton" style="all:unset;cursor:inherit;color:var(--ink3);background:none;border:none;padding:0;font-size:8.2pt;margin-left:4px;">Next &rarr;</button></span>
    </div>
  </div>
</section>
'''

def render_toc(total):
    return [''.join('''<li %s><span class="pg">%02d</span><span class="txt">%s</span></li>''' % (i + 2, i + 2, papers[i]["title"][:65])) for i in range(total)]

toc_items = render_toc(len(papers))

syn_lines = []
for i, s in enumerate(synthesis, 1):
    syn_lines.append('''<li><span class="n">%02d</span><span class="t"><b>%s</b> %s</span></li>''' % (i, s[:8], s[8:]))

synthesis_page = '''
<section class="sheet cat-paper" data-t="Synthesis">
  <div class="hd">
    <span class="hd-kicker">TOP</span>
    <h2 class="hd-title">Synthesis<small>論文から得られた設計原則 (5 本柱)</small></h2>
    <span class="hd-no">02</span>
  </div>
  <div class="body">
    <ol class="syn-list">
      %s
    </ol>
  </div>
</section>
''' % "\n".join(syn_lines)

toc_ol = ""
for j in range(3):
    start = j * 3
    cols = [toc_items[i] for i in range(start, min(start + 3, len(toc_items)))]
    toc_ol += '''<div class="toc-sec"><h4>PAPER %02d-%02d</h4><ol>%s</ol><ol>%s</ol><ol>%s</ol></div>''' % (start + 1, min(start + 3, len(toc_items)), cols[0], cols[1] if len(cols) > 1 else "", cols[2] if len(cols) > 2 else "")

cover = f'''
<section class="sheet cover cat-paper" data-t="Contents">
  <div class="cover-in">
    <div class="cover-label">SSSS RESEARCH</div>
    <h1 class="cover-h1">Papers</h1>
    <p class="cover-sub">''' + c["research_question"] + '''</p>
    <div class="cover-meta">
      <div><span class="k">papers</span><span class="v">''' + str(len(papers)) + ''' papers &middot; JSON + 1 paper 1 page</span></div>
      <div><span class="k">loop</span><span class="v">Generation &rarr; VLM &rarr; DB &rarr; ML &rarr; Repair &rarr; Generation</span></div>
    </div>
  </div>
</section>

<section class="sheet cat-paper" data-t="Contents">
  <div class="hd">
    <span class="hd-kicker">Contents</span>
    <h2 class="hd-title">Papers<small>''' + str(len(papers)) + ''' papers</small></h2>
    <span class="hd-no">01</span>
  </div>
  <div class="body">
    <div class="toc">''' + toc_ol + '''</div>
  </div>
</section>
'''

html = CSS + "\n" + cover + synthesis_page + "\n".join(render_paper(p, i, len(papers)) for i, p in enumerate(papers)) + "\n"
html += '''
</div>
</div>
<script>
(function(){var sheets=[].slice.call(document.querySelectorAll('.sheet'));if(!sheets.length)return;
var nav=document.getElementById('nav');var curNo=document.getElementById('curNo');var curAll=document.getElementById('curAll');var curTtl=document.getElementById('curTtl');
var stage=document.getElementById('stage');var current=0;var buffer='';
function pad(n){return n<10?'0'+n:String(n)}
function titleOf(i){return sheets[i].getAttribute('data-t')||('p.'+pad(i+1))}
function sync(){curNo.textContent=pad(current+1);curAll.textContent=sheets.length;curTtl.textContent=titleOf(current);if(history.replaceState)history.replaceState(null,'','#'+(current+1))}
function goto(i,smooth){current=Math.max(0,Math.min(sheets.length-1,i));sheets[current].scrollIntoView({behavior:smooth===false?'auto':'smooth',block:'start'});sync()}
function nearest(){var mid=window.innerHeight/2,best=0;for(var i=0;i<sheets.length;i++){if(sheets[i].getBoundingClientRect().top<=mid)best=i}return best}
function fit(){var avail=document.documentElement.clientWidth-16;var w=sheets[0].getBoundingClientRect().width;if(!w)return;var scale=Math.min(1,avail/w);if(scale<1){stage.style.transform='scale('+scale+')';stage.style.width=(w*scale)+'px';stage.style.marginLeft='auto';stage.style.marginRight='auto'}else{stage.style.transform='';stage.style.width='';stage.style.marginLeft='';stage.style.marginRight=''}}
var resizeTimer=null;window.addEventListener('resize',function(){clearTimeout(resizeTimer);resizeTimer=setTimeout(fit,120)});
[].slice.call(document.querySelectorAll('[data-go]')).forEach(function(el){el.addEventListener('click',function(){goto(parseInt(el.getAttribute('data-go'),10))})});
document.getElementById('first').addEventListener('click',function(){goto(0)});
document.getElementById('prev').addEventListener('click',function(){goto(current-1)});
document.getElementById('next').addEventListener('click',function(){goto(current+1)});
document.getElementById('last').addEventListener('click',function(){goto(sheets.length-1)});
var jumpTimer=null;document.addEventListener('keydown',function(e){if(e.metaKey||e.ctrlKey||e.altKey)return;var k=e.key;
if(k>='0'&&k<='9'){buffer+=k;clearTimeout(jumpTimer);jumpTimer=setTimeout(function(){var n=parseInt(buffer,10);buffer='';if(n>=1&&n<=sheets.length)goto(n-1)},600);return}
switch(k){case'ArrowRight':case'PageDown':case' ':case'Enter':e.preventDefault();goto(current+1);break;
case'ArrowLeft':case'PageUp':e.preventDefault();goto(current-1);break;
case'Home':e.preventDefault();goto(0);break;case'End':e.preventDefault();goto(sheets.length-1);break}});
var jumpKeys=['first','prev','next','last'];jumpKeys.forEach(function(id){var btn=document.getElementById(id);if(btn)btn.addEventListener('click',function(e){e.preventDefault()})});
function initNav(){var n=document.createElement('nav');n.className='nav';n.id='nav';n.innerHTML='<button type="button" id="first" title="first">&#8676;</button><button type="button" id="prev" title="prev">&#9664;</button><span class="cur"><span id="curNo">01</span><em> / <span id="curAll"></span></em></span><button type="button" id="next" title="next">&#9654;</button><button type="button" id="last" title="last">&#8677;</button>';document.body.appendChild(n);sync();fit();}
initNav();
})();
</script>
</body>
</html>
'''

open(html_path, "w", encoding="utf-8").write(html)
print("written:", html_path)
print("sheets:", len(papers) + 2, "(cover + toc +", len(papers), "papers + synthesis)")
