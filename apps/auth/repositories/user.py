from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.base_repository import BaseRepository
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return await self.get_by_field("email", email)

    async def get_by_username(self, username: str) -> Optional[User]:
        """Get a user by username."""
        return await self.get_by_field("username", username)

    async def get_active_users(self) -> List[User]:
        """Get all active users."""
        query = select(self.model).where(self.model.is_active == True)
        result = await self.db.execute(query)
        return result.scalars().all()