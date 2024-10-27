from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.exceptions import ResponseValidationError
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import JWT_Token, PasswordHasher
from app.db.db import get_session
from app.db.db_shortcuts import get_object_or_404
from app.models.user import User
from app.routes import user_router
from app.serializers.token import Token
from app.serializers.user import UserInSerializer, UserOutSerializerWithToken


@user_router.post(
    "/signup",
    response_model=UserOutSerializerWithToken,
    responses={400: {"description": "Email already exists"}},
    summary="User Registration",
    description=(
        "Register a new user with email, password and receive a JWT token."
    ),
)
async def register_user(
    body: UserInSerializer,
    async_session: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    body.password = PasswordHasher.hash_password(body.password)
    user = User(**dict(body))
    async_session.add(user)
    try:
        await async_session.commit()
        jwt_token: str = JWT_Token.create_token({"user_email": user.email})
        return {"user": user, "access_token": jwt_token}
    except (IntegrityError, ResponseValidationError):
        raise HTTPException(
            status_code=400, detail="User with this email already exists."
        )


@user_router.post(
    "/login",
    response_model=Token,
    responses={
        400: {"description": "Invalid password."},
        404: {"description": "User not found."},
    },
    summary="User Login",
    description=(
        "Login an existing user with email and password and "
        "receive a new JWT token."
    ),
)
async def login_user(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user: User = await get_object_or_404(User, email=user_data.username)
    if PasswordHasher.check_password(user_data.password, user.password):
        jwt_token: str = JWT_Token.create_token({"user_email": user.email})
        return Token(access_token=jwt_token)
    raise HTTPException(
        status_code=400, detail="Invalid password, please pass correct one."
    )
