import requests
from fastapi import APIRouter, HTTPException

from schemas.v1.DailyEnglish import EnglishLesson

router = APIRouter()

URL = "https://api.datamuse.com/words"


@router.get("/english/lesson/daily", response_model=EnglishLesson, status_code=200)
def get_daily_english_lesson():
    response = requests.get(URL, params={"ml": "random", "max": 3})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Could not fetch word of the day")

    words = response.json()
    if not words:
        raise HTTPException(status_code=500, detail="No words found")

    word_of_the_day = words[0]["word"]

    lesson = EnglishLesson(
        word=word_of_the_day,
        definition="This is a placeholder definition.",
        example_sentence=f"The word '{word_of_the_day}' is fascinating!",
        part_of_speech="noun",
    )
    return lesson
