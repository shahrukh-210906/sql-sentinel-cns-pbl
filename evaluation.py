"""Compute classification metrics for the current training pipeline."""
import time

def evaluate(detector, rows):
    tp = tn = fp = fn = 0
    errors = []
    started = time.perf_counter()
    for row in rows:
        prediction = int(detector(row['text'])['malicious'])
        truth = row['label']
        tp += prediction == truth == 1
        tn += prediction == truth == 0
        fp += prediction == 1 and truth == 0
        fn += prediction == 0 and truth == 1
        if prediction != truth:
            errors.append({'text': row['text'], 'label': truth, 'prediction': prediction})
    elapsed = time.perf_counter()-started
    precision = tp/(tp+fp) if tp+fp else 0
    recall = tp/(tp+fn) if tp+fn else 0
    return dict(accuracy=(tp+tn)/len(rows), precision=precision, recall=recall,
                f1=2*precision*recall/(precision+recall) if precision+recall else 0,
                false_positive_rate=fp/(fp+tn), confusion=dict(tp=tp,tn=tn,fp=fp,fn=fn),
                milliseconds_per_input=elapsed*1000/len(rows), errors=errors)

