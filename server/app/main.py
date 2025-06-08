import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.user_routes import router as user_router
from app.api.daily_concept import router as concept_router
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.getenv('DEVELOPMENT_URL'),
        os.getenv('DEPLOYMENT_URL'),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(user_router)
app.include_router(concept_router)
