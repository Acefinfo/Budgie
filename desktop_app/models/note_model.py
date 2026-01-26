from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class Note:
    id: Optional[int]
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Note":
        # Safe parsing of datetimes if backend returns ISO strings
        def parse_dt(v):
            if not v:
                return None
            try:
                # if backend returns ISO format
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except Exception:
                return v
        
        return Note(
            id=data.get("id"),
            title=data.get("title", ""),
            content=data.get("content", ""),
            created_at=parse_dt(data.get("created_at")),
            updated_at=parse_dt(data.get("updated_at")),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
        }

            