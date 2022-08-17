from datetime import datetime, timedelta
from typing import Optional, TypedDict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from bantre.system.user import User
from bantre.util.config import get_settings

from ..database import get_session


pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

settings = get_settings()


class AccessToken(BaseModel):
    """Type hinting for access token jwt dict"""

    user_id: int
    exp: int


class RefreshToken(AccessToken):
    """Type hinting for refresh token jwt dict"""

    token_id: int


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.exec(select(User).where(User.username == username)).first()


def get_user_by_uid(db: Session, id: int) -> User | None:
    return db.get(User, id)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def decode_token(db: Session, token: str, key: str) -> User | None:
    try:
        payload = jwt.decode(token, key)
        user_id: int = payload.get("id")  # type: ignore
        if user_id is None:
            return None
    except JWTError:
        return None
    return get_user_by_uid(db, user_id)


def token_required(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User:
    user = decode_token(db=session, token=token, key=settings.access_token_key)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def token_optional(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> User | None:
    """
    This function is like token_required, but returns the anonymous user if not validated.
    It is very important to make sure that the front end makes sure it is logged in so that we dont make a bunch of db entries as the anonymous user
    """
    user = decode_token(db=session, token=token, key=settings.access_token_key)
    if user is None:
        # TODO: Let user be none?
        user = User(id=-1, username="Anonymous", admin=False, email="", password="")
    return user


def create_access_token(
    id: int,
    expires_delta: Optional[timedelta],
):
    to_encode = {
        "id": id,
        "token_type": "access_token",
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.access_token_lifetime)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.access_token_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_refresh_token(
    id: int,
    expires_delta: Optional[timedelta],
):
    to_encode = {
        "id": id,
        "token_type": "refresh_token",
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(settings.access_token_lifetime)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.refresh_token_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt
