from typing import List

from pydantic import BaseModel


class QuoteSchema(BaseModel):
    quote: str


class FavoritesSchema(BaseModel):
    favorites: List[str]


class QuoteData(BaseModel):
    author: str
    book: str
    quote: str
