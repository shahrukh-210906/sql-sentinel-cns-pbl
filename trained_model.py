"""Load only the locally trained artifact; never accept uploaded pickle files."""
from pathlib import Path
import joblib
from detector import normalize

ROOT=Path(__file__).resolve().parent

class TrainedDetector:
    def __init__(self, path=None):
        self.pipeline=joblib.load(path or ROOT/'models/sql_detector.joblib')

    def predict(self,text):
        value=normalize(text)
        probability=float(self.pipeline.predict_proba([value])[0,1])
        vectorizer=self.pipeline.named_steps['features']
        classifier=self.pipeline.named_steps['classifier']
        vector=vectorizer.transform([value]).tocoo()
        vocabulary=vectorizer.get_feature_names_out()
        evidence=sorted([(float(weight*classifier.coef_[0,index]),vocabulary[index])
                         for index,weight in zip(vector.col,vector.data)],reverse=True)
        return dict(malicious=probability>=.5,score=round(probability,6),
                    reasons=[f'{token!r}: {effect:+.3f}' for effect,token in evidence[:6]],
                    features=[dict(token=token,contribution=effect) for effect,token in evidence[:6]])
