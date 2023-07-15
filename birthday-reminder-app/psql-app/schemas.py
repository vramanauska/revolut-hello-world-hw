from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: str
    bday: str


class UserCreate(UserBase):
    bday: str = Field(..., pattern="^\\d{4}-\\d{2}-\\d{2}$")
    pass


class User(UserBase):
    class Config:
        orm_mode = True


class StringResponse:
    message: str
