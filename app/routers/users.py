from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from .. import models, schemas, database, auth
from datetime import timedelta

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    
    hashed_pwd = auth.get_password_hash(user.mot_de_passe)
    new_user = models.User(
        nom=user.nom,
        email=user.email,
        mot_de_passe=hashed_pwd,
        role=models.RoleEnum.employe  # par défaut employé
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.SessionLocal)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.mot_de_passe):
        raise HTTPException(status_code=400, detail="Identifiants invalides")
    
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(auth.get_current_active_user)):
    return current_user
