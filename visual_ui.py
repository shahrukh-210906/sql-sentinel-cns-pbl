"""Trusted presentation templates. Escape all input and model evidence as text."""
import html

def esc(value):
    return html.escape(str(value))

ICONS = {
    'input':'<rect x="4" y="5" width="16" height="14" rx="3"/><path d="m8 10 3 2-3 2m5 0h3"/>',
    'decode':'<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-3-12-2 14"/>',
    'rules':'<rect x="5" y="3" width="14" height="18" rx="3"/><path d="m8 8 1 1 2-2m2 1h3m-8 5 1 1 2-2m2 1h3"/>',
    'patterns':'<path d="M4 7h4m4 0h8M4 12h8m4 0h4M4 17h4m4 0h8"/><circle cx="10" cy="7" r="2"/><circle cx="14" cy="12" r="2"/><circle cx="10" cy="17" r="2"/>',
    'score':'<path d="M4 19V5m0 14h16M8 15l4-5 4 2 4-7"/>',
}

def icon(name):
    return f'<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

BASE = '''<meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{margin:0;font:14px/1.5 system-ui,-apple-system,sans-serif;color:#18283f;background:transparent}
.card{background:white;border:1px solid #e2e8f0;border-radius:18px;overflow:hidden;--accent:#285ad6;--tint:#edf3ff;--delay:0s}
.card.ml{--accent:#7650b9;--tint:#f3effb}.top{padding:18px 22px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #edf0f5}
.label{font-size:12px;color:#596b80;font-weight:650;letter-spacing:1px;text-transform:uppercase}.badge{padding:5px 10px;border-radius:20px;font-size:12px;font-weight:600;background:#f1f5f9;color:#596b80}
.scene{padding:26px 24px 22px;background:radial-gradient(ellipse at 50% 20%,var(--tint),white 78%)}
.flow{display:grid;grid-template-columns:1fr 44px 1fr 44px 1fr;align-items:center}.node{text-align:center;min-width:0}.node-icon{width:58px;height:58px;margin:0 auto 10px;border-radius:17px;background:white;border:1px solid #dfe6f0;display:grid;place-items:center;color:var(--accent);box-shadow:0 4px 12px #18283f05}
.node-icon svg{width:28px;height:28px}.node b{display:block;font-size:14px;font-weight:600}.node small{display:block;font-size:12px;color:#596b80;margin-top:3px}
.wire{height:2px;background:#dce5f2;position:relative;margin-top:-34px}.wire:after{content:'';position:absolute;right:0;top:-3px;width:7px;height:7px;border-right:2px solid #a7b7cf;border-top:2px solid #a7b7cf;transform:rotate(45deg)}
.wire i{position:absolute;top:-3px;left:0;width:8px;height:8px;border-radius:50%;background:var(--accent);opacity:0}
.playing .node-icon{animation:pulse .7s ease both;animation-delay:calc(var(--i)*.65s)}.playing .wire i{animation:travel .65s ease-in-out both;animation-delay:calc(var(--i)*.65s + .3s)}
@keyframes pulse{50%{background:var(--tint);border-color:var(--accent);box-shadow:0 0 0 5px var(--tint);transform:translateY(-3px)}}
@keyframes travel{10%{opacity:1}90%{opacity:1}100%{transform:translateX(38px);opacity:0}}
.query{margin-top:24px;padding:14px 16px;background:#fff;border:1px solid #e2e8f0;border-radius:11px}.query .label{font-size:11px;letter-spacing:.7px}.query code{display:block;color:#304766;font:14px/1.65 Consolas,monospace;overflow-wrap:anywhere;margin-top:6px}
.work{padding:20px 24px 24px}.work-title{display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;color:#596b80;font-size:13px}.work-title strong{color:#18283f;font-size:14px;font-weight:600}
.checks{display:grid;grid-template-columns:1fr 1fr;gap:9px}.check{border:1px solid #e2e8f0;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;gap:8px;font-size:13px}.check.hit{background:#fff2f4;border-color:#f0cbd3}.check .status{font-size:12px;white-space:nowrap;color:#596b80}.check.hit .status{color:#a82545;font-weight:650}.pending{opacity:.7}
.playing .check,.playing .chip{animation:enter .3s both;animation-delay:calc(var(--delay) + var(--i)*.06s)}
.chips{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin-bottom:20px}.chip{padding:11px 12px;border:1px solid #e8dff6;background:#faf8fe;border-radius:10px;min-width:0}.chip code{display:block;color:#65409e;font:14px/1.5 Consolas,monospace;overflow-wrap:anywhere}.chip small{font-size:12px;color:#596b80}.chip .mini{height:3px;background:#ece5f7;margin-top:8px;border-radius:4px}.chip .mini i{display:block;height:100%;background:#8966be;border-radius:4px}
.score{display:flex;align-items:center;justify-content:space-between;color:#596b80;font-size:13px}.score b{font-size:27px;color:var(--accent);letter-spacing:-1px}.meter{height:10px;background:#ece6f5;border-radius:8px;margin:10px 0;position:relative}.meter i{height:100%;display:block;background:var(--accent);border-radius:8px;transform-origin:left;transform:scaleX(var(--score))}.playing .meter i{animation:fill .65s both;animation-delay:var(--delay)}
.threshold{position:absolute;left:50%;top:-4px;height:18px;border-left:2px solid #6c788c}.labels{display:flex;justify-content:space-between;font-size:12px;color:#596b80}.labels span:nth-child(2){text-align:center}
.verdict{padding:18px 24px;border-top:1px solid #e2e8f0;display:flex;gap:12px;align-items:center;background:#f8fafc}.verdict.bad{background:#fff5f6}.verdict.good{background:#f0faf5}.result-icon{font-size:19px;font-weight:700;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:white;color:#596b80;flex-shrink:0}.bad .result-icon,.bad strong{color:#a82545}.good .result-icon,.good strong{color:#176c49}.verdict strong{font-size:19px;font-weight:650}.verdict p{font-size:12px;color:#596b80;margin:3px 0 0}.playing .verdict{animation:enter .3s both;animation-delay:calc(var(--delay) + .45s)}
.empty-note{font-size:13px;color:#596b80;margin:0 0 14px}.empty-score{height:70px;display:flex;align-items:center;justify-content:center;border:1px dashed #d9cdea;border-radius:10px;color:#7650b9;background:#faf8fe;font-size:14px}
@keyframes enter{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}@keyframes fill{from{transform:scaleX(0)}to{transform:scaleX(var(--score))}}
@media(max-width:540px){.scene,.work{padding:20px 16px}.top{padding:15px 16px}.flow{grid-template-columns:1fr 25px 1fr 25px 1fr}.node b{font-size:12px}.node small{font-size:11px}.node-icon{width:48px;height:48px;border-radius:14px}.wire{margin-top:-30px}.checks{grid-template-columns:1fr}.chips{grid-template-columns:repeat(3,minmax(0,1fr))}.chip{padding:8px}.verdict{padding:16px}.labels{font-size:11px}@keyframes travel{to{transform:translateX(19px);opacity:0}}}
@media(prefers-reduced-motion:reduce){*{animation:none!important}}
</style>'''

