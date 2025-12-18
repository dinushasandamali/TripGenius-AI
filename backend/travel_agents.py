"""
Travel Planning Agentic System - FastAPI Ready Version
Uses .env for Gemini API key
"""

import os
import json
import operator
from typing import TypedDict, List, Annotated, Dict, Any, Optional
from datetime import datetime, timedelta
import requests

from dotenv import load_dotenv
import google.generativeai as genai
from langgraph.graph import StateGraph, END

# =============================================================================
# ENV & GEMINI SETUP
# =============================================================================

load_dotenv()  # Load .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def call_gemini(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

# =============================================================================
# DESTINATION DATABASE
# =============================================================================

# Local fallback data kept for resilience and testing
DESTINATIONS_DB = {
    "paris": {
        "attractions": [
            {"name": "Eiffel Tower", "cost": 30, "duration": 2, "category": "landmark", "description": "Iconic iron tower with city views"},
            {"name": "Louvre Museum", "cost": 22, "duration": 3, "category": "museum", "description": "World-famous art museum (Mona Lisa, classical art)"},
            {"name": "Notre-Dame Cathedral", "cost": 0, "duration": 1.5, "category": "landmark", "description": "Historic Gothic cathedral on Île de la Cité"},
        ],
        "avg_meal_cost": 30,
        "avg_transport_day": 15,
    },
    "tokyo": {
        "attractions": [
            {"name": "Senso-ji Temple", "cost": 0, "duration": 1.5, "category": "landmark", "description": "Ancient Buddhist temple in Asakusa"},
            {"name": "Tsukiji Outer Market", "cost": 10, "duration": 2, "category": "food", "description": "Street food stalls and fresh seafood"},
            {"name": "Tokyo Skytree", "cost": 25, "duration": 2, "category": "landmark", "description": "Observation deck with panoramic city views"},
        ],
        "avg_meal_cost": 20,
        "avg_transport_day": 10,
    },
    "new york": {
        "attractions": [
            {"name": "Central Park", "cost": 0, "duration": 2.5, "category": "nature", "description": "Large urban park with walking paths and lakes"},
            {"name": "Metropolitan Museum of Art", "cost": 30, "duration": 3, "category": "museum", "description": "One of the largest and finest art museums"},
            {"name": "Statue of Liberty & Ellis Island", "cost": 25, "duration": 3, "category": "landmark", "description": "Ferry ride and historic immigration museum"},
        ],
        "avg_meal_cost": 30,
        "avg_transport_day": 15,
    },
    "london": {
        "attractions": [
            {"name": "British Museum", "cost": 0, "duration": 3, "category": "museum", "description": "Free-entry museum with historic artifacts"},
            {"name": "London Eye", "cost": 35, "duration": 1, "category": "activity", "description": "Observation wheel overlooking the Thames"},
            {"name": "Tower of London", "cost": 35, "duration": 2.5, "category": "landmark", "description": "Medieval fortress and Crown Jewels"},
        ],
        "avg_meal_cost": 25,
        "avg_transport_day": 15,
    },
    # Sri Lanka (country-level, budget friendly)
    "sri lanka": {
        "attractions": [
            {"name": "Sigiriya Rock Fortress", "cost": 35, "duration": 3, "category": "landmark", "description": "Ancient rock fortress and UNESCO World Heritage site"},
            {"name": "Temple of the Tooth (Kandy)", "cost": 10, "duration": 2, "category": "cultural", "description": "Sacred Buddhist temple complex in Kandy"},
            {"name": "Ella Nine Arch Bridge", "cost": 0, "duration": 2, "category": "nature", "description": "Scenic railway bridge in the hill country"},
            {"name": "Galle Fort", "cost": 5, "duration": 3, "category": "heritage", "description": "Dutch-era coastal fort and lighthouse"},
        ],
        "avg_meal_cost": 8,
        "avg_transport_day": 5,
    },
    "colombo": {
        "attractions": [
            {"name": "Galle Face Green", "cost": 0, "duration": 2, "category": "nature", "description": "Seafront promenade with street food"},
            {"name": "Gangaramaya Temple", "cost": 3, "duration": 1.5, "category": "cultural", "description": "Modern Buddhist temple and museum"},
            {"name": "Pettah Market", "cost": 0, "duration": 2, "category": "shopping", "description": "Lively local market for textiles and spices"},
        ],
        "avg_meal_cost": 7,
        "avg_transport_day": 4,
    },
    "kandy": {
        "attractions": [
            {"name": "Temple of the Tooth", "cost": 10, "duration": 2, "category": "cultural", "description": "Important Buddhist relic temple by Kandy Lake"},
            {"name": "Royal Botanical Gardens, Peradeniya", "cost": 7, "duration": 2.5, "category": "nature", "description": "Expansive gardens with orchids and palms"},
        ],
        "avg_meal_cost": 7,
        "avg_transport_day": 4,
    },
    "singapore": {
        "attractions": [
            {"name": "Gardens by the Bay", "cost": 20, "duration": 3, "category": "nature", "description": "Supertree Grove and climate-controlled domes"},
            {"name": "Marina Bay Sands SkyPark", "cost": 25, "duration": 1.5, "category": "landmark", "description": "Skydeck overlooking Marina Bay skyline"},
            {"name": "Sentosa Island Beaches", "cost": 0, "duration": 3, "category": "beach", "description": "Resort island with free public beaches"},
        ],
        "avg_meal_cost": 15,
        "avg_transport_day": 8,
    },
    "dubai": {
        "attractions": [
            {"name": "Burj Khalifa At The Top", "cost": 45, "duration": 2, "category": "landmark", "description": "Observation deck in the world’s tallest building"},
            {"name": "Desert Safari with BBQ Dinner", "cost": 60, "duration": 6, "category": "activity", "description": "Dune bashing, camel rides, and buffet dinner"},
            {"name": "Dubai Mall & Fountain Show", "cost": 0, "duration": 3, "category": "shopping", "description": "Indoor mall with evening fountain show"},
        ],
        "avg_meal_cost": 20,
        "avg_transport_day": 12,
    },
    "bali": {
        "attractions": [
            {"name": "Uluwatu Temple & Kecak Dance", "cost": 15, "duration": 3, "category": "cultural", "description": "Clifftop temple with sunset dance performance"},
            {"name": "Tegallalang Rice Terraces", "cost": 5, "duration": 2, "category": "nature", "description": "Iconic terraced rice fields near Ubud"},
            {"name": "Tanah Lot Temple", "cost": 8, "duration": 2, "category": "landmark", "description": "Sea temple famous for sunset views"},
        ],
        "avg_meal_cost": 10,
        "avg_transport_day": 7,
    },
    "rome": {
        "attractions": [
            {"name": "Colosseum & Roman Forum", "cost": 25, "duration": 3, "category": "landmark", "description": "Ancient amphitheater and ruins of Imperial Rome"},
            {"name": "Vatican Museums & Sistine Chapel", "cost": 30, "duration": 3, "category": "museum", "description": "Art collections and Michelangelo’s ceiling"},
            {"name": "Trevi Fountain & Spanish Steps", "cost": 0, "duration": 2, "category": "landmark", "description": "Baroque fountain and famous city steps"},
        ],
        "avg_meal_cost": 20,
        "avg_transport_day": 8,
    },
}

