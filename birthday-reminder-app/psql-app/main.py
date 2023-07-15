from datetime import datetime
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.put("/hello/{name}", response_model=None, status_code=204)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db=db, user=user)


@app.get("/hello/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/hello/{name}", response_model=Optional[str])
def read_user(name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, name=name)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    today = datetime.now().date()
    birthday = datetime.strptime(db_user.bday, "%Y-%m-%d").date()
    next_birthday = birthday.replace(year=today.year)

    if today.month == birthday.month and today.day == birthday.day:
        message = f"Hi, {name}! Happy birthday!"
    else:
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year+1)
        days_to_birthday = (next_birthday - today).days
        message = f"Hi, {name}! Your B-Day is in {days_to_birthday} day(s)"

    return message
