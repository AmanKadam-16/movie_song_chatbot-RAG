from passlib.context import CryptContext
from datetime import timedelta, datetime
from movie_assistant.core.config import settings
from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
JWT_SECRET = settings.SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM
ACCESS_TOKEN_EXPIRY_MINUTES = settings.ACCESS_TOKEN_EXPIRY

security = HTTPBearer()


def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_token(data: dict) -> str:
    claim_data = data.copy()
    token_expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    claim_data["exp"] = token_expiry
    token = jwt.encode(claims=claim_data, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token


def decode_token(token: str) -> dict:
    try:
        decoded_payload = jwt.decode(
            token=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM]
        )
        return decoded_payload
    except JWTError as je:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=je)


def get_current_user(credential: HTTPAuthorizationCredentials = Depends(security)):
    token = credential.credentials
    token_claims = decode_token(token=token)
    return token_claims


def authorize_role(role_scope: list[str]):
    def wrapper(payload=Depends(get_current_user)):
        role = payload.get("role")
        if role not in role_scope:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient permissions.",
            )

    return wrapper
