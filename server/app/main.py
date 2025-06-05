from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.user_routes import router as user_router
from app.api.daily_concept import router as concept_router

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user_router)
app.include_router(concept_router)
