from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import require_role
from schemas import (
    OfficeLicenceCreate, OfficeLicenceRead, OfficeLicenceUpdate,
    AgentRead, AgentCreate, AgentUpdate,
    OrdinateurCreate, OrdinateurRead, OrdinateurUpdate,
    EcranCreate, EcranRead, EcranUpdate,
    DocumentCreate, DocumentRead, DocumentUpdate,
    InventaireRead,
)
from db.session import get_db
from db.models import OfficeLicence, Ordinateur, Ecran, Agent, Document
from core import logger
from sqlalchemy.exc import IntegrityError

inventaire = APIRouter(dependencies=[Depends(require_role("read", "user", "admin"))])
agent = APIRouter(dependencies=[Depends(require_role("user", "admin"))])
ordinateur = APIRouter(dependencies=[Depends(require_role("user", "admin"))])
ecran = APIRouter(dependencies=[Depends(require_role("user", "admin"))])
licence = APIRouter(dependencies=[Depends(require_role("user", "admin"))])
document = APIRouter(dependencies=[Depends(require_role("user", "admin"))])


# Inventaire — single fetch for the whole inventory page

@inventaire.get("/", response_model=InventaireRead)
def read_inventaire(db: Session = Depends(get_db)):
    return InventaireRead(
        agents=db.query(Agent).all(),
        ordinateurs=db.query(Ordinateur).all(),
        ecrans=db.query(Ecran).all(),
        licences=db.query(OfficeLicence).all(),
        documents=db.query(Document).all(),
    )


# Agent endpoints

@agent.post("/", response_model=AgentRead, status_code=status.HTTP_201_CREATED)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    db_agent = Agent(**agent.model_dump(exclude_unset=True))
    db.add(db_agent)
    try:
        db.commit()
        db.refresh(db_agent)
        logger.info(f"Agent créé avec succès - {agent.email}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: agent existe déjà - {agent.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un agent avec cet email existe déjà",
        )
    return db_agent


@agent.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent introuvable")
    db.delete(db_agent)
    db.commit()
    return


@agent.put("/{agent_id}", response_model=AgentRead)
def update_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent introuvable")
    for key, value in agent.model_dump(exclude_unset=True).items():
        setattr(db_agent, key, value)
    db.commit()
    db.refresh(db_agent)
    return db_agent


# Ordinateur endpoints

@ordinateur.post("/", response_model=OrdinateurRead, status_code=status.HTTP_201_CREATED)
def create_ordinateur(ordinateur: OrdinateurCreate, db: Session = Depends(get_db)):
    db_ordinateur = Ordinateur(**ordinateur.model_dump(exclude_unset=True))
    db.add(db_ordinateur)
    try:
        db.commit()
        db.refresh(db_ordinateur)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un ordinateur avec ce tag, IP ou MAC existe déjà",
        )
    return db_ordinateur


@ordinateur.delete("/{ordinateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ordinateur(ordinateur_id: int, db: Session = Depends(get_db)):
    db_ordinateur = db.query(Ordinateur).filter(Ordinateur.id == ordinateur_id).first()
    if not db_ordinateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordinateur inexistant")
    db.delete(db_ordinateur)
    db.commit()
    return None


@ordinateur.put("/{ordinateur_id}", response_model=OrdinateurRead)
def update_ordinateur(ordinateur_id: int, ordinateur: OrdinateurUpdate, db: Session = Depends(get_db)):
    db_ordinateur = db.query(Ordinateur).filter(Ordinateur.id == ordinateur_id).first()
    if not db_ordinateur:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordinateur inexistant")
    for key, value in ordinateur.model_dump(exclude_unset=True).items():
        setattr(db_ordinateur, key, value)
    db.commit()
    db.refresh(db_ordinateur)
    return db_ordinateur


# Office Licence endpoints

@licence.post("/", response_model=OfficeLicenceRead, status_code=status.HTTP_201_CREATED)
def create_license(license: OfficeLicenceCreate, db: Session = Depends(get_db)):
    db_licence = OfficeLicence(**license.model_dump(exclude_unset=True))
    db.add(db_licence)
    try:
        db.commit()
        db.refresh(db_licence)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une licence avec ces caractéristiques existe déjà",
        )
    return db_licence


@licence.delete("/{licence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(licence_id: int, db: Session = Depends(get_db)):
    db_licence = db.query(OfficeLicence).filter(OfficeLicence.id == licence_id).first()
    if not db_licence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Licence inexistante")
    db.delete(db_licence)
    db.commit()
    return None


@licence.put("/{licence_id}", response_model=OfficeLicenceRead)
def update_license(licence_id: int, licence: OfficeLicenceUpdate, db: Session = Depends(get_db)):
    db_licence = db.query(OfficeLicence).filter(OfficeLicence.id == licence_id).first()
    if not db_licence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Licence inexistante")
    for key, value in licence.model_dump(exclude_unset=True).items():
        setattr(db_licence, key, value)
    db.commit()
    db.refresh(db_licence)
    return db_licence


# Ecran endpoints

@ecran.post("/", response_model=EcranRead, status_code=status.HTTP_201_CREATED)
def create_ecran(ecran: EcranCreate, db: Session = Depends(get_db)):
    db_ecran = Ecran(**ecran.model_dump(exclude_unset=True))
    db.add(db_ecran)
    try:
        db.commit()
        db.refresh(db_ecran)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un écran avec ce tag existe déjà",
        )
    return db_ecran


@ecran.delete("/{ecran_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ecran(ecran_id: int, db: Session = Depends(get_db)):
    db_ecran = db.query(Ecran).filter(Ecran.id == ecran_id).first()
    if not db_ecran:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ecran inexistant")
    db.delete(db_ecran)
    db.commit()
    return None


@ecran.put("/{ecran_id}", response_model=EcranRead)
def update_ecran(ecran_id: int, ecran: EcranUpdate, db: Session = Depends(get_db)):
    db_ecran = db.query(Ecran).filter(Ecran.id == ecran_id).first()
    if not db_ecran:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ecran inexistant")
    for key, value in ecran.model_dump(exclude_unset=True).items():
        setattr(db_ecran, key, value)
    db.commit()
    db.refresh(db_ecran)
    return db_ecran


# Document endpoints (unified — type field discriminates devis / BC / facture)

@document.post("/", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
def create_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    db_doc = Document(**doc.model_dump(exclude_unset=True))
    db.add(db_doc)
    try:
        db.commit()
        db.refresh(db_doc)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Document invalide (contraintes violées)",
        )
    return db_doc


@document.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document inexistant")
    db.delete(db_doc)
    db.commit()
    return None


@document.put("/{document_id}", response_model=DocumentRead)
def update_document(document_id: int, doc: DocumentUpdate, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document inexistant")
    for key, value in doc.model_dump(exclude_unset=True).items():
        setattr(db_doc, key, value)
    db.commit()
    db.refresh(db_doc)
    return db_doc
