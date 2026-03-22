# Regulatory Intelligence Assistant

**AI-powered regulatory intelligence for life sciences professionals — query FDA guidance documents, EU AI Act, ISO 42001, NIST AI RMF, and ICH guidelines with source citations and a governance framework designed for regulated environments.**

## Business Problem

Regulatory affairs professionals, clinical development teams, and AI strategy leaders at pharmaceutical and medical device companies spend significant time manually searching regulatory guidance documents. This tool enables natural language querying across 17 regulatory documents with source-cited, governed responses — and surfaces cross-framework insights across FDA, EU, ISO, and NIST simultaneously.

## What This Tool Does

- Answers regulatory questions across 17 documents covering FDA AI/ML SaMD, CDx, cybersecurity, EU AI Act, ISO 42001, NIST AI RMF, and ICH GCP
- Returns responses with exact source document citations and page references
- Intelligently routes queries to the most relevant document corpus
- Surfaces cross-framework alignment between regulatory standards
- Flags low-confidence answers and requires human review for all regulatory decisions
- Logs every query and response with timestamp and session ID for audit trail

## Document Coverage

**FDA AI/ML and SaMD:** AI/ML Action Plan 2021, PCCP Marketing Submission Recommendations 2024, PCCP Guiding Principles 2023, SaMD Clinical Evaluation 2017, AI in Drug and Biological Products 2025

**FDA Medical Devices:** 510(k) Substantial Equivalence 2014, De Novo Classification 2021, Multiple Function Device Products 2022, Clinical Decision Support Software 2022, Cybersecurity Premarket Submissions 2025, Cybersecurity Postmarket 2016

**FDA Diagnostics:** Companion Diagnostic Devices Guidance 2014

**EU Regulation:** EU AI Act Regulation 2024/1689

**International Standards:** ISO 42001 AI Management Systems 2023, NIST AI RMF 1.0 2023

**Clinical Research:** ICH E6(R3) Good Clinical Practice 2023

## Demo Questions

1. `What is a Predetermined Change Control Plan for AI/ML SaMD and what are its three components?`
2. `How do ISO 42001 and NIST AI RMF align on AI risk management requirements?`
3. `What are the FDA requirements for companion diagnostic devices and contemporaneous approval?`
4. `What cybersecurity requirements does FDA expect in premarket submissions for AI-enabled medical devices?`
5. `What does the EU AI Act require for transparency of high-risk AI systems?`

## Architecture

Data flow: Regulatory PDFs → PyPDF text extraction → RecursiveCharacterTextSplitter 800-token chunks → ChromaDB vector store 3325 chunks → Intelligent document routing → Anthropic Claude Haiku with governance system prompt → Cited response and audit log entry

## Governance Framework

This project includes a full governance memo in GOVERNANCE.md covering intended use, data sources, known limitations, hallucination risk controls, human review requirements, audit logging design, and regulatory context mapping across EU AI Act, FDA SaMD, HIPAA, and ISO 42001. The governance architecture was designed before the code was written.

## Setup and Installation

**1. Clone the repository**
```bash
git clone https://github.com/AshishYadav165/regulatory-intelligence-assistant.git
cd regulatory-intelligence-assistant
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv && source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
cp .env.example .env
```
Add your API keys to .env

**5. Download regulatory documents into /docs folder**

**6. Ingest documents**
```bash
python ingest.py
```

**7. Launch the application**
```bash
python -m streamlit run app.py
```

## Technology Stack

- **LLM:** Anthropic Claude Haiku — selected for document comprehension accuracy in regulated contexts
- **Vector database:** ChromaDB with sentence transformer embeddings
- **Document processing:** LangChain and PyPDF
- **Interface:** Streamlit
- **Audit logging:** JSON Lines format with SHA-256 response hashing
- **Query routing:** Keyword-based document targeting with semantic fallback

## Regulatory Context

- **EU AI Act:** likely limited-risk classification — transparency obligations apply
- **FDA:** does not meet the definition of a medical device under current scope
- **HIPAA:** no protected health information is processed
- **ISO 42001:** governance design aligned with AI management system requirements

## Known Limitations

- Coverage limited to 17 indexed documents — does not include EMA or PMDA guidance
- Documents reflect versions indexed at setup — verify currency with original sources
- Not a substitute for qualified regulatory affairs counsel

## Author

**Ashish Yadav** | Senior Life Sciences Executive | AI Strategy and Governance | PrecisionPulse Consulting LLC

Dual ISO Lead Auditor: ISO 42001 (AI Management Systems) + ISO 13485 (Medical Devices QMS)
