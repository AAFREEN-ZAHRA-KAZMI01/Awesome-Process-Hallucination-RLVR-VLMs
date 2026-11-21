"""Build draw.io files whose geometry copies the paper's figures exactly:
TikZ figures from logged node coordinates, the framework figure from framework_fig.py coordinates."""
import json, re, html, os
G=json.load(open('drawio_work/geometry.json'))
OUT='diagrams/'
S=2.0; M=10   # px per pt, margin px
CM=28.4528
def col(spec):
    base={'black':(0,0,0),'white':(1,1,1),'blue':(0,0,1),'red':(1,0,0),'green':(0,1,0),'yellow':(1,1,0),'cyan':(0,1,1),'orange':(1,.5,0),'gray':(.5,.5,.5)}
    parts=spec.split('!'); c=base[parts[0]]; i=1
    while i<len(parts):
        p=float(parts[i])/100; other=base[parts[i+1]] if i+1<len(parts) else (1,1,1)
        c=tuple(p*a+(1-p)*b for a,b in zip(c,other)); i+=2
    return '#%02X%02X%02X'%tuple(round(255*v) for v in c)
def tex2html(t):
    t=t.strip()
    t=re.sub(r'\\textcolor\{([^}]*)\}\{([^{}]*)\}',lambda m:f"<font color='{col(m.group(1))}'>{m.group(2)}</font>",t)
    t=t.replace(r'$r^{\mathrm{acc}}=1$','<i>r</i><sup>acc</sup> = 1').replace(r'$\Rightarrow$','⇒').replace(r'$\kappa$','κ')
    t=re.sub(r'\(\\emph\{n\}\\,=\\,([^)]*)\)',r'(<i>n</i> = \1)',t)
    t=t.replace(r'\emph{n}\,=\,','<i>n</i> = ')
    for _ in range(3):
        t=re.sub(r'\\textbf\{([^{}]*)\}',r'<b>\1</b>',t); t=re.sub(r'\\emph\{([^{}]*)\}',r'<i>\1</i>',t)
    t=re.sub(r'\\\\(\[[^\]]*\])?','<br>',t)
    t=t.replace(r'\quad','&nbsp;&nbsp;&nbsp;&nbsp;').replace(r'\,',' ').replace('--','–').replace(r'\ ',' ').replace(r'\-','').replace('~',' ').replace(r'\&','&')
    t=re.sub(r'\$([^$]*)\$',r'\1',t)
    t=re.sub(r'\s+',' ',t)
    return t
class Page:
    def __init__(s,name,w,h): s.name=name; s.w=int(w); s.h=int(h); s.c=[]; s.n=1
    def nid(s): s.n+=1; return f"c{s.n}"
    def v(s,x,y,w,h,val,st,i=None):
        i=i or s.nid(); s.c.append(f'<mxCell id="{i}" value="{html.escape(val)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>'); return i
    def e(s,a,b,st):
        s.c.append(f'<mxCell id="{s.nid()}" style="{st}" edge="1" parent="1" source="{a}" target="{b}"><mxGeometry relative="1" as="geometry"/></mxCell>')
    def ep(s,p1,p2,st):
        s.c.append(f'<mxCell id="{s.nid()}" style="{st}" edge="1" parent="1"><mxGeometry relative="1" as="geometry"><mxPoint x="{p1[0]:.1f}" y="{p1[1]:.1f}" as="sourcePoint"/><mxPoint x="{p2[0]:.1f}" y="{p2[1]:.1f}" as="targetPoint"/></mxGeometry></mxCell>')
    def xml(s): return (f'<diagram name="{s.name}" id="{re.sub(r"[^A-Za-z0-9]","_",s.name)}"><mxGraphModel dx="{s.w}" dy="{s.h}" grid="0" gridSize="10" page="1" pageScale="1" pageWidth="{s.w}" pageHeight="{s.h}" background="#ffffff"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'+''.join(s.c)+'</root></mxGraphModel></diagram>')
