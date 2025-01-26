import random

import quote
from fastapi import APIRouter

from schemas.v1.affirmations import FavoritesSchema, QuoteData, QuoteSchema
from utils.enums import ErrorMessageCodes
from utils.errors import ApiException

router = APIRouter()

favorites = []


@router.get(
    "/quote", response_model=QuoteData, summary="Retrieve a random affirmation or quote"
)
def get_random_quote():
    try:
        quotes = quote.quote("inspiration")
        if not quotes:
            raise ApiException(
                msg="No quotes available.",
                error_code=ErrorMessageCodes.NOT_FOUND,
                status_code=404,
            )

        random_quote = random.choice(quotes)

        return QuoteData(
            quote=random_quote["quote"],
            author=random_quote["author"],
            book=random_quote["book"],
        )
    except Exception:
        raise ApiException(
            msg="Error fetching quote.",
            error_code=ErrorMessageCodes.NOT_FOUND,
            status_code=404,
        )


@router.post(
    "/favorites", response_model=FavoritesSchema, summary="Save a quote to favorites"
)
def save_to_favorites(quote: QuoteSchema):
    try:
        if quote.quote not in favorites:
            favorites.append(quote.quote)
        return FavoritesSchema(favorites=favorites)
    except Exception:
        raise ApiException(
            msg="Error saving to favorites.",
            error_code=ErrorMessageCodes.NOT_FOUND,
            status_code=404,
        )


@router.get(
    "/favorites",
    response_model=FavoritesSchema,
    summary="Retrieve saved favorite quotes",
)
def get_favorites():
    return FavoritesSchema(favorites=favorites)
