import os
import json
import math
from ai_service import _execute_groq_completion, load_prompt_template

MEMORY_FILE = os.path.join(os.path.dirname(__file__), "data", "career_memory.json")

def _load_memory() -> list:
    """Loads stored career artifacts from a local JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_memory(memory_data: list):
    """Saves career artifacts to local storage."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4)

def ingest_career_artifact(doc_id: str, text: str, metadata: dict) -> bool:
    """Ingests a career artifact into local pure-Python storage."""
    try:
        memory = _load_memory()
        # Remove existing if updating
        memory = [item for item in memory if item.get("id") != doc_id]
        
        memory.append({
            "id": doc_id,
            "text": text,
            "metadata": metadata
        })
        _save_memory(memory)
        return True
    except Exception as e:
        print(f"Ingestion Error: {e}")
        return false

def query_career_memory(query_text: str, n_results: int = 3) -> list[dict]:
    """
    Performs keyword & semantic token overlap scoring to retrieve 
    the most relevant career artifacts without relying on native C++ vector libraries.
    """
    memory = _load_memory()
    if not memory:
        return []

    query_tokens = set(query_text.lower().split())
    scored_items = []

    for item in memory:
        doc_text = item.get("text", "")
        doc_tokens = set(doc_text.lower().split())
        
        # Calculate Jaccard token similarity score as a lightweight relevance metric
        intersection = query_tokens.intersection(doc_tokens)
        union = query_tokens.union(doc_tokens)
        score = len(intersection) / len(union) if union else 0.0
        
        # Boost score if title matches keywords
        title = item.get("metadata", {}).get("title", "").lower()
        if any(token in title for token in query_tokens):
            score += 0.5

        scored_items.append((score, item))

    # Sort by relevance score descending
    scored_items.sort(key=lambda x: x[0], reverse=True)

    # Return top N results formatted for RAG context
    results = []
    for score, item in scored_items[:n_results]:
        results.append({
            "content": item.get("text"),
            "metadata": item.get("metadata", {})
        })
    
    return results