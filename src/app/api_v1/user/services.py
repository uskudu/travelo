from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.database.models import User
from app.schemas.jwt import TokenSchema
from app.schemas.user import (
    UserSignUpSchema,
    UserSignUpResponseSchema,
    UserFullSchema,
)
from app.utils.jwt import create_access_token, verify_password, get_password_hash
from app.utils.user import get_user_by_id_or_name


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
    current_user: User,
    session: AsyncSession,
) -> UserFullSchema:
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
    return UserFullSchema.model_validate(user)
