# src/database.py
from typing import List, Dict, Any

# In-memory "database" to store the results of comment analysis
# In a real-world application, you would replace this with a proper database
# like PostgreSQL, MongoDB, or a simple file-based DB like SQLite.
comment_analysis_db: List[Dict[str, Any]] = []

def add_analysis_to_db(analysis_result: Dict[str, Any]):
    """Adds a new analysis result to the in-memory database."""
    comment_analysis_db.append(analysis_result)

def get_all_analyses_from_db() -> List[Dict[str, Any]]:
    """Retrieves all analysis results from the in-memory database."""
    return comment_analysis_db
