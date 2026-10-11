# Demonstration and Viva Guide

## Five-minute demonstration

1. Run `python experiment.py`, then the unit tests, then `python app.py`.
2. Open the dashboard and explain that the input is never executed.
3. Analyze `admin' OR 1=1 --` and explain the Boolean signature.
4. Analyze `O'Reilly books` to demonstrate that an apostrophe alone is not sufficient for a rule alert.
5. Analyze `sleep advice sample100` to show an ML false positive.
6. Analyze `sample100; DELETE FROM inventory` to show a rule/ML disagreement.
7. Show metrics and explain that synthetic development results are not independent validation.

## Questions and answers

**Why are these two approaches technically different?** Rules encode manual syntax knowledge. NB learns feature frequencies and class priors from labeled data.

**What is SQL injection?** Untrusted values alter SQL query structure when an application mixes data with executable query text.

**Why use parameterized queries even with a detector?** A detector may miss attacks. Parameter binding keeps values separate from SQL structure.

**What does Naive Bayes assume?** Features are conditionally independent given the class; overlapping n-grams violate this approximation, which can contribute to overconfident scores.

**What is smoothing for?** Adding one avoids zero likelihood for known vocabulary features absent from a class.

**Why work in log space?** Multiplying many small likelihoods underflows; adding logarithms is numerically stable.

**Are model scores probabilities of real attacks?** They are model outputs under NB assumptions, not empirically calibrated probabilities.

**What is a false positive?** Benign input flagged as malicious; it can harm usability if used for blocking.

**What is a false negative?** An attack-labeled input missed by a detector; it can leave malicious requests unflagged.

**Why not report accuracy alone?** Class balance affects accuracy. Precision, recall, F1 and the confusion matrix expose different error costs.

**Did you evaluate on an independent dataset?** No. Templates differ between splits, but the corpus is synthetic and development feedback included a rule correction. A frozen external dataset remains necessary.

**Which approach is better?** Rules are better for the demonstrated corpus and transparency. The experiment does not prove universal superiority.

**What are the main failure cases?** NB mistakes innocent sleep advice and misses stacked DELETE and comment-obfuscated input; rules can miss unconfigured syntax or flag legitimate SQL discussion.

**What is each member's contribution?** Answer using actual work records. Suggested work allocation is in README; do not present it as completed personal work.

## Submission checklist

- Complete names, roll numbers and actual contribution records.
- Confirm 2+2 or 2+3 subgroup allocation; review both methods together.
- Retain CSV, JSON, tests and source alongside the report.
- Present the synthetic-data and development-evaluation limitations explicitly.
- Capture screenshots from your own run if requested by your instructor.
- Use `presentation.html` as a browser slide deck; a research draft is included for a three-person subgroup.
