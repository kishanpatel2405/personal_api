from pydantic import BaseModel


class EnglishLesson(BaseModel):
    word: str
    definition: str
    example_sentence: str
    part_of_speech: str
