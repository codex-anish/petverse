import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.gemini_api_key)

MODEL_NAME = "gemini-3-flash-preview"

def get_flash_model():
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=4096,
        ),
    )

def get_pro_model():
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,
            max_output_tokens=4096,
        ),
    )

def get_creative_model():
    return genai.GenerativeModel(
        model_name=MODEL_NAME,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=4096,
        ),
    )