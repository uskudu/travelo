from pydantic import BaseModel, ConfigDict

from app.schemas.jwt import TokenSchema


class ReviewsSchema(BaseModel):
    review_id: int
    text: str = ""
    user_id: str
    country_id: int
    likes: int = 0
    dislikes: int = 0


class VisitedSchema(BaseModel):
    visited_id: int
    user_id: str
    country_id: int
    review_id: int = ""


class FavouriteSchema(BaseModel):
    favourite_id: int
    user_id: str
    country_id: int


class WishlistSchema(BaseModel):
    wishlist_id: int
    user_id: str
    country_id: int


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


class CountryCreateSchema(CountrySchema):
    pass


class CountryAddResponseSchema(BaseModel):
    msg: str
