"""Two independent SQL injection classifiers; no submitted text is executed."""
import math
import re
from collections import Counter
from urllib.parse import unquote

def normalize(text):
    for _ in range(2):
        text = unquote(text)
    return re.sub(r'\s+', ' ', text.lower()).strip()

RULES = [
    ('Boolean condition', r"\b(?:or|and)\s+(?:\d+\s*=\s*\d+|'[^']*'\s*=\s*'[^']*')"),
    ('UNION query', r'\bunion\s+(?:all\s+)?select\b'),
    ('Stacked command', r';\s*(?:drop|delete|update|insert|alter|exec)\b'),
    ('Delay function', r'\b(?:sleep|benchmark|pg_sleep)\s*\(|\bwaitfor\s+delay\b'),
    ('Comment after quote', r"['\"]\s*(?:--|#|/\*)"),
    ('Metadata extraction', r'\binformation_schema\b|\bload_file\s*\('),
]

def rule_detect(text):
    value = normalize(text)
    value = re.sub(r'/\*.*?\*/', ' ', value)
    hits = [name for name, pattern in RULES if re.search(pattern, value)]
    return {'malicious': bool(hits), 'reasons': hits or ['No configured rule matched']}

def grams(text):
    value = ' ' + normalize(text) + ' '
    return Counter(value[i:i+n] for n in (2, 3) for i in range(len(value)-n+1))

class NaiveBayes:
    """Multinomial character n-gram NB with Laplace smoothing, trained on data."""
    def fit(self, rows):
        self.counts = [Counter(), Counter()]
        self.documents = [0, 0]
        for row in rows:
            label = int(row['label'])
            self.documents[label] += 1
            self.counts[label].update(grams(row['text']))
        self.vocabulary = set(self.counts[0]) | set(self.counts[1])
        self.totals = [sum(c.values()) + len(self.vocabulary) for c in self.counts]
        return self

    def predict(self, text):
        features = grams(text)
        scores = [math.log(n / sum(self.documents)) for n in self.documents]
        contributions = []
        for token, count in features.items():
            if token not in self.vocabulary:
                continue
            likelihoods = [math.log((self.counts[c][token]+1)/self.totals[c]) for c in (0, 1)]
            for c in (0, 1):
                scores[c] += count * likelihoods[c]
            contributions.append((count*(likelihoods[1]-likelihoods[0]), token))
        difference = max(-700, min(700, scores[0]-scores[1]))
        probability = 1 / (1 + math.exp(difference))
        return {'malicious': probability >= .5, 'score': round(probability, 6),
                'reasons': ['Influential n-gram: '+repr(token) for _, token in sorted(contributions, reverse=True)[:4]]}
