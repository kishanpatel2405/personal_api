from typing import Optional

from pydantic import BaseModel


class MusicRecommendation(BaseModel):
    song_title: str
    artist: str
    genre: str
    url: Optional[str] = None
