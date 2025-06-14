from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenDataSchema(BaseModel):
    user_id: str | None = None
