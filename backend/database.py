import json
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path(__file__).resolve().parent.parent / "uploads" / "documents.json"


def load_documents() -> List[Dict]:
    if not DATA_FILE.exists():
        return []

    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def save_documents(documents: List[Dict]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(documents, indent=2), encoding="utf-8")
