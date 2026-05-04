from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, model_validator
from db.models.document import DocumentType


class DocumentCreate(BaseModel):
    type: DocumentType
    nom: str = Field(..., min_length=1, max_length=255)
    numero: str = Field(..., min_length=1, max_length=50)
    path: str = Field(..., min_length=1, max_length=255)
    date_document: date
    montant_ttc: float | None = Field(None, ge=0)
    montant_ht: float | None = Field(None, ge=0)
    ordinateur_id: int | None = None
    ecran_id: int | None = None
    office_licence_id: int | None = None

    @model_validator(mode="after")
    def _single_owner(self):
        owners = sum(
            x is not None
            for x in (self.ordinateur_id, self.ecran_id, self.office_licence_id)
        )
        if owners > 1:
            raise ValueError(
                "Un document ne peut être lié qu'à un seul équipement à la fois."
            )
        return self

    @model_validator(mode="after")
    def _montants_only_facture(self):
        if self.type != DocumentType.facture and (
            self.montant_ttc is not None or self.montant_ht is not None
        ):
            raise ValueError("montant_ttc/montant_ht ne s'appliquent qu'aux factures.")
        return self


class DocumentUpdate(BaseModel):
    nom: str | None = Field(None, min_length=1, max_length=255)
    numero: str | None = Field(None, min_length=1, max_length=50)
    path: str | None = Field(None, min_length=1, max_length=255)
    date_document: date | None = None
    montant_ttc: float | None = Field(None, ge=0)
    montant_ht: float | None = Field(None, ge=0)
    ordinateur_id: int | None = None
    ecran_id: int | None = None
    office_licence_id: int | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    type: DocumentType
    nom: str
    numero: str
    path: str
    date_document: date
    montant_ttc: float | None = None
    montant_ht: float | None = None
    ordinateur_id: int | None = None
    ecran_id: int | None = None
    office_licence_id: int | None = None
    created_at: datetime
    updated_at: datetime | None = None
