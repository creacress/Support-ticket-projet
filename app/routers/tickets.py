from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from .. import models, schemas, database, auth

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("/", response_model=schemas.Ticket)
def create_ticket(
    ticket: schemas.TicketCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    new_ticket = models.Ticket(
        titre=ticket.titre,
        description=ticket.description,
        priorite=ticket.priorite,
        id_employe=current_user.id
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket


@router.get("/", response_model=List[schemas.Ticket])
def get_all_tickets(
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role == models.RoleEnum.employe:
        return db.query(models.Ticket).filter(models.Ticket.id_employe == current_user.id).all()
    return db.query(models.Ticket).all()


@router.get("/{ticket_id}", response_model=schemas.Ticket)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")
    return ticket


@router.put("/{ticket_id}", response_model=schemas.Ticket)
def update_ticket(
    ticket_id: int,
    updates: schemas.TicketCreate,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    if current_user.role == models.RoleEnum.employe and ticket.id_employe != current_user.id:
        raise HTTPException(status_code=403, detail="Non autorisé à modifier ce ticket")

    ticket.titre = updates.titre
    ticket.description = updates.description
    ticket.priorite = updates.priorite
    ticket.date_mise_a_jour = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return ticket


@router.put("/{ticket_id}/assign")
def assign_ticket(
    ticket_id: int,
    technician_id: int,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Accès admin requis")

    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    ticket.id_technicien = technician_id
    ticket.date_mise_a_jour = datetime.utcnow()
    db.commit()
    return {"message": f"Ticket #{ticket.id} assigné au technicien {technician_id}"}


@router.put("/{ticket_id}/status")
def update_ticket_status(
    ticket_id: int,
    statut: models.StatutEnum,
    db: Session = Depends(database.SessionLocal),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket introuvable")

    if current_user.role == models.RoleEnum.technicien and ticket.id_technicien != current_user.id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez pas modifier ce ticket")

    ticket.statut = statut
    ticket.date_mise_a_jour = datetime.utcnow()
    db.commit()
    return {"message": f"Statut du ticket #{ticket.id} mis à jour à {statut.value}"}
