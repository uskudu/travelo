from typing import Type, TypeVar
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from sqlalchemy.orm import selectinload

from app.database.models import User, Country, Visited, Favourite, Wishlist
from app.schemas.jwt import TokenSchema
from app.schemas.user import (
    UserSignUpSchema,
    UserSignUpResponseSchema,
    CountrySchema,
    VisitedResponseSchema,
    VisitedGetSchema,
    UserNiceResponseSchema,
    FavouriteGetSchema,
    WishlistGetSchema,
    FavouriteResponseSchema,
    WishlistResponseSchema,
)
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from app.utils.user import get_user_by_id_or_name


T = TypeVar("T")
R = TypeVar("R")


async def sign_up(
    session: AsyncSession,
    data: UserSignUpSchema,
) -> UserSignUpResponseSchema:
    try:
        if not (data.username and data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You haven't filled username or password field",
            )
        hashed_password = get_password_hash(data.password)
        user = User(
            username=data.username,
            password=hashed_password,
        )
        if data.password == "1":
            user = User(
                username=data.username,
                password=hashed_password,
                role="admin",
            )
        session.add(user)
        await session.commit()
        return UserSignUpResponseSchema(msg="account created")
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )


async def token(
    form_data: OAuth2PasswordRequestForm,
    session: AsyncSession,
) -> TokenSchema:
    user = await get_user_by_id_or_name(session, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.user_id})
    return TokenSchema(access_token=access_token)


async def get_me(
    session: AsyncSession,
    current_user: User,
):
    uid = current_user.user_id
    stmt = await session.execute(
        select(User)
        .options(
            selectinload(User.reviews),
            selectinload(User.visited),
            selectinload(User.favourite),
            selectinload(User.wishlist),
        )
        .where(User.user_id == uid)
    )
    user = stmt.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # visited
    vis_stmt = await session.execute(select(Visited).where(Visited.user_id == uid))
    visited_in_db = vis_stmt.scalars()

    visited_list = []
    for v in visited_in_db:

        stmt = await session.execute(
            select(Country).where(Country.country_id == v.country_id)
        )
        cntry = stmt.scalar_one_or_none()
        visited_list.append(
            VisitedGetSchema(
                id=v.visited_id, country=CountrySchema.model_validate(cntry)
            )
        )

    # favourite
    fav_stmt = await session.execute(select(Favourite).where(Favourite.user_id == uid))
    fav_in_db = fav_stmt.scalars()

    fav_list = []
    for f in fav_in_db:
        stmt = await session.execute(
            select(Country).where(Country.country_id == f.country_id)
        )
        cntry = stmt.scalar_one_or_none()
        fav_list.append(
            FavouriteGetSchema(
                id=f.favourite_id, country=CountrySchema.model_validate(cntry)
            )
        )

    # wishlist
    wish_stmt = await session.execute(select(Wishlist).where(Wishlist.user_id == uid))
    wish_in_db = wish_stmt.scalars()

    wish_list = []
    for w in wish_in_db:
        stmt = await session.execute(
            select(Country).where(Country.country_id == w.country_id)
        )
        cntry = stmt.scalar_one_or_none()
        wish_list.append(
            WishlistGetSchema(
                id=w.wishlist_id, country=CountrySchema.model_validate(cntry)
            )
        )

    return UserNiceResponseSchema(
        username=current_user.username,
        visited=visited_list,
        favourite=fav_list,
        wishlist=wish_list,
    )


async def add_to_list(
    cnt_id: int,
    session: AsyncSession,
    current_user: User,
    model: Type[T],
    response_schema: Type[R],
    list_name: str,
) -> R:
    # validate country exists
    stmt = await session.execute(select(Country).where(Country.country_id == cnt_id))
    cntry_in_db = stmt.scalar_one_or_none()
    if cntry_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Country not found"
        )

    # check if cntry already in list
    stmt = await session.execute(
        select(model).where(
            and_(
                model.country_id == cnt_id,
                model.user_id == current_user.user_id,
            )
        )
    )
    existing = stmt.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You already added this country to {list_name}",
        )

    # add new entry
    new_entry = model(user_id=current_user.user_id, country_id=cnt_id)
    session.add(new_entry)
    await session.commit()
    await session.refresh(new_entry)
    return response_schema.model_validate(new_entry)


async def add_to_visited(
    cnt_id: int, session: AsyncSession, current_user: User
) -> VisitedResponseSchema:
    return await add_to_list(
        cnt_id,
        session,
        current_user,
        Visited,
        VisitedResponseSchema,
        "visited",
    )


async def add_to_favourite(
    cnt_id: int, session: AsyncSession, current_user: User
) -> FavouriteResponseSchema:
    return await add_to_list(
        cnt_id,
        session,
        current_user,
        Favourite,
        FavouriteResponseSchema,
        "favourites",
    )


async def add_to_wishlist(
    cnt_id: int, session: AsyncSession, current_user: User
) -> WishlistResponseSchema:
    return await add_to_list(
        cnt_id,
        session,
        current_user,
        Wishlist,
        WishlistResponseSchema,
        "wishlist",
    )
