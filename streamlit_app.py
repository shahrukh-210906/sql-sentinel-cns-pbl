"""Streamlit UI for the trained SQL injection comparison."""
import html
import json
import re
from pathlib import Path
import pandas as pd
import streamlit as st
from detector import RULES,normalize,rule_detect
from trained_model import TrainedDetector

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='SQL Sentinel',page_icon='🔎',layout='wide',initial_sidebar_state='expanded')
st.markdown('''<style>
.stApp{background:#f7f8fc;color:#19253b} .block-container{max-width:1200px;padding-top:2rem;padding-bottom:1rem}
h1{letter-spacing:-1.5px!important;font-weight:650!important}h3{font-size:1.15rem!important}
[data-testid="stSidebar"]{background:white;border-right:1px solid #e2e7ef}
[data-baseweb="tab-list"]{gap:10px;background:#edf1f8;padding:6px;border-radius:12px}
button[data-baseweb="tab"]{padding:12px 24px;border-radius:8px;min-height:48px}
button[data-baseweb="tab"][aria-selected="true"]{background:white;color:#315fe7}
[data-baseweb="tab-highlight"]{display:none}
.stButton button{border-radius:9px;min-height:44px}textarea{font-family:Consolas,monospace!important}
[data-testid="stMetric"]{background:white;border:1px solid #e2e7ef;border-radius:12px;padding:16px}
</style>''',unsafe_allow_html=True)

@st.cache_resource
def model():
    return TrainedDetector()

@st.cache_data
def metrics():
    return json.loads((ROOT/'results/trained_metrics.json').read_text(encoding='utf-8'))

if not (ROOT/'models/sql_detector.joblib').exists():
    st.error('Train the model first: python train_model.py')
    st.stop()

CASES={
 'Login bypass':("admin' OR 1=1 --",'OR 1=1 tries to make a login condition always true.'),
 'Normal username':('alex','An ordinary username.'),
 'Encoded attack':("admin%27%20OR%201%3D1%20--",'Decoding reveals the hidden punctuation.'),
 'Boolean keyword':("guest' OR TRUE --",'A Boolean keyword can change query logic.'),
 'Benign SQL lesson':('SQL textbook: UNION SELECT combines rows alex0','SQL terminology can also be legitimate text.'),
 'Custom input':('','Input is inspected as text, never executed.')}

def clear_result():
    st.session_state.pop('analysis',None)

def change_example():
    st.session_state['payload']=CASES[st.session_state['example']][0]
    clear_result()

with st.sidebar:
    st.markdown('### SQL Sentinel')
    st.caption('CNS · PROJECT 76')
    st.selectbox('Example',list(CASES),key='example',on_change=change_example)
    if 'payload' not in st.session_state: st.session_state['payload']=CASES['Login bypass'][0]
    text=st.text_area('User input',key='payload',height=160,max_chars=4000,on_change=clear_result)
    animate=st.toggle('Animate the steps',value=True)
    st.caption(CASES[st.session_state['example']][1])
    st.divider()
    st.caption('Text inspection only. No SQL is executed.')

st.title('One input. Two perspectives.')
st.caption('A trained ML model and a rule checklist. Explore, then compare.')
rule_tab,ml_tab,compare_tab=st.tabs(['Rule-based','ML-based','Comparison'])

def analyze():
    text=st.session_state['payload']
    if not text.strip():
        st.warning('Enter an input first.')
        return
    normalized=normalize(text)
    rule_input=re.sub(r'/\*.*?\*/',' ',normalized)
    st.session_state['analysis']=dict(text=text,normalized=normalized,
        rule_based=rule_detect(text),ml_based=model().predict(text),
        checks=[dict(name=name,matched=bool(re.search(pattern,rule_input))) for name,pattern in RULES])