FONT="fontFamily=Times New Roman;"
def tikz_page(k,name,stylemap,fs=8):
    g=G[str(k)]; x0,y0,x1,y1=g['bbox']
    pw=(x1-x0)*S+2*M; ph=(y0-y1)*S+2*M
    P=Page(name,pw,ph)
    tx=lambda x:(x-x0)*S+M; ty=lambda y:(y0-y)*S+M
    src=g['src']
    # filled / drawn rectangles (cm coordinates)
    for m in re.finditer(r'\\(fill|draw)\[([^\]]*)\]\s*\(([-\d.]+),([-\d.]+)\)\s*rectangle\s*\(([-\d.]+),([-\d.]+)\)',src):
        kind,c,a,b,c2,d=m.groups(); ax_,ay_,cx_,dy_=[float(v)*CM for v in (a,b,c2,d)]
        X,Y=tx(min(ax_,cx_)),ty(max(ay_,dy_)); Wd,Ht=abs(cx_-ax_)*S,abs(dy_-ay_)*S
        st=(f"rounded=0;html=1;fillColor={col(c)};strokeColor=none;" if kind=='fill' else f"rounded=0;html=1;fillColor=none;strokeColor={col(c)};strokeWidth={0.4*S};")
        P.v(X,Y,Wd,Ht,'',st)
    ids={}
    for nd in g['nodes']:
        ax_,ay_,bx_,by_=nd['geo']; X,Y=tx(min(ax_,bx_)),ty(max(ay_,by_)); Wd,Ht=abs(bx_-ax_)*S,abs(ay_-by_)*S
        st=stylemap(nd['opts'])
        ids[nd['name']]=P.v(X,Y,Wd,Ht,tex2html(nd['text']),st+FONT+f"fontSize={fs*S:.0f};",f"n_{nd['name']}")
    # arrows
    arrst={k_:v_ for k_,v_ in []}
    def arrowstyle(opts):
        c='#000000'
        mm=re.search(r'(red!\d+|black!\d+)',opts or '')
        if mm: c=col(mm.group(1))
        dashed='dashed=1;' if 'dashed' in (opts or '') else ''
        return c,dashed
    i0=src.find('arr/.style={'); defs=''
    if i0>=0:
        j=i0+len('arr/.style='); d=0
        for q in range(j,len(src)):
            if src[q]=='{': d+=1
            elif src[q]=='}':
                d-=1
                if d==0: break
        defs=src[j:q+1]
    base_c,_=arrowstyle(defs)
    width=0.8*S if 'thick' in defs else 0.4*S
    stmts=[]
    for m in re.finditer(r'\\foreach \\a/\\b in \{([^}]*)\} \\draw\[arr\] \(\\a\)--\(\\b\);',src):
        for pair in m.group(1).split(','): a,b=pair.split('/'); stmts.append(('',a.strip(),'--',b.strip()))
    for m in re.finditer(r'\\draw\[(arr[^\]]*)\]\s*\(([\w.]+)\)\s*(--|\|-|-\|)\s*\(([\w.]+)\)',src):
        stmts.append((m.group(1),m.group(2),m.group(3),m.group(4)))
    anc={'north':(0.5,0),'south':(0.5,1),'east':(1,0.5),'west':(0,0.5)}
    for opts,a,op,b in stmts:
        c,dashed=arrowstyle(opts) if opts not in ('','arr') else (base_c,'')
        if opts.startswith('arr,') or opts.startswith('arr '):
            c2,dashed=arrowstyle(opts); c=c2 if 'red' in opts else base_c
        an,aa=(a.split('.')+[None])[:2]; bn,ba=(b.split('.')+[None])[:2]
        st=f"html=1;endArrow=classic;endFill=1;endSize={4.5*S:.0f};strokeColor={c};strokeWidth={width:.1f};{dashed}"
        if op=='--': st+="edgeStyle=none;"
        else: st+="edgeStyle=orthogonalEdgeStyle;rounded=0;"
        if aa: st+=f"exitX={anc[aa][0]};exitY={anc[aa][1]};exitDx=0;exitDy=0;"
        if ba: st+=f"entryX={anc[ba][0]};entryY={anc[ba][1]};entryDx=0;entryDy=0;"
        P.e(ids[an],ids[bn],st)
    return P
