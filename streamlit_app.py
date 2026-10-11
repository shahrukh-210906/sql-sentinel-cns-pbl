"""Streamlit UI for the trained SQL injection comparison."""
import json
import re
from pathlib import Path
import streamlit as st
from detector import RULES,normalize,rule_detect
from trained_model import TrainedDetector
from visual_ui import simulation, benchmark

ROOT=Path(__file__).resolve().parent
st.set_page_config(page_title='SQL Sentinel',page_icon=':material/shield:',layout='wide',initial_sidebar_state='auto')
st.markdown('<style>'+(ROOT/'ui.css').read_text(encoding='utf-8')+'</style>',unsafe_allow_html=True)

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
    st.markdown('''<div class="brand"><div class="brand-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6l-8-3Z"/><path d="m8 12 3 3 5-6"/></svg></div><div><strong>SQL Sentinel</strong><small>CNS · Project 76</small></div></div>''',unsafe_allow_html=True)
    st.caption('01 / CHOOSE YOUR INPUT')
    st.selectbox('Example',list(CASES),key='example',on_change=change_example)
    if 'payload' not in st.session_state: st.session_state['payload']=CASES['Login bypass'][0]
    text=st.text_area('User input',key='payload',height=140,max_chars=4000,on_change=clear_result)
    animate=st.toggle('Animate the steps',value=True)
    st.caption(CASES[st.session_state['example']][1])
    st.markdown('''<div class="sidebar-foot"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="5" y="10" width="14" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/></svg>Text inspection only · No SQL execution</div>''',unsafe_allow_html=True)

st.markdown('''<div class="hero"><span class="eyebrow">SQL injection lab</span><h1>See what catches the attack.</h1><p>One input. Two detectors. Follow the evidence.</p></div>''',unsafe_allow_html=True)
rule_tab,ml_tab,compare_tab=st.tabs(['Rule-based','ML-based','Comparison'],key='detector_tab',on_change='rerun')

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

def animation(kind, data):
    st.iframe(simulation(kind, data, text, animate, RULES), height='content',
              alt='Animated detector processing steps')


def panel_heading(title, note, button, key):
    heading, action = st.columns([3, 1.6], vertical_alignment='center')
    with heading:
        st.markdown(f'<div class="panel-heading">{title}</div><p class="panel-note">{note}</p>', unsafe_allow_html=True)
    with action:
        st.button(button, key=key, type='primary', on_click=analyze, width='stretch')

with rule_tab:
    panel_heading('Fixed rules. Clear signals.', 'Match a known pattern → flag the input.', 'Run Rule-based', 'run_rules')
    animation('rules',st.session_state.get('analysis'))

with ml_tab:
    panel_heading('Learned patterns. One score.', 'Character features → weighted prediction.', 'Run ML-based', 'run_ml')
    animation('ml',st.session_state.get('analysis'))

with compare_tab:
    panel_heading('Side by side.', 'Compare this input and the test benchmark.', 'Compare both', 'run_compare')
    data=st.session_state.get('analysis')
    a,b=st.columns(2)
    for column,name,key in [(a,'Rule-based','rule_based'),(b,'ML-based','ml_based')]:
        with column:
            if data:
                st.metric(name,'Suspicious' if data[key]['malicious'] else 'Not flagged')
            else: st.metric(name,'—')
    if data:
        agree=data['rule_based']['malicious']==data['ml_based']['malicious']
        st.caption('Both detectors agree on this input.' if agree else 'Different verdicts — inspect each detector’s evidence.')
    report=metrics()
    st.iframe(benchmark(report), height='content', alt='Rule-based and ML-based benchmark comparison')
    with st.expander('Training details & limitations'):
        st.write(report['model'])
        st.write('Model selection uses validation only. Test rows never enter the fitted vocabulary or model weights. Templates differ by split, but related SQL concepts and correlated variants remain.')
        st.write('Authored synthetic data; no independent real-world validation. Higher is better for accuracy, precision, recall and F1. Lower is better for false-positive rate.')
        st.json({key:report[key] for key in ['selected_C','candidates','dataset_sha256','sklearn_version']})
        st.download_button('Download benchmark',json.dumps(report,indent=2),file_name='trained_metrics.json',mime='application/json')
st.caption('Detection can miss attacks. Use parameterized queries to prevent SQL injection.')
