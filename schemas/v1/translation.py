from pydantic import BaseModel


class TranslationResponse(BaseModel):
    translated_text: str
