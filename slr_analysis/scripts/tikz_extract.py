"""Compile each TikZ figure of the paper standalone and log the exact geometry of every node
(north-west / south-east corners, in pt), so draw.io copies can use identical positions."""
import re, subprocess, json, sys
W='/home/claude/drawio_exact/'
s=open('/home/claude/paper/main.tex').read()
aux=open('/home/claude/paper/main.aux').read()
envs=re.findall(r'\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}',s,re.S)
pre=r'''\documentclass[border=0pt]{standalone}
\usepackage{amsmath,amssymb}\usepackage{xcolor}\usepackage{tikz}\usepackage{mathptmx}
\usetikzlibrary{positioning,arrows.meta,shapes.geometric,fit,calc}
\begin{document}
'''
def bal(t,i):
    d=0
    for j in range(i,len(t)):
        if t[j]=='{': d+=1
        elif t[j]=='}':
            d-=1
            if d==0: return j
res={}
for k,e in enumerate(envs):
    e=re.sub(r'\\ref\{([^}]+)\}',lambda m:re.search(r'\\newlabel\{'+re.escape(m.group(1))+r'\}\{\{([^}]*)\}',aux).group(1),e)
    e=re.sub(r'~?\\cite\{[^}]+\}','',e)
    # name every node and collect its options/text
    out=''; i=0; n=0; nodes=[]
    for m in re.finditer(r'\\node',e):
        pass
    pos=0; buf=''
    while True:
        m=re.compile(r'\\node(?![a-zA-Z])').search(e,pos)
        if not m: buf+=e[pos:]; break
        buf+=e[pos:m.end()]; j=m.end()
        opts=''
        if e[j]=='[':
            d=0
            for q in range(j,len(e)):
                if e[q]=='[': d+=1
                elif e[q]==']':
                    d-=1
                    if d==0: break
            opts=e[j:q+1]; j=q+1
        rest=e[j:]
        mm=re.match(r'\s*\((\w+)\)',rest)
        if mm: name=mm.group(1); head=opts+rest[:mm.end()]; j2=j+mm.end()
        else:
            n+=1; name=f'auto{n}'; head=opts+f' ({name})'; j2=j
        # text: find first { after optional 'at (...)'
        bi=e.index('{',j2); be=bal(e,bi); text=e[bi+1:be]
        buf+=head+e[j2:be+1]; pos=be+1
        nodes.append({'name':name,'opts':opts,'text':text})
    names=[x['name'] for x in nodes]
    dump=''.join(r'\path ('+nm+r'.north west); \pgfgetlastxy{\ax}{\ay}\path ('+nm+r'.south east); \pgfgetlastxy{\bx}{\by}\typeout{NODE '+nm+r' \ax\space\ay\space\bx\space\by}'
                 for nm in names)
    dump+=r'\path (current bounding box.north west); \pgfgetlastxy{\ax}{\ay}\path (current bounding box.south east); \pgfgetlastxy{\bx}{\by}\typeout{BBOX \ax\space\ay\space\bx\space\by}'
    body=buf.replace(r'\end{tikzpicture}',dump+'\n'+r'\end{tikzpicture}')
    open(W+f'x{k}.tex','w').write(pre+body+'\n\\end{document}\n')
    r=subprocess.run(['pdflatex','-interaction=nonstopmode','-output-directory',W,W+f'x{k}.tex'],capture_output=True,text=True)
    log=open(W+f'x{k}.log').read()
    geo={}
    for mm in re.finditer(r'NODE (\w+) ([-\d.]+)pt ([-\d.]+)pt ([-\d.]+)pt ([-\d.]+)pt',log):
        geo[mm.group(1)]=[float(mm.group(i)) for i in range(2,6)]
    bb=[float(v) for v in re.search(r'BBOX ([-\d.]+)pt ([-\d.]+)pt ([-\d.]+)pt ([-\d.]+)pt',log).groups()]
    for x in nodes: x['geo']=geo.get(x['name'])
    res[k]={'nodes':nodes,'bbox':bb,'src':body,'ok':r.returncode==0}
    print(k,r.returncode,len(nodes),sum(1 for x in nodes if x['geo']),bb)
json.dump(res,open(W+'geometry.json','w'),indent=1)
