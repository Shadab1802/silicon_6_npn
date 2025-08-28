from fastapi import APIRouter

#creating router instance
router = APIRouter()

@router.get("/users")
def get_users():
    return {"message":"List Of Users"}