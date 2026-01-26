from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# ------------------------------
# Base class for note schemas
# ------------------------------
class NoteBase(BaseModel):
    """
    Base model for Note, shared between create, update, and output schemas.

    This base class includes common fields for both creating, updating, and reading note data.
    
    Attributes:
        title (str): The title of the note.
        content (str): The content or body of the note.
    """
    title: str
    content: str

class NoteCreate(NoteBase):
    """
    Schema for creating a new note.

    This schema inherits from `NoteBase` and is used for validating the data 
    that is sent when creating a new note via an API request.

    No additional fields are required, and it utilizes the base fields for validation.
    """
    pass

class NoteUpdate(NoteBase):
    """
    Schema for updating an existing note.

    This schema inherits from `NoteBase` and is used for validating the data
    sent when updating an existing note. Like `NoteCreate`, it shares the base fields,
    allowing partial updates to the note's title or content.
    
    In a full implementation, this could also include optional fields to indicate
    which parts of the note are being updated (though in this case it's the same as `NoteBase`).
    """
    pass

class NoteOut(NoteBase):
    """
    Schema for reading a note (output schema).

    This schema is used when retrieving a note from the database to send to the client.
    In addition to the fields from `NoteBase`, it includes the `id` (unique identifier), 
    `created_at` (timestamp of creation), and `updated_at` (timestamp of last update).
    
    Attributes:
        id (int): The unique identifier for the note.
        created_at (datetime): The timestamp when the note was created.
        updated_at (datetime): The timestamp when the note was last updated.
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """
        Configuration for the schema's behavior.

        `orm_mode` is set to `True` to allow the schema to work seamlessly with ORM models (e.g., SQLAlchemy).
        This enables the model to convert database records into Pydantic models.
        """
        orm_mode = True
