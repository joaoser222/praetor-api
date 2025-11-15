from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
from config.database import get_db
from config.security import decode_token, is_jwt_token
from core.exceptions import UnauthorizedException, ForbiddenException
from .models import User
from .repositories.user import UserRepository


class TokenBearer:
    """
    Validates JWT access tokens (hybrid model).
    Automatically detects and validates JWT tokens.
    Can extract token from header 'Authorization' or cookie 'access_token'.
    
    Note: In the hybrid model, access tokens are always JWT.
    """

    def __init__(self, auto_error: bool = True):
        self.auto_error = auto_error

    async def __call__(self, request: Request) -> Dict[str, Any]:
        # 1. Try to get the token from the header Authorization
        auth: Optional[str] = request.headers.get("Authorization")
        token = None

        if auth and auth.startswith("Bearer "):
            token = auth[len("Bearer "):]

        # 2. Try to get the token from the cookie (HttpOnly)
        if not token:
            token = request.cookies.get("access_token")

        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                )
            else:
                return None

        # 3. Validate JWT token (access tokens are always JWT in hybrid model)
        if not is_jwt_token(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format. Expected JWT token.",
            )
        
        # Validate JWT token
        try:
            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid JWT token payload",
                )
            return {
                "token": token,
                "type": "jwt",  # Access tokens are always JWT in hybrid model
                "payload": payload,
                "user_id": int(user_id)
            }
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired JWT token",
            )


# Maintain compatibility with existing code
class JWTBearer(TokenBearer):
    """
    Compatibility class. In the hybrid model, access tokens are always JWT.
    Use TokenBearer for consistency.
    """
    pass


token_scheme = TokenBearer()
jwt_scheme = token_scheme  # Maintain compatibility


async def get_current_user(
    token_data: Dict[str, Any] = Depends(token_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get the current user based on the JWT access token.
    
    In the hybrid model, access tokens are always JWT, so validation
    has already been done in TokenBearer. This function just retrieves
    the user from the database.
    """
    # JWT validation has already been done in TokenBearer
    user_id = token_data["user_id"]

    # Search the user in the database
    user_repo = UserRepository(db)
    user = await user_repo.get(user_id)
    if user is None or not user.status:
        raise UnauthorizedException(detail="User not found or not active")
    return user


def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise ForbiddenException(detail="The user doesn't have enough privileges")
    return current_user