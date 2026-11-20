# Contributing
1. Check that the paper uses reinforcement learning (or RL-style post-training) on a vision-language model and targets hallucination in the reasoning or the answer.
2. Add one row to `data/papers.csv` (id `C01`, `C02`, ... for community additions): title, first_author, year, venue, family, method, code, url.
3. Choose the reward family: Judge / model-based, Region / rationale annotation, Rule-based / objective, Calibration / test-time.
4. Regenerate `data/papers.json` (`python -c "import pandas as pd; pd.read_csv('data/papers.csv').to_json('data/papers.json', orient='records', indent=1)"`) and run `python build_site.py`.
5. Open a pull request with a one-line reason why the paper fits.
