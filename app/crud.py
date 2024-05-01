from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_kakao_id(db: Session, kakao_id: str):
    return db.query(models.User).filter(models.User.kakao_id == kakao_id).first()

def create_user(db: Session, user_data: schemas.UserCreate):
    db_user = models.User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