def simulation(kind, data, text, animate, rules):
    is_rule = kind == 'rules'
    playing = bool(animate and data)
    names = [('input','Input','Your text'),('decode','Normalize','Decode + clean'),('rules','Match','6 fixed rules')] if is_rule else [('input','Input','Your text'),('patterns','Patterns','Character features'),('score','Score','Learned weights')]
    stages = ''.join(f'<div class="node" style="--i:{i}"><div class="node-icon">{icon(key)}</div><b>{name}</b><small>{note}</small></div>' + (f'<div class="wire" style="--i:{i}"><i></i></div>' if i < 2 else '') for i,(key,name,note) in enumerate(names))
    detection = data['rule_based' if is_rule else 'ml_based'] if data else None
    if is_rule:
        checks = data['checks'] if data else [dict(name=name, matched=False) for name,_ in rules]
        count = sum(c['matched'] for c in checks)
        body = f'<div class="work-title"><strong>Rule checklist</strong><span>{count if data else "—"} / 6 matched</span></div><div class="checks">'
        for i, check in enumerate(checks):
            status = 'Matched' if check['matched'] else ('Clear' if data else 'Waiting')
            body += f'<div class="check {"hit" if check["matched"] else ""} {"pending" if not data else ""}" style="--i:{i}"><span>{esc(check["name"])}</span><span class="status">{status}</span></div>'
        body += '</div>'
        evidence = ' · '.join(detection['reasons']) if data else 'Choose an example, then run the detector.'
    else:
        body = '<div class="work-title"><strong>Learned evidence</strong><span>+ attack · − benign</span></div>'
        if data:
            features = detection['features']
            largest = max([abs(f['contribution']) for f in features] or [1]) or 1
            body += '<div class="chips">' + ''.join(f'<div class="chip" style="--i:{i}"><code>{esc(f["token"].replace(" ","␣"))}</code><small>{f["contribution"]:+.2f} impact</small><div class="mini"><i style="width:{abs(f["contribution"])/largest*100:.1f}%"></i></div></div>' for i,f in enumerate(features)) + '</div>'
            body += f'<div class="score"><span>Attack score <small>· uncalibrated</small></span><b>{detection["score"]*100:.1f}%</b></div><div class="meter"><i style="--score:{detection["score"]}"></i><div class="threshold"></div></div><div class="labels"><span>0%</span><span>50% threshold</span><span>100%</span></div>'
        else:
            body += '<p class="empty-note">Small character patterns contribute to one attack score.</p><div class="empty-score">Patterns → weights → prediction</div>'
        evidence = 'Score ≥ 50% is flagged as suspicious.' if data else 'Choose an example, then run the detector.'
    verdict = ('Suspicious input' if detection['malicious'] else 'Not flagged') if data else 'Ready when you are'
    result_class = ('bad' if detection['malicious'] else 'good') if data else ''
    result_icon = ('!' if detection['malicious'] else '✓') if data else '→'
    payload = data['normalized'] if data else text
    payload_label = 'Normalized input' if data else 'Input preview'
    return BASE + f'<div data-run="{esc(data.get("run_id", 0) if data else 0)}" class="card {"ml" if not is_rule else ""} {"playing" if playing else ""}" style="--delay:{"1.95s" if playing else "0s"}"><div class="top"><span class="label">{"Rule-based engine" if is_rule else "Machine learning engine"}</span><span class="badge">{"Analysis complete" if data else "Interactive simulation"}</span></div><div class="scene"><div class="flow">{stages}</div><div class="query"><div class="label">{payload_label}</div><code>{esc(payload[:200]) or "Enter some text to begin"}</code></div></div><div class="work">{body}</div><div class="verdict {result_class}"><span class="result-icon" aria-hidden="true">{result_icon}</span><div><strong>{verdict}</strong><p>{esc(evidence)}</p></div></div></div>'

