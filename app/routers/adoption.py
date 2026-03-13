from fastapi import APIRouter, HTTPException
from app.models.schemas import AdoptionMatchRequest, AdoptionMatchResponse
from app.services.adoption_service import match_pets

router = APIRouter(prefix="/api/v1/adoption", tags=["Adoption"])

@router.post("/match", response_model=AdoptionMatchResponse)
async def adoption_match(req: AdoptionMatchRequest):
    try:
        return await match_pets(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))