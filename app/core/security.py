import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from app.core.config import settings
from jwt.exceptions import InvalidTokenError
from app.models.shared import TokenPayload
from app.helpers.custom_exception import credentials_exception


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def create_token(data: TokenPayload, refresh: bool = False) -> str:
    to_encode = {
        "sub": data.sub,
        "permissions": list(data.permissions),
        "is_superuser": data.is_superuser
    }
    secret_key = settings.REFRESH_SECRET_KEY if refresh else settings.SECRET_KEY
    expire_minutes = settings.REFRESH_TOKEN_EXPIRE_MINUTES if refresh else settings.ACCESS_TOKEN_EXPIRE_MINUTES
    to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str, refresh: bool = False) -> TokenPayload:
    try:
        secret_key = settings.REFRESH_SECRET_KEY if refresh else settings.SECRET_KEY
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return TokenPayload(**payload)
    except InvalidTokenError:
        raise credentials_exception