def toks(o): return [t.strip().split('=')[0] for t in (o or '').strip('[]').split(',')]
def has(o,k):
    if k in ('hd','hdg','st','side','b','box','dashed'): return k in toks(o)
    return k in (o or '')
# ---- style maps per figure (mirror the TikZ styles) ----
def sm_teaser(o):
    if has(o,'draw=gray'): return f"rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacing=6;strokeColor={col('gray!60')};fillColor=#FFFFFF;"
    if has(o,'text width=8.1cm'): return "text;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacing=6;"
    return "text;html=1;align=center;verticalAlign=middle;spacing=0;"
def sm_method(o):
    if has(o,'side'): return f"rounded=1;absoluteArcSize=1;arcSize={3*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacing=4;strokeColor={col('black!55')};fillColor={col('blue!6')};"
    return f"rounded=1;absoluteArcSize=1;arcSize={3*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacing=4;strokeColor={col('black!55')};fillColor=#FFFFFF;"
def sm_prisma(o):
    if has(o,'hdg'): return f"rounded=1;absoluteArcSize=1;arcSize={6*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontStyle=1;strokeColor=#000000;fillColor={col('black!10')};"
    if has(o,'hd'): return f"rounded=1;absoluteArcSize=1;arcSize={6*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontStyle=1;strokeColor=#000000;fillColor={col('yellow!35')};"
    if has(o,'st'): return f"rounded=1;absoluteArcSize=1;arcSize={6*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;fontStyle=1;horizontal=0;strokeColor=#000000;fillColor={col('cyan!25')};"
    return f"rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=middle;spacing={3*S:.0f};strokeColor=#000000;fillColor=#FFFFFF;"
def sm_case(o):
    if has(o,'dashed'): return f"rounded=1;absoluteArcSize=1;arcSize={8*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;dashed=1;strokeColor={col('red!70')};fontColor={col('red!70!black')};fillColor=#FFFFFF;"
    fill='#FFFFFF'
    if has(o,'blue!8'): fill=col('blue!8')
    if has(o,'black!3'): fill=col('black!3')
    return f"rounded=1;absoluteArcSize=1;arcSize={3*S};whiteSpace=wrap;html=1;align=center;verticalAlign=middle;spacing=4;strokeColor={col('black!60')};fillColor={fill};"
pages=[tikz_page(0,'Fig. 1 Teaser',sm_teaser),tikz_page(1,'Fig. 2 Research design',sm_method),tikz_page(2,'Fig. 3 PRISMA 2020',sm_prisma)]
# ---- Fig. 10 framework from framework_fig.py coordinates (inches) ----
src=open('scripts/framework_fig.py').read(); ns={}
exec(src[src.index('cells = {'):src.index('}\nfor (ri')+1],ns); cells=ns['cells']
I=72*S
Wf,Hf=7.16,6.85
P=Page('Fig. 10 Framework',Wf*I,Hf*I)
INK,QUIET,EDGE,ACC='#1F2328','#57606A','#8C959F','#0969DA'
FF="fontFamily=DejaVu Sans;"
def txt(x,y,t,fs,color=INK,bold=False,ha='left',va='baseline',italic=False,w=None):
    lines=t.split('\n'); fpx=fs*S; lh=fpx*1.2; h=lh*len(lines)
    width=w or min(max(len(l) for l in lines)*fpx*0.56+6, Wf*I-x*I-4)
    X=x*I-(width/2 if ha=='center' else 0)
    if va=='center': Y=y*I-h/2
    elif va=='top': Y=y*I
    else: Y=y*I-fpx*0.95
    st=f"text;html=1;whiteSpace=nowrap;align={ha};verticalAlign=top;spacing=0;fontSize={fpx:.0f};fontColor={color};{FF}fontStyle={(1 if bold else 0)+(2 if italic else 0)};"
    P.v(X,Y,width,h,'<br>'.join(html.escape(l) for l in lines),st)
x0,cw,gap=1.35,1.85,0.08; cols=[x0+i*(cw+gap) for i in range(3)]
rhs=[1.3,2.0,1.3]; rows=[0.98,0.98+1.3+0.08,0.98+1.3+2.0+0.16]
txt(0.15,0.28,"No published reward checks the reasoning text without a judge model or labels",10,bold=True,va='center')
txt(0.15,0.50,"Rows: what the reward verifies.  Columns: where the verification signal comes from.  S-numbers = included studies.",8,QUIET,va='center')
for c,(h,s_) in zip(cols,[("No extra model","rule or internal signal"),("Labelled evidence","region or rationale labels"),("External model","judge LLM, rubric or reward model")]):
    txt(c+cw/2,0.73,h,9,bold=True,ha='center',w=cw*I); txt(c+cw/2,0.88,s_,8,QUIET,ha='center',w=cw*I)
for r,rh,(h,s_) in zip(rows,rhs,[("Final answer","or confidence;\nexact match, IoU"),("Perception","attention, regions,\nvisual facts"),("Reasoning text","checked against\nthe image")]):
    txt(0.15,r+rh/2-0.12,h,9,bold=True,va='center'); txt(0.15,r+rh/2+0.12,s_,8,QUIET,va='top')
for (ri,ci),items in cells.items():
    x,y,rh=cols[ci],rows[ri],rhs[ri]
    if items is None:
        P.v(x*I,y*I,cw*I,rh*I,'',f"rounded=1;absoluteArcSize=1;arcSize={0.16*I:.0f};html=1;fillColor=#E6F0FB;strokeColor={ACC};strokeWidth={1.6*S};")
        txt(x+0.1,y+0.22,"EMPTY — gap G1",8.5,ACC,bold=True)
        txt(x+0.1,y+0.42,"judge-free, label-free check\nof the reasoning text\nagainst the image",8,INK,va='top')
        txt(x+0.1,y+0.88,"nearest: S03 CORA (trained\nRM); S61 PEARL\n(perception only)",8,QUIET,va='top')
    else:
        P.v(x*I,y*I,cw*I,rh*I,'',f"rounded=1;absoluteArcSize=1;arcSize={0.16*I:.0f};html=1;fillColor=#FFFFFF;strokeColor={EDGE};strokeWidth={0.9*S};")
        if not items: txt(x+0.1,y+0.22,"none found",8,QUIET,italic=True)
        for k_,t in enumerate(items or []): txt(x+0.1,y+0.2+k_*0.17,t,8,INK)
ya=rows[-1]+rhs[-1]+0.25
P.ep((cols[0]*I,ya*I),((cols[2]+cw)*I,ya*I),f"html=1;endArrow=block;endFill=1;endSize={5*S:.0f};strokeColor={EDGE};strokeWidth={1*S};")
txt(cols[0],ya+0.2,"Extra model, annotation and compute cost rise from left to right →",8,QUIET)
txt(cols[0],ya+0.42,"Not placed: diagnostic S16, S41, S59; test-time reward model S22; benchmark S23; surveys S24, S25.",8,QUIET)
txt(cols[0],ya+0.64,"Base paper MC-R1 (not in the 66; abstract): final answer × labelled evidence, plus a key-token check.",8,INK)
pages.append(P)
pages.append(tikz_page(3,'Fig. 12 Case study',sm_case))
# ---- write ----
for f in os.listdir(OUT):
    if f.endswith('.drawio'): os.remove(OUT+f)
head='<mxfile host="app.diagrams.net" agent="26I-7675 SLR (geometry copied from the paper figures)">'
open(OUT+'26I-7675_all_diagrams.drawio','w').write(head+''.join(p.xml() for p in pages)+'</mxfile>')
names=['fig1_teaser','fig2_research_design','fig3_prisma_2020','fig10_framework','fig12_case_study']
os.makedirs(OUT+'paste_xml',exist_ok=True)
for f in os.listdir(OUT+'paste_xml'): os.remove(OUT+'paste_xml/'+f)
for nm,p in zip(names,pages):
    open(OUT+nm+'.drawio','w').write(head+p.xml()+'</mxfile>')
    x=p.xml(); open(OUT+'paste_xml/'+nm+'.xml.txt','w').write(x[x.index('<mxGraphModel'):x.index('</diagram>')])
print('written', [ (p.name,p.w,p.h,len(p.c)) for p in pages])