def benchmark(report):
    rows = ''
    for key,label in [('accuracy','Accuracy'),('precision','Precision'),('recall','Recall'),('f1','F1 score'),('false_positive_rate','False alarms')]:
        bars = ''.join(f'<div class="bar-row"><span class="method">{"Rules" if method == "rule_based" else "ML"}</span><div class="track"><i class="{method}" style="width:{report[method][key]*100:.4f}%"></i></div><b>{report[method][key]*100:.1f}%</b></div>' for method in ['rule_based','ml_based'])
        rows += f'<div class="benchmark-row"><div class="metric-label">{label}<small>{"Lower is better" if key == "false_positive_rate" else "Higher is better"}</small></div><div class="bar-pair">{bars}</div></div>'
    return BASE + '''<style>.benchmark{padding:22px 24px}.benchmark-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.benchmark-head strong{font-size:18px;letter-spacing:-.5px}.legend{font-size:12px;color:#596b80;display:flex;gap:14px}.legend span:before{content:'';display:inline-block;width:8px;height:8px;background:#285ad6;border-radius:50%;margin-right:6px}.legend span:last-child:before{background:#7650b9}.benchmark-row{display:grid;grid-template-columns:140px 1fr;gap:24px;padding:15px 0;border-top:1px solid #edf0f5}.metric-label{font-size:14px;font-weight:600}.metric-label small{display:block;font-size:12px;font-weight:400;color:#596b80;margin-top:3px}.bar-row{display:flex;gap:10px;align-items:center}.bar-row+.bar-row{margin-top:7px}.method{width:34px;color:#596b80;font-size:12px}.track{flex:1;background:#f0f3f8;height:7px;border-radius:6px;overflow:hidden}.track i{display:block;height:100%;border-radius:6px}.rule_based{background:#285ad6}.ml_based{background:#7650b9}.bar-row b{font-size:12px;width:47px;text-align:right;font-weight:600}.bench-note{font-size:12px;color:#596b80;margin:16px 0 0}@media(max-width:540px){.benchmark{padding:20px 16px}.benchmark-row{grid-template-columns:100px 1fr;gap:12px}.metric-label{font-size:13px}.metric-label small{font-size:11px}.method{display:none}.bar-row{gap:6px}.benchmark-head strong{font-size:17px}}</style>''' + f'<div class="card benchmark"><div class="benchmark-head"><strong>How they performed</strong><div class="legend"><span>Rules</span><span>ML</span></div></div>{rows}<p class="bench-note">{report["split_counts"]["test"]} synthetic test inputs · {report["test_families"]} held-out families. Real-world results may differ.</p></div>'
