import json
import unittest
from pathlib import Path
from training_data import build
from train_model import validate
from trained_model import TrainedDetector

ROOT=Path(__file__).resolve().parents[1]

class TrainingTests(unittest.TestCase):
    def test_corpus_split_validation(self):
        validate(build())

    def test_cross_split_normalized_duplicate_rejected(self):
        rows=build()
        duplicate=dict(rows[0],split='test',family='new-test-family')
        with self.assertRaises(ValueError): validate(rows+[duplicate])

    def test_conflicting_labels_rejected(self):
        rows=build()
        duplicate=dict(rows[0],label=1)
        with self.assertRaises(ValueError): validate(rows+[duplicate])

    def test_selected_model_uses_validation_scores(self):
        report=json.loads((ROOT/'results/trained_metrics.json').read_text())
        scores={r['C']:r['validation_f1'] for r in report['candidates']}
        self.assertEqual(scores[report['selected_C']],max(scores.values()))
        for method in ('rule_based','ml_based'):
            confusion=report[method]['confusion']
            self.assertEqual(sum(confusion.values()),report['split_counts']['test'])

    def test_saved_model_is_repeatable(self):
        text="admin' OR 1=1 --"
        self.assertEqual(TrainedDetector().predict(text),TrainedDetector().predict(text))

    def test_streamlit_tabs_and_shared_result(self):
        from streamlit.testing.v1 import AppTest
        app=AppTest.from_file(str(ROOT/'streamlit_app.py')).run(timeout=30)
        self.assertEqual(len(app.exception),0)
        self.assertEqual([tab.label for tab in app.tabs],['Rule-based','ML-based','Comparison'])
        app.button(key='run_ml').click().run(timeout=30)
        self.assertEqual(len(app.exception),0)
        self.assertIn('analysis',app.session_state)
        self.assertEqual(app.metric[0].value,'Suspicious')
        app.selectbox(key='example').select('Normal username').run(timeout=30)
        self.assertNotIn('analysis',app.session_state)
        app.button(key='run_compare').click().run(timeout=30)
        self.assertEqual(len(app.exception),0)
        self.assertEqual(app.session_state['analysis']['text'],'alex')

if __name__=='__main__': unittest.main()
