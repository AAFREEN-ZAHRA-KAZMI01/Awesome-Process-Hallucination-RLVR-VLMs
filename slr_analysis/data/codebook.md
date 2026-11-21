# Codebook

## extraction_form.xlsx (supplementary extraction spreadsheet)
Sheet 1: the 27-field extraction form for all 66 included studies (bibliographic, content, quality QA1–QA8, framework coding, decision). The last five columns (theory/approach = RL algorithm, context/domain, research design, sample/data size, measures) were coded from the extracted text with keyword rules in `scripts/add_fields.py` and spot-checked.
A final column gives the venue or journal and its verification status.
Sheet 2: base paper MC-R1 (record R114; abstract-level extraction, not counted in the 66).
Sheet 3: screening log of the 327 screened records. Sheet 4: backward and forward snowballing log (185 rows).

## snowballing_log.csv (185 rows)
Backward citation searching on the base paper MC-R1 (61 OpenAlex references, direction = "backward (base paper)") and on five seeds (S18 PAPO, S01 PaLMR, S03 CORA, S17 Perception-R1, S61 PEARL; 59 rows) and forward searching through OpenAlex citations of Perception-R1, PEARL and PaLMR (65 rows), 20 Nov 2026. Column `direction` = backward / backward (base paper) / forward; title, first author, year, seeds citing it, decision (Already included / Excluded at title / Potentially eligible) and reason.

## included_studies.csv (66 rows, one per included study)
| Variable | Meaning |
|---|---|
| id | Study ID S01–S66 (= reference key in references.bib) |
| short | Short name of the study |
| year | Publication year |
| kind | Primary / Survey / Benchmark |
| contribution | Reward or contribution in one line |
| quality, qpct | Quality rating (High ≥ 75%, Medium 50–74%) and percentage of available points (QA1–QA8) |
| arxiv, arxiv_month | arXiv identifier and submission month (YYYY-MM) |
| venue_status | Venue confirmed / Venue via DBLP/OpenAlex / Author-stated venue / Preprint only |
| venue_note | Venue note as recorded in the reference list |
| row | Framework verification target: Answer/confidence, Perception, Reasoning text (or Diagnostic study, Test-time PRM, Benchmark, Survey) |
| col | Framework verification source: No extra model, Labelled evidence, External model (– if not placed) |
| q7_limitations | QA7 score: 1 = limitations section, 0.5 = scattered, 0 = none |
| q8_code | QA8 score: 1 = own code link, 0.5 = project page only, 0 = none |
| method, data, evaluation, findings, limitations | Extraction fields (text) |
| reference | Full IEEE-style reference |
| source | Source through which the study was found (arXiv, OpenAlex, IEEE Xplore, Known item) |

## cards.json
Full extraction card per study (13 fields incl. per-item quality scores and notes).

## screening_log_full.csv (327 rows)
Every screened record: ID, source, title, record ID/link, year, peer-review check, title/abstract decision (Include / Exclude / Uncertain) and IC/EC reason, full-text decision and reason, evidence, study ID, notes.

## second_rater.csv (65 rows)
Second rater's decisions on the agreement sample: `decision` (Include / Uncertain / Exclude), `reason_code` (IC/EC reason), `blind` (False for the 16 records the rater already knew as included studies). The second rater was a language model (Claude, Anthropic) given the IC/EC sheet, titles and, where retrievable, abstracts.

## kappa_sample_blinded.csv (65 rows)
Seed-42 random sample of the screened records for the agreement check; author decisions removed. Second rater adds `decision` and saves as `second_rater.csv`.

No personal data of human participants is stored here. Pilot responses (when added) are anonymous: no names or e-mails are collected.

## pilot_responses.csv (19 rows)
Anonymised Google Form export, 20–21 Nov 2026. `code` E01–E19 (order of submission; timestamps removed); `consent`; `role`; `ml_experience_years`; `trained_vlm_or_llm` (Yes/No/Maybe); `rl_familiarity_1to5`; seven relevance ratings (1–4) for P1–P6 and F; three open answers and an optional comment.

## pilot_open_coding.csv (19 rows)
Author's coding of the open answers: `Q1_reward_choice` (reward type named), `Q1_judge_free_label_free` (1 = judge-free and label-free reward), `Q2_missing_types` (reward types proposed for the framework), `Q3_benchmarks_show_faithfulness` (No / Not fully / Mostly no / Not sufficiently / no answer / invalid).
