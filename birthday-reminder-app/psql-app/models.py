from sqlalchemy import Column, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    name = Column(String, primary_key=True)
    bday = Column(String)
