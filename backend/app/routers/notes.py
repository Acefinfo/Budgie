from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.notes import Note as NoteModel
from app.schemas.notes import NoteCreate, NoteOut
from app.core.deps import get_db
from app.core.security import get_current_user

# Create an instance of the FastAPI APIRouter
router = APIRouter()

# ------------------------------
# GET /notes/ - list notes
# ------------------------------
@router.get("/", response_model=List[NoteOut])
def list_notes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Retrieve all notes belonging to the currently authenticated user.

    Args:
        db (Session): SQLAlchemy session dependency.
        current_user (User): Authenticated user object, provided by `get_current_user`.

    Returns:
        List[NoteOut]: List of all notes associated with the user.
    """
    notes = db.query(NoteModel).filter(NoteModel.user_id == current_user.id).order_by(NoteModel.created_at.desc()).all()
    return notes


# ------------------------------
# POST /notes/ - create note
# ------------------------------
@router.post("/", response_model=NoteOut)
def create_note(note_in: NoteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Create a new note for the currently logged-in user.

    Args:
        note_in (NoteCreate): Pydantic model containing title and content.
        db (Session): SQLAlchemy session dependency.
        current_user (User): Authenticated user object.

    Returns:
        NoteOut: The newly created note record.
    """
    note = NoteModel(
        title=note_in.title,
        content=note_in.content,
        user_id=current_user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


# ------------------------------
# PUT /notes/{note_id} - update note
# ------------------------------
@router.put("/{note_id}", response_model=NoteOut)
def update_note(note_id: int, note_in: NoteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Update an existing note. Only the owner can modify their own note.

    Args:
        note_id (int): ID of the note to update.
        note_in (NoteCreate): Updated title and content.
        db (Session): Database session.
        current_user (User): The logged-in user.

    Returns:
        NoteOut: The updated note details.

    Raises:
        HTTPException: 404 if the note does not exist or doesn’t belong to the current user.
    """
    note = db.query(NoteModel).filter(
        NoteModel.id == note_id,
        NoteModel.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note.title = note_in.title
    note.content = note_in.content
    db.commit()
    db.refresh(note)
    return note


# ------------------------------
# DELETE /notes/{note_id} - delete note
# ------------------------------
@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    """
    Delete a note that belongs to the current user.

    Args:
        note_id (int): ID of the note to delete.
        db (Session): Database session.
        current_user (User): Authenticated user.

    Returns:
        None: Returns HTTP 204 No Content if successful.

    Raises:
        HTTPException: 404 if note not found or doesn’t belong to user.
    """
    note = db.query(NoteModel).filter(
        NoteModel.id == note_id,
        NoteModel.user_id == current_user.id
    ).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return
