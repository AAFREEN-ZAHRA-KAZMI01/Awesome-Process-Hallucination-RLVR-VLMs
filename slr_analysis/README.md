# Assignment 3 (Track A, SLR) — analysis files

**Author:** Aafreen Zahra Kazmi, Roll No. 26I-7675 (single-member group, permitted by the instructor)
**Course:** Research Methodology (MG 3010), FAST-NUCES
**Repository:** https://github.com/AAFREEN-ZAHRA-KAZMI01/Awesome-Process-Hallucination-RLVR-VLMs
**Base paper:** X. Chen, B. Zhang, X. Shi, J. Yu, "MC-R1: Mitigating Hallucinations via Reinforcement Learning With String-Match-Based Verifiable Rewards Under Modality Conflicts," *IEEE Transactions on Multimedia*, vol. 28, pp. 13829–13842, 2026, DOI 10.1109/TMM.2026.3726309 (Q1, SCImago).
**Paper:** Beyond the Final Answer: A Systematic Literature Review of Reward Design Against Process Hallucination in RL-Trained Vision-Language Models

## Run
1. Open `26I-7675_MAI-1B.ipynb` in Google Colab (upload this whole folder) or in Jupyter from this folder.
2. Run all cells. Dependencies are in `requirements.txt` (Python 3.10+). Random seed = 42.
3. Figures are written to `figures/` (400 DPI PNG + vector PDF) and tables to `tables/`.

## Contents
| Path | What it is |
|---|---|
| `26I-7675_MAI-1B.ipynb` | Analysis: descriptive synthesis, bibliometrics (trend, venues, keyword network, LDA topics), evaluation practice, reported gains, sensitivity analysis, framework figure, kappa, pilot CVI |
| `data/` | Anonymised data, `extraction_form.xlsx` (supplementary extraction spreadsheet), `snowballing_log.csv`, `codebook.md` |
| `figures/`, `tables/` | Outputs used in the paper |
| `diagrams/` | Editable draw.io sources of all five diagrams (Figs. 1, 2, 3, 10, 12): one multi-page file, one file per figure, and paste-ready XML; see `diagrams/README_diagrams.txt` |
| `instruments/create_pilot_form.gs` | Google Apps Script that creates the pilot questionnaire (Google Form) with consent text |
| `instruments/pilot_questionnaire.pdf` | Printable questionnaire and consent form |
| `instruments/Consent_form.docx` | Stand-alone informed-consent form (for interviews or offline responses) |
| `scripts/` | `add_fields.py` (codes the five extra extraction fields), `mcr1_backward.py` (base-paper backward snowballing log), `pilot.py` (pilot CVI and figure) |
| `evidence/` | Add: SCImago screenshot of the base paper's journal (IEEE Transactions on Multimedia, Q1) |

## Screening agreement
Results in `tables/kappa_results.csv` and `tables/fig_kappa_confusion.png`: 65 records, 87.7% agreement, kappa = 0.76 (3 classes), 0.78 binary (95% CI 0.60–0.91); blind subset (49) kappa = 0.51.

## Pilot
`data/pilot_responses.csv`: 19 anonymised responses (E01–E19, 20–21 Nov 2026). Results in `tables/pilot_cvi.csv` and `figures/fig_pilot`: S-CVI/Ave (P1–P6) = 0.52 for all 19, 0.60 for the 12 who had trained a VLM/LLM; P6 and F (0.83) meet the 0.78 cut-off in that subgroup. Open answers coded in `data/pilot_open_coding.csv`.

## Still to add by the author
* `evidence/`: SCImago screenshot of IEEE Transactions on Multimedia; plagiarism/AI report.

## Data and ethics
The corpus consists of published papers. Pilot responses are anonymous (codes E01..), collected after an informed-consent item in the form; no names or e-mails are stored. AI assistance (drafting, LaTeX and code) is declared in the paper's Acknowledgment.
