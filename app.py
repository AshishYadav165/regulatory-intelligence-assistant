import streamlit as st
import uuid
from rag_engine import query_rag
from audit_log import log_query

st.set_page_config(
    page_title='Regulatory Intelligence Assistant',
    page_icon='📋',
    layout='wide'
)

st.title('Regulatory Intelligence Assistant')
st.markdown('**AI-powered Q&A over FDA guidance documents** | Life sciences and regulatory affairs use')

st.warning(
    'GOVERNANCE NOTICE: This tool is for research and regulatory affairs use only. '
    'All outputs must be verified by a qualified regulatory professional before use '
    'in any regulatory submission, labeling decision, or clinical application. '
    'See GOVERNANCE.md for full usage policy.'
)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
if 'history' not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header('Document Coverage')
    st.markdown('**Indexed Documents:**')
    st.markdown('- FDA AI/ML SaMD Action Plan 2021')
    st.markdown('- PCCP Marketing Submission Recommendations 2024')
    st.markdown('- PCCP Guiding Principles FDA/HC/MHRA 2023')
    st.markdown('- Clinical Decision Support Software 2022')
    st.markdown('- Companion Diagnostic Devices 2014')
    st.markdown('- 510(k) Substantial Equivalence 2014')
    st.markdown('- SaMD Clinical Evaluation 2017')
    st.markdown('- De Novo Classification Process 2021')
    st.markdown('- Multiple Function Device Products 2022')
    st.markdown('- Cybersecurity in Medical Devices 2025')
    st.markdown('- EU AI Act 2024')
    st.markdown('- ICH E6(R3) GCP 2023')
    st.markdown('- NIST AI RMF 1.0 2023')
    st.markdown('- ISO 42001 AI Management Systems 2023')
    st.divider()
    st.markdown('**LLM:** Anthropic Claude Haiku')
    st.markdown('**Retrieval:** ChromaDB top-4 chunks')
    st.markdown(f'**Session:** {st.session_state.session_id}')

st.markdown('**Try these questions:**')
col1, col2 = st.columns(2)
with col1:
    if st.button('What is a Predetermined Change Control Plan?'):
        st.session_state.prefill = 'What is a Predetermined Change Control Plan for AI/ML SaMD?'
    if st.button('What are FDA requirements for companion diagnostics?'):
        st.session_state.prefill = 'What are the FDA requirements for companion diagnostic devices?'
with col2:
    if st.button('How does the EU AI Act classify medical AI?'):
        st.session_state.prefill = 'How does the EU AI Act classify AI systems used in medical devices?'
    if st.button('What does ISO 42001 require for AI governance?'):
        st.session_state.prefill = 'What are the key requirements of ISO 42001 for AI management systems?'

prefill = st.session_state.pop('prefill', '')
question = st.text_area('Ask a regulatory question:', value=prefill, height=80,
    placeholder='e.g. What does FDA require for post-market surveillance of AI/ML SaMD?')

if st.button('Submit question', type='primary') and question.strip():
    with st.spinner('Retrieving from regulatory documents...'):
        result = query_rag(question)
        log_query(st.session_state.session_id, question,
                  result['response'], result['sources'], 'anthropic')
        st.session_state.history.append({
            'question': question,
            'response': result['response'],
            'sources': result['sources']
        })

for item in reversed(st.session_state.history):
    with st.expander(f'Q: {item["question"][:80]}...', expanded=True):
        st.markdown(item['response'])
        if item['sources']:
            st.markdown('**Sources cited:**')
            for s in item['sources']:
                st.markdown(f'- {s}')
