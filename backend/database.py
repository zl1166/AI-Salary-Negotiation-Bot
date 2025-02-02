import json
import os
from typing import Optional, Dict

DATA_FILE = "negotiation_data.json"

def load_sessions() -> Dict:
    """Load all sessions from file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                # Ensure data is a dictionary
                if isinstance(data, dict):
                    return data
                else:
                    return {}
        return {}
    except Exception as e:
        print(f"Error loading sessions: {str(e)}")
        return {}

def save_session(session_id: str, session_data: Dict) -> None:
    """Save a single session"""
    try:
        sessions = load_sessions()
        
        # Initialize facts if not present
        if "facts" not in session_data:
            session_data["facts"] = {
                "candidate": [],  # List of fact sentences
                "recruiter": []   # List of fact sentences
            }
            
        sessions[session_id] = session_data
        
        # Save to JSON file
        with open(DATA_FILE, "w") as file:
            json.dump(sessions, file, indent=4)
            
        print(f"Successfully saved session {session_id}")
    except Exception as e:
        print(f"Error saving session: {str(e)}")
        raise e

def get_session(session_id: str) -> Optional[Dict]:
    """Get a single session by ID"""
    try:
        sessions = load_sessions()
        return sessions.get(session_id)
    except Exception as e:
        print(f"Error getting session: {str(e)}")
        return None
