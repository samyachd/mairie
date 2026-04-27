from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import require_role
from schemas import (OfficeLicenceCreate, OfficeLicenceRead, OfficeLicenceUpdate,
                     AgentRead, AgentCreate, AgentUpdate,
                      OrdinateurCreate, OrdinateurRead, OrdinateurUpdate, 
                      EcranCreate, EcranRead, EcranUpdate, 
                      DevisRead, BonDeCommandeRead, FactureRead, InventaireRead)
from db.session import get_db
from db.models import OfficeLicence, Ordinateur, Ecran, Devis, BonDeCommande, Facture, Agent
from core import logger
from sqlalchemy.exc import IntegrityError

inventaire = APIRouter(dependencies=[Depends(require_role("user","admin"))])
agent = APIRouter(dependencies=[Depends(require_role("user","admin"))])
ordinateur = APIRouter(dependencies=[Depends(require_role("user","admin"))])
ecran = APIRouter(dependencies=[Depends(require_role("user","admin"))])
licence = APIRouter(dependencies=[Depends(require_role("user","admin"))])
devis = APIRouter(dependencies=[Depends(require_role("user","admin"))])
bon_de_commande = APIRouter(dependencies=[Depends(require_role("user","admin"))])
facture = APIRouter(dependencies=[Depends(require_role("user","admin"))])

# Inventaire endpoint : on charge tout l'inventaire en une seule requête pour éviter les multiples appels depuis le frontend

@inventaire.get("/", response_model=InventaireRead)
def read_inventaire(db: Session = Depends(get_db)):
    return InventaireRead(
        agents=db.query(Agent).all(),
        ordinateurs=db.query(Ordinateur).all(),
        ecrans=db.query(Ecran).all(),
        licences=db.query(OfficeLicence).all(),  # ← clé adaptée selon ton choix
        devis=db.query(Devis).all(),
        bons_de_commande=db.query(BonDeCommande).all(),
        factures=db.query(Facture).all(),
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
        logger.warning(f"IntegrityError: Un agent avec cet email existe déjà - {agent.email}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un agent avec ce email existe déjà"
        )
    return db_agent

@agent.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        logger.warning(f"Agent avec l'ID {agent_id} non trouvé pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    db.delete(db_agent)
    db.commit()
    logger.info(f"Agent {agent_id} supprimé avec succès")
    return

@agent.put("/{agent_id}", response_model=AgentRead)
def update_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db)):
    db_agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not db_agent:
        logger.warning(f"Agent avec l'ID {agent_id} non trouvé")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agent not found")
    for key, value in agent.dict(exclude_unset=True).items():
        setattr(db_agent, key, value)
    db.commit()
    db.refresh(db_agent)
    logger.info(f"Agent {agent_id} mis à jour avec succès")
    return db_agent

# Ordinateur endpoints

@ordinateur.post("/", response_model=OrdinateurRead, status_code=status.HTTP_201_CREATED)
def create_ordinateur(ordinateur: OrdinateurCreate, db: Session = Depends(get_db)):
    db_ordinateur = Ordinateur(**ordinateur.model_dump(exclude_unset=True))
    db.add(db_ordinateur)
    try:
        db.commit()
        db.refresh(db_ordinateur)
        logger.info(f"Ordinateur créé avec succès - {ordinateur.tag}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: Un ordinateur avec ce tag, IP ou MAC existe déjà - {ordinateur}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un ordinateur avec ce tag, IP ou MAC existe déjà"
        )
    return db_ordinateur

@ordinateur.delete("/{ordinateur_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ordinateur(ordinateur_id: int, db: Session = Depends(get_db)):
    db_ordinateur = db.query(Ordinateur).filter(Ordinateur.id == ordinateur_id).first()
    if not db_ordinateur:
        logger.warning(f"Ordinateur avec l'ID {ordinateur_id} non trouvé pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordinateur inexistant")
    db.delete(db_ordinateur)
    db.commit()
    logger.info(f"Ordinateur avec l'ID {ordinateur_id} supprimé avec succès")
    return None

@ordinateur.put("/{ordinateur_id}", response_model=OrdinateurRead)
def update_ordinateur(ordinateur_id: int, ordinateur: OrdinateurUpdate, db: Session = Depends(get_db)):
    db_ordinateur = db.query(Ordinateur).filter(Ordinateur.id == ordinateur_id).first()
    if not db_ordinateur:
        logger.warning(f"Ordinateur avec l'ID {ordinateur_id} non trouvé pour mise à jour")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ordinateur inexistant")
    data = ordinateur.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_ordinateur, key, value)
    db.commit()
    db.refresh(db_ordinateur)
    logger.info(f"Ordinateur avec l'ID {ordinateur_id} mis à jour avec succès")
    return db_ordinateur

