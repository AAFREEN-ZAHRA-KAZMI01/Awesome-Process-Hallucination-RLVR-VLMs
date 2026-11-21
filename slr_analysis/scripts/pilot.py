"""Pilot validation: content validity (I-CVI, S-CVI/Ave, modified kappa*) and open-answer coding.
Input: data/pilot_responses.csv (anonymised Google Form export). Outputs: tables/pilot_cvi.csv,
tables/pilot_profile.csv, figures/fig_pilot.(png|pdf)."""
import math, os, pandas as pd, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
os.makedirs("tables", exist_ok=True); os.makedirs("figures", exist_ok=True)
plt.rcParams.update({"font.size": 8, "font.family": "DejaVu Sans"})
ITEMS = ["P1", "P2", "P3", "P4", "P5", "P6", "F"]
r = pd.read_csv("data/pilot_responses.csv")
R = pd.DataFrame({i: r[[c for c in r.columns if f"[{i}." in c][0]].astype(str).str.extract(r"^(\d)")[0].astype(int) for i in ITEMS})
R.index = r["code"]
trained = (r["trained_vlm_or_llm"] == "Yes").values

def cvi(M):
    n = len(M); a = (M >= 3).sum(); i = a / n
    pc = np.array([math.comb(n, int(k)) * 0.5 ** n for k in a])
    return a, i, (i - pc) / (1 - pc)

rows = []
for name, M in [("all", R), ("trained", R[trained])]:
    a, i, k = cvi(M)
    for it in ITEMS:
        rows.append(dict(panel=name, n=len(M), item=it, rated_3_or_4=int(a[it]), I_CVI=round(i[it], 2),
                         modified_kappa=round(k[it], 2), median=M[it].median()))
t = pd.DataFrame(rows); t.to_csv("tables/pilot_cvi.csv", index=False)
print(t.pivot(index="item", columns="panel", values=["I_CVI", "modified_kappa", "median"]).to_string())
for name, M in [("all", R), ("trained", R[trained])]:
    print(f"S-CVI/Ave P1-P6 ({name}, n={len(M)}) =", round(cvi(M)[1][ITEMS[:6]].mean(), 2))
prof = pd.DataFrame({"role": r["role"].value_counts(), }).rename_axis("value")
pd.concat([r["role"].value_counts().rename("n").to_frame().assign(field="role"),
           r["ml_experience_years"].value_counts().rename("n").to_frame().assign(field="years"),
           r["trained_vlm_or_llm"].value_counts().rename("n").to_frame().assign(field="trained")]).to_csv("tables/pilot_profile.csv")

# figure: rating heatmap (participants x items) + I-CVI bars
order = np.argsort(-R.sum(axis=1).values, kind="stable")
Rs = R.iloc[order]; tr = trained[order]
fig, (ax, bx) = plt.subplots(1, 2, figsize=(3.5, 3.0), gridspec_kw=dict(width_ratios=[1.25, 1], wspace=0.45))
cmap = ListedColormap(["#d9534f", "#f0ad4e", "#9fd3a8", "#2e8b57"])
ax.imshow(Rs.values, cmap=cmap, vmin=0.5, vmax=4.5, aspect="auto")
ax.set_xticks(range(len(ITEMS))); ax.set_xticklabels(ITEMS)
ax.set_yticks(range(len(Rs))); ax.set_yticklabels([f"{c}{'*' if t_ else ''}" for c, t_ in zip(Rs.index, tr)])
for y in range(len(Rs)):
    for x in range(len(ITEMS)):
        ax.text(x, y, Rs.values[y, x], ha="center", va="center", fontsize=8, color="black")
ax.set_title("Relevance ratings (1-4)", fontsize=8)
ax.tick_params(length=0)
ia = cvi(R)[1]; it_ = cvi(R[trained])[1]; x = np.arange(len(ITEMS))
bx.bar(x - 0.2, ia.values, 0.38, color="#7f8c8d", label=f"all (n={len(R)})")
bx.bar(x + 0.2, it_.values, 0.38, color="#2c6fbb", label=f"trained* (n={trained.sum()})")
bx.axhline(0.78, color="black", lw=0.8, ls="--"); bx.text(-0.45, 0.80, "0.78 cut-off", fontsize=8)
bx.set_xticks(x); bx.set_xticklabels(["1","2","3","4","5","6","F"]); bx.set_xlabel("Item (P1-P6, F)", labelpad=1); bx.set_ylim(0, 1.12); bx.set_ylabel("I-CVI", labelpad=1)
bx.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), frameon=False, fontsize=8, ncol=1)
bx.set_title("Item-level CVI", fontsize=8)
for s_ in ["top", "right"]: bx.spines[s_].set_visible(False)
fig.savefig("figures/fig_pilot.png", dpi=400, bbox_inches="tight"); fig.savefig("figures/fig_pilot.pdf", bbox_inches="tight")
print("saved figures/fig_pilot")
