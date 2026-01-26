import requests
from typing import List
from models.note_model import Note

try:
    from services.expense_api_service import BASE_URL,get_headers
except Exception:
    from services.expense_api_service import BASE_URL, get_headers

NOTES_ENDPOINT = f"{BASE_URL.rstrip('/')}/notes"

def get_notes() -> List[Note]:
    response = requests.get(
        f"{NOTES_ENDPOINT}/",headers=get_headers()
    )
    response.raise_for_status()
    data = response.json()
    return [Note.from_dict(item) for item in data]

def create_note(title: str, content: str) -> Note:
    payload = {"title": title, "content": content}
    resp = requests.post(f"{NOTES_ENDPOINT}/", json=payload, headers=get_headers())
    resp.raise_for_status()
    return Note.from_dict(resp.json())

def update_note(note_id: int, title: str, content: str) -> Note:
    payload = {"title": title, "content": content}
    resp = requests.put(f"{NOTES_ENDPOINT}/{note_id}", json=payload, headers=get_headers())
    resp.raise_for_status()
    return Note.from_dict(resp.json())

def delete_note(note_id: int) -> bool:
    resp = requests.delete(f"{NOTES_ENDPOINT}/{note_id}", headers=get_headers())
    if resp.status_code in (200, 204):
        return True
    # raise for unexpected error
    resp.raise_for_status()
    return False