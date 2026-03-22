# Regulatory Intelligence RAG Assistant

**AI-powered regulatory intelligence for life sciences professionals — query FDA guidance documents with source citations and a governance framework designed for regulated environments.**

## Business Problem
Regulatory affairs professionals, clinical development teams, and AI strategy leaders at pharmaceutical and medical device companies spend significant time manually searching FDA guidance documents to answer regulatory questions — a process that is slow, error-prone, and difficult to audit. This tool enables natural language querying over a curated FDA guidance library with source-cited, governed responses.

## What This Tool Does
•	Answers regulatory questions over 8 FDA guidance documents covering AI/ML in SaMD, CDx, 510(k), and clinical decision support
•	Returns responses with exact source document citations and page references
•	Flags low-confidence answers and requires human review for all regulatory decisions
•	Logs every query and response with timestamp and session ID for audit trail purposes
•	Built on Anthropic Claude Haiku — selected for superior performance on document comprehension tasks in regulated contexts

## Architecture
[Architecture diagram — see /architecture/diagram.png]

Data flow: FDA PDFs → PyPDF text extraction → RecursiveCharacterTextSplitter (800-token chunks) → ChromaDB vector store → Semantic retrieval (top-4 chunks) → Anthropic Claude Haiku with governance system prompt → Cited response + audit log entry

## Governance Framework
This project includes a full governance memo (GOVERNANCE.md) covering intended use, data sources, known limitations, hallucination risk controls, human review requirements, audit logging design, and regulatory context mapping (EU AI Act, FDA SaMD guidance). The governance architecture was designed before the code was written.

See [GOVERNANCE.md](GOVERNANCE.md) for the complete governance policy.

## Demo Questions
•	'What is a Predetermined Change Control Plan for AI/ML SaMD and what does FDA require?'
•	'What are the FDA requirements for companion diagnostic devices co-developed with a therapeutic?'
•	'How does FDA define a medical device versus software that is not a device?'
•	'What post-market surveillance obligations apply to AI/ML-based medical devices?'

## Setup and Installation
1. Clone the repository
git clone https://github.com/yourusername/regulatory-intelligence-assistant.git
cd regulatory-intelligence-assistant
2. Create and activate a virtual environment
python -m venv venv && source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Set up environment variables — copy .env.example to .env and add your API keys
cp .env.example .env
5. Download FDA guidance PDFs into /docs (links in documentation)
6. Ingest documents into the vector store
python ingest.py
7. Launch the application
streamlit run app.py

## Technology Stack
•	LLM: Anthropic Claude Haiku (claude-haiku-4-5) — selected for document comprehension accuracy
•	Vector database: ChromaDB with default sentence transformer embeddings
•	Document processing: LangChain + PyPDF
•	Interface: Streamlit
•	Audit logging: JSON Lines format with SHA-256 response hashing

## Regulatory Context
•	This tool is scoped as a research and regulatory affairs support tool — not a medical device as currently implemented
•	EU AI Act: likely limited-risk classification — transparency obligations apply
•	FDA: does not meet the definition of a medical device under current scope
•	HIPAA: no protected health information is processed

## Known Limitations
•	Coverage limited to 8 FDA guidance documents — does not include EMA, PMDA, or ICH guidelines
•	Guidance documents may not reflect the most recent FDA updates — index date shown in application
•	Performs less accurately on highly technical chemistry, manufacturing, or biostatistics queries
•	Not a substitute for qualified regulatory affairs counsel

## Author
Ashish Yadav | Senior Life Sciences Executive | AI Strategy & Governance | PrecisionPulse Consulting LLC | Dual ISO Lead Auditor: ISO 42001 (AI Management Systems) + ISO 13485 (Medical Devices QMS)
