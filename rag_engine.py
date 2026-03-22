import chromadb
from chromadb.utils import embedding_functions
from llm_router import get_llm_response

CHROMA_DIR = 'chroma_db'
COLLECTION_NAME = 'fda_guidance'
TOP_K = 4

SYSTEM_PROMPT = """You are a regulatory intelligence assistant for life sciences professionals.
You answer questions based ONLY on the FDA guidance documents provided as context.
You must:
1. Only use information from the provided context passages
2. Always cite the source document for every claim
3. If the context does not contain enough information, say so explicitly
4. Never speculate beyond what the documents state
5. Flag any answer where you have low confidence with [LOW CONFIDENCE]
6. End every response with: HUMAN REVIEW REQUIRED for any regulatory decision."""

def query_rag(question: str) -> dict:
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_collection(
        name=COLLECTION_NAME, embedding_function=embed_fn
    )
    results = collection.query(query_texts=[question], n_results=TOP_K)
    chunks = results['documents'][0]
    metadatas = results['metadatas'][0]
    context = ''
    sources = []
    for i, (chunk, meta) in enumerate(zip(chunks, metadatas)):
        context += f'\n[Source {i+1}: {meta["source"]}, Page {meta["page"]}]\n{chunk}\n'
        source_ref = f'{meta["source"]} (page {meta["page"]})'
        if source_ref not in sources:
            sources.append(source_ref)
    prompt = f'{SYSTEM_PROMPT}\n\nCONTEXT:\n{context}\n\nQUESTION: {question}'
    response = get_llm_response(prompt, provider='anthropic')
    return {'response': response, 'sources': sources, 'chunks_retrieved': len(chunks)}
