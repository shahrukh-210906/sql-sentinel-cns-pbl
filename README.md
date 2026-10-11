# SQL Sentinel — CNS Project 76

The new Streamlit app has **Rule-based**, **ML-based**, and **Comparison** tabs, animated processing, real rule matches, learned feature contributions, and one shared input.

## Hosted app and detailed report

Live app: https://cryptopbl.streamlit.app/

Source: https://github.com/shahrukh-210906/sql-sentinel-cns-pbl

The detailed technical report is in `docs/Project-Technical-Report.docx`, with a PDF copy and editable Markdown source. It explains the algorithms, equations, parameters, training, source files, animations, state, results, tests, deployment, and limitations.

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

Inspect `results/trained_metrics.json` for selection, errors, family results, version information, and dataset fingerprint. All rows are in `data/training_corpus.csv`. See `docs/trained-model.md`.

For a separately prepared corpus, run `train_model.py --csv path\to\corpus.csv`. Columns are `text,label,split,family`; label is 0/1; split is train/validation/test. Keep families and normalized texts separate across splits. The trainer rejects split leakage and conflicting labels. Never tune using the test set. Load only trusted locally generated model artifacts.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`streamlit_app.py` provides the app; `train_model.py` trains and evaluates; `training_data.py` builds synthetic examples; `trained_model.py` provides predictions and explanations. Animations illustrate processing, not latency. Inputs are inspected locally and never executed as SQL. Actual applications should use parameterized queries.

The earlier app (`python app.py`, port 8765), Naive Bayes baseline, `results/metrics.json`, and academic drafts are preserved as legacy material. Their model description and metrics do not describe the Streamlit version. Revise drafts using the training update and fill in team names before submission.
