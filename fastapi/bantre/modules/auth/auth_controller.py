from datetime import datetime, timedelta
from os import access

from pydantic import BaseModel

from bantre.database import Session, get_session
from bantre.modules.auth.auth_model import RefreshTokenModel
from bantre.util import config
from bantre.util.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from fastapi import APIRouter, Body, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


auth_router = APIRouter()


# Return model
class TokenResponse(BaseModel):
    """Both access token and refresh token are serialized"""

    access_token: str
    refresh_token: str


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    response: Response,
    formdata: OAuth2PasswordRequestForm = Depends(),
    settings: config.Settings = Depends(config.get_settings),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, formdata.username, formdata.password)
    if not user or not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_lifetime)
    access_token = create_access_token(id=user.id, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=30)
    refresh_token = create_refresh_token(
        id=user.id, expires_delta=refresh_token_expires
    )
    set_refresh_token_cookie(response, refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


class RefreshToken(BaseModel):
    refresh_token: str


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(
    response: Response,
    refresh_token: RefreshToken = Body(default=None),
    session: Session = Depends(get_session),
    settings: config.Settings = Depends(config.get_settings),
):
    user = decode_token(
        session, refresh_token.refresh_token, settings.refresh_token_key
    )
    if not user or not user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not valid",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_lifetime)
    access_token = create_access_token(id=user.id, expires_delta=access_token_expires)
    refresh_token_expires = timedelta(days=30)
    new_refresh_token = create_refresh_token(
        id=user.id, expires_delta=refresh_token_expires
    )
    set_refresh_token_cookie(response, new_refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)


def set_refresh_token_cookie(response: Response, refresh_token: str):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=60 * 60 * 24 * 30,
        httponly=True,
        secure=True,
    )
