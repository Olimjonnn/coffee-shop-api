from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from sqlalchemy.future import select


class UserService:

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: str) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()