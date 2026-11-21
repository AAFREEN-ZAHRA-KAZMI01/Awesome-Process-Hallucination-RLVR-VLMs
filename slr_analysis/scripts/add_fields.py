"""Add the brief's extra extraction fields (approach/RL algorithm, context, design,
sample/data size, measures) and refresh the snowballing sheet with all 124 rows."""
import re, json, copy, csv, sys
import openpyxl, pandas as pd
from openpyxl.utils import get_column_letter
X = sys.argv[1]
cards = json.load(open('data/cards.json'))
inc = pd.read_csv('data/included_studies.csv').set_index('id')

def rl_alg(t):
    algs = ['GRPO','DAPO','GSPO','PPO','DPO','RLOO','REINFORCE','KTO','ORPO','RLHF','RLAIF','SFT']
    found = [a for a in algs if re.search(r'\b[A-Z\-]*'+a+r'\b', t)]
    # keep base names
    out=[]
    for a in found:
        if a=='PPO' and 'GRPO' in found and not re.search(r'\bPPO\b',t): continue
        if a=='DPO' and not re.search(r'\bDPO\b',t): continue
        out.append(a)
    return ', '.join(dict.fromkeys(out)) or 'Not stated'

DOM = [('Mathematics', r'math|geometry|MathVista|MathVerse|MathVision|WeMath|GeoQA'),
       ('General VQA / multimodal reasoning', r'MMMU|MMStar|MMBench|VQA|general'),
       ('Hallucination / grounding', r'POPE|Hallusion|AMBER|CHAIR|hallucinat|grounding|RefCOCO'),
       ('Charts / documents', r'chart|ChartQA|document|DocVQA|table'),
       ('Captioning', r'caption'),
       ('Video', r'video'),
       ('Medical', r'medical|clinical|radiolog'),
       ('Spatial / embodied', r'spatial|embodied|robot|navigation')]
def context(t):
    d=[n for n,p in DOM if re.search(p,t,re.I)]
    return '; '.join(d[:3]) or 'Not stated'

def design(i, c):
    k = inc.loc[i,'kind'] if i in inc.index else ''
    m = c.get('Method / approach','')
    if k=='Survey' or 'survey' in c.get('Publication details','').lower()[:30]: return 'Literature survey (secondary)'
    if k=='Benchmark' or re.search(r'\bbenchmark\b.*(introduc|construct|propos)', m, re.I) and not re.search('reward',m,re.I):
        return 'Benchmark construction + evaluation'
    if k=='Diagnostic' or re.search(r'diagnos|analysis of|we analy[sz]e|study of', m, re.I) and not re.search('propos',m,re.I):
        return 'Empirical diagnostic study'
    return 'Experimental (new method vs. baselines on benchmarks)'

def size(c):
    t = c.get('Dataset / data source','')
    n = re.findall(r'\b\d+(?:\.\d+)?\s?[KkM]\b(?:\+)?(?:\s(?:samples|examples|images|pairs|questions|items|instances|prompts))?|\b\d{1,3}(?:,\d{3})+\s(?:samples|examples|images|pairs|questions|items)', t)
    b = re.findall(r'(?:Qwen[\w\.\-]*|InternVL[\w\.\-]*|LLaVA[\w\.\-]*|MiMo[\w\.\-]*|Gemma[\w\.\-]*|LLaMA[\w\.\-]*)[-\s]?\d+(?:\.\d+)?B', t)
    parts=[]
    if n: parts.append('data: '+', '.join(dict.fromkeys(n)))
    if b: parts.append('backbones: '+', '.join(dict.fromkeys(b)))
    return '; '.join(parts) or 'Size not reported in extracted text'

MEAS = [('Accuracy',r'accura|MathVista|MMMU|MathVerse|MMStar'),('Hallucination rate / POPE F1',r'POPE|AMBER|hallucination rate|CHAIR'),
        ('CHAIR',r'CHAIR'),('Faithfulness / consistency',r'faithful|consisten'),('Calibration (ECE)',r'ECE|calibrat'),
        ('Grounding IoU / mAP',r'IoU|mAP|grounding'),('Judge / human rating',r'judge|human eval|GPT-4|rating'),
        ('Cost (GPU hours / tokens / time)',r'GPU|cost|latency|tokens|time')]
def measures(c):
    t=c.get('Evaluation','')+' '+c.get('Key findings','')
    m=[n for n,p in MEAS if re.search(p,t,re.I)]
    return '; '.join(m) or 'See Evaluation column'

wb = openpyxl.load_workbook(X)
ws = wb['Extraction (66 studies)']
hdr=[c.value for c in ws[1]]
new=['Theory / approach (RL algorithm)','Context / application domain','Research design','Sample / data size','Measures (outcome metrics)']
if new[0] not in hdr:
    start=len(hdr)+1
    for j,h in enumerate(new):
        cell=ws.cell(1,start+j,h); src=ws.cell(1,len(hdr))
        cell._style=copy.copy(src._style); ws.column_dimensions[get_column_letter(start+j)].width=32
    for r in range(2,ws.max_row+1):
        i=ws.cell(r,1).value; c=cards.get(i,{})
        t=' '.join(str(c.get(k,'')) for k in ['Method / approach','Dataset / data source','Evaluation','Research problem'])
        vals=[rl_alg(c.get('Method / approach','')+' '+c.get('Evaluation','')), context(t), design(i,c), size(c), measures(c)]
        for j,v in enumerate(vals):
            cell=ws.cell(r,start+j,v); cell._style=copy.copy(ws.cell(r,len(hdr))._style)
# snowballing sheet
del wb['Snowballing log']
sn=wb.create_sheet('Snowballing log (124)')
rows=list(csv.reader(open('data/snowballing_log.csv')))
for row in rows: sn.append(row)
for c in sn[1]: c.font=openpyxl.styles.Font(bold=True)
for j in range(1,len(rows[0])+1): sn.column_dimensions[get_column_letter(j)].width=22 if j>1 else 70
sn.freeze_panes='A2'
wb.save(X)
df=pd.read_excel(X,sheet_name=None)
for k,v in df.items(): print(k,v.shape)
print(df['Extraction (66 studies)'][new].head(8).to_string())
print(df['Extraction (66 studies)'][new[2]].value_counts())
