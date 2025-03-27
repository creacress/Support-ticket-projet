from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base
import enum
from datetime import datetime

class RoleEnum(str, enum.Enum):
    employe = "Employé"
    technicien = "Technicien"
    admin = "Admin"

class StatutEnum(str, enum.Enum):
    ouvert = "Ouvert"
    en_cours = "En cours"
    resolu = "Résolu"
    ferme = "Fermé"

class PrioriteEnum(str, enum.Enum):
    faible = "Faible"
    moyenne = "Moyenne"
    elevee = "Élevée"
    critique = "Critique"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    mot_de_passe = Column(String)
    role = Column(Enum(RoleEnum))
    date_inscription = Column(DateTime, default=datetime.utcnow)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    titre = Column(String)
    description = Column(String)
    statut = Column(Enum(StatutEnum), default=StatutEnum.ouvert)
    priorite = Column(Enum(PrioriteEnum), default=PrioriteEnum.moyenne)
    date_creation = Column(DateTime, default=datetime.utcnow)
    date_mise_a_jour = Column(DateTime, default=datetime.utcnow)
    id_employe = Column(Integer, ForeignKey("users.id"))
    id_technicien = Column(Integer, ForeignKey("users.id"), nullable=True)

class Commentaire(Base):
    __tablename__ = "commentaires"
    id = Column(Integer, primary_key=True, index=True)
    contenu = Column(String)
    date_creation = Column(DateTime, default=datetime.utcnow)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    auteur_id = Column(Integer, ForeignKey("users.id"))

    ticket = relationship("Ticket", backref="commentaires")
    auteur = relationship("User")
