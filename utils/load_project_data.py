import json
import os

def load_project_data(path=None):
    """Load project data fetched from the Open Cosmos API."""
    if path is None:
        path = os.path.join(os.path.dirname(__file__), '..', 'project_data.json')
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {path} not found. Run fetch_project_data.py first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: {path} is not valid JSON.")
        return None
