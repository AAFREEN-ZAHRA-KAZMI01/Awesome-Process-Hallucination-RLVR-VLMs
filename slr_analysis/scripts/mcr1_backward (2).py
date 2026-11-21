"""Backward snowballing of the base paper MC-R1 (IEEE TMM 2026, OpenAlex W7203919802):
61 referenced works retrieved from OpenAlex on 20 Nov 2026, title-level decision with IC/EC reason."""
import csv
B='benchmark/dataset only, no training reward (IC2)'
D='prompting- or decoding-only mitigation (EC2)'
T='text-only LLM (EC1)'
F='pre-2022 or general foundational work (IC4)'
M='domain-specific pipeline (EC3)'
O='off-topic: not VLM reward design (IC1/IC2)'
S='survey: considered for the reviews table, not a primary study'
rows=[
("ROUGE: A Package for Automatic Evaluation of Summaries",2004,"Excluded at title",F),
("Training Language Models to Follow Instructions with Human Feedback",2022,"Excluded at title",T),
("DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning",2025,"Excluded at title","text-only; cited as foundational work (EC1)"),
("Survey of Hallucination in Natural Language Generation",2023,"Excluded at title","text-only survey (EC1)"),
("Improved Baselines with Visual Instruction Tuning",2024,"Excluded at title","backbone model, no RL reward (IC2); cited as foundational"),
("Evaluating Object Hallucination in Large Vision-Language Models",2023,"Excluded at title",B),
("MMBench: Is Your Multi-modal Model an All-Around Player?",2024,"Excluded at title",B),
("MMMU: A Massive Multi-Discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI",2024,"Excluded at title",B),
("HybridFlow: A Flexible and Efficient RLHF Framework",2025,"Excluded at title","training infrastructure, text-only (EC1)"),
("A survey on multimodal large language models",2024,"Excluded at title",S+" (already in Table I)"),
("MME: A Comprehensive Evaluation Benchmark for Multimodal Large Language Models",2025,"Excluded at title",B),
("MathVista: Evaluating Mathematical Reasoning of Foundation Models in Visual Contexts",2023,"Excluded at title",B),
("Are We on the Right Way for Evaluating Large Vision-Language Models?",2024,"Excluded at title",B),
("HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models",2023,"Excluded at title",T),
("OCRBench: on the hidden mystery of OCR in large multimodal models",2024,"Excluded at title",B),
("Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding",2024,"Excluded at title",D),
("Vision-R1: Incentivizing Reasoning Capability in Multimodal Large Language Models",2025,"Already included","S19"),
("OPERA: Alleviating Hallucination in Multi-Modal Large Language Models via Over-Trust Penalty and Retrospection-Allocation",2024,"Excluded at title",D),
("A Diagram is Worth a Dozen Images",2016,"Excluded at title",F),
("Visual-RFT: Visual Reinforcement Fine-Tuning",2025,"Already included","S20"),
("RLHF-V: Towards Trustworthy MLLMs via Behavior Alignment from Fine-Grained Correctional Human Feedback",2024,"Potentially eligible","fine-grained human-feedback objective for hallucination; check IC2 (preference vs RL)"),
("Detecting and Preventing Hallucinations in Large Vision Language Models",2024,"Potentially eligible","reward model for hallucination detection used in training; check IC2"),
("MedVLM-R1: Incentivizing Medical Reasoning Capability of Vision-Language Models (VLMs) via Reinforcement Learning",2025,"Excluded at title",M),
("Mitigating Hallucinations in Large Vision-Language Models with Instruction Contrastive Decoding",2024,"Excluded at title",D),
("The Emerged Security and Privacy of LLM Agent: A Survey with Case Studies",2025,"Excluded at title",O),
("Med-R1: Reinforcement Learning for Generalizable Medical Reasoning in Vision-Language Models",2026,"Excluded at title",M),
("HalluciDoctor: Mitigating Hallucinatory Toxicity in Visual Instruction Data",2024,"Excluded at title","instruction-data cleaning, no RL reward (IC2)"),
("Performance and exploration of ChatGPT in medical examination, records and education in Chinese",2023,"Excluded at title",T),
("IBD: Alleviating Hallucinations in Large Vision-Language Models via Image-Biased Decoding",2025,"Excluded at title",D),
("Multi-Level Policy and Reward-Based Deep Reinforcement Learning Framework for Image Captioning",2019,"Excluded at title",F),
("Unique Security and Privacy Threats of Large Language Models: A Comprehensive Survey",2025,"Excluded at title",O),
("VIGC: Visual Instruction Generation and Correction",2024,"Excluded at title","data generation, no RL reward (IC2)"),
("Plausible May Not Be Faithful: Probing Object Hallucination in Vision-Language Pre-training",2023,"Excluded at title","pre-training analysis, no RL reward (IC2)"),
("Multi-Task Paired Masking With Alignment Modeling for Medical Vision-Language Pre-Training",2023,"Excluded at title",M),
("Reference-free Hallucination Detection for Large Vision-Language Models",2024,"Excluded at title","detection only, no training reward (IC2)"),
("Reasoning beyond limits: Advances and open problems for LLMs",2025,"Excluded at title",T),
("HaloQuest: A Visual Hallucination Dataset for Advancing Multimodal Reasoning",2024,"Excluded at title",B),
("Skill-Based Hierarchical Reinforcement Learning for Target Visual Navigation",2023,"Excluded at title",O),
("The Frontier of Data Erasure: A Survey on Machine Unlearning for Large Language Models",2025,"Excluded at title",O),
("GPT4Ego: Unleashing the Potential of Pre-Trained Models for Zero-Shot Egocentric Action Recognition",2024,"Excluded at title",O),
("Beyond Multimodal Hallucinations: Enhancing LVLMs through Hallucination-Aware Direct Preference Optimization",2025,"Potentially eligible","hallucination-aware preference objective; check IC2 (DPO vs RL)"),
("UniDCP: Unifying Multiple Medical Vision-Language Tasks via Dynamic Cross-Modal Learnable Prompts",2024,"Excluded at title",M),
("MossVLN: Memory-Observation Synergistic System for Continuous Vision-Language Navigation",2025,"Excluded at title",O),
("Deep Reinforcement Polishing Network for Video Captioning",2020,"Excluded at title",F),
("Learning Perceptual Hallucination for Multi-Robot Navigation in Narrow Hallways",2023,"Excluded at title",O),
("Mitigating Hallucinations in Large Vision-Language Models via Reasoning Uncertainty-Guided Refinement",2025,"Potentially eligible","reasoning-level hallucination mitigation; check whether a training reward is used (EC2)"),
("Generalizable Prompt Learning via Gradient Constrained Sharpness-Aware Minimization",2024,"Excluded at title",O),
("How Vision-Language Tasks Benefit From Large Pre-Trained Models: A Survey",2025,"Excluded at title",S),
("Woodpecker",2025,"Excluded at title","post-hoc correction, no training reward (EC2)"),
("Towards Specific Domain Prompt Learning via Improved Text Label Optimization",2024,"Excluded at title",O),
("UniAlign: A Universal Cross-Modality Knowledge Alignment Framework for Fine-Grained Action Recognition",2025,"Excluded at title",O),
("GPT-4 Technical Report",2023,"Excluded at title","model report, no reward design (IC2)"),
("Gemini: A Family of Highly Capable Multimodal Models",2023,"Excluded at title","model report, no reward design (IC2)"),
("Qwen2.5-VL Technical Report",2025,"Excluded at title","backbone report, no reward design (IC2)"),
("Deep reinforcement learning from human preferences",2017,"Excluded at title",F),
("Tulu 3: Pushing Frontiers in Open Language Model Post-Training",2024,"Excluded at title",T),
("Seed1.5-VL Technical Report",2025,"Excluded at title","model report, no reward design (IC2)"),
("Enhancing the Reasoning Ability of Multimodal Large Language Models via Mixed Preference Optimization",2024,"Potentially eligible","preference objective for multimodal reasoning; check IC2"),
("Holistic Analysis of Hallucination in GPT-4V(ision): Bias and Interference Challenges",2023,"Excluded at title","evaluation of a closed model, no training reward (IC2)"),
("Robust Multimodal Large Language Models Against Modality Conflict",2025,"Potentially eligible","RL with LLM-judge reward under modality conflict (screening record R170, Uncertain)"),
("Reinforcement Fine-Tuning Powers Reasoning Capability of Multimodal Large Language Models",2025,"Excluded at title","position/survey paper, no new reward (IC2)"),
]
assert len(rows)==61
old=list(csv.DictReader(open('data/snowballing_log.csv')))
old=[r for r in old if r.get('cited_by_seed')!='MC-R1 (base)']
f=list(old[0].keys())
for t,y,d,r in rows:
    old.append(dict(direction='backward (base paper)',title=t,first_author='',year=y,cited_by_seed='MC-R1 (base)',decision=d,reason=r))
w=csv.DictWriter(open('data/snowballing_log.csv','w',newline=''),fieldnames=f); w.writeheader(); w.writerows(old)
import collections; print(len(old)); print(collections.Counter(r['decision'] for r in old if r['cited_by_seed']=='MC-R1 (base)'))
print(collections.Counter((r['direction'],r['decision']) for r in old))
