from fastapi import APIRouter, Query
from app.services.ai import generate_concept
from app.services.generate_specific_concept import generate_specific_concept
from app.db.user_repository import add_term_to_history, save_daily_concept
from app.db.mongodb import db  # נוודא שזה קיים
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.get("/get-concept")
def get_concept(category: str = Query(...)):
    concept = generate_concept(category)
    return {"category": category, "concept": concept}


@router.get("/daily-concept")
async def get_specific_concept(category: str = Query(...), user_id: str = Query(...)):
    try:
        print(f"Received user_id: {user_id}, category: {category}")
        user = await db["users"].find_one({"_id": ObjectId(user_id)})

        today = datetime.utcnow().strftime("%Y-%m-%d")
        daily = user.get("daily", {})
        if today in daily:
            print("✅ Loaded from cache for today")
            return daily[today]

        seen_terms = user.get("history", {}).get(category, [])
        result = generate_specific_concept(category, seen_terms)
        print(result)

        await add_term_to_history(user_id, category, result["term"])
        await save_daily_concept(user_id, category, result["term"], result["explanation"])

        return {
            "category": category,
            "term": result["term"],
            "explanation": result["explanation"]
        }
    except Exception as e:
        print(f"ERROR: {e}")
        return {"error": str(e)}