# =============================================================================
# TOOLS
# =============================================================================

class ExternalDestinationAPI:
    """Lightweight client to pull destination data from an external API.

    Expected response shape (can be adapted as needed):
    {
      "destination": "paris",
      "avg_meal_cost": 30,
      "avg_transport_day": 15,
      "attractions": [
        {"name": "...", "cost": 10, "duration": 2, "category": "museum", "description": "..."},
        ...
      ]
    }
    """

    @staticmethod
    def fetch_destination(destination: str) -> Optional[Dict[str, Any]]:
        base_url = os.getenv("DESTINATIONS_API_URL")
        api_key = os.getenv("DESTINATIONS_API_KEY")

        if not base_url:
            return None

        try:
            resp = requests.get(
                base_url,
                params={"destination": destination},
                headers={"Authorization": f"Bearer {api_key}"} if api_key else None,
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json()

            # Basic normalization to the structure used in the app.
            attractions = data.get("attractions") or []
            avg_meal_cost = data.get("avg_meal_cost", 0)
            avg_transport_day = data.get("avg_transport_day", 0)

            if not attractions:
                return None

            return {
                "attractions": attractions,
                "avg_meal_cost": avg_meal_cost,
                "avg_transport_day": avg_transport_day,
            }
        except Exception:
            return None


class SearchTool:
    @staticmethod
    def search_destination(destination: str) -> Dict[str, Any]:
        key = destination.lower()
        external_data = ExternalDestinationAPI.fetch_destination(destination)

        if external_data:
            source = "external"
            data = external_data
        elif key in DESTINATIONS_DB:
            source = "local"
            data = DESTINATIONS_DB[key]
        else:
            return {"found": False, "message": f"{destination} not supported"}

        return {"found": True, "data": data, "source": source}

class TimeCalculator:
    @staticmethod
    def plan_daily_schedule(activities: List[Dict]) -> List[Dict]:
        schedule = []
        time = datetime.strptime("09:00", "%H:%M")
        for act in activities:
            end = time + timedelta(hours=act["duration"])
            schedule.append({
                "activity": act["name"],
                "start": time.strftime("%H:%M"),
                "end": end.strftime("%H:%M"),
                "cost": act["cost"]
            })
            time = end + timedelta(minutes=30)
        return schedule

class BudgetCalculator:
    @staticmethod
    def validate(total: float, budget: float) -> Dict:
        return {
            "total_cost": round(total, 2),
            "budget": budget,
            "difference": round(budget - total, 2),
            "within_budget": total <= budget
        }

# =============================================================================
# STATE
# =============================================================================

class TravelPlanState(TypedDict, total=False):
    destination: str
    budget: float
    num_days: int
    interests: List[str]
    travel_style: str

    destination_research: Dict
    filtered_activities: List[Dict]
    daily_itineraries: List[Dict]
    budget_analysis: Dict
    final_plan: str

    messages: Annotated[List[str], operator.add]

# =============================================================================
# AGENTS
# =============================================================================

class DestinationResearchAgent:
    def __call__(self, state: TravelPlanState):
        result = SearchTool.search_destination(state["destination"])
        if not result["found"]:
            return {"messages": ["❌ Destination not found"], "filtered_activities": []}

        activities = result["data"]["attractions"]
        interests = state.get("interests", [])

        if interests:
            activities = [
                a for a in activities
                if any(i in a["category"] or i in a["description"] for i in interests)
            ] or activities

        return {
            "destination_research": result["data"],
            "filtered_activities": activities,
            "messages": ["✅ Research completed"]
        }

class TripPlannerAgent:
    def __call__(self, state: TravelPlanState):
        tc = TimeCalculator()
        days = state["num_days"]
        acts = state["filtered_activities"]

        plans = []
        idx = 0
        for d in range(1, days + 1):
            day_acts = acts[idx:idx + 3]
            idx += 3
            schedule = tc.plan_daily_schedule(day_acts)

            cost = sum(a["cost"] for a in day_acts)
            plans.append({
                "day": d,
                "schedule": schedule,
                "costs": {
                    "activities": cost,
                    "meals": state.get("destination_research", {}).get("avg_meal_cost", 0),        
                    "transport": state.get("destination_research", {}).get("avg_transport_day", 15),

                    "total": cost + state["destination_research"]["avg_meal_cost"] +
                             state["destination_research"]["avg_transport_day"]
                }
            })

        return {"daily_itineraries": plans, "messages": ["📅 Itinerary planned"]}

class BudgetAgent:
    def __call__(self, state: TravelPlanState):
        total = sum(d["costs"]["total"] for d in state["daily_itineraries"])
        analysis = BudgetCalculator.validate(total, state["budget"])
        return {"budget_analysis": analysis, "messages": ["💵 Budget analyzed"]}

class CoordinatorAgent:
    def __call__(self, state: TravelPlanState):
        prompt = f"""
Create a professional travel plan.

Destination: {state['destination']}
Days: {state['num_days']}
Budget: {state['budget']}
Itinerary: {json.dumps(state['daily_itineraries'], indent=2)}
Budget: {json.dumps(state['budget_analysis'], indent=2)}
"""
        return {
            "final_plan": call_gemini(prompt),
            "messages": ["📋 Final plan generated"]
        }

# =============================================================================
# GRAPH
# =============================================================================

def build_travel_agent_graph():
    graph = StateGraph(TravelPlanState)

    graph.add_node("research", DestinationResearchAgent())
    graph.add_node("plan", TripPlannerAgent())
    graph.add_node("budget", BudgetAgent())
    graph.add_node("final", CoordinatorAgent())

    graph.set_entry_point("research")
    graph.add_edge("research", "plan")
    graph.add_edge("plan", "budget")
    graph.add_edge("budget", "final")
    graph.add_edge("final", END)

    return graph.compile()

# =============================================================================
# API ENTRY FUNCTION (USED BY FASTAPI)
# =============================================================================

def create_travel_plan(destination, budget, num_days, interests, travel_style="mid-range"):
    app = build_travel_agent_graph()
    return app.invoke({
        "destination": destination,
        "budget": budget,
        "num_days": num_days,
        "interests": interests,
        "travel_style": travel_style,
        "messages": []
    })
