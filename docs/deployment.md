# Live deployment

App: https://cryptopbl.streamlit.app/

Repository: https://github.com/shahrukh-210906/sql-sentinel-cns-pbl

Branch: main. Entrypoint: streamlit_app.py. Cloud runtime: Python 3.12.15. Training runtime: Python 3.12.8. Direct dependency versions are pinned in requirements.txt.

Verified on 11 October 2026: app startup, three tabs, trained model attack score and feature explanations, normal username not flagged by both detectors, and frozen benchmark display. Ten local automated checks passed before deployment.

The model is bundled and loaded for inference. No per-visitor training or inference API key is required. GitHub updates trigger Cloud updates. Cloud inputs are processed on the hosted server; do not submit sensitive production data.

Detailed report: Project-Technical-Report.docx. The corresponding Markdown is editable source; the PDF is a readable copy.
