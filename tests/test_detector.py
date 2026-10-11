import unittest
from dataset import build
from detector import NaiveBayes, rule_detect

class DetectionTests(unittest.TestCase):
    def test_encoding_and_comments(self):
        self.assertTrue(rule_detect("x%27%20OR%201%3D1--")['malicious'])
        self.assertTrue(rule_detect("x'/**/OR/**/2=2--")['malicious'])
    def test_benign_quotes(self):
        self.assertFalse(rule_detect("O'Reilly books")['malicious'])
    def test_dataset_is_disjoint(self):
        rows=build()
        train={r['text'] for r in rows if r['split']=='train'}
        test={r['text'] for r in rows if r['split']=='test'}
        self.assertFalse(train & test)
    def test_learning(self):
        model=NaiveBayes().fit([r for r in build() if r['split']=='train'])
        self.assertTrue(model.predict("admin' OR 1=1 --")['malicious'])
        self.assertFalse(model.predict('customer item123')['malicious'])

if __name__=='__main__': unittest.main()
