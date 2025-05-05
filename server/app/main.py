from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from app import ai

app = FastAPI()

# Enable CORS so the frontend can talk to the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root route to check if the API is running
@app.get("/")
def root():
    return {"message": "One Concept a Day – API is running"}

# Endpoint to get a daily concept based on the user's selected category
@app.get("/daily-concept")
def get_concept(category: str = Query(..., description="User's selected topic of interest")):
    concept = ai.generate_concept(category)
    return {
        "category": category,
        "concept": concept
    }
