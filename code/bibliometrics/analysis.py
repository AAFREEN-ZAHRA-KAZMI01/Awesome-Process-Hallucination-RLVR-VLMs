"""Bibliometric + sensitivity analysis of the 66-study SLR corpus.
Input: corpus_workbook.xlsx (Extraction + Screening sheets). Seed fixed. Run: python analysis.py
Steps: 1 load -> 2 descriptive bibliometrics -> 3 keyword co-occurrence -> 4 LDA topics -> 5 sensitivity -> 6 figures (400 DPI)
"""
import re, json, itertools, collections
import numpy as np, pandas as pd, openpyxl, networkx as nx
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
SEED=42; np.random.seed(SEED); DPI=400
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.spines.top':False,'axes.spines.right':False})
NAVY,GREY,TEAL='#1F3864','#8C8C8C','#2A9D8F'

# 1 ---- load
wb=openpyxl.load_workbook('corpus_workbook.xlsx',data_only=True)
ex=wb['Extraction']; sc=wb['Screening']
cols=['id','authors','year','kind','pubtype','peer','problem','rq','method','dataset','evaluation','findings','limits','repro','Q1','Q2','Q3','Q4','Q5','Q6','Q7','Q8','Q9','pts','maxpts','pct','rating','qnote','decision']
rows=[[ex.cell(r,c).value for c in range(1,30)] for r in range(4,ex.max_row+1) if ex.cell(r,1).value]
df=pd.DataFrame(rows,columns=cols)
df['year']=df.year.astype(int); df['pct']=df.pct.astype(float)
src={sc.cell(r,14).value:str(sc.cell(r,2).value) for r in range(4,331) if sc.cell(r,14).value}
df['source']=df.id.map(src).fillna('unknown').str.split(' ').str[0]
df['preprint']=df.pubtype.str.contains('preprint',case=False,na=False)
df['peer_verified']=df.peer.astype(str).str.startswith('Yes')
df['own_code']=pd.to_numeric(df.Q8,errors='coerce')==1  # Q8 = 1 means own code link found
df['text']=(df.problem.fillna('')+' '+df.method.fillna('')+' '+df.findings.fillna('')).str.lower()
N=len(df); out={'N':N}

# 2 ---- descriptive bibliometrics
out['by_year']=df.year.value_counts().sort_index().to_dict()
out['by_source']=df.source.value_counts().to_dict()
out['preprint_share']=round(df.preprint.mean(),3); out['peer_verified_share']=round(df.peer_verified.mean(),3)
out['quality_mean_pct']=round(df.pct.mean()*100,1); out['rating']=df.rating.value_counts().to_dict()
df.to_csv('results/corpus_table.csv',index=False)

# 3 ---- keyword co-occurrence (controlled vocabulary, documented)
VOCAB={'GRPO':r'\bgrpo\b','DAPO':r'\bdapo\b','PPO':r'\bppo\b','process reward':r'process reward|step[- ]level|process[- ]aware|process supervision','perception reward':r'perception','visual grounding':r'ground','reward model':r'reward model|prm\b','LLM/VLM judge':r'judge|gpt-|gemini|teacher','rationale/CoT':r'chain-of-thought|cot\b|rationale|reasoning trace','caption':r'caption','region/bbox':r'region|bounding|box|spatial','calibration/confidence':r'calibrat|confidence|uncertain|entropy','faithfulness':r'faithful','hallucination':r'hallucinat','consistency':r'consistenc','benchmark':r'benchmark|mathvista|mathverse|pope|hallusion','rule-based reward':r'rule-based|verifiable|string[- ]match|iou'}
M=pd.DataFrame({k:df.text.str.contains(v,regex=True) for k,v in VOCAB.items()}).astype(int)
freq=M.sum().sort_values(ascending=False); out['keyword_freq']=freq.to_dict()
A=(M.T.values@M.values).copy(); np.fill_diagonal(A,0); co=pd.DataFrame(A,index=M.columns,columns=M.columns); co.to_csv('results/keyword_cooccurrence.csv')
G=nx.Graph()
for k in VOCAB: G.add_node(k,w=int(freq[k]))
for a,b in itertools.combinations(VOCAB,2):
    if co.loc[a,b]>=5: G.add_edge(a,b,w=int(co.loc[a,b]))

# 4 ---- LDA topics (k=4)
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS as ESW
GEN=list(ESW)+['visual','reasoning','reward','rewards','grpo','vlms','vlm','authors','improves','model','models','training','rlvr','multimodal','image','data','based','using','use','method','propose','proposes']
cv=CountVectorizer(stop_words=GEN,min_df=3,max_df=0.8,ngram_range=(1,2),token_pattern=r'[a-z][a-z\-]{2,}')
X=cv.fit_transform(df.text); K=4
lda=LatentDirichletAllocation(n_components=K,random_state=SEED,learning_method='batch',max_iter=200).fit(X)
terms=np.array(cv.get_feature_names_out()); topics={}
for i,comp in enumerate(lda.components_): topics[f'T{i+1}']=list(terms[comp.argsort()[::-1][:8]])
df['topic']=['T%d'%(i+1) for i in lda.transform(X).argmax(1)]
out['lda_topics']=topics; out['topic_sizes']=df.topic.value_counts().sort_index().to_dict()

