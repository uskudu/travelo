from pydantic import BaseModel, ConfigDict

from app.schemas.jwt import TokenSchema


class ReviewsSchema(BaseModel):
    review_id: int
    text: str = ""
    user_id: str
    country_id: int
    likes: int = 0
    dislikes: int = 0

    model_config = ConfigDict(from_attributes=True)


class VisitedSchema(BaseModel):
    visited_id: int
    user_id: str
    country_id: int
    review_id: int | None = None

    model_config = ConfigDict(from_attributes=True)


class FavouriteSchema(BaseModel):
    favourite_id: int
    user_id: str
    country_id: int

    model_config = ConfigDict(from_attributes=True)


class WishlistSchema(BaseModel):
    wishlist_id: int
    user_id: str
    country_id: int

    model_config = ConfigDict(from_attributes=True)


class UserFullSchema(BaseModel):
    username: str
    role: str
    reviews: list[ReviewsSchema]
    visited: list[VisitedSchema]
    favourite: list[FavouriteSchema]
    wishlist: list[WishlistSchema]

    model_config = ConfigDict(from_attributes=True)


class UserSchema(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserResponseSchema(BaseModel):
    user: UserSchema

    model_config = ConfigDict(from_attributes=True)


class UserSignUpSchema(UserSchema):
    pass


class UserSignUpResponseSchema(BaseModel):
    msg: str

    model_config = ConfigDict(from_attributes=True)


class UserSignInSchema(UserSchema):
    pass


class UserSignInResponseSchema(BaseModel):
    msg: str
    token: TokenSchema

    model_config = ConfigDict(from_attributes=True)


class CountrySchema(BaseModel):
    iso2: str
    title: str
    flag: str

    model_config = ConfigDict(from_attributes=True)


class CountryCreateSchema(CountrySchema):
    pass


class CountryAddResponseSchema(BaseModel):
    msg: str


class VisitedResponseSchema(VisitedSchema):
    pass


class FavouriteResponseSchema(FavouriteSchema):
    pass


class WishlistResponseSchema(WishlistSchema):
    pass


class VisitedGetSchema(BaseModel):
    id: int
    country: CountrySchema
    review: str | None = None

    model_config = ConfigDict(from_attributes=True)


class FavouriteGetSchema(BaseModel):
    id: int
    country: CountrySchema

    model_config = ConfigDict(from_attributes=True)


class WishlistGetSchema(BaseModel):
    id: int
    country: CountrySchema

    model_config = ConfigDict(from_attributes=True)


class UserNiceResponseSchema(BaseModel):
    username: str
    # reviews: list[ReviewsNiceResponseSchema]
    visited: list[VisitedGetSchema]
    favourite: list[FavouriteGetSchema]
    wishlist: list[WishlistGetSchema]

    model_config = ConfigDict(from_attributes=True)
