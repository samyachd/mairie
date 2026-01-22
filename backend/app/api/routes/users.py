import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.core.constants import PAGINATION_LIMIT_DEFAULT, PAGINATION_SKIP_DEFAULT
from backend.app.db.models import User
from backend.app.db.session import get_db
from backend.app.schemas.users import UserCreate, UserRead, UserUpdate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = User(**user.model_dump(exclude_unset=True))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created: {db_user.id}")
        return db_user
    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        raise HTTPException(status_code=400, detail="Error creating user")


@router.get("/", response_model=list[UserRead])
def read_users(
    skip: int = PAGINATION_SKIP_DEFAULT,
    limit: int = PAGINATION_LIMIT_DEFAULT,
    db: Session = Depends(get_db),
):
    users = db.query(User).offset(skip).limit(limit).all()
    logger.debug(f"Retrieved {len(users)} users")
    return users


@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"Delete user not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    logger.info(f"User deleted: {user_id}")
    return None


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        logger.warning(f"Update user not found: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    data = user.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    logger.info(f"User updated: {user_id}")
    return db_user