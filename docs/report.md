# 1. Title Page

**SQL Sentinel: SQL Injection Detection System**  
Cryptography and Network Security - Project 76  
Approach 1: Rule-based signatures  
Approach 2: Character n-gram Multinomial Naive Bayes  
Team members, roll numbers, institution, supervisor and subgroup allocation: **to be supplied by the team**.  
Date: 5 October 2026

# 2. Abstract

SQL injection occurs when untrusted input changes the meaning of a database query. This project implements and compares two techniques for identifying suspicious request input: explicit regular-expression signatures and a supervised character n-gram Multinomial Naive Bayes classifier. Both methods share a bounded URL-decoding and case-normalization stage, but differ in how they make decisions. Rules identify configured SQL structures, whereas the classifier learns class-conditional feature frequencies from labeled examples. A dependency-free Python implementation provides a local browser dashboard, explanations, and an HTTP analysis endpoint. Experiments use 480 synthetic samples divided into 240 training and 240 evaluation inputs with disjoint template families. The final rule detector achieves 100 percent accuracy on this development evaluation, while the classifier achieves 75 percent accuracy, with 80 percent precision and 66.67 percent recall. The rule detector is preferred for this demonstration because its decisions are easier to explain and it produces fewer errors on the selected cases. These findings are limited by the small template-derived corpus, correlated samples, and a rule correction made during development. They do not establish performance on independent application traffic. The system never executes submitted SQL, and detection is presented as a supplementary measure alongside parameterized queries. Future work includes independent datasets, richer contextual features, threshold calibration, and repeated performance experiments.

# 3. Introduction

Web applications frequently accept usernames, search terms and identifiers that eventually become database parameters. Concatenating such values into query strings can let user input alter query structure. SQL injection can affect confidentiality, integrity and availability. OWASP recommends prepared statements with parameter binding as a primary defense [1]. This project investigates detection rather than implementing a vulnerable database application.

# 4. Problem Statement

Given one user-input string, identify whether it resembles an SQL injection attempt, explain the decision, and compare rule-based and learned methods on common labeled inputs. The input is a request parameter, not a complete SQL program. Legitimate prose about SQL can resemble an attack; the classifier does not know application context.

# 5. Objectives

- Implement two technically different detection methods.
- Display both verdicts and evidence in one interface.
- Measure accuracy, precision, recall, F1, false-positive rate and processing time.
- Record errors so strengths and weaknesses can be inspected.
- Provide repeatable experiments and a technically qualified recommendation.

# 6. Literature Review

OWASP's prevention guidance discusses parameterized queries, safe stored procedures, allow-list validation and least privilege [1]. This is implementation guidance, not evidence that input classification guarantees safety. Its injection-prevention guidance places controls in the context of the application data flow [2]. Pattern-based detection research examines explicit pattern matching for SQL injection [3]. A broader analysis surveys SQL injection detection techniques [4]. These research publications motivate the comparison; their reported results are not reproduced or used as this project's measurements. No state-of-the-art claim is made.

# 7. Existing System / Existing Approach

An application using string concatenation exposes query structure to untrusted values. Parameter binding separates code and values and should be adopted irrespective of a detector verdict [1]. A blacklist can identify familiar patterns but requires maintenance and may miss dialect-specific or obfuscated syntax. Learned text classification can recognize statistical regularities but depends on representative labels and can react to innocent words. Our experiment isolates those tradeoffs in a local text-analysis service.

# 8. Proposed Approach 1

The rule detector performs at most two URL-decoding passes, lowercases input and normalizes whitespace. Block comments are replaced with spaces for signature matching. Six signature groups cover numeric or quoted Boolean expressions, UNION SELECT, stacked commands, delay calls, comments following a quote, and metadata extraction. Any matching signature produces a suspicious verdict. A list of matched rule names explains the result. The expressions are heuristic and do not implement a SQL parser. Numeric comparisons are conservatively flagged even when not tautologies.

# 9. Proposed Approach 2

