import random
import time

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from utils.enums import TimeLimit

router = APIRouter()

router.mount("/static", StaticFiles(directory="static"), name="static")

typing_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes a man perfect.",
    "Typing fast is a skill worth mastering.",
    "A journey of a thousand miles begins with a single step."
]


@router.get("/", response_class=HTMLResponse)
async def get_index():
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())


@router.get("/typing-speed-test/start", response_class=JSONResponse)
async def start_typing_test(time_limit: TimeLimit):
    time_limit_seconds = time_limit.value

    text = random.choice(typing_texts)

    return JSONResponse(
        content={
            "message": "Typing test started. Type the following text:",
            "text": text,
            "time_limit_seconds": time_limit_seconds
        }
    )


@router.post("/typing-speed-test/submit", response_class=JSONResponse)
async def submit_typing_test(typed_text: str, original_text: str, start_time: float, time_limit: TimeLimit):
    elapsed_time = time.time() - start_time

    if elapsed_time > time_limit.value:
        raise HTTPException(status_code=400, detail="Time limit exceeded")

    typed_words = len(typed_text.split())
    original_words = len(original_text.split())

    wpm = (typed_words / elapsed_time) * 60

    correct_chars = sum(1 for o, t in zip(original_text, typed_text) if o == t)
    accuracy = (correct_chars / len(original_text)) * 100

    return JSONResponse(
        content={
            "elapsed_time_seconds": elapsed_time,
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2)
        }
    )