# 5 ---- sensitivity: re-compute headline results under protocol changes
FAM={'judge/model-based':r'judge|reward model|prm\b|trained|teacher|gpt-|gemini','region/rationale annotation':r'region|bounding|annotat|rationale|caption','rule-based/objective':r'rule-based|verifiable|string|iou|exact|object','calibration/test-time':r'calibrat|confidence|entropy|test-time|uncertain'}
def fam(t):
    sc_={k:len(re.findall(v,t)) for k,v in FAM.items()}; return max(sc_,key=sc_.get)
df['family']=df.text.map(fam)
def summarise(d):
    return {'n':len(d),'mean_quality_pct':round(d.pct.mean()*100,1),'code_share':round(d.own_code.mean()*100,1),
            'median_year':float(d.year.median()),'top_family':d.family.value_counts().idxmax(),
            'family_shares':(d.family.value_counts(normalize=True).round(3)*100).to_dict()}
scen={'S0 baseline (all 66)':df,
      'S1 drop arXiv-sourced studies':df[df.source!='arXiv'],
      'S2 drop OpenAlex-sourced studies':df[df.source!='OpenAlex'],
      'S3 peer-reviewed verified only':df[df.peer_verified],
      'S4 QA threshold >= 75%':df[df.pct>=0.75],
      'S5 QA threshold >= 88%':df[df.pct>=0.875],
      'S6 exclude provisional S45-S66':df[~df.id.isin([f'S{i}' for i in range(45,67)])]}
sens={k:summarise(v) for k,v in scen.items() if len(v)>0}
base=set(df[df.family==sens['S0 baseline (all 66)']['top_family']].id)
out['sensitivity']=sens
pd.DataFrame([{ 'scenario':k,**{a:b for a,b in v.items() if a!='family_shares'},**{f'share_{f}':v['family_shares'].get(f,0) for f in FAM}} for k,v in sens.items()]).to_csv('results/sensitivity_table.csv',index=False)
# keyword-rank stability (Spearman) per scenario
base_rank=freq.rank(ascending=False)
stab={}
for k,v in scen.items():
    Mk=M.loc[v.index].sum(); stab[k]=round(float(pd.Series(Mk).rank(ascending=False).corr(base_rank,method='spearman')),3)
out['keyword_rank_stability_spearman']=stab
json.dump(out,open('results/results.json','w'),indent=1,default=str)

# 6 ---- figures (self-drawn from the analysis above; 400 DPI)
fig,ax=plt.subplots(1,2,figsize=(3.5*2,2.4))
y=df.year.value_counts().sort_index(); ax[0].bar(y.index.astype(str),y.values,color=NAVY); ax[0].set_xlabel('Publication year'); ax[0].set_ylabel('Included studies')
for i,v in enumerate(y.values): ax[0].text(i,v+.5,str(v),ha='center')
s=df.source.value_counts(); ax[1].barh(s.index[::-1],s.values[::-1],color=TEAL); ax[1].set_xlabel('Included studies by source'); plt.tight_layout(); plt.savefig('figures/fig1_trend_source.png',dpi=DPI); plt.close()
fig,ax=plt.subplots(figsize=(3.5,3.3)); pos=nx.circular_layout(G)
nx.draw_networkx_edges(G,pos,width=[G[a][b]['w']/12 for a,b in G.edges],edge_color=GREY,alpha=.6,ax=ax)
nx.draw_networkx_nodes(G,pos,node_size=[G.nodes[n]['w']*14 for n in G],node_color=NAVY,alpha=.9,ax=ax)
nx.draw_networkx_labels(G,pos,font_size=5.5,font_color='black',verticalalignment='bottom',horizontalalignment='center',ax=ax); ax.set_xlim(-1.5,1.5); ax.set_ylim(-1.35,1.35); ax.axis('off'); plt.tight_layout(); plt.savefig('figures/fig2_keyword_network.png',dpi=DPI); plt.close()
fig,ax=plt.subplots(figsize=(3.5,2.4)); f=freq.sort_values(); ax.barh(f.index,f.values,color=NAVY); ax.set_xlabel('Studies mentioning the term (of %d)'%N); plt.tight_layout(); plt.savefig('figures/fig3_keyword_freq.png',dpi=DPI); plt.close()
fig,ax=plt.subplots(figsize=(3.5,2.4)); ts=df.topic.value_counts().sort_index(); ax.bar(ts.index,ts.values,color=TEAL); ax.set_ylabel('Studies'); ax.set_xlabel('LDA topic (k=4, seed 42)')
for i,v in enumerate(ts.values): ax.text(i,v+.4,str(v),ha='center')
plt.tight_layout(); plt.savefig('figures/fig4_lda_topics.png',dpi=DPI); plt.close()
fig,ax=plt.subplots(figsize=(3.5*2,2.6)); T=pd.DataFrame({k:pd.Series(v['family_shares']) for k,v in sens.items()}).fillna(0).T[list(FAM)]
T.index=[i.split(' ')[0] for i in T.index]; T.plot(kind='bar',stacked=True,ax=ax,color=[NAVY,TEAL,GREY,'#E9C46A'],width=.7); ax.set_ylabel('Share of studies (%)'); ax.set_xlabel('Protocol scenario'); ax.legend(fontsize=6,frameon=False,loc='upper left',bbox_to_anchor=(1,1)); plt.xticks(rotation=0); plt.tight_layout(); plt.savefig('figures/fig5_sensitivity.png',dpi=DPI); plt.close()
print(json.dumps({k:out[k] for k in ['N','by_year','by_source','preprint_share','peer_verified_share','quality_mean_pct','rating','topic_sizes']},indent=1,default=str)); print(pd.read_csv('results/sensitivity_table.csv').to_string()); print(stab)
