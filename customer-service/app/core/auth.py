from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas.auth import AuthToken
from app.core.config import settings
from app.domain.services.session_service import SessionService
from app.api.v1.dependencies import get_session_service

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="v1/auth/login", scheme_name="JWT"
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def verify_password(password: str, hashed_pass: str)-> bool:
    return password_context.verify(password, hashed_pass)

async def verify_token(
    token: str = Depends(reuseable_oauth),
    session_service: SessionService = Depends(get_session_service)
) -> str:
    try:
        # Décodage du token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
        # Vérification des informations du payload
        user_id = payload['id']
        expire_at = payload['expire']
        token_type = payload['type']
            
        
        if not token_type or not user_id or not expire_at:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide.",
                    headers={"WWW-Authenticate": "Bearer"}
            )
                
        expire_at_dt = datetime.fromisoformat(expire_at)
        if expire_at_dt < datetime.utcnow():
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expiré.",
                    headers={"WWW-Authenticate": "Bearer"}
            )
        
        session = await session_service.get_session_by_field(token_type, token)
        if not session or not session.is_active:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token revoqué.",
                    headers={"WWW-Authenticate": "Bearer"}
            )
        
        return token  
    except JWTError as e:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide.",
                    headers={"WWW-Authenticate": "Bearer"}
            )

async def verify_refresh_token(
    token: str = Depends(reuseable_oauth),
    session_service: SessionService = Depends(get_session_service)
) -> str:
    try:
        # Décodage du token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
        # Vérification des informations du payload
        user_id = payload['id']
        expire_at = payload['expire']
        token_type = payload['type']
            
        
        if not token_type or not user_id or not expire_at or token_type != "refresh_token":
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide.",
                    headers={"WWW-Authenticate": "Bearer"}
            )
                
        expire_at_dt = datetime.fromisoformat(expire_at)
        if expire_at_dt < datetime.utcnow():
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expiré.",
                    headers={"WWW-Authenticate": "Bearer"}
            )
        
        session = await session_service.get_session_by_field(token_type, token)
        if not session or not session.is_active:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token revoqué.",
                    headers={"WWW-Authenticate": "Bearer"}
            )
        
        return token  
    except JWTError as e:
        raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token invalide.",
                    headers={"WWW-Authenticate": "Bearer"}
            )

def create_access_token(data: Union[AuthToken, None], expires_delta: int = 15):
    expires_delta = datetime.now() + timedelta(minutes=expires_delta)

    datetime_string = expires_delta.strftime('%Y-%m-%d %H:%M:%S')
    to_encode = data.dict()
    to_encode['expire'] = datetime_string
    to_encode['type'] = "access_token"
    return dict(token=jwt.encode(to_encode, SECRET_KEY, ALGORITHM), expire=datetime_string)


def create_refresh_token(data: Union[AuthToken, None]):
    expires_delta = datetime.now() + timedelta(days=7)
    datetime_string = expires_delta.strftime('%Y-%m-%d %H:%M:%S')

    to_encode = data.dict()
    to_encode['expire'] = datetime_string
    to_encode['type'] = "refresh_token"
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


def create_token(user: AuthToken, exp_access: Optional[int] = None, exp_refresh: Optional[int] = None):
    if exp_access:
        access_token = create_access_token(user, exp_access)
    else:
        access_token = create_access_token(user)

    if exp_refresh:
        refresh_token = create_refresh_token(user, exp_refresh)
    else:
        refresh_token = create_refresh_token(user)
    token = dict(token_type="bearer", access_token=access_token['token'], expire=access_token['expire'], refresh_token=refresh_token)
    
    return token
