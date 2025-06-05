from datetime import datetime, timezone
from app.db.user_repository import add_term_to_history, save_daily_concept, get_user_by_id
from app.services.generate_specific_concept import generate_specific_concept

async def get_daily_concept_service(user_id: str, category: str):
    user = await get_user_by_id(user_id)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

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