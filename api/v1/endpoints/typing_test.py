from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse  # Changed from HTMLResponse to JSONResponse
from fastapi.staticfiles import StaticFiles
from enum import Enum
import random
import time

from starlette.responses import HTMLResponse

from utils.enums import TimeLimit

router = APIRouter()

# Serve the static directory (make sure you have a `static` folder with `index.html`)
router.mount("/static", StaticFiles(directory="static"), name="static")

# Sample texts for typing tests
typing_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes a man perfect.",
    "Typing fast is a skill worth mastering.",
    "A journey of a thousand miles begins with a single step."
]

@router.get("/", response_class=HTMLResponse)
async def get_index():
    # Serve the HTML file for typing test
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@router.get("/typing-speed-test/start", response_class=JSONResponse)
async def start_typing_test(time_limit: TimeLimit):
    # Get the time limit from the enum
    time_limit_seconds = time_limit.value

    # Generate a random text for the user to type
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

    # Validate time limit
    if elapsed_time > time_limit.value:
        raise HTTPException(status_code=400, detail="Time limit exceeded")

    # Calculate typing speed and accuracy
    typed_words = len(typed_text.split())
    original_words = len(original_text.split())

    # Words Per Minute (WPM)
    wpm = (typed_words / elapsed_time) * 60

    # Accuracy
    correct_chars = sum(1 for o, t in zip(original_text, typed_text) if o == t)
    accuracy = (correct_chars / len(original_text)) * 100

    return JSONResponse(
        content={
            "elapsed_time_seconds": elapsed_time,
            "wpm": round(wpm, 2),
            "accuracy": round(accuracy, 2)
        }
    )