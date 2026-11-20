"""Self-drawn figures (matplotlib), counts from counts.json. Outputs PNG (400 DPI), vector PDF and SVG in figures/.
Edit counts.json after snowballing (cs_* fields) and rerun: python figures.py. The script checks the PRISMA arithmetic.
Figures: fig_prisma (PRISMA 2020, databases + citation searching), fig_method_flow (research design), fig_framework_template (placeholders for YOUR framework)."""
import json, os
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
C=json.load(open('counts.json')); os.makedirs('figures',exist_ok=True)
NAVY='#1F3864'; LIGHT='#EAF0FA'; RED='#FBEBEB'; GRN='#E5F4E4'; GREY='#F2F2F2'
# arithmetic checks (every box must match the screening log)
assert C['identified_db']-C['duplicates']==C['screened']+C['not_screened'], 'identified - duplicates != screened + not screened'
assert C['screened']-C['excluded_ta']-C['uncertain']==C['sought'], 'screening arithmetic'
assert C['sought']-C['not_retrieved']==C['assessed'] and C['assessed']-C['excluded_ft']==C['included_db'], 'full-text arithmetic'
cs_new=C['cs_identified']-C['cs_dupe_in_log']
assert C['cs_screened']<=cs_new or cs_new==0
total_incl=C['included_db']+C['cs_included']
def save(fig,name):
    for ext in ('png','pdf','svg'): fig.savefig(f'figures/{name}.{ext}',dpi=400,bbox_inches='tight',facecolor='white')
    plt.close(fig)
def mk(w,h):
    fig,ax=plt.subplots(figsize=(w,h)); ax.set_xlim(0,100); ax.set_ylim(-14,100); ax.axis('off'); return fig,ax
def box(ax,x,y,w,h,t,fc=LIGHT,bold=False,fs=7):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.2,rounding_size=1',fc=fc,ec=NAVY,lw=0.9))
    ax.text(x+w/2,y+h/2,t,ha='center',va='center',fontsize=fs,fontweight='bold' if bold else 'normal',linespacing=1.25)
