import json
from app.core.gemini import get_creative_model
from app.models.schemas import ReminderRequest, ReminderResponse, ReminderItem

PROMPT = """
You are a friendly pet care advisor for Pawzio app.

Pet: {name} | {species} | {breed} | {age_years} yrs | {weight_kg} kg
Month: {month} | Season: {season}
Known conditions: {conditions}
Days since last vet visit: {vet_days}

Generate 4-5 personalized care reminders for this pet RIGHT NOW.

Respond ONLY with this JSON — no markdown:
{{
  "reminders": [
    {{
      "title": "Short action title",
      "detail": "2 sentence explanation with specific advice.",
      "priority": "urgent|normal|informational",
      "category": "health|grooming|nutrition|exercise|vet_visit"
    }}
  ],
  "fun_fact": "One fun breed-specific fact."
}}

Be specific to the breed, season, and age. Not generic advice.
"""

def _clean(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return raw.strip()

MONTHS = [
    "", "January","February","March","April","May","June",
    "July","August","September","October","November","December"
]

async def generate_reminders(req: ReminderRequest) -> ReminderResponse:
    model = get_creative_model()
    p = req.pet
    prompt = PROMPT.format(
        name=p.name, species=p.species, breed=p.breed,
        age_years=p.age_years, weight_kg=p.weight_kg,
        month=MONTHS[req.current_month],
        season=req.current_season,
        conditions=", ".join(req.known_conditions) or "None",
        vet_days=req.last_vet_visit_days,
    )
    res  = model.generate_content(prompt)
    data = json.loads(_clean(res.text))
    items = [
        ReminderItem(
            title=r["title"], detail=r["detail"],
            priority=r["priority"], category=r["category"],
        )
        for r in data["reminders"]
    ]
    return ReminderResponse(
        pet_id=p.pet_id,
        pet_name=p.name,
        reminders=items,
        fun_fact=data["fun_fact"],
    )
