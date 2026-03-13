from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.diet_service import generate_diet

router = APIRouter(prefix="/api/v1/diet", tags=["Diet"])

class DietRequest(BaseModel):
    pet_name:   str = "My Pet"
    species:    str = "dog"
    age_years:  float = 2.0
    weight_kg:  float = 10.0
    conditions: str = ""

@router.post("/generate")
async def diet_generate(req: DietRequest):
    try:
        return await generate_diet(
            req.pet_name, req.species,
            req.age_years, req.weight_kg, req.conditions
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))