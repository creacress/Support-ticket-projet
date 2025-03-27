from fastapi import APIRouter

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/")
def get_comments():
    return {"message": "Liste des commentaires"}