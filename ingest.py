import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = 'docs'
CHROMA_DIR = 'chroma_db'
COLLECTION_NAME = 'fda_guidance'

def ingest_documents():
    print('Starting document ingestion...')
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    embed_fn = embedding_functions.DefaultEmbeddingFunction()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME, embedding_function=embed_fn
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    all_files = os.listdir(DOCS_DIR)
    pdf_files = [f for f in all_files if f.endswith('.pdf')]
    txt_files = [f for f in all_files if f.endswith('.txt')]
    print(f'Found {len(pdf_files)} PDF files and {len(txt_files)} text files')
    for pdf_file in pdf_files:
        path = os.path.join(DOCS_DIR, pdf_file)
        try:
            loader = PyPDFLoader(path)
            pages = loader.load()
            chunks = splitter.split_documents(pages)
            for i, chunk in enumerate(chunks):
                doc_id = f'{pdf_file}_{i}'
                collection.upsert(
                    documents=[chunk.page_content],
                    metadatas=[{'source': pdf_file, 'page': chunk.metadata.get('page', 0)}],
                    ids=[doc_id]
                )
            print(f'  Ingested PDF: {pdf_file} ({len(chunks)} chunks)')
        except Exception as e:
            print(f'  ERROR with {pdf_file}: {e}')
    for txt_file in txt_files:
        path = os.path.join(DOCS_DIR, txt_file)
        try:
            loader = TextLoader(path, encoding='utf-8')
            pages = loader.load()
            chunks = splitter.split_documents(pages)
            for i, chunk in enumerate(chunks):
                doc_id = f'{txt_file}_{i}'
                collection.upsert(
                    documents=[chunk.page_content],
                    metadatas=[{'source': txt_file, 'page': 0}],
                    ids=[doc_id]
                )
            print(f'  Ingested TXT: {txt_file} ({len(chunks)} chunks)')
        except Exception as e:
            print(f'  ERROR with {txt_file}: {e}')
    print(f'Ingestion complete. Total documents in store: {collection.count()}')

if __name__ == '__main__':
    ingest_documents()
