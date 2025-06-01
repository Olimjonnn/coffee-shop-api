import asyncio
from datetime import datetime, timedelta
from app.db.session import async_session
from app.models.users import User
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


async def delete_unverified_users_async():
    async with async_session() as session:
        async with session.begin():
            threshold_date = datetime.utcnow() - timedelta(days=2)
            stmt = delete(User).where(
                User.is_verified == False,
                User.created_at < threshold_date
            )
            result = await session.execute(stmt)
            return f"Deleted {result.rowcount} unverified users"

def delete_unverified_users():
    return asyncio.run(delete_unverified_users_async())