def animation(kind,data):
    # All user/model strings are escaped before inclusion in HTML.
    esc=lambda value:html.escape(str(value))
    duration='3s' if animate and data else '0s'
    names=['Input','Decode','Check rules'] if kind=='rules' else ['Input','Character patterns','Learned score']
    stages=''.join(f'<div class="node n{i}"><span>{i+1:02d}</span><b>{esc(name)}</b></div>'+
                   ('<div class="wire"><i></i></div>' if i<2 else '') for i,name in enumerate(names))
    if data:
        if kind=='rules':
            body='<div class="checks">'+''.join(f'<div class="check" style="--i:{i}"><span>{esc(c["name"])}</span><b class="'+
                ('bad' if c['matched'] else 'good')+'">'+('Match' if c['matched'] else 'No match')+'</b></div>'
                for i,c in enumerate(data['checks']))+'</div>'
            detection=data['rule_based']
            evidence=' · '.join(detection['reasons'])
        else:
            detection=data['ml_based']
            features=detection['features']
            body='<div class="tag">LEARNED FEATURE CONTRIBUTIONS</div><div class="chips">'+''.join(
                f'<span class="chip" style="--i:{i}">{esc(f["token"].replace(" ","␣"))}<small>{f["contribution"]:+.2f}</small></span>'
                for i,f in enumerate(features))+'</div>'
            body+=f'<div class="score"><span>Attack score · uncalibrated</span><b>{detection["score"]*100:.1f}%</b></div><div class="meter"><i style="--score:{detection["score"]}"></i><div class="threshold"></div></div><div class="labels"><span>0%</span><span>50% decision threshold</span><span>100%</span></div>'
            evidence='Character TF-IDF + Logistic Regression'
        verdict='Suspicious input' if detection['malicious'] else 'Not flagged'
        verdict_class='bad' if detection['malicious'] else 'good'
        payload=data['normalized'][:200]
        ending=f'<div class="verdict {verdict_class}"><strong>{verdict}</strong><p>{esc(evidence)}</p></div>'
    else:
        body='<div class="empty">Run the detector to reveal its evidence.</div>'
        payload=text[:200]
        ending='<div class="verdict"><strong>Ready to analyze</strong></div>'
    css=f'''
    <style>*{{box-sizing:border-box}}body{{margin:0;font:14px/1.6 system-ui;color:#19253b;background:#f7f8fc}}
    .card{{border:1px solid #dfe5ef;border-radius:14px;background:white;overflow:hidden;--delay:{duration}}}
    .scene{{padding:24px;background:linear-gradient(#315fe705 1px,transparent 1px),linear-gradient(90deg,#315fe705 1px,transparent 1px);background-size:24px 24px}}
    .flow{{display:grid;grid-template-columns:1fr 28px 1fr 28px 1fr;align-items:center}}.node{{padding:15px 6px;border:1px solid #dfe5ef;border-radius:9px;text-align:center;background:white}}
    .node span{{display:block;font-size:20px;color:{'#315fe7' if kind=='rules' else '#8159d7'}}}.node b{{font-size:11px;display:block;font-weight:600}}
    .node{{animation:pulse 1s 1}}.n1{{animation-delay:1s}}.n2{{animation-delay:2s}}@keyframes pulse{{50%{{background:#eef3ff;box-shadow:0 0 0 4px #315fe711;transform:translateY(-3px)}}}}
    .wire{{height:2px;background:#d9e2f4;position:relative}}.wire i{{height:8px;width:15px;background:#315fe7;border-radius:3px;position:absolute;top:-3px;animation:packet 1s 3}}@keyframes packet{{from{{left:0;opacity:0}}30%{{opacity:1}}to{{left:100%;opacity:0}}}}
    code{{display:block;padding:12px;margin-top:20px;border:1px solid #e2e7ef;border-radius:7px;background:#fff;color:#315fe7;overflow-wrap:anywhere;font-size:12px}}
    .work{{padding:22px}}.checks{{display:grid;grid-template-columns:1fr 1fr;gap:8px}}.check{{border:1px solid #e0e7f1;border-radius:7px;padding:10px 12px;display:flex;justify-content:space-between;gap:8px;font-size:11px;animation:enter .3s both;animation-delay:calc(var(--delay) + var(--i)*.07s)}}
    .bad{{color:#b82f50}}.good{{color:#14734b}}.check b{{font-size:10px}}.tag{{font-size:10px;color:#617087;letter-spacing:1px}}
    .chips{{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0 24px;min-height:55px}}.chip{{border:1px solid #dfd4f4;border-radius:7px;background:#f6f0ff;padding:7px 12px;font:13px monospace;color:#8159d7;animation:enter .3s both;animation-delay:calc(var(--delay) + var(--i)*.1s)}}.chip small{{display:block;font-size:10px;margin-top:4px}}
    @keyframes enter{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}.score{{display:flex;justify-content:space-between;font-size:12px;color:#617087}}.score b{{font-size:21px;color:#8159d7}}
    .meter{{height:8px;background:#ede6fa;border-radius:9px;margin-top:8px;position:relative}}.meter i{{height:100%;display:block;background:#8159d7;border-radius:9px;transform-origin:left;transform:scaleX(var(--score));animation:fill .8s both;animation-delay:var(--delay)}}@keyframes fill{{from{{transform:scaleX(0)}}to{{transform:scaleX(var(--score))}}}}.threshold{{position:absolute;left:50%;top:-4px;height:16px;border-left:2px solid #8793a6}}
    .labels{{display:flex;justify-content:space-between;font-size:10px;color:#617087;margin-top:6px}}.verdict{{background:#f8fafd;border-top:1px solid #e1e7f0;padding:18px 24px;animation:enter .4s both;animation-delay:calc(var(--delay) + .6s)}}.verdict strong{{font-size:20px}}.verdict p{{font-size:11px;color:#617087;margin:4px 0 0}}.empty{{padding:30px 0;color:#617087;font-size:13px}}
    @media(max-width:500px){{.scene,.work{{padding:16px}}.checks{{grid-template-columns:1fr}}.node b{{font-size:10px}}}}
    @media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
    {('*{animation:none!important}' if not animate or not data else '')}
    </style>'''
    st.iframe(css+f'<div class="card"><div class="scene"><div class="flow">{stages}</div><code>{esc(payload)}</code></div><div class="work">{body}</div>{ending}</div>',height='content',alt='Animated detector processing steps')

