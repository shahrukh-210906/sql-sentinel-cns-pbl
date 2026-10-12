import unittest
from detector import rule_detect
from trained_model import TrainedDetector

class DetectionTests(unittest.TestCase):
    def test_encoding_and_comments(self):
        self.assertTrue(rule_detect("x%27%20OR%201%3D1--")['malicious'])
        self.assertTrue(rule_detect("x'/**/OR/**/2=2--")['malicious'])
    def test_benign_quotes(self):
        self.assertFalse(rule_detect("O'Reilly books")['malicious'])
    def test_learning(self):
        model=TrainedDetector()
        self.assertTrue(model.predict("admin' OR 1=1 --")['malicious'])
        self.assertFalse(model.predict('customer item123')['malicious'])

if __name__=='__main__': unittest.main()
