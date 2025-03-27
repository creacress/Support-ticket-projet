from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .models import RoleEnum, StatutEnum, PrioriteEnum

class UserBase(BaseModel):
    email: str
    nom: str

class UserCreate(UserBase):
    mot_de_passe: str

class User(UserBase):
    id: int
    role: RoleEnum
    date_inscription: datetime

    class Config:
        orm_mode = True

class TicketBase(BaseModel):
    titre: str
    description: str
    priorite: PrioriteEnum

class TicketCreate(TicketBase):
    pass

class Ticket(TicketBase):
    id: int
    statut: StatutEnum
    date_creation: datetime
    date_mise_a_jour: datetime
    id_employe: int
    id_technicien: Optional[int]

    class Config:
        orm_mode = True

class CommentaireBase(BaseModel):
    contenu: str
    ticket_id: int

class CommentaireCreate(CommentaireBase):
    pass

class Commentaire(CommentaireBase):
    id: int
    auteur_id: int
    date_creation: datetime

    class Config:
        orm_mode = True
