from sqlalchemy.ext.asyncio import AsyncSession

from config.security import (
    create_access_token,
    get_password_hash,
    verify_password,
    generate_opaque_token,
    get_opaque_refresh_token_expiry,
)
from core.base_service import BaseService
from core.exceptions import UnauthorizedException, ValidationException
from ..models import User
from ..repositories.user import UserRepository
from ..repositories.token import TokenRepository
from ..schemas.user import UserCreate

class UserService(BaseService):
    def __init__(self, db: AsyncSession):
        super().__init__(db)
        self.repo = UserRepository(db)
        self.token_repo = TokenRepository(db)

    async def create_user(self, user_in: UserCreate) -> User:
        """Creates a new user."""
        if await self.repo.get_by_email(user_in.email):
            raise ValidationException(detail="Email already registered")
        if await self.repo.get_by_username(user_in.username):
            raise ValidationException(detail="Username already taken")
            
        hashed_password = get_password_hash(user_in.password)
        user_data = user_in.model_dump(exclude={"password"})
        user_data["hashed_password"] = hashed_password
        
        # Manually create the model instance to use hashed_password
        db_user = User(**user_data)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def authenticate_user(self, email: str, password: str) -> dict:
        """
        Authenticates a user and returns tokens using the hybrid model.
        
        Hybrid Model:
        - Access Token: JWT (stateless, performático, sem consulta ao banco)
        - Refresh Token: Opaque no banco (pode ser revogado facilmente)
        
        This combines the best of both worlds:
        - Performance: JWT access tokens don't require database lookups
        - Security: Refresh tokens can be revoked by removing from database
        
        Args:
            email: User email
            password: User password
        
        Returns:
            dict with access_token (JWT), refresh_token (opaque), token_type and auth_type
        """
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedException(detail="Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedException(detail="Inactive user")

        # Generate JWT access token (stateless, performático)
        token_data = {"sub": str(user.id)}
        access_token = create_access_token(data=token_data)
        
        # Generate refresh token (armazenado no banco, pode ser revogado)
        refresh_token_value = generate_opaque_token()
        await self.token_repo.create_token(
            token=refresh_token_value,
            user_id=user.id,
            expires_at=get_opaque_refresh_token_expiry()
        )
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token_value,
            "token_type": "bearer",
            "auth_type": "hybrid"
        }

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refreshes an access token using a refresh token.
        
        This method validates the opaque refresh token stored in the database
        and generates a new JWT access token.
        
        Args:
            refresh_token: The opaque refresh token
        
        Returns:
            dict with new access_token, refresh_token, token_type and auth_type
        
        Raises:
            UnauthorizedException: If refresh token is invalid, expired, or revoked
        """
        # Validate refresh token in database
        token_repo = TokenRepository(self.db)
        db_token = await token_repo.get_by_token(refresh_token)
        
        if not db_token:
            raise UnauthorizedException(detail="Refresh token not found")
        
        if not db_token.is_active:
            raise UnauthorizedException(detail="Refresh token has been revoked")
        
        # Check expiration
        from datetime import datetime, timezone
        if db_token.expires_at < datetime.now(timezone.utc):
            raise UnauthorizedException(detail="Refresh token has expired")
        
        # Get user
        user = await self.repo.get(db_token.user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(detail="User not found or inactive")
        
        # Revoke old refresh token (token rotation for security)
        await token_repo.revoke_token(refresh_token)
        
        # Generate new JWT access token
        token_data = {"sub": str(user.id)}
        new_access_token = create_access_token(data=token_data)
        
        # Generate new refresh token
        new_refresh_token_value = generate_opaque_token()
        await token_repo.create_token(
            token=new_refresh_token_value,
            user_id=user.id,
            expires_at=get_opaque_refresh_token_expiry()
        )
        
        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token_value,
            "token_type": "bearer",
            "auth_type": "hybrid"
        }

    async def logout(self, refresh_token: str) -> dict:
        """
        Logout user by revoking the refresh token.
        
        This invalidates the refresh token, preventing it from being used
        to generate new access tokens. The current access token will remain
        valid until it expires (short-lived JWT).
        
        Args:
            refresh_token: The refresh token to revoke
        
        Returns:
            dict with success message
        
        Raises:
            UnauthorizedException: If refresh token is invalid
        """
        token_repo = TokenRepository(self.db)
        revoked = await token_repo.revoke_token(refresh_token)
        
        if not revoked:
            raise UnauthorizedException(detail="Invalid refresh token")
        
        return {"message": "Successfully logged out"}

    async def logout_all_sessions(self, user_id: int) -> dict:
        """
        Logout user from all sessions by revoking all refresh tokens.
        
        This is useful for security purposes (e.g., password change,
        suspicious activity, or admin action).
        
        Args:
            user_id: The user ID to revoke all tokens for
        
        Returns:
            dict with count of revoked tokens
        """
        token_repo = TokenRepository(self.db)
        count = await token_repo.revoke_user_tokens(user_id=user_id)
        
        return {
            "message": f"Successfully logged out from {count} session(s)",
            "revoked_sessions": count
        }