with rule_tab:
    st.subheader('The rule checklist')
    st.caption('Known warning signs → a match raises a warning.')
    st.button('Run Rule-based',key='run_rules',type='primary',on_click=analyze)
    animation('rules',st.session_state.get('analysis'))

with ml_tab:
    st.subheader('The trained pattern detector')
    st.caption('Character patterns → weighted evidence → a learned score.')
    st.button('Run ML-based',key='run_ml',type='primary',on_click=analyze)
    animation('ml',st.session_state.get('analysis'))

with compare_tab:
    st.subheader('Same input. Different methods.')
    st.button('Compare both',key='run_compare',type='primary',on_click=analyze)
    data=st.session_state.get('analysis')
    a,b=st.columns(2)
    for column,name,key in [(a,'Rule-based','rule_based'),(b,'ML-based','ml_based')]:
        with column:
            if data:
                st.metric(name,'Suspicious' if data[key]['malicious'] else 'Not flagged')
            else: st.metric(name,'—')
    if data:
        agree=data['rule_based']['malicious']==data['ml_based']['malicious']
        st.info('Both detectors agree.' if agree else 'The detectors disagree. Different methods can miss attacks or raise false alarms.')
    report=metrics()
    st.caption('FAMILY-SEPARATED SYNTHETIC TEST BENCHMARK')
    table=pd.DataFrame([dict(Metric=label,**{'Rule-based':report['rule_based'][key],
                  'ML-based':report['ml_based'][key]}) for key,label in
                  [('accuracy','Accuracy ↑'),('precision','Precision ↑'),('recall','Recall ↑'),
                   ('f1','F1 ↑'),('false_positive_rate','False-positive rate ↓')]])
    st.dataframe(table.style.format({'Rule-based':'{:.1%}','ML-based':'{:.1%}'}),hide_index=True,width='stretch')
    st.caption(f"Train {report['split_counts']['train']} · Validation {report['split_counts']['validation']} · Test {report['split_counts']['test']} · {report['test_families']} test families")
    with st.expander('Training details & limitations'):
        st.write(report['model'])
        st.write('Model selection uses validation only. Test rows never enter the fitted vocabulary or model weights. Templates differ by split, but related SQL concepts and correlated variants remain.')
        st.write('Authored synthetic data; no independent real-world validation. Higher is better for accuracy, precision, recall and F1. Lower is better for false-positive rate.')
        st.json({key:report[key] for key in ['selected_C','candidates','dataset_sha256','sklearn_version']})
        st.download_button('Download benchmark',json.dumps(report,indent=2),file_name='trained_metrics.json',mime='application/json')
st.caption('Detection can miss attacks. Use parameterized queries to prevent SQL injection.')
