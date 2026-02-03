from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import get_current_user
from schemas.officelicenses_schemas import LicenseCreate, LicenseRead, LicenseUpdate
from db.session import get_db
from db.models import OfficeLicenses

router = APIRouter(dependencies=[Depends(get_current_user)])

@router.post("/", response_model=LicenseRead, status_code=status.HTTP_201_CREATED)
def create_license(license: LicenseCreate, db: Session = Depends(get_db)):
    db_license = OfficeLicenses(**license.model_dump(exclude_unset=True))
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

@router.get("/", response_model=list[LicenseRead])
def read_licenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    licenses = db.query(OfficeLicenses).offset(skip).limit(limit).all()
    return licenses

@router.get("/{license_id}", response_model=LicenseRead)
def read_license(license_id: int, db: Session = Depends(get_db)):
    db_license = db.query(OfficeLicenses).filter(OfficeLicenses.id == license_id).first()
    return db_license

@router.delete("/{license_id}")
def delete_license(license_id: int, db: Session = Depends(get_db)):
    db_license = db.query(OfficeLicenses).filter(OfficeLicenses.id == license_id).first()
    if not db_license:
        raise HTTPException(status_code=404, detail="License not found")
    db.delete(db_license)
    db.commit()
    return None

@router.put("/{license_id}", response_model=LicenseRead)
def update_license(license_id: int, license: LicenseUpdate, db: Session = Depends(get_db)):
    db_license = db.query(OfficeLicenses).filter(OfficeLicenses.id == license_id).first()
    if not db_license:
        raise HTTPException(status_code=404, detail="License not found")

    data = license.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_license, key, value)

    db.commit()
    db.refresh(db_license)
    return db_license