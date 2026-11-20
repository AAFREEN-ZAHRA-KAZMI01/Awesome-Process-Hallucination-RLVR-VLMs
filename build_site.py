"""Rebuilds index.html (searchable paper table) from data/papers.json. Usage: python build_site.py"""
import json, html
P = json.load(open("data/papers.json"))
rows = "\n".join(
    f"<tr data-f=\"{html.escape(p['family'])}\"><td>{p['id']}</td><td><a href=\"{html.escape(p['url'])}\" target=\"_blank\">{html.escape(p['title'])}</a></td>"
    f"<td>{html.escape(p['first_author'])}</td><td>{p['year']}</td><td>{html.escape(p['venue'])}</td><td>{html.escape(p['family'])}</td>"
    f"<td>{html.escape(p['method'])}</td><td>{p['code']}</td><td>{p['quality']}</td></tr>" for p in P)
fams = sorted({p["family"] for p in P})
opts = "".join(f"<option>{html.escape(f)}</option>" for f in fams)
page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Process Hallucination in RL-Trained VLMs</title>
<style>
:root{{--bg:#fff;--fg:#1d2433;--muted:#5b6475;--line:#e3e7ee;--accent:#1f3b73;--chip:#eef2f8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#11151c;--fg:#e6e9ef;--muted:#9aa3b2;--line:#273041;--accent:#8fb4ff;--chip:#1b2230}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:1200px;margin:0 auto;padding:24px 16px}} h1{{font-size:24px;margin:0 0 4px}} p{{color:var(--muted);margin:0 0 16px}}
.bar{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px}} input,select{{padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--bg);color:var(--fg);font:inherit}}
input{{flex:1;min-width:200px}} .wrap{{overflow-x:auto;border:1px solid var(--line);border-radius:10px}}
table{{border-collapse:collapse;width:100%;font-size:13.5px}} th,td{{padding:8px 10px;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}}
th{{position:sticky;top:0;background:var(--chip);cursor:pointer;white-space:nowrap}} a{{color:var(--accent);text-decoration:none}} a:hover{{text-decoration:underline}}
#n{{color:var(--muted);font-size:13px;margin:8px 0}}
</style></head><body><main>
<h1>Process Hallucination in RL-Trained Vision-Language Models</h1>
<p>66 studies from a systematic review (2022–2026), grouped by the reward family they use. Click a column to sort.</p>
<div class="bar"><input id="q" placeholder="Search title, author, method…"><select id="f"><option value="">All reward families</option>{opts}</select></div>
<div id="n"></div>
<div class="wrap"><table id="t"><thead><tr><th>ID</th><th>Paper</th><th>First author</th><th>Year</th><th>Venue</th><th>Reward family</th><th>Method</th><th>Code</th><th>Quality</th></tr></thead>
<tbody>{rows}</tbody></table></div></main>
<script>
const q=document.getElementById('q'),f=document.getElementById('f'),rows=[...document.querySelectorAll('#t tbody tr')],n=document.getElementById('n');
function run(){{const s=q.value.toLowerCase(),fam=f.value;let k=0;rows.forEach(r=>{{const ok=(!fam||r.dataset.f===fam)&&r.textContent.toLowerCase().includes(s);r.style.display=ok?'':'none';if(ok)k++}});n.textContent=k+' of '+rows.length+' papers'}}
q.oninput=run;f.onchange=run;run();
document.querySelectorAll('#t th').forEach((th,i)=>th.onclick=()=>{{const tb=th.closest('table').tBodies[0],asc=th.dataset.a!=='1';th.dataset.a=asc?'1':'0';
[...tb.rows].sort((a,b)=>{{const x=a.cells[i].innerText,y=b.cells[i].innerText,nx=parseFloat(x),ny=parseFloat(y);return (isNaN(nx)||isNaN(ny)?x.localeCompare(y):nx-ny)*(asc?1:-1)}}).forEach(r=>tb.appendChild(r))}});
</script></body></html>"""
open("index.html", "w").write(page); print("index.html written:", len(P), "papers")
