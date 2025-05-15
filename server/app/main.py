from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.daily_concept import router as concept_router  
from app.api.user_routes import router as user_router



app = FastAPI()
app.include_router(concept_router)
app.include_router(user_router)


# Enable CORS so the frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
