from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User


async def get_user_by_id_or_name(
    session: AsyncSession,
    identifier: str,
) -> User:
    stmt = await session.execute(select(User).where(User.user_id == identifier))
    res = stmt.scalar_one_or_none()
    if not res:
        stmt = await session.execute(select(User).where(User.username == identifier))
        res = stmt.scalar_one_or_none()
    return res
