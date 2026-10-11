# Trained model update

The Streamlit version replaces the original Naive Bayes demo with character TF-IDF plus Logistic Regression.

The authored synthetic corpus has 1,560 training, 240 validation, and 384 test rows. Templates belong to one split only; normalized cross-split duplicates and conflicting labels are rejected. Neutral identifiers appear in both classes. Test variants within families are correlated, so these are not 384 independent real-world cases.

C=0.5, 2, and 8 each achieved validation F1=1.0. The first tied value, C=0.5, was selected. The chosen model remains fitted only on training rows; threshold is 0.5. Scores are uncalibrated.

On the frozen synthetic test corpus, ML produced TP=190, TN=180, FP=12, FN=2. Rules produced TP=108, TN=120, FP=72, FN=84. ML accuracy is 96.4%; rule accuracy is 59.4%. Full metrics and errors are in results/trained_metrics.json.

Detection including explanations averaged about 1.67 ms/input for ML and 0.006 ms/input for rules in this run. This single local timing includes different explanation work and is not a controlled latency benchmark.

Evaluation includes legitimate SQL prose and attacks beyond current signatures. It supports an ML advantage on this corpus only. Since model and corpus both changed, the results cannot isolate model improvement over the old demo. Independent licensed real-world evaluation remains future work. No traffic interception, SQL execution, or production protection is provided.

Reproduce with train_model.py. The previous academic report, paper, presentation, and viva describe the legacy demo; revise them using this update before submission.
