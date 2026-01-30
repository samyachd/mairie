from fastapi import APIRouter, Depends, HTTPException, status
from core.dependencies import get_current_user
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.ordinateurs_schemas import PCCreate, PCRead, PCUpdate
from db.session import get_db
from db.models import Ordinateurs

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=PCRead, status_code=status.HTTP_201_CREATED)
def create_pc(pc: PCCreate, db: Session = Depends(get_db)):
    db_pc = Ordinateurs(**pc.model_dump(exclude_unset=True))
    db.add(db_pc)
    try:
        db.commit()
        db.refresh(db_pc)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un PC avec ce tag, IP ou MAC existe déjà"
        )
    return db_pc

@router.get("/", response_model=list[PCRead])
def read_pcs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    pcs = db.query(Ordinateurs).offset(skip).limit(limit).all()
    return pcs

@router.get("/{pc_id}", response_model=PCRead)
def read_pc(pc_id: int, db: Session = Depends(get_db)):
    db_pc = db.query(Ordinateurs).filter(Ordinateurs.id == pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PC inexistant")
    return db_pc

@router.delete("/{pc_id}")
def delete_pc(pc_id: int, db: Session = Depends(get_db)):
    db_pc = db.query(Ordinateurs).filter(Ordinateurs.id == pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PC inexistant")
    db.delete(db_pc)
    db.commit()
    return None

@router.put("/{pc_id}", response_model=PCRead)
def update_pc(pc_id: int, pc: PCUpdate, db: Session = Depends(get_db)):
    db_pc = db.query(Ordinateurs).filter(Ordinateurs.id == pc_id).first()
    if not db_pc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PC inexistant")
    
    data = pc.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_pc, key, value)

    db.commit()
    db.refresh(db_pc)
    return db_pc