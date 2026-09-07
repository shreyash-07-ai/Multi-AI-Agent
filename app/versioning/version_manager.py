import json
from pathlib import Path
from datetime import datetime
from app.config import DATA_DIR

STATE = DATA_DIR / "versions.json"

def _load():
    if not STATE.exists():
        return {}
    return json.loads(STATE.read_text(encoding="utf-8"))

def save_version(session_id, artifacts, trace):
    data = _load()
    history = data.setdefault(session_id, [])
    version = len(history) + 1
    record = {
        "version": version,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "artifacts": artifacts,
        "trace": trace,
    }
    history.append(record)
    STATE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return version

def get_versions(session_id):
    return _load().get(session_id, [])
