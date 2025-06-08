from datetime import datetime, timezone
from app.db.user_repository import add_term_to_history, save_daily_concept, get_user_by_id
from app.services.generate_specific_concept import generate_specific_concept


async def get_daily_concept_service(user_id: str, category: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    daily = user.daily or {}
    if today in daily:
        return daily[today]

    history = user.history or {}
    seen_terms = history.get(category, [])

    result = generate_specific_concept(category, seen_terms)
    
    await add_term_to_history(user_id, category, result["term"])
    await save_daily_concept(user_id, category, result["term"], result["explanation"])

    return {
        "category": category,
        "term": result["term"],
        "explanation": result["explanation"]
    }
