from pydantic import BaseModel, Field


class User(BaseModel):
    class Config:
        orm_mode = True
    name: str
    bday: str = Field(..., pattern="^\\d{4}-\\d{2}-\\d{2}$")


class StringResponse:
    message: str
