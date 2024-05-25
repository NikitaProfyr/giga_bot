from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    user_name: str
    tg_channel_id: str


class UserCreateSchema(UserSchema):
    status_chat: str
