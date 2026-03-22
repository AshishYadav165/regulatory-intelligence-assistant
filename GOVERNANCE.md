# Governance Policy — Regulatory Intelligence RAG Assistant

**Version 1.0 | March 2026 | Ashish Yadav, PrecisionPulse Consulting LLC**

This governance policy was authored before the technical implementation of this tool. Governance architecture is a design-first requirement for any AI system deployed in a regulated life sciences context.

## 1. Purpose and Scope
This tool is designed to help regulatory affairs professionals, clinical development teams, and AI governance leads at pharmaceutical, biotechnology, and medical device companies retrieve and summarize information from FDA guidance documents.

This tool is NOT designed for: clinical decision-making, patient care contexts, replacement of qualified regulatory affairs counsel, use by non-specialist audiences, or use in any context where AI-generated output would directly drive a regulatory, clinical, or commercial decision without human review.

## 2. Intended Users
•	Regulatory affairs professionals with background knowledge of FDA guidance frameworks
•	Clinical development teams researching regulatory requirements for AI/ML-based products
•	AI governance and strategy leads assessing regulatory obligations
•	Research and academic users studying FDA regulatory frameworks

Non-intended users: patients, general public, non-specialist audiences, automated systems using this tool as an upstream input to regulated decisions without human review.

## 3. Data Sources and Provenance
•	All source documents are FDA guidance documents published on FDA.gov — public domain, freely available
•	Documents are static snapshots indexed at the time of setup — they do not auto-update
•	The index date is displayed in the application sidebar
•	Source documents covered: AI/ML in SaMD (2021), SaMD Marketing Submissions (2023 draft), Predetermined Change Control Plan (2024), Clinical Decision Support Software (2022), Companion Diagnostic Devices, 510(k) Substantial Equivalence, Software Not Medical Devices (2019), FDA AI/ML Action Plan (2021)
•	No proprietary, confidential, or personally identifiable information is processed or stored

## 4. Known Limitations
•	Coverage is limited to 8 indexed FDA guidance documents — EMA, PMDA, ICH, and non-FDA regulatory frameworks are not covered
•	The tool cannot determine whether a newer version of a guidance document supersedes the indexed version — users must verify currency with FDA.gov
•	Performance degrades on highly technical queries involving chemistry, manufacturing controls, biostatistics, or clinical trial design
•	The tool does not have access to FDA's internal deliberations, unpublished guidance, or informal regulatory positions
•	Retrieval accuracy depends on the quality of semantic similarity between query and indexed chunks — queries using non-standard terminology may produce poor retrieval

## 5. Hallucination Risk and Controls
Risk: LLMs can generate plausible-sounding but factually incorrect regulatory statements. In a regulatory context, this risk is material.

•	Control 1 — Retrieval-grounded responses: the LLM is instructed to answer ONLY from retrieved document passages, not from general knowledge
•	Control 2 — Mandatory source citation: every substantive claim must be attributed to a specific source document and page
•	Control 3 — Explicit uncertainty flagging: responses where retrieved context is insufficient are flagged with [LOW CONFIDENCE]
•	Control 4 — Human review mandate: every response ends with HUMAN REVIEW REQUIRED to reinforce that AI output is not a final regulatory position
•	Control 5 — Audit logging: all responses are logged with a hash value enabling post-hoc review of any specific output

## 6. Human Review Requirements
Human review by a qualified regulatory professional is required before any output from this tool is used to:
•	Draft, inform, or validate any regulatory submission (510(k), PMA, CDx submission, IND, NDA, BLA)
•	Make labeling or promotional claims about a medical device or drug product
•	Advise on regulatory strategy for a specific product or program
•	Train regulatory or clinical staff
•	Form the basis of a legal or compliance position

## 7. Audit Logging and Traceability
•	Every query and response is logged to a JSON Lines file in the /logs directory
•	Log entries capture: timestamp (UTC), session ID, LLM provider used, query text, SHA-256 hash of response, sources cited, response length in tokens
•	Logs are stored locally and are not transmitted to any external service
•	Log files are named by date: queries_YYYYMMDD.jsonl
•	Retention: logs should be retained for a minimum of 90 days for quality review purposes in production use

## 8. Regulatory Context Analysis

EU AI Act (Regulation 2024/1689):
•	Current scope: research and regulatory affairs support tool — not a medical device or clinical decision support system as implemented
•	Risk classification: likely limited-risk under Article 6 — transparency obligation applies (users must be informed they are interacting with an AI system)
•	If scope expands to clinical decision support or automated regulatory decision-making: reassess for high-risk classification under Annex III

FDA Software as a Medical Device:
•	Current implementation does not meet the definition of a medical device — it does not diagnose, treat, cure, mitigate, or prevent disease
•	Does not qualify as Clinical Decision Support Software under the 21st Century Cures Act in current form
•	Scope expansion to patient-facing outputs or clinical recommendations would require re-evaluation

HIPAA (Health Insurance Portability and Accountability Act):
•	No protected health information (PHI) is processed, stored, or transmitted by this tool
•	HIPAA does not apply to current implementation

ISO 42001:2023 (AI Management Systems):
•	This governance policy reflects the documentation and transparency requirements of ISO 42001
•	Key controls addressed: purpose specification, data provenance, limitation disclosure, human oversight, and traceability

## 9. Responsible Use Principles
•	Transparency: users are always informed they are interacting with an AI system
•	Human oversight: no regulatory decision should be automated without qualified human review
•	Accuracy over completeness: the tool is designed to refuse or flag uncertain answers rather than generate confident-sounding incorrect responses
•	Auditability: every output is traceable through the audit log
•	Iterative improvement: known limitations are documented and the governance policy is updated as the tool evolves

---
Governance policy authored by: Ashish Yadav
Dual ISO Lead Auditor: ISO 42001 (AI Management Systems) + ISO 13485 (Medical Devices QMS)
PrecisionPulse Consulting LLC | Version 1.0 | March 2026
