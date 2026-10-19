from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from api.dependencies import get_create_user_service, get_login_service
from api.security import get_current_user, require_roles
from application.dto.auth import (
    CreateUserRequest,
    CreateUserResponse,
    LoginRequest,
    LoginResponse,
)
from application.exceptions.auth import (
    AuthenticationConfigurationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from application.services.create_user import CreateUserService
from application.services.login import LoginService
from common.user_role import UserRole
from identity.user import User, UserPublic

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginBody(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=1)


class CreateUserBody(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=64,
        pattern=r"^[A-Za-z0-9._-]+$",
    )
    password: str = Field(min_length=12, max_length=256)
    role: UserRole


@router.post("/login", response_model=LoginResponse)
def login(
    body: LoginBody,
    service: LoginService = Depends(get_login_service),
) -> LoginResponse:
    try:
        return service.execute(
            LoginRequest(username=body.username, password=body.password)
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
    except AuthenticationConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc


@router.get("/me", response_model=UserPublic)
def get_me(user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.from_user(user)


@router.post(
    "/users",
    response_model=CreateUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    body: CreateUserBody,
    service: CreateUserService = Depends(get_create_user_service),
    _administrator: User = Depends(require_roles(UserRole.ADMINISTRATOR)),
) -> CreateUserResponse:
    try:
        return service.execute(
            CreateUserRequest(
                username=body.username,
                password=body.password,
                role=body.role,
            )
        )
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc
