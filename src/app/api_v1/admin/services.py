from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, Country
from app.schemas.user import (
    CountryAddResponseSchema,
    CountryCreateSchema,
)


async def add_countries(
    session: AsyncSession,
    current_user: User,
    cnts: list[CountryCreateSchema],
) -> CountryAddResponseSchema:
    cnts = [Country(**cnt.model_dump()) for cnt in cnts]
    session.add_all(cnts)
    await session.commit()
    return CountryAddResponseSchema(msg="countries successfully added")


async def add_countries_all(
    session: AsyncSession,
    current_user: User,
    countries: list,
) -> CountryAddResponseSchema:
    cnts = [Country(**cnt) for cnt in countries]
    session.add_all(cnts)
    await session.commit()
    return CountryAddResponseSchema(msg="countries successfully added")
