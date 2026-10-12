"""Shared text normalization and six SQL injection detection rules."""
import re
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

