import json
import re
from app.core.gemini import get_creative_model
from app.models.schemas import AdoptionMatchRequest, AdoptionMatchResponse, PetMatchResult

PROMPT = """
You are a pet adoption counselor.

Adopter lifestyle: "{lifestyle}"

Available pets:
{pets_json}

Rank every pet by compatibility. Respond ONLY with valid JSON, no markdown, no explanation, no extra text. Just the raw JSON object:
{{
  "ranked_matches": [
    {{
      "pet_id": "p1",
      "name": "Luna",
      "compatibility_score": 85,
      "match_reason": "Short reason.",
      "potential_concerns": "Short concern or none."
    }}
  ],
  "top_pick_id": "p1",
  "summary": "One sentence."
}}
Keep match_reason and potential_concerns under 20 words each. Sort highest to lowest score.
"""

def _extract_json(raw: str) -> dict:
    """Extract JSON from Gemini response regardless of formatting."""
    raw = raw.strip()

    # Try direct parse first
    try:
        return json.loads(raw)
    except Exception:
        pass

    # Remove markdown code fences
    raw = re.sub(r"```json|```", "", raw).strip()
    try:
        return json.loads(raw)
    except Exception:
        pass

    # Find the first { ... } block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    raise ValueError(f"Could not parse JSON from Gemini response: {raw[:200]}")

async def match_pets(req: AdoptionMatchRequest) -> AdoptionMatchResponse:
    model  = get_creative_model()
    pets   = [p.model_dump() for p in req.available_pets]
    prompt = PROMPT.format(
        lifestyle=req.adopter_lifestyle_text,
        pets_json=json.dumps(pets, indent=2),
    )

    res  = model.generate_content(prompt)
    data = _extract_json(res.text)

    ranked = [
        PetMatchResult(
            pet_id=m["pet_id"],
            name=m["name"],
            compatibility_score=int(m["compatibility_score"]),
            match_reason=m["match_reason"],
            potential_concerns=str(m.get("potential_concerns", "")),
        )
        for m in data["ranked_matches"]
    ]

    return AdoptionMatchResponse(
        ranked_matches=ranked,
        top_pick_id=data["top_pick_id"],
        summary=data["summary"],
    )