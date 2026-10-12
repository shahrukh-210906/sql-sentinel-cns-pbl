# SQL Sentinel — CNS Project 76

The Streamlit app has **Rule-based**, **ML-based**, and **Comparison** tabs, animated processing, real rule matches, learned feature contributions, and one shared input.

## Hosted app

Live app: https://cryptopbl.streamlit.app/

Source: https://github.com/shahrukh-210906/sql-sentinel-cns-pbl

## Run

Double-click `run_streamlit.bat` on Windows. Requires Python 3.12 or newer. The launcher installs dependencies into `.venv` and starts http://127.0.0.1:8501.

Manual setup:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe train_model.py
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

The trained model is included. Retraining is optional; restart Streamlit afterward to load the new model. Stop with Ctrl+C.

## Training results

Character TF-IDF (2–5 grams) + Logistic Regression. Training: 1,560 rows. Validation: 240 rows. Test: 384 rows from 32 template families. Vocabulary and weights use training rows only; regularization is selected using validation only.

| Metric | Rules | ML |
|---|---:|---:|
| Accuracy | 59.4% | 96.4% |
| Precision | 60.0% | 94.1% |
| Recall | 56.3% | 99.0% |
| F1 | 58.1% | 96.4% |
| False-positive rate | 37.5% | 6.3% |

These are **authored synthetic** results, not independent real-world validation. Related SQL concepts and correlated variants remain across splits. The corpus includes legitimate SQL prose and less obvious attacks. Both corpus and model changed from the old demo, so improvement cannot be attributed solely to the model. Rules remain faster. ML scores are uncalibrated.

Inspect `results/trained_metrics.json` for selection, errors, family results, version information, and dataset fingerprint. All rows are in `data/training_corpus.csv`.

For a separately prepared corpus, run `train_model.py --csv path\to\corpus.csv`. Columns are `text,label,split,family`; label is 0/1; split is train/validation/test. Keep families and normalized texts separate across splits. The trainer rejects split leakage and conflicting labels. Never tune using the test set. Load only trusted locally generated model artifacts.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`streamlit_app.py` provides the app; `train_model.py` trains and evaluates; `training_data.py` builds synthetic examples; `trained_model.py` provides predictions and explanations. Animations illustrate processing, not latency. Inputs are inspected locally and never executed as SQL. Actual applications should use parameterized queries.

## Project files

- `streamlit_app.py`: three-tab app and input handling.
- `visual_ui.py` and `ui.css`: simulation, charts, and styling.
- `detector.py`: normalization and the six detection rules.
- `trained_model.py`: load the trained model and explain predictions.
- `training_data.py`, `train_model.py`, and `evaluation.py`: data generation, training, and evaluation.
- `models/`, `data/`, and `results/trained_metrics.json`: trained artifact, current corpus, and benchmark.
- `tests/`: current detector, training, and app checks.

The old HTTP app, Naive Bayes implementation, old dataset, outdated drafts, and generated previews were removed on 12 October 2026. Start the current app with `run_streamlit.bat`; port 8765 belongs to the removed version.
