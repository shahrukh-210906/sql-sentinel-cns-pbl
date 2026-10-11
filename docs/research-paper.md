# Comparing Rule-Based and Character N-Gram SQL Injection Detection

**Draft research paper for Project 76. Authors and affiliation: to be completed.**

## Abstract

This study compares explicit SQL injection signatures with a supervised character n-gram Multinomial Naive Bayes classifier. Both methods are implemented in dependency-free Python and tested on the same synthetic request-input corpus. Final development measurements show 100% rule-based accuracy and 75% classifier accuracy over 240 evaluation examples. The classifier yields 20 false positives and 40 false negatives, illustrating lexical confounding and incomplete training coverage. The rule method is preferred within this demonstration, but correlated synthetic examples and a development-time rule correction prevent interpreting these figures as independent validation. The contribution is a reproducible educational comparison, not a novel algorithm or a production protection claim.

**Keywords:** SQL injection, signatures, Naive Bayes, character n-grams, comparative evaluation.

## I. Introduction and Motivation

Input classification may supplement application defenses by highlighting suspicious parameters. It cannot replace prepared statements [1]. The research question is: how do transparent signatures and a simple learned classifier differ in measured errors, explanations and processing cost on a reproducible local corpus?

## II. Related Work and Gap

OWASP describes primary prevention controls [1], [2]. Pattern matching is discussed in [3], while [4] considers detection techniques more broadly. These sources motivate the approaches, but the present work does not reproduce their experiments. The practical educational gap addressed is a small, auditable implementation exposing both predictions and failure cases under the same setup. No claim is made that this gap is new in the literature.

## III. Methodology and Contribution

The signature method searches six SQL-related pattern groups after normalization. The ML method estimates class-conditional bigram and trigram counts with Laplace smoothing, then chooses the class with the greater log posterior score. Training uses only the training split. Both methods receive identical evaluation strings. The contribution consists of the dual-method dashboard, deterministic corpus generation, evaluation exports and documented limits.

## IV. Experimental Setup

The corpus has 480 synthetic rows, evenly split into training and evaluation. Each split is balanced by label and uses distinct template families. Each family has 20 correlated variants. Python 3.12.14 on Windows 11 produced the recorded measurements. Accuracy, precision, recall, F1, false-positive rate and single-pass processing time are reported. A regression test led to a block-comment normalization correction during development; final evaluation therefore cannot be described as blind testing.

## V. Results

| Method | Accuracy | Precision | Recall | F1 | FP | FN | ms/input |
|---|---:|---:|---:|---:|---:|---:|---:|
| Rules | 100% | 100% | 100% | 100% | 0 | 0 | 0.0065 |
| N-gram NB | 75% | 80% | 66.67% | 72.73% | 20 | 40 | 0.0383 |

Table I. Development-corpus comparison. Exact measurements are preserved in `results/metrics.json`.

## VI. Discussion and Threats to Validity

Benign sleep advice triggers false positives in NB, while stacked DELETE and comment-obfuscated Boolean input produce false negatives. The training templates offer insufficient coverage of these families. Rules are easier to explain and perform better here, but the corpus reflects author-selected signatures and is not representative traffic. Repeated variants inflate apparent sample size, the labels represent template intent, and latency lacks repeated-run uncertainty analysis. Further corpus tuning must be evaluated on new independent samples. No statistically significant or real-world superiority claim is supported.

## VII. Conclusion and Future Work

Explicit signatures offer the stronger local demonstration under the recorded conditions. The trained classifier satisfies the independent-method requirement while revealing why data coverage matters. Future work should use independently sourced licensed data, family-aware validation, hard negatives, calibrated thresholds and repeated performance measurements. Application prevention remains based on parameterized queries.

## References

Use references [1]-[4] in `report.md`; their titles, identifiers and source links are supplied there. Expand author metadata from the primary papers and apply the instructor's required paper template before formal submission. No publication, authorship or completed team contribution is claimed by this draft.
