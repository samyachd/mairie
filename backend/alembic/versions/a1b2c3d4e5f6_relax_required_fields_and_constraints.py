"""relax required fields and tighten constraints

- BaseEquipement.date_achat → nullable
- OfficeLicence.version, date_achat → nullable
- OfficeLicence: add `clef` and `mail_activation`
- type_equipement (ordinateur, ecran) → enum
- ordinateur.ip_address → drop unique
- ordinateur.agent_id → unique (1-to-1 with agent)
- ecran: check `ordinateur_id IS NULL OR slot IS NOT NULL`
- documents (devis, bon_de_commande, facture).numero → unique

Revision ID: a1b2c3d4e5f6
Revises: 85bd87dc3d00
Create Date: 2026-05-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "85bd87dc3d00"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TYPE_ENUM_NAME = "type_equipement_enum"
TYPE_ENUM_VALUES = ("PC FIXE", "PC PORTABLE", "ECRAN", "AUTRE")


def upgrade() -> None:
    bind = op.get_bind()

    # ── Enum type for type_equipement ──────────────────────────────────────
    type_enum = sa.Enum(*TYPE_ENUM_VALUES, name=TYPE_ENUM_NAME)
    type_enum.create(bind, checkfirst=True)

    # Bucket existing free-text values into the new enum's allowed set.
    # Anything that doesn't match the keywords gets bucketed to AUTRE so we
    # don't lose rows on the cast.
    for table in ("ordinateur", "ecran"):
        op.execute(
            f"""
            UPDATE {table}
            SET type_equipement = CASE
                WHEN UPPER(type_equipement) LIKE '%ECRAN%' AND UPPER(type_equipement) NOT LIKE '%PORTABLE%'
                    THEN 'ECRAN'
                WHEN UPPER(type_equipement) LIKE '%PORTABLE%'
                    OR UPPER(type_equipement) LIKE '%LATITUDE%'
                    OR UPPER(type_equipement) LIKE '%PRECISION%'
                    OR UPPER(type_equipement) LIKE '%SURFACE%'
                    OR UPPER(type_equipement) LIKE '%TABLETTE%'
                    OR UPPER(type_equipement) LIKE '%XPS%'
                    THEN 'PC PORTABLE'
                WHEN UPPER(type_equipement) LIKE '%FIXE%'
                    OR UPPER(type_equipement) LIKE '%OPTIPLEX%'
                    OR UPPER(type_equipement) LIKE '%MICRO PC%'
                    OR UPPER(type_equipement) LIKE '%AIO%'
                    OR UPPER(type_equipement) LIKE '%ECOLES%'
                    OR UPPER(type_equipement) LIKE '%TOUT EN UN%'
                    THEN 'PC FIXE'
                WHEN type_equipement IS NULL OR type_equipement = ''
                    THEN NULL
                ELSE 'AUTRE'
            END
            """
        )

    op.alter_column(
        "ordinateur",
        "type_equipement",
        existing_type=sa.String(length=255),
        type_=type_enum,
        existing_nullable=True,
        postgresql_using=f"type_equipement::{TYPE_ENUM_NAME}",
    )
    op.alter_column(
        "ecran",
        "type_equipement",
        existing_type=sa.String(length=255),
        type_=type_enum,
        existing_nullable=True,
        postgresql_using=f"type_equipement::{TYPE_ENUM_NAME}",
    )

    # ── BaseEquipement.date_achat → nullable ───────────────────────────────
    op.alter_column("ordinateur", "date_achat", existing_type=sa.Date(), nullable=True)
    op.alter_column("ecran", "date_achat", existing_type=sa.Date(), nullable=True)

    # ── OfficeLicence: nullable version/date_achat + new fields ────────────
    op.alter_column("office_licence", "version", existing_type=sa.String(length=500), nullable=True)
    op.alter_column("office_licence", "date_achat", existing_type=sa.Date(), nullable=True)
    op.add_column("office_licence", sa.Column("clef", sa.String(length=255), nullable=True))
    op.add_column("office_licence", sa.Column("mail_activation", sa.String(length=255), nullable=True))

    # ── ordinateur.ip_address: drop unique ─────────────────────────────────
    # Initial migration created the unique via UniqueConstraint inline in
    # create_table — Alembic auto-names that constraint `ordinateur_ip_address_key`
    # on Postgres. Use a DO block so the migration is idempotent across naming.
    op.execute(
        """
        DO $$
        DECLARE c_name text;
        BEGIN
            SELECT conname INTO c_name
            FROM pg_constraint
            WHERE conrelid = 'ordinateur'::regclass
              AND contype = 'u'
              AND pg_get_constraintdef(oid) ILIKE '%(ip_address)%';
            IF c_name IS NOT NULL THEN
                EXECUTE format('ALTER TABLE ordinateur DROP CONSTRAINT %I', c_name);
            END IF;
        END$$;
        """
    )

    # ── ordinateur.agent_id: unique (1-to-1) ───────────────────────────────
    op.create_unique_constraint("uq_ordinateur_agent_id", "ordinateur", ["agent_id"])

    # ── ecran: slot required when linked to an ordinateur ──────────────────
    op.create_check_constraint(
        "ck_slot_required_when_linked",
        "ecran",
        "ordinateur_id IS NULL OR slot IS NOT NULL",
    )

    # ── documents.numero: unique per type ──────────────────────────────────
    for table in ("devis", "bon_de_commande", "facture"):
        op.create_unique_constraint(f"uq_{table}_numero", table, ["numero"])


def downgrade() -> None:
    bind = op.get_bind()

    for table in ("devis", "bon_de_commande", "facture"):
        op.drop_constraint(f"uq_{table}_numero", table, type_="unique")

    op.drop_constraint("ck_slot_required_when_linked", "ecran", type_="check")

    op.drop_constraint("uq_ordinateur_agent_id", "ordinateur", type_="unique")

    op.create_unique_constraint("ordinateur_ip_address_key", "ordinateur", ["ip_address"])

    op.drop_column("office_licence", "mail_activation")
    op.drop_column("office_licence", "clef")
    op.alter_column("office_licence", "date_achat", existing_type=sa.Date(), nullable=False)
    op.alter_column("office_licence", "version", existing_type=sa.String(length=500), nullable=False)

    op.alter_column("ecran", "date_achat", existing_type=sa.Date(), nullable=False)
    op.alter_column("ordinateur", "date_achat", existing_type=sa.Date(), nullable=False)

    op.alter_column(
        "ecran",
        "type_equipement",
        existing_type=sa.Enum(*TYPE_ENUM_VALUES, name=TYPE_ENUM_NAME),
        type_=sa.String(length=255),
        existing_nullable=True,
        postgresql_using="type_equipement::text",
    )
    op.alter_column(
        "ordinateur",
        "type_equipement",
        existing_type=sa.Enum(*TYPE_ENUM_VALUES, name=TYPE_ENUM_NAME),
        type_=sa.String(length=255),
        existing_nullable=True,
        postgresql_using="type_equipement::text",
    )

    sa.Enum(name=TYPE_ENUM_NAME).drop(bind, checkfirst=True)
