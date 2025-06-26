from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.admin import services
from app.database.db_helper import get_session
from app.database.models import User, Country
from app.schemas.user import (
    CountryAddResponseSchema,
    CountryCreateSchema,
    VisitedResponseSchema,
)
from app.utils.jwt import require_role

from app.utils.countries import fetch_countries


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post("/add-countries", response_model=CountryAddResponseSchema)
async def add_countries(
    cnts: list[CountryCreateSchema],
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("admin")),
):
    return await services.add_countries(session, current_user, cnts)


@router.post("/add-countries-all", response_model=CountryAddResponseSchema)
async def add_countries_all(
    cnts: list[Country] = Depends(fetch_countries),
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("admin")),
):
    return await services.add_countries_all(session, current_user, cnts)
