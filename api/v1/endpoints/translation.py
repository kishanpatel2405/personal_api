from fastapi import APIRouter, HTTPException, Query
from googletrans import Translator

from schemas.v1.translation import TranslationResponse
from utils.enums import SupportedLanguages

router = APIRouter()
translator = Translator()


@router.get("/translate", response_model=TranslationResponse, status_code=200)
async def translate(
        text: str = Query(..., description="Text to be translated"),
        target_language: SupportedLanguages = Query(..., description="Target language")
):
    try:
        translated = translator.translate(text, dest=target_language.value)
        return TranslationResponse(translated_text=translated.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
