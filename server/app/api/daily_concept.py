from fastapi import APIRouter, Query
from app.services.ai import generate_concept

router = APIRouter()

@router.get("/daily-concept")
def get_concept(category: str = Query(..., description="User's selected topic of interest")):
    concept = generate_concept(category)
    return {"category": category, "concept": concept}
