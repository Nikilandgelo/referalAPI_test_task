from time import time
from uuid import UUID

from authlib.jose import JWTClaims, jwt
from authlib.jose.errors import (
    BadSignatureError,
    DecodeError,
    ExpiredTokenError,
)
from bcrypt import checkpw, gensalt, hashpw
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import SQLModel

from app.config.settings import Settings, get_settings

settings: Settings = get_settings()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class PasswordHasher:

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plain-text password using bcrypt.

        Args:
            password (str): The plain-text password to be hashed.

        Returns:
            str: The hashed password as a UTF-8 encoded string.
        """
        return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """
        Verify a plain-text password against a hashed password.

        Args:
            password (str): The plain-text password to be checked.
            hashed_password (str): The hashed password to compare against.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return checkpw(
            password.encode("utf-8"), hashed_password.encode("utf-8")
        )


class JWT_Token:
    @staticmethod
    def create_token(payload: dict) -> str:
        """
        Create a JWT token with the given payload.

        This method encodes the provided payload into a JWT token, adding
        an expiration time and using the configured algorithm and secret key.

        Args:
            payload (dict): A dictionary containing the claims to be included\
            in the JWT token.

        Returns:
            str: The encoded JWT token as a UTF-8 string.
        """
        payload["exp"] = time() + settings.SECONDS_TO_EXPIRE
        jwt_token: bytes = jwt.encode(
            header={"alg": settings.JWT_ALGORITHM},
            payload=payload,
            key=settings.SECRET_KEY,
        )
        return jwt_token.decode("utf-8")

    @staticmethod
    def check_jwt_token(jwt_token: str) -> str | None:
        """
        Validate and decode a JWT token.

        This method attempts to decode and validate the provided JWT token
        using the configured secret key. It checks for token expiration
        and signature validity.

        Args:
            jwt_token (str): The JWT token to be validated and decoded.

        Returns:
            `str`: The user's email extracted from the token if valid.\n
            `None`: If the token is invalid or expired.
        """
        try:
            token: JWTClaims = jwt.decode(jwt_token, settings.SECRET_KEY)
            token.validate_exp(time(), 0)
            return token.get("user_email")
        except (BadSignatureError, DecodeError, ExpiredTokenError):
            return None


def verify_ownership(object: SQLModel, fieldname_owner: str, user_uuid: UUID):
    if not hasattr(object, fieldname_owner):
        raise AttributeError(
            (
                f"Model {object.__class__.__name__} does not have "
                f"attribute '{fieldname_owner}'."
            )
        )
    if getattr(object, fieldname_owner) != user_uuid:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to perform this action.",
        )
