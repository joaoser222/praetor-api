from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def commit(self):
        """Commits the current transaction."""
        await self.db.commit()

    async def rollback(self):
        """Rolls back the current transaction."""
        await self.db.rollback()

    async def refresh(self, instance: object):
        """Refreshes the state of the given instance from the database."""
        await self.db.refresh(instance)