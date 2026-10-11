"""Expanded authored corpus. Synthetic examples, not independent field data."""
import csv
from pathlib import Path

FAMILIES = {
 'train': {
  0: ['customer {x}', '{x}@example.com', 'find {x} shoes', "O'Reilly {x}", 'order number {x}',
      'learn SQL select {x}', 'sleep advice for {x}', 'sleep better tonight {x}',
      'union membership {x}', 'delete my shopping cart {x}', 'drop shipping guide {x}',
      'benchmark the laptop {x}', 'select a gift {x}', "D'Angelo {x}", 'please update my address {x}',
      'wait for delivery {x}', 'one or two tickets {x}', 'research information schema {x}',
      'how to use UNION SELECT in SQL {x}', 'database tutorial SELECT * FROM products {x}',
      'notes about OR 1=1 in database class {x}', 'normal search 1=1 {x}', 'please sleep(5) before retrying {x}',
      'shipping reference {x}; thanks', 'summer clothes {x}', 'SQL course {x}'],
  1: ["{x}' OR 1=1 --", "{x}' OR 'a'='a' --", "{x}' UNION SELECT username,password FROM users --",
      '{x}; DROP TABLE accounts', '{x}; DELETE FROM customers', "{x}' AND SLEEP(5) --", "{x}'#",
      "{x}' AND pg_sleep(3) --", "{x}'/**/OR/**/2=2--", "{x}' UNION ALL SELECT NULL --",
      "{x}' OR TRUE --", "{x}' AND FALSE --", "{x}' OR 1 BETWEEN 0 AND 2 --",
      "{x}' OR 5>2 --", "{x}' OR 'a' LIKE 'a' --", "{x}' || 'a'='a' --",
      "{x}' AND EXISTS(SELECT 1 FROM users) --", "{x}' AND ASCII(SUBSTRING(password,1,1))>64 --",
      "{x}'; UPDATE accounts SET role='admin' --", "{x}'; INSERT INTO users VALUES(1,'evil') --",
      "{x}' AND EXTRACTVALUE(1,CONCAT(0x7e,VERSION())) --", "{x}' AND LOAD_FILE('/etc/passwd') --",
      "{x}' UNION SELECT table_name FROM information_schema.tables --",
      "{x}'; WAITFOR DELAY '00:00:05' --", "{x}' OR 7 IN (7,8) --", "{x}' OR NOT FALSE --"]
 },
 'validation': {
  0: ['delivery for {x}', 'sleep recommendations {x}', 'union event at {x}', "O'Connor {x}",
      'delete saved search {x}', 'SQL lesson: UNION ALL SELECT {x}', 'waitfor delay example in a textbook {x}',
      'notes on Boolean conditions OR 2=2 {x}', 'benchmark(1000) function explanation {x}', 'running shoes {x}'],
  1: ["{x}' oR 7=7 --", "{x}' UNION ALL SELECT email FROM members --", '{x}; DELETE FROM inventory',
      "{x}' AND pg_sleep(8) --", "{x}'/**/OR/**/9=9--", "{x}' OR 6>1 --",
      "{x}' OR TRUE #", "{x}' AND EXISTS(SELECT id FROM accounts) #", "{x}' OR 'b' LIKE 'b' --",
      "{x}'; UPDATE users SET active=1 --"]
 },
 'test': {
  0: ['send parcel to {x}', "D'Souza {x}", 'sleep hygiene checklist {x}', 'trade union registration {x}',
      'delete playlist named {x}', 'SQL textbook: UNION SELECT combines rows {x}',
      'lecture notes: OR 3=3 is true {x}', 'pg_sleep(2) is covered in the tutorial {x}',
      'information_schema.tables documentation {x}', 'select this hotel for {x}',
      'please update account details {x}', 'drop the package at {x}', 'year-end report {x}',
      'ASCII function study notes {x}', 'waitfor delay syntax notes {x}', 'please load_file(path) in the tutorial {x}'],
  1: ["{x}' OR 3=3 -- tail", "{x}' UNION SELECT address FROM clients #", '{x}; DROP TABLE audit_log',
      "{x}'; DELETE FROM sessions WHERE id=8 --", "{x}' AND SLEEP(7) #", "{x}'/**/OR/**/8=8#",
      "{x}' OR TRUE /*", "{x}' OR 12>8 #", "{x}' OR 9 BETWEEN 8 AND 10 #",
      "{x}' OR 'cat' LIKE 'cat' #", "{x}' AND EXISTS(SELECT name FROM clients) #",
      "{x}' AND ASCII(SUBSTRING(secret,2,1))>70 #", "{x}' OR NOT FALSE #",
      "{x}' UNION ALL SELECT NULL,NULL,NULL #", "{x}'; WAITFOR DELAY '00:00:07' --",
      "{x}' AND EXTRACTVALUE(1,CONCAT(0x3a,DATABASE())) #"]
 }
}

def build():
    rows = []
    for split, groups in FAMILIES.items():
        for label, templates in groups.items():
            for family, template in enumerate(templates):
                for index in range(30 if split == 'train' else 12):
                    # Same neutral identifiers in both classes; no label encoded in identifiers.
                    identifier = ['alex','riley','guest','entry','search','item'][index % 6] + str(index)
                    rows.append(dict(text=template.format(x=identifier), label=label, split=split,
                                     family=f'{split}-{label}-{family}'))
    return rows

def save(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path,'w',encoding='utf-8',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=['text','label','split','family'])
        writer.writeheader()
        writer.writerows(rows)
