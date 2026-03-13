from fastapi import APIRouter, HTTPException
from app.models.schemas import ReminderRequest, ReminderResponse
from app.services.reminder_service import generate_reminders

router = APIRouter(prefix="/api/v1/reminders", tags=["Reminders"])

@router.post("/generate", response_model=ReminderResponse)
async def reminders_generate(req: ReminderRequest):
    try:
        return await generate_reminders(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))