from typing import Annotated

from fastapi import Depends, HTTPException

from app.core.security import JWT_Token, oauth2
from app.db.db_interactions import DBInteractionsManager
from app.models.user import User


async def get_user_from_jwt(token: Annotated[str, Depends(oauth2)]):
    """
    This function validates the JWT token, extracts the user's email from it,
    and then fetches the corresponding user from the database.

    Args:
        token (Annotated[str, Depends(oauth2)]): The JWT token to be validated.
            This is automatically provided by FastAPI's dependency injection
            system.

    Returns:
        User: The user object retrieved from the database.

    Raises:
        HTTPException:
            - 401 error if the token is invalid.
            - 404 error if the user is not found in the database.
    """
    user_email: str | None = JWT_Token.check_jwt_token(token)
    if not user_email:
        raise HTTPException(401, "Invalid token. Please log in again.")

    user: User | None = await DBInteractionsManager.get_record_from_db(
        {"email": user_email}, User
    )
    if not user:
        raise HTTPException(404, "User not found.")
    return user
