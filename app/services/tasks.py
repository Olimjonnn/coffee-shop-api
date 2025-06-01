from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete
from app.models.users import User
from app.db.session import async_session
from app.core.config import settings
from celery_worker import celery_app


@celery_app.task(name='app.services.tasks.cleanup_unverified_users')
def cleanup_unverified_users():
    import asyncio
    async def _cleanup():
        async with async_session() as session:
            cutoff_date = datetime.utcnow() - timedelta(days=2)
            stmt = delete(User).where(
                User.is_verified == False,
                User.created_at < cutoff_date
            )
            await session.execute(stmt)
            await session.commit()
    asyncio.run(_cleanup())


