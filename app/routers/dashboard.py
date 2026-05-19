from fastapi import APIRouter

router = APIRouter()

@router.get('/summary')
async def summary():
    return {"message": "Dashboard summary endpoint pronto para agregações."}
