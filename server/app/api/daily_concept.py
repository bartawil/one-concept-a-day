from fastapi import APIRouter, HTTPException, Query, Depends, Request
import time
from collections import defaultdict

from app.services.ai import generate_concept
from app.services.daily_concept_service import get_daily_concept_service
from app.middleware.auth import get_current_user

router = APIRouter()

# Simple rate limiting for public endpoint
rate_limit_storage = defaultdict(list)
RATE_LIMIT_REQUESTS = 5  # 5 requests
RATE_LIMIT_WINDOW = 3600  # per hour (3600 seconds)

def check_rate_limit(request: Request):
    """Simple rate limiting by IP address"""
    client_ip = request.client.host
    current_time = time.time()
    
    # Clean old requests
    rate_limit_storage[client_ip] = [
        req_time for req_time in rate_limit_storage[client_ip]
        if current_time - req_time < RATE_LIMIT_WINDOW
    ]
    
    # Check if over limit
    if len(rate_limit_storage[client_ip]) >= RATE_LIMIT_REQUESTS:
        raise HTTPException(
            status_code=429, 
            detail="Rate limit exceeded: 5 requests per hour. Sign up for unlimited access!"
        )
    
    # Add current request
    rate_limit_storage[client_ip].append(current_time)

@router.get("/get-concept")
def get_concept(category: str = Query(...), request: Request = None):
    check_rate_limit(request)
    concept = generate_concept(category)
    return {"category": category, "concept": concept}


@router.get("/daily-concept")
async def get_specific_concept(
    category: str = Query(...), 
    user_id: str = Query(...),
    current_user: dict = Depends(get_current_user)
):
    # Verify that the user can only access their own data
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
        
    try:
        return await get_daily_concept_service(user_id, category)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
