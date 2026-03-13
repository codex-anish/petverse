import json
from app.core.gemini import get_flash_model
from app.models.schemas import TriageRequest, TriageResponse, UrgencyLevel

PROMPT = """
You are an expert veterinary triage assistant.

Pet: {name} | {species} | {breed} | {age_years} yrs | {weight_kg} kg
Symptoms: "{symptom_text}"

Respond ONLY with this exact JSON — no markdown, no extra text:
{{
  "urgency_level": "CRITICAL|URGENT|MODERATE|MILD|NORMAL",
  "summary": "One sentence verdict.",
  "explanation": "2-3 sentences explaining urgency.",
  "recommended_action": "Exact next step for owner.",
  "trigger_sos": true or false,
  "home_care_tips": ["tip1", "tip2"]
}}

Rules:
- CRITICAL (poison/seizure/can't breathe) → trigger_sos = true, home_care_tips = []
- URGENT (needs vet today) → trigger_sos = false, home_care_tips = []
- MODERATE/MILD/NORMAL → trigger_sos = false, give 2-3 tips
"""

def _clean(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()

async def analyze_symptoms(req: TriageRequest) -> TriageResponse:
    model = get_flash_model()
    p = req.pet
    prompt = PROMPT.format(
        name=p.name, species=p.species, breed=p.breed,
        age_years=p.age_years, weight_kg=p.weight_kg,
        symptom_text=req.symptom_text,
    )
    res  = model.generate_content(prompt)
    data = json.loads(_clean(res.text))
    return TriageResponse(
        pet_id=p.pet_id,
        urgency_level=UrgencyLevel(data["urgency_level"]),
        summary=data["summary"],
        explanation=data["explanation"],
        recommended_action=data["recommended_action"],
        trigger_sos=data["trigger_sos"],
        home_care_tips=data.get("home_care_tips", []),
    )