def arr(ax,x1,y1,x2,y2): ax.annotate('',xy=(x2,y2),xytext=(x1,y1),arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=1))
# ---- PRISMA 2020
fig,ax=mk(7.2,8.4)
ax.text(1,98,'Identification',fontsize=8,fontweight='bold',color=NAVY); ax.text(1,68,'Screening',fontsize=8,fontweight='bold',color=NAVY); ax.text(1,35,'Eligibility',fontsize=8,fontweight='bold',color=NAVY); ax.text(1,9,'Included',fontsize=8,fontweight='bold',color=NAVY)
L,W=12,36; M,MW=52,22; R,RW=77,22   # left=databases, middle=side boxes, right=citation searching
box(ax,L,86,W,11,f"Records identified from databases\nn = {C['identified_db']:,}\n"+C['by_source'].replace(' | ',' · ').replace(' · SpringerLink',chr(10)+'SpringerLink').replace(' · OpenAlex',chr(10)+'OpenAlex'),fc='#D9E2F3',fs=5.6)
box(ax,L,70,W,9,f"Records after duplicates removed\nn = {C['identified_db']-C['duplicates']:,}")
arr(ax,L+W/2,86,L+W/2,79.2)
box(ax,M,70,MW,9,f"Duplicates removed\nn = {C['duplicates']}\nNot screened: n = {C['not_screened']}",fc=GREY,fs=6)
arr(ax,L+W,74.5,M,74.5)
box(ax,L,54,W,9,f"Records screened (title/abstract)\nn = {C['screened']}"); arr(ax,L+W/2,70,L+W/2,63.2)
box(ax,M,54,MW,9,f"Excluded at title/abstract\nn = {C['excluded_ta']}\nUncertain: n = {C['uncertain']}",fc=RED,fs=6); arr(ax,L+W,58.5,M,58.5)
box(ax,L,38,W,9,f"Full texts sought\nn = {C['sought']}"); arr(ax,L+W/2,54,L+W/2,47.2)
box(ax,M,38,MW,9,f"Full text not retrieved\nn = {C['not_retrieved']}",fc='#FFF4D6',fs=6); arr(ax,L+W,42.5,M,42.5)
box(ax,L,22,W,9,f"Full texts assessed for eligibility\nn = {C['assessed']}"); arr(ax,L+W/2,38,L+W/2,31.2)
box(ax,M,22,MW,9,f"Excluded, n = {C['excluded_ft']}\n{C['ft_reasons']}",fc=RED,fs=6); arr(ax,L+W,26.5,M,26.5)
box(ax,L,6,W,9,f"Studies included (databases)\nn = {C['included_db']}",fc=GRN); arr(ax,L+W/2,22,L+W/2,15.2)
# citation searching column
box(ax,R,86,RW,11,f"Identified by citation\nsearching\nn = {C['cs_identified']}",fc='#D9E2F3',fs=5.6)
box(ax,R,70,RW,9,f"New after checking the log\nn = {cs_new}\n(in log: {C['cs_dupe_in_log']})",fs=6); arr(ax,R+RW/2,86,R+RW/2,79.2)
box(ax,R,54,RW,9,f"Screened\nn = {C['cs_screened']}\nExcluded: {C['cs_excluded_ta']}",fs=6); arr(ax,R+RW/2,70,R+RW/2,63.2)
box(ax,R,38,RW,9,f"Sought n = {C['cs_sought']}\nNot retrieved: {C['cs_not_retrieved']}",fs=6); arr(ax,R+RW/2,54,R+RW/2,47.2)
box(ax,R,22,RW,9,f"Assessed n = {C['cs_assessed']}\nExcluded: {C['cs_excluded_ft']}",fs=6); arr(ax,R+RW/2,38,R+RW/2,31.2)
box(ax,R,6,RW,9,f"Included (citation searching)\nn = {C['cs_included']}",fc=GRN,fs=6); arr(ax,R+RW/2,22,R+RW/2,15.2)
box(ax,L+W/2+8,-12,40,8,f"Total studies included in the review\nn = {total_incl}",fc=GRN,bold=True,fs=7)
save(fig,'fig_prisma')
# ---- research design flow
fig,ax=mk(3.5,6.6)
steps=['Problem and base paper\n(MC-R1, IEEE TMM 2026)','Protocol: PICOC, RQs, IC/EC,\nQA checklist, extraction form','Search: 5 sources,\nexact strings, search log','Screening: title/abstract\nthen full text (2 screeners, kappa)','Citation searching\n(backward + forward)','Extraction and quality\nassessment (Q1-Q8)','Analysis: bibliometrics,\ntopic model, sensitivity','Synthesis: framework,\npropositions, gaps','Pilot validation\n(expert ratings)']
n=len(steps); h=8.2; gap=2.3
for i,s in enumerate(steps):
    y=100-(i+1)*(h+gap)+gap; box(ax,8,y,84,h,s,fs=6.2)
    if i<n-1: arr(ax,50,y,50,y-gap+0.2)
save(fig,'fig_method_flow')
# ---- framework TEMPLATE (placeholders: fill with YOUR synthesis)
fig,ax=mk(3.5,2.6)
box(ax,2,60,28,28,'[Input / problem]\nreplace with your\nconcept',fs=6); box(ax,36,60,28,28,'[Mechanism]\nreplace',fs=6); box(ax,70,60,28,28,'[Outcome]\nreplace',fs=6)
arr(ax,30,74,36,74); arr(ax,64,74,70,74)
box(ax,2,10,28,28,'[Moderator]\nreplace',fs=6,fc=GREY); box(ax,36,10,28,28,'[Evidence]\nstudies S__',fs=6,fc=GREY); box(ax,70,10,28,28,'[Proposition P1..Pk]\nreplace',fs=6,fc=GREY)
arr(ax,16,38,40,60); arr(ax,50,38,50,60); arr(ax,84,38,84,60)
save(fig,'fig_framework_template')
print('ok; total included =',total_incl)
