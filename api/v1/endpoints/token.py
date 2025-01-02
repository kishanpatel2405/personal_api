from fastapi import APIRouter, Depends, Request

from core.security import JWTRefreshTokenBearer
from schemas.v1.token import (USER_ID_CLAIM, AccessToken, RefreshToken,
                              RefreshTokenResponse)
from services.authentication import get_user_by_id

router = APIRouter()


@router.get("/token/refresh", response_model=RefreshTokenResponse, name="token", status_code=200)
async def token_refresh(request: Request, token: RefreshToken = Depends(JWTRefreshTokenBearer())):
    db_user = get_user_by_id(request.app.db_session(), user_id=token.payload.get(USER_ID_CLAIM))
    return RefreshTokenResponse(access=str(AccessToken.for_user(db_user)))
