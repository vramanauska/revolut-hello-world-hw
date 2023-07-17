from sqlalchemy.orm import Session

from . import models, schemas


def get_user_by_username(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.User):
    db_username = models.User(name=user.name, bday=user.bday)
    db.add(db_username)
    db.commit()
    db.refresh(db_username)
    return db_username
