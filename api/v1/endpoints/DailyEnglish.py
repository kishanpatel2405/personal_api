import requests
from fastapi import APIRouter

from schemas.v1.DailyEnglish import EnglishLesson

router = APIRouter()

WORDNIK_API_KEY = "YOUR_WORDNIK_API_KEY"
WORDNIK_API_URL = "https://api.wordnik.com/v4/words.json/wordOfTheDay"


@router.get("/english/lesson/daily", response_model=EnglishLesson, status_code=200)
def get_daily_english_lesson():
    response = requests.get(WORDNIK_API_URL, params={"apiKey": WORDNIK_API_KEY})
    if response.status_code != 200:
        return {"error": "Could not fetch word of the day"}

    word_data = response.json()
    lesson = EnglishLesson(
        word=word_data["word"],
        definition=word_data["definitions"][0]["text"],
        example_sentence=word_data["examples"][0]["text"],
        part_of_speech=word_data["partOfSpeech"],
    )
    return lesson
