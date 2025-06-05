from fastapi import APIRouter, Query
from app.services.ai import generate_concept
from app.services.daily_concept_service import get_daily_concept_service

router = APIRouter()

@router.get("/get-concept")
def get_concept(category: str = Query(...)):
    concept = generate_concept(category)
    return {"category": category, "concept": concept}


@router.get("/daily-concept")
async def get_specific_concept(category: str = Query(...), user_id: str = Query(...)):
    return await get_daily_concept_service(user_id, category)
