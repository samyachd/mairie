from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.users import  UserCreate, UserRead, UserUpdate
from app.db.session import get_db
from app.db.models import Users

router = APIRouter()

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = Users(**user.model_dump(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=list[UserRead])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(Users).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserRead).filter(UserRead.id == user_id).first()
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None

@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(Users).filter(Users.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    data = user.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user