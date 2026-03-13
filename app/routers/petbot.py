from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.gemini import get_flash_model

router = APIRouter(prefix="/api/v1/petbot", tags=["PetBot"])

class PetBotRequest(BaseModel):
    question: str
    pet_name: str = "my pet"
    species: str = "dog"

class PetBotResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=PetBotResponse)
async def ask_petbot(req: PetBotRequest):
    try:
        model = get_flash_model()
        prompt = f"""You are PetBot, a friendly and knowledgeable pet care assistant.
The user has a {req.species} named {req.pet_name}.
Answer their question in a warm, helpful, and concise way (2-4 sentences max).
If it's a greeting like "hello" or "hi", respond warmly and ask how you can help with their pet.
Never give overly medical advice — always suggest consulting a vet for serious issues.

User question: {req.question}

Respond naturally and helpfully."""

        response = model.generate_content(prompt)
        return PetBotResponse(answer=response.text.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))