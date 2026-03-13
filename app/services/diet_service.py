import json
from app.core.gemini import get_creative_model

def _clean(raw: str) -> str:
    raw = raw.strip()
    if "```" in raw:
        parts = raw.split("```")
        for p in parts:
            p = p.strip()
            if p.startswith("json"):
                p = p[4:].strip()
            try:
                json.loads(p)
                return p
            except:
                continue
    return raw.strip()

async def generate_diet(pet_name: str, species: str, age: float, weight: float, conditions: str) -> dict:
    model = get_creative_model()

    avoid_defaults = {
        "dog":    ["Chocolate", "Grapes & raisins", "Onions & garlic", "Xylitol", "Avocado", "Macadamia nuts"],
        "cat":    ["Onions & garlic", "Raw fish (regularly)", "Milk & dairy", "Chocolate", "Grapes", "Dog food"],
        "rabbit": ["Iceberg lettuce", "Potatoes", "Onions", "Chocolate", "Bread & crackers", "Avocado"],
        "bird":   ["Avocado", "Chocolate", "Onions & garlic", "Caffeine", "Fruit seeds/pits", "Salt"],
    }

    prompt = f"""You are a professional pet nutritionist.
Create a detailed daily diet plan for:
- Name: {pet_name}
- Species: {species}
- Age: {age} years
- Weight: {weight} kg
- Health notes: {conditions or "None"}

Respond ONLY with valid JSON, no markdown, no extra text:
{{
  "daily_calories": <number>,
  "meals_per_day": <number>,
  "morning": "<detailed morning meal>",
  "afternoon": "<detailed afternoon meal>",
  "evening": "<detailed evening meal>",
  "snacks": "<healthy snack options>",
  "water": "<daily water recommendation>",
  "tips": ["<tip1>", "<tip2>", "<tip3>"]
}}"""

    try:
        res = model.generate_content(prompt)
        data = json.loads(_clean(res.text))
    except Exception:
        # Sensible fallback if Gemini fails
        cal = {"dog": 700, "cat": 280, "rabbit": 150, "bird": 80}.get(species, 500)
        data = {
            "daily_calories": round(cal * weight / 10),
            "meals_per_day": 3,
            "morning":   f"High-protein breakfast for {species}s — lean meat or quality kibble.",
            "afternoon": "Light midday meal, about 25% of daily intake.",
            "evening":   "Balanced dinner — protein with complex carbohydrates.",
            "snacks":    "Species-appropriate treats in moderation (max 10% of daily calories).",
            "water":     f"{round(weight * 50)}ml of fresh clean water daily.",
            "tips":      ["Feed at consistent times daily", "Always keep fresh water available", "Consult your vet before changing diet significantly"],
        }

    return {
        "pet_name":       pet_name,
        "species":        species,
        "daily_calories": data.get("daily_calories", 500),
        "meals_per_day":  data.get("meals_per_day", 3),
        "morning":        data.get("morning", ""),
        "afternoon":      data.get("afternoon", ""),
        "evening":        data.get("evening", ""),
        "snacks":         data.get("snacks", ""),
        "water":          data.get("water", f"{round(weight * 50)}ml daily"),
        "avoid":          avoid_defaults.get(species, ["Chocolate", "Onions", "Grapes"]),
        "tips":           data.get("tips", []),
    }