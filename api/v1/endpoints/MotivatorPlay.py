from typing import List, Optional

import spotipy
from fastapi import APIRouter
from spotipy.oauth2 import SpotifyClientCredentials

from schemas.v1.MotivatorPlay import MusicRecommendation

router = APIRouter()
sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="YOUR_SPOTIFY_CLIENT_ID", client_secret="YOUR_SPOTIFY_CLIENT_SECRET"
    )
)


@router.get(
    "/music/recommendations", response_model=List[MusicRecommendation], status_code=200
)
def get_motivational_music(
    genre: str = "motivational",
    mood: Optional[str] = None,
    activity: Optional[str] = None,
):
    results = sp.search(q=genre, limit=10, type="track")
    music_data = [
        MusicRecommendation(
            song_title=track["name"],
            artist=track["artists"][0]["name"],
            genre=genre,
            url=track["external_urls"]["spotify"],
        )
        for track in results["tracks"]["items"]
    ]
    return music_data
