from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database, auth
from typing import List
from datetime import datetime

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=schemas.Commentaire)
def add_comment(comment: schemas.CommentaireCreate, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_active_user)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == comment.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")
    
    new_comment = models.Commentaire(
        contenu=comment.contenu,
        ticket_id=comment.ticket_id,
        auteur_id=current_user.id,
        date_creation=datetime.utcnow()
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/ticket/{ticket_id}", response_model=List[schemas.Commentaire])
def get_comments(ticket_id: int, db: Session = Depends(database.SessionLocal), current_user: models.User = Depends(auth.get_current_active_user)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")
    
    return db.query(models.Commentaire).filter(models.Commentaire.ticket_id == ticket_id).all()
