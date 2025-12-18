from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from travel_agents import create_travel_plan

app = FastAPI(title="Travel Planning Agentic API")

# CORS (for Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelRequest(BaseModel):
    destination: str
    budget: float
    num_days: int
    interests: List[str]
    travel_style: str

@app.post("/create-plan")
def create_plan(req: TravelRequest):
    return create_travel_plan(
        destination=req.destination,
        budget=req.budget,
        num_days=req.num_days,
        interests=req.interests,
        travel_style=req.travel_style
    )

@app.get("/")
def root():
    return {"status": "Backend running 🚀"}
