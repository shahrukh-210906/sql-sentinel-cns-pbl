import json
import platform
import time
from pathlib import Path
from dataset import build, save
from detector import NaiveBayes, rule_detect

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

def run():
    rows = build()
    train = [r for r in rows if r['split']=='train']
    test = [r for r in rows if r['split']=='test']
    start = time.perf_counter()
    model = NaiveBayes().fit(train)
    training = time.perf_counter()-start
    results = dict(dataset='Synthetic demonstration; disjoint template families; not real-world validation',
                   train_count=len(train),test_count=len(test),python=platform.python_version(),
                   platform=platform.platform(), training_seconds=training,
                   rule_based=evaluate(rule_detect,test),ml_based=evaluate(model.predict,test))
    Path('results').mkdir(exist_ok=True)
    save()
    Path('results/metrics.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    return results

if __name__ == '__main__':
    print(json.dumps(run(),indent=2))
