import asyncio

from app.database.models import *
from app.database.db_helper import get_session

from app.utils.countries import countries


async def seed_countries(session):
    cnts = [Country(**cnt) for cnt in countries]
    session.add_all(cnts)
    await session.commit()


async def main():
    async for session in get_session():
        await seed_countries(session)
        print("sxs")


asyncio.run(main())
