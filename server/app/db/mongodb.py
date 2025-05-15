from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Read MongoDB URI and DB name
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB", "one_concept_a_day")

# Initialize MongoDB client
client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
