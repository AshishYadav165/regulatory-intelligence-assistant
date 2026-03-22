import os, json, hashlib
from datetime import datetime

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

def log_query(session_id: str, query: str, response: str, sources: list, provider: str):
    log_entry = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'session_id': session_id,
        'provider': provider,
        'query': query,
        'response_hash': hashlib.sha256(response.encode()).hexdigest()[:16],
        'sources_cited': sources,
        'response_length_tokens': len(response.split()),
    }
    log_file = os.path.join(LOG_DIR, f'queries_{datetime.utcnow().strftime("%Y%m%d")}.jsonl')
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_entry) + '\n')
