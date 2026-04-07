from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import require_role
from schemas.office_license import OfficeLicenseCreate, OfficeLicenseRead, OfficeLicenseUpdate
from db.session import get_db
from db.models.office_license import OfficeLicense

router = APIRouter(dependencies=[Depends(require_role("user","admin"))])

@router.post("/", response_model=OfficeLicenseRead, status_code=status.HTTP_201_CREATED)
def create_license(license: OfficeLicenseCreate, db: Session = Depends(get_db)):
    db_license = OfficeLicense(**license.model_dump(exclude_unset=True))
    db.add(db_license)
    db.commit()
    db.refresh(db_license)
    return db_license

@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(license_id: int, db: Session = Depends(require_role(get_db))):
    db_license = db.query(OfficeLicense).filter(OfficeLicense.id == license_id).first()
    if not db_license:
        raise HTTPException(status_code=404, detail="License not found")
    db.delete(db_license)
    db.commit()
    return None

@router.put("/{license_id}", response_model=OfficeLicenseRead)
def update_license(license_id: int, license: OfficeLicenseUpdate, db: Session = Depends(require_role(get_db))):
    db_license = db.query(OfficeLicense).filter(OfficeLicense.id == license_id).first()
    if not db_license:
        raise HTTPException(status_code=404, detail="License not found")

    data = license.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_license, key, value)

    db.commit()
    db.refresh(db_license)
    return db_license