# Office License endpoints

@licence.post("/", response_model=OfficeLicenceRead, status_code=status.HTTP_201_CREATED)
def create_license(license: OfficeLicenceCreate, db: Session = Depends(get_db)):
    db_licence = OfficeLicence(**license.model_dump(exclude_unset=True))
    db.add(db_licence)
    try:
        db.commit()
        db.refresh(db_licence)
        logger.info(f"Licence créée avec succès - {license.tag}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: Une license avec ce tag, IP ou MAC existe déjà - {licence}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une licence avec ce tag, IP ou MAC existe déjà"
        )
    return db_licence

@licence.delete("/{licence_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(licence_id: int, db: Session = Depends(require_role(get_db))):
    db_licence = db.query(OfficeLicence).filter(OfficeLicence.id == licence_id).first()
    if not db_licence:
        logger.warning(f"Licence avec l'ID {licence_id} non trouvée pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License inexistant")
    db.delete(db_licence)
    db.commit()
    logger.info(f"Licence avec l'ID {licence_id} supprimée avec succès")
    return None

@licence.put("/{licence_id}", response_model=OfficeLicenceRead)
def update_license(licence_id: int, licence: OfficeLicenceUpdate, db: Session = Depends(require_role(get_db))):
    db_licence = db.query(OfficeLicence).filter(OfficeLicence.id == licence_id).first()
    if not db_licence:
        logger.warning(f"Licence avec l'ID {licence_id} non trouvée pour mise à jour")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License inexistant")
    data = licence.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_licence, key, value)
    db.commit()
    db.refresh(db_licence)
    logger.info(f"Licence avec l'ID {licence_id} mise à jour avec succès")
    return db_licence

# Ecran endpoints

@ecran.post("/", response_model=EcranRead, status_code=status.HTTP_201_CREATED)
def create_ecran(ecran: EcranCreate, db: Session = Depends(get_db)):
    db_ecran = Ecran(**ecran.model_dump(exclude_unset=True))
    db.add(db_ecran)
    try:
        db.commit()
        db.refresh(db_ecran)
        logger.info(f"Ecran créé avec succès - {ecran.tag}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: Un ecran avec ce tag, IP ou MAC existe déjà - {ecran}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un ecran avec ce tag, IP ou MAC existe déjà"
        )
    return db_ecran

