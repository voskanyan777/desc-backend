import sys
from pathlib import Path
BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))



from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from .schemas import UserSchema
from .utils import *
from pydantic import BaseModel
from db.orm import SyncOrm
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer
from app.logger_file import logger


http_bearer = HTTPBearer()

oauth2_scheme = OAuth2PasswordBearer('/token')

sync_orm = SyncOrm()


class Token(BaseModel):
    access_token: str
    token_type: str


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)


def validate_auth_user(
        email: str = Form(),
        password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )

    user = sync_orm.get_user(email)
    if not user:
        raise unauthed_exc
    hashed_password = user[1]
    user = UserSchema(login=user[0], password=user[1], email=user[2])
    if not validate_password(
            password=password,
            hashed_password=hashed_password,
    ):
        raise unauthed_exc

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user inactive",
        )

    return user


@auth_router.post('/login/', response_model=Token)
def auth_user(user: UserSchema = Depends(validate_auth_user)) -> Token:
    jwt_payload = {
        'sub': user.login,
        'email': user.email
    }
    token = encode_jwt(jwt_payload)
    logger.info(f'The admin {user.login}/{user.email} has logged in')
    return Token(
        access_token=token,
        token_type='Bearer'
    )


def get_current_token_payload_user(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
        # token: str = Depends(oauth2_scheme)
) -> UserSchema:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'invalid token error {e}')

    return payload


def get_current_auth_user(payload: dict = Depends(get_current_token_payload_user)) -> UserSchema:
    user_email: str | None = payload.get('email')
    user = sync_orm.get_user(user_email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid (user not found)'
        )
    user = UserSchema(login=user[0], password=user[1], email=user[2])
    return user


def get_current_active_auth_user(user: UserSchema = Depends(get_current_auth_user)):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive'
    )


@auth_router.get('/users/me')
def auth_user_check_self_info(user: UserSchema = Depends(get_current_active_auth_user)):
    return {
        'username': user.login,
        'email': user.email
    }


@auth_router.post('/registration')
def user_registration(login: str, user_email: str, password: str):
    hashed_password = hash_password(password)
    sync_orm.add_user(login, user_email, hashed_password)
    return {
        'data': None,
        'status': 'ok'
    }


