from fastapi import APIRouter, HTTPException
from app.models.schemas import TriageRequest, TriageResponse
from app.services.triage_service import analyze_symptoms

router = APIRouter(prefix="/api/v1/triage", tags=["Triage"])

@router.post("/symptom-check", response_model=TriageResponse)
async def symptom_check(req: TriageRequest):
    try:
        return await analyze_symptoms(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))