@ecran.delete("/{ecran_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ecran(ecran_id: int, db: Session = Depends(get_db)):
    db_ecran = db.query(Ecran).filter(Ecran.id == ecran_id).first()
    if not db_ecran:
        logger.warning(f"Ecran avec l'ID {ecran_id} non trouvé pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ecran inexistant")
    db.delete(db_ecran)
    db.commit()
    logger.info(f"Ecran avec l'ID {ecran_id} supprimé avec succès")
    return None

@ecran.put("/{ecran_id}", response_model=EcranRead)
def update_ecran(ecran_id: int, ecran: EcranUpdate, db: Session = Depends(get_db)):
    db_ecran = db.query(Ecran).filter(Ecran.id == ecran_id).first()
    if not db_ecran:
        logger.warning(f"Ecran avec l'ID {ecran_id} non trouvé pour mise à jour")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ecran inexistant")
    data = ecran.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(db_ecran, key, value)
    db.commit()
    db.refresh(db_ecran)
    logger.info(f"Ecran avec l'ID {ecran_id} mis à jour avec succès")
    return db_ecran

# Devis endpoints

@devis.post("/", response_model=DevisRead, status_code=status.HTTP_201_CREATED)
def create_devis(devis: DevisRead, db: Session = Depends(get_db)):
    db_devis = Devis(**devis.model_dump(exclude_unset=True))
    db.add(db_devis)
    try:
        db.commit()
        db.refresh(db_devis)
        logger.info(f"Devis créé avec succès - {devis.tag}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: Un devis avec ce tag, IP ou MAC existe déjà - {devis}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un devis avec ce tag, IP ou MAC existe déjà"
        )
    return db_devis

@devis.delete("/{devis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_devis(devis_id: int, db: Session = Depends(get_db)):
    db_devis = db.query(Devis).filter(Devis.id == devis_id).first()
    if not db_devis:
        logger.warning(f"Devis avec l'ID {devis_id} non trouvé pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Devis inexistant")
    db.delete(db_devis)
    db.commit()
    logger.info(f"Devis avec l'ID {devis_id} supprimé avec succès")
    return None

@devis.put("/{devis_id}", response_model=DevisRead)
def update_devis(devis_id: int, devis: DevisRead, db: Session = Depends(get_db)):
    db_devis = db.query(Devis).filter(Devis.id == devis_id).first()
    if not db_devis:
        logger.warning(f"Devis avec l'ID {devis_id} non trouvé pour mise à jour")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Devis inexistant")
    for key, value in devis.model_dump(exclude_unset=True).items():
        setattr(db_devis, key, value)
    db.commit()
    db.refresh(db_devis)
    logger.info(f"Devis avec l'ID {devis_id} mis à jour avec succès")
    return db_devis

# Facture endpoints

@facture.post("/", response_model=FactureRead, status_code=status.HTTP_201_CREATED)
def create_facture(facture: FactureRead, db: Session = Depends(get_db)):
    db_facture = Facture(**facture.model_dump(exclude_unset=True))
    db.add(db_facture)
    try:
        db.commit()
        db.refresh(db_facture)
        logger.info(f"Facture créée avec succès - {facture.tag}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: Une facture avec ce tag, IP ou MAC existe déjà - {facture.tag}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une facture avec ce tag, IP ou MAC existe déjà"
        )
    return db_facture

@facture.delete("/{facture_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_facture(facture_id: int, db: Session = Depends(get_db)):
    db_facture = db.query(Facture).filter(Facture.id == facture_id).first()
    if not db_facture:
        logger.warning(f"Facture avec l'ID {facture_id} non trouvée pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facture inexistant")
    db.delete(db_facture)
    db.commit()
    logger.info(f"Facture avec l'ID {facture_id} supprimée avec succès")
    return None

@facture.put("/{facture_id}", response_model=FactureRead)
def update_facture(facture_id: int, facture: FactureRead, db: Session = Depends(get_db)):
    db_facture = db.query(Facture).filter(Facture.id == facture_id).first()
    if not db_facture:
        logger.warning(f"Facture avec l'ID {facture_id} non trouvée pour mise à jour")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Facture inexistant")
    for key, value in facture.model_dump(exclude_unset=True).items():
        setattr(db_facture, key, value)
    db.commit()
    db.refresh(db_facture)
    logger.info(f"Facture avec l'ID {facture_id} mise à jour avec succès")
    return db_facture

# Bon de commande endpoints

@bon_de_commande.post("/", response_model=BonDeCommandeRead, status_code=status.HTTP_201_CREATED)
def create_bon_de_commande(bon_de_commande: BonDeCommandeRead, db: Session = Depends(get_db)):
    db_bon_de_commande = BonDeCommande(**bon_de_commande.model_dump(exclude_unset=True))
    db.add(db_bon_de_commande)
    try:
        db.commit()
        db.refresh(db_bon_de_commande)
        logger.info(f"Bon de commande créé avec succès - {bon_de_commande.tag}")
    except IntegrityError:
        db.rollback()
        logger.warning(f"IntegrityError: Un bon de commande avec ce tag, IP ou MAC existe déjà - {bon_de_commande.tag}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un bon de commande avec ce tag, IP ou MAC existe déjà"
        )
    return db_bon_de_commande

@bon_de_commande.delete("/{bon_de_commande_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bon_de_commande(bon_de_commande_id: int, db: Session = Depends(get_db)):
    db_bon_de_commande = db.query(BonDeCommande).filter(BonDeCommande.id == bon_de_commande_id).first()
    if not db_bon_de_commande:
        logger.warning(f"Bon de commande avec l'ID {bon_de_commande_id} non trouvé pour suppression")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bon de commande inexistant")
    db.delete(db_bon_de_commande)
    db.commit()
    logger.info(f"Bon de commande avec l'ID {bon_de_commande_id} supprimé avec succès")
    return None

@bon_de_commande.put("/{bon_de_commande_id}", response_model=BonDeCommandeRead)
def update_bon_de_commande(bon_de_commande_id: int, bon_de_commande: BonDeCommandeRead, db: Session = Depends(get_db)):
    db_bon_de_commande = db.query(BonDeCommande).filter(BonDeCommande.id == bon_de_commande_id).first()
    if not db_bon_de_commande:
        logger.warning(f"Bon de commande avec l'ID {bon_de_commande_id} non trouvé pour mise à jour")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bon de commande inexistant")
    for key, value in bon_de_commande.model_dump(exclude_unset=True).items():
        setattr(db_bon_de_commande, key, value)
    db.commit()
    db.refresh(db_bon_de_commande)
    logger.info(f"Bon de commande avec l'ID {bon_de_commande_id} mis à jour avec succès")
    return db_bon_de_commande