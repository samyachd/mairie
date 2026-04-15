from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.dependencies import require_role
from db.models import Log

log = APIRouter(dependencies=[Depends(require_role("admin"))])

@log.get("/")
def get_logs(
    db: Session = Depends(get_db)):
    return db.query(Log).order_by(Log.timestamp.desc()).all()

@log.get("/user/{user_id}")
def get_logs_par_user(
    user_id: int,
    db: Session = Depends(get_db)):
    return db.query(Log).filter(Log.user_id == user_id).order_by(Log.timestamp.desc()).all()

@log.get("/table/{table_cible}")
def get_logs_par_table(
    table_cible: str,
    db: Session = Depends(get_db)):
    return db.query(Log).filter(Log.table_cible == table_cible).order_by(Log.timestamp.desc()).all()