from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, CheckConstraint

import uuid


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "countries"
    country_id: Mapped[int] = mapped_column(primary_key=True)
    iso2: Mapped[str]
    title: Mapped[str]
    flag: Mapped[str]


class User(Base):
    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid.uuid4())
    )
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")

    reviews: Mapped[list["Reviews"]] = relationship(back_populates="user")
    visited: Mapped[list["Visited"]] = relationship(back_populates="user")
    favourite: Mapped[list["Favourite"]] = relationship(back_populates="user")
    wishlist: Mapped[list["Wishlist"]] = relationship(back_populates="user")

    def to_dict(self):
        username = self.username
        role = self.role
        reviews = self.reviews
        visited = self.visited
        favourite = self.favourite
        wishlist = self.wishlist


class Reviews(Base):
    __tablename__ = "reviews"
    review_id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str]
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.country_id", ondelete="CASCADE")
    )
    likes: Mapped[int]
    dislikes: Mapped[int]

    user: Mapped["User"] = relationship(back_populates="reviews")

    __table_args__ = (
        CheckConstraint("likes >= 0"),
        CheckConstraint("dislikes >= 0"),
    )


class Visited(Base):
    __tablename__ = "visited"
    visited_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.country_id", ondelete="CASCADE")
    )
    review_id: Mapped[str] = mapped_column(
        ForeignKey("reviews.review_id", ondelete="CASCADE"),
        nullable=True,
    )

    user: Mapped["User"] = relationship(back_populates="visited")


class Favourite(Base):
    __tablename__ = "favourite"
    favourite_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.country_id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="favourite")


class Wishlist(Base):
    __tablename__ = "wishlist"
    wishlist_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE")
    )
    country_id: Mapped[int] = mapped_column(
        ForeignKey("countries.country_id", ondelete="CASCADE")
    )

    user: Mapped["User"] = relationship(back_populates="wishlist")