The ML detector uses overlapping character bigrams and trigrams from normalized text. Each training sample contributes n-gram counts to its labeled class. Laplace smoothing estimates P(g|c)=(count(g,c)+1)/(total(c)+|V|). At prediction time the classifier computes log P(c)+sum(count(g,input)*log P(g|c)) for each class. Unknown features are ignored. A logistic transformation of the score difference yields an uncalibrated attack score; 0.5 is the fixed classification threshold. The four largest positive attack-vs-benign contributions are displayed. These contributions explain local model evidence, not causality. The approach learns from data rather than executing the rule signatures.

# 10. Methodology

1. Define the request-input classification problem and consult technical sources.
2. Generate labeled benign and malicious templates separately for training and evaluation.
3. Fit the ML vocabulary, priors and n-gram counts on training rows only.
4. Run both methods on the same evaluation rows.
5. Calculate confusion matrices and metrics; record every disagreement with labels.
6. Compare errors, interpretability, latency and implementation effort.

The corpus and signatures were authored for this project. Train/evaluation text sets do not overlap. However, templates share SQL concepts and each family has 20 closely related variants. A block-comment regression test exposed a rule bug and prompted a correction during development. Consequently, the final evaluation is not a blind holdout. Do not treat its metrics as an unbiased estimate of generalization. A new frozen external test corpus is needed after further development.

# 11. System / Network Architecture

```text
Browser dashboard --> local HTTP service --> input validation
                                             |
                                +------------+------------+
                                |                         |
                         Signature detector         Trained NB model
                                |                         |
                                +-------- JSON -----------+
                                             |
                                    Browser explanations

Synthetic corpus --> training split --> NB feature counts
                 --> evaluation split --> both detectors --> metrics.json
```

Figure 1. Local analysis and evaluation architecture. Both detectors inspect the same input independently. There is no database query-execution path.

# 12. Implementation

`detector.py` implements shared normalization, signatures and the classifier. `dataset.py` creates the corpus. `experiment.py` fits the classifier, evaluates both approaches and exports `data/synthetic.csv` and `results/metrics.json`. `app.py` serves the browser dashboard and API using Python's standard HTTP server. It binds to loopback, limits the request body to 20,000 bytes and accepts at most 4,000 input characters. The dashboard renders strings using DOM text nodes, so submitted markup is not interpreted as HTML. `tests/test_detector.py` verifies representative encoded attacks, comment obfuscation, benign apostrophes, split disjointness and model learning.

# 13. Experimental Setup

Python 3.12.14 on Windows 11 was used for the recorded run. The corpus contains 480 rows: 240 training and 240 evaluation. Each split contains 120 benign and 120 malicious inputs, generated from six templates per class with 20 variants each. Split assignments are fixed rather than random, ensuring repeatability. The label is the template's intended attack status. No real user data or external traffic is included. Training took approximately 0.0026 seconds in the recorded run. Latency is one wall-clock pass using `time.perf_counter`, includes detector preprocessing, excludes HTTP/UI transport, and is sensitive to hardware and scheduling. No confidence intervals are warranted from this run.

# 14. Results

| Metric | Rule-based | ML-based |
|---|---:|---:|
| Accuracy | 100.00% | 75.00% |
| Precision | 100.00% | 80.00% |
| Recall | 100.00% | 66.67% |
| F1 | 100.00% | 72.73% |
| False-positive rate | 0.00% | 16.67% |
| Mean detector time per input | 0.0065 ms | 0.0383 ms |
| True positives | 120 | 80 |
| True negatives | 120 | 100 |
| False positives | 0 | 20 |
| False negatives | 0 | 40 |

Table 1. Final development-corpus results; see the JSON artifact for exact run values. Precision=TP/(TP+FP), recall=TP/(TP+FN), accuracy=(TP+TN)/N, F1=2PR/(P+R), and false-positive rate=FP/(FP+TN).

