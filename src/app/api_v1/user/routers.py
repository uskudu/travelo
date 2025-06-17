from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.user import services
from app.database.db_helper import get_session
from app.database.models import User, Country
from app.schemas.jwt import TokenSchema
from app.schemas.user import (
    UserSignUpSchema,
    UserSignUpResponseSchema,
    UserFullSchema,
    CountryAddResponseSchema,
    CountrySchema,
    CountryCreateSchema,
)
from app.utils.jwt import get_current_user, require_role

from app.utils.countries import fetch_countries


router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/sign-up", response_model=UserSignUpResponseSchema)
async def sign_up(
    session: Annotated[AsyncSession, Depends(get_session)],
    data: UserSignUpSchema,
) -> UserSignUpResponseSchema:
    return await services.sign_up(session, data)


@router.post("/token", response_model=TokenSchema)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    return await services.token(form_data, session)


@router.get("/me", response_model=UserFullSchema)
async def get_me(
    current_user: Annotated[User, Depends(get_current_user)],
    session: AsyncSession = Depends(get_session),
):
    return await services.get_me(session, current_user)


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
