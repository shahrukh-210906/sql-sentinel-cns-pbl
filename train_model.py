"""Train and select on validation only, then evaluate the frozen test split once."""
import argparse
import csv
import hashlib
import json
import platform
import time
from pathlib import Path
import joblib
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline
from detector import normalize,rule_detect
from experiment import evaluate
from training_data import build,save
from trained_model import TrainedDetector

ROOT=Path(__file__).resolve().parent

def validate(rows):
    if not rows: raise ValueError('Dataset is empty')
    seen={}
    families={}
    for row in rows:
        row['label']=int(row['label'])
        if row['label'] not in (0,1) or row['split'] not in ('train','validation','test'):
            raise ValueError('Labels must be 0/1 and splits train/validation/test')
        if not isinstance(row['text'],str) or not row['text'].strip() or len(row['text'])>4000:
            raise ValueError('Each text must contain 1-4000 characters')
        value=normalize(row['text'])
        if value in seen and seen[value] != (row['split'],row['label']):
            raise ValueError('Duplicate normalized text crosses splits or has conflicting labels')
        seen[value]=(row['split'],row['label'])
        group=row['family']
        if group in families and families[group]!=row['split']:
            raise ValueError('A template family crosses splits')
        families[group]=row['split']
    for split in ('train','validation','test'):
        if {r['label'] for r in rows if r['split']==split}!={0,1}:
            raise ValueError('Each split needs both labels')

def run(csv_path=None):
    if csv_path:
        with open(csv_path,encoding='utf-8-sig',newline='') as handle: rows=list(csv.DictReader(handle))
    else: rows=build()
    validate(rows)
    splits={split:[r for r in rows if r['split']==split] for split in ('train','validation','test')}
    train=splits['train']; validation=splits['validation']
    x=[normalize(r['text']) for r in train]; y=[r['label'] for r in train]
    vx=[normalize(r['text']) for r in validation]; vy=[r['label'] for r in validation]
    start=time.perf_counter(); candidates=[]; best=None; best_f1=-1
    for regularization in (.5,2.,8.):
        pipeline=Pipeline([('features',TfidfVectorizer(analyzer='char',ngram_range=(2,5),
                             min_df=2,max_features=20000,sublinear_tf=True)),
                           ('classifier',LogisticRegression(C=regularization,max_iter=1000,
                             class_weight='balanced',random_state=76))])
        pipeline.fit(x,y)
        score=float(f1_score(vy,pipeline.predict(vx)))
        candidates.append(dict(C=regularization,validation_f1=score))
        if score>best_f1: best_f1=score;best=pipeline
    # Keep training-only vocabulary/weights; validation is used only for model selection.
    (ROOT/'models').mkdir(exist_ok=True)
    joblib.dump(best,ROOT/'models/sql_detector.joblib')
    model=TrainedDetector()
    test=splits['test']
    model_metrics=evaluate(model.predict,test)
    rule_metrics=evaluate(rule_detect,test)
    # Per-family aggregation makes repetition visible; it does not establish independence.
    family_results=[]
    for family in sorted({r['family'] for r in test}):
        group=[r for r in test if r['family']==family]
        family_results.append(dict(family=family,count=len(group),label=group[0]['label'],
            rules_accuracy=evaluate(rule_detect,group)['accuracy'] if len({r['label'] for r in group})>1 else
                sum(rule_detect(r['text'])['malicious']==bool(r['label']) for r in group)/len(group),
            ml_accuracy=sum(model.predict(r['text'])['malicious']==bool(r['label']) for r in group)/len(group)))
    elapsed=time.perf_counter()-start
    save(ROOT/'data/training_corpus.csv',rows)
    fingerprint=hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()
    result=dict(model='Character TF-IDF (2-5 grams) + Logistic Regression',
        data_source=str(csv_path) if csv_path else 'Authored synthetic corpus v2',
        limitations='Synthetic family-separated development benchmark, not independent real-world validation. Correlated variants.',
        split_counts={k:len(v) for k,v in splits.items()},test_families=len(family_results),
        candidates=candidates,selected_C=best.named_steps['classifier'].C,
        threshold=.5,sklearn_version=sklearn.__version__,python=platform.python_version(),
        dataset_sha256=fingerprint,training_and_evaluation_seconds=elapsed,
        rule_based=rule_metrics,ml_based=model_metrics,family_results=family_results)
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/trained_metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('family_results','rule_based','ml_based')},indent=2))
    for key in ('rule_based','ml_based'):
        print(key, {k:v for k,v in result[key].items() if k!='errors'})
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--csv',type=Path,help='CSV with text,label,split,family columns')
    run(parser.parse_args().csv)