The ML model falsely flags all 20 benign `sleep advice` examples. It misses the 20 stacked DELETE examples and 20 comment-obfuscated Boolean examples. These failures demonstrate sensitivity to vocabulary and training coverage. Changing the training corpus to address them would require a fresh independent evaluation to avoid tuning on the same samples.

# 15. Comparative Analysis

| Dimension | Rules | ML |
|---|---|---|
| Decision basis | Human-authored syntax signatures | Learned n-gram likelihoods |
| Explanation | Named matching signatures | Statistical feature contributions |
| Data requirement | No labeled training corpus | Labeled corpus required |
| Maintenance | Modify and verify signatures | Review labels, retrain and recalibrate |
| Local measured quality | Better on selected templates | False positives and missed families |
| Storage | Small fixed signature set | Counts scale with vocabulary |
| Scope of generalization | Configured patterns | Training distribution |

Table 2. Methodological and practical comparison. Rules are the better choice for this particular demonstration because they are transparent, faster in the recorded run and more accurate on the selected templates. The evidence does not establish that rules outperform ML on other data. A hybrid could be investigated, but it is not counted as one of the two implemented approaches.

# 16. Security Analysis

Submitted text is not executed and there are no database credentials. The server is local-only and retains no submitted-input history. Body and character limits bound ordinary request size. The Python development HTTP server is not a hardened deployment gateway; slow clients, concurrency and network exposure require a production server and deployment review. Bounded decoding can miss deeper encoding. Case conversion and comment handling are approximate and may differ from database interpretation. Regexes cover selected syntax only. ML scores are not calibrated probabilities and cannot establish that a query is safe. Parameter binding, least privilege and application-level validation remain required [1].

# 17. Discussion

The two subgroups can demonstrate distinct security methodologies: manually encoded knowledge and supervised statistical learning. The synthetic experiment is intentionally reproducible and exposes failure cases rather than concealing them. The corpus is small, balanced and repetitive; deployment distributions may be highly imbalanced, making false positives more consequential. Template relatives are correlated, so 240 evaluation rows do not represent 240 independent attack ideas. Complete SQL statements, dialect variations, Unicode, legitimate SQL documentation and adversarially crafted strings require broader evaluation. No claim of novelty or deployable protection is made.

# 18. Conclusion

The project delivers two functioning detectors, a local interface and reproducible comparative measurements. Rule-based detection is preferred within the demonstrated scope. ML provides a different, data-driven decision mechanism but its errors show that simple n-gram learning with a small synthetic corpus is insufficient for production judgments. Independent evaluation is the next requirement before drawing broader conclusions.

# 19. Future Scope

Use a licensed, independently labeled request-input dataset; freeze an external test set before tuning; group evaluation by attack family; study different SQL dialects and encoding styles; add legitimate SQL prose as difficult negatives; compare TF-IDF with logistic regression; calibrate scores on a validation split; repeat latency and memory measurements; and assess a hybrid detector without weakening parameterized database access.

# 20. References

[1] OWASP Foundation, "SQL Injection Prevention Cheat Sheet," OWASP Cheat Sheet Series. [Online]. Available: https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html. Accessed: Oct. 5, 2026.

[2] OWASP Foundation, "Injection Prevention Cheat Sheet," OWASP Cheat Sheet Series. [Online]. Available: https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html. Accessed: Oct. 5, 2026.

[3] "Preventing SQL Injection attack using pattern matching algorithm," arXiv:1504.06920, 2015. [Online]. Available: https://arxiv.org/abs/1504.06920.

[4] "Analysis of SQL Injection Detection Techniques," arXiv:1605.02796, 2016. [Online]. Available: https://arxiv.org/abs/1605.02796.

# 21. Appendix

Run commands are in `README.md`. The corpus, source code, test suite and raw JSON metrics form the reproducibility appendix. Team names and actual contribution records must be completed by the students; no contributions are asserted here. The supplied guidelines require a team of 4-5 students, split 2+2 or 2+3, and a draft paper for a three-student subgroup. All members must understand both approaches. The supplied presentation window was Sept. 28-Oct. 1, 2026; confirm the current submission arrangement with the instructor.
