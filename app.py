import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from dataset import build
from detector import NaiveBayes, rule_detect, normalize, RULES
import re

ROOT = Path(__file__).resolve().parent
MODEL = NaiveBayes().fit([r for r in build() if r['split']=='train'])

class Handler(BaseHTTPRequestHandler):
    def send(self, status, value, kind='application/json'):
        raw = value.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', kind+'; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self):
        if self.path == '/':
            self.send(200,(ROOT/'web/index.html').read_text(encoding='utf-8'),'text/html')
        elif self.path == '/api/metrics':
            file = ROOT/'results/metrics.json'
            self.send(200,file.read_text() if file.exists() else '{}')
        else:
            self.send(404,json.dumps({'error':'Not found'}))

    def do_POST(self):
        if self.path != '/api/detect':
            return self.send(404,json.dumps({'error':'Not found'}))
        try:
            length = int(self.headers.get('Content-Length','0'))
            if not 0 < length <= 20000:
                return self.send(413,json.dumps({'error':'Request too large or empty'}))
            data = json.loads(self.rfile.read(length))
            text = data.get('text') if isinstance(data,dict) else None
            if not isinstance(text,str) or not text.strip() or len(text)>4000:
                return self.send(400,json.dumps({'error':'Enter 1 to 4000 characters'}))
            normalized = normalize(text)
            rule_input = re.sub(r'/\*.*?\*/', ' ', normalized)
            self.send(200,json.dumps({'rule_based':rule_detect(text),'ml_based':MODEL.predict(text),
                'normalized':normalized,
                'rule_checks':[{'name':name,'matched':bool(re.search(pattern,rule_input))} for name,pattern in RULES]}))
        except (ValueError, UnicodeError):
            self.send(400,json.dumps({'error':'Invalid JSON request'}))

if __name__ == '__main__':
    print('SQL Sentinel: http://127.0.0.1:8765')
    ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
