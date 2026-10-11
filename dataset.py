"""Deterministic synthetic corpus with disjoint template families per split."""
import csv
from pathlib import Path

TRAIN_BAD = ["{x}' OR 1=1 --", "{x}' UNION SELECT username,password FROM users --", "{x}; DROP TABLE accounts", "{x}' AND SLEEP(5) --", "{x}'#", "{x}' OR 'a'='a' --"]
TEST_BAD = ["{x}' oR 7=7 --", "{x}' UNION ALL SELECT email FROM customers --", "{x}; DELETE FROM inventory", "{x}' AND pg_sleep(3) --", "{x}'/**/OR/**/2=2--", "{x}' AND 1=2 UNION SELECT NULL --"]
TRAIN_GOOD = ["customer {x}", "{x}@example.com", "find {x} shoes", "O'Reilly {x}", "order number {x}", "learn SQL select {x}"]
TEST_GOOD = ["delivery for {x}", "{x} hiking boots", "D'Angelo {x}", "union membership {x}", "sleep advice {x}", "select a gift for {x}"]

def build():
    rows = []
    for split, groups in [('train', (TRAIN_GOOD, TRAIN_BAD)), ('test', (TEST_GOOD, TEST_BAD))]:
        for label, templates in enumerate(groups):
            for family, template in enumerate(templates):
                for i in range(20):
                    x = ('item' if split == 'train' else 'sample') + str(i+100)
                    rows.append({'text': template.format(x=x), 'label': label,
                                 'split': split, 'family': f'{split}-{label}-{family}'})
    return rows

def save():
    Path('data').mkdir(exist_ok=True)
    with open('data/synthetic.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['text','label','split','family'])
        writer.writeheader()
        writer.writerows(build())

if __name__ == '__main__':
    save()
