import chromadb
from chromadb.utils import embedding_functions
from llm_router import get_llm_response

CHROMA_DIR = 'chroma_db'
COLLECTION_NAME = 'fda_guidance'
TOP_K = 6

SYSTEM_PROMPT = """You are a regulatory intelligence assistant for life sciences professionals.
You have access to a curated corpus of regulatory documents including:
- FDA guidance on AI/ML SaMD, CDx, cybersecurity, PCCP, De Novo, and 510(k)
- EU AI Act (Regulation EU 2024/1689)
- ISO 42001 AI Management Systems standard
- NIST AI Risk Management Framework 1.0
- ICH E6(R3) Good Clinical Practice

CRITICAL INSTRUCTION: Answer using ONLY the context passages provided below.

When multiple frameworks appear in the context (e.g. ISO 42001 and NIST AI RMF together):
- Treat this as cross-framework convergence — explain how the frameworks align or complement each other
- Clearly label which requirement comes from which standard
- Note where frameworks reference or reinforce each other
- This multi-framework view is valuable for regulated life sciences contexts

Rules:
1. Read ALL context passages carefully before answering
2. Cite the exact source document and page for every claim
3. Clearly distinguish between different regulatory frameworks in your answer
4. If the context truly does not contain the answer, say so clearly
5. Never add information beyond what the context passages contain
6. Flag uncertain answers with [LOW CONFIDENCE]
7. Always end with: HUMAN REVIEW REQUIRED for any regulatory decision."""

DOCUMENT_KEYWORDS = {
    'iso 42001': 'iso_42001_standard_ocr.pdf',
    'iso42001': 'iso_42001_standard_ocr.pdf',
    'eu ai act': 'eu_ai_act_regulation_2024_1689.pdf',
    'eu artificial intelligence act': 'eu_ai_act_regulation_2024_1689.pdf',
    'regulation 2024/1689': 'eu_ai_act_regulation_2024_1689.pdf',
    'annex iii': 'eu_ai_act_regulation_2024_1689.pdf',
    'nist': 'nist_ai_rmf_1_0_2023.pdf',
    'ich e6': 'ich_e6_r3_good_clinical_practice_2023.pdf',
    'companion diagnostic': 'fda_companion_diagnostic_devices_2014.pdf',
    'pccp': 'fda_pccp_marketing_submission_recommendations_2024.pdf',
    'predetermined change control': 'fda_pccp_marketing_submission_recommendations_2024.pdf',
    'de novo': 'fda_de_novo_classification_2021.pdf',
    'cybersecurity': 'fda_cybersecurity_premarket_submissions_2025.pdf',
    '510k': 'fda_510k_substantial_equivalence_2014.pdf',
    'substantial equivalence': 'fda_510k_substantial_equivalence_2014.pdf',
}

def get_targeted_chunks(collection, question: str, embed_fn):
    question_lower = question.lower()
    target_source = None
    for keyword, source in DOCUMENT_KEYWORDS.items():
        if keyword in question_lower:
            target_source = source
            break
    if target_source:
        try:
            targeted = collection.query(
                query_texts=[question],
                n_results=4,
                where={'source': target_source}
            )
            general = collection.query(
                query_texts=[question],
                n_results=2
            )
            chunks = targeted['documents'][0] + general['documents'][0]
            metas = targeted['metadatas'][0] + general['metadatas'][0]
            return chunks, metas
        except:
            pass
    results = collection.query(query_texts=[question], n_results=TOP_K)
    return results['documents'][0], results['metadatas'][0]

def query_rag(question: str) -> dict:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_collection(
        name=COLLECTION_NAME, embedding_function=embed_fn
    )
    chunks, metadatas = get_targeted_chunks(collection, question, embed_fn)
    context = ''
    sources = []
    for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
        context += f'\n[Source {i+1}: {meta["source"]}, Page {meta["page"]}]\n{chunk}\n'
        source_ref = f'{meta["source"]} (page {meta["page"]})'
        if source_ref not in sources:
            sources.append(source_ref)
    prompt = f'{SYSTEM_PROMPT}\n\nCONTEXT PASSAGES:\n{context}\n\nQUESTION: {question}\n\nAnswer using the context passages above:'
    response = get_llm_response(prompt, provider='anthropic')
    return {'response': response, 'sources': sources, 'chunks_retrieved': len(chunks)}
