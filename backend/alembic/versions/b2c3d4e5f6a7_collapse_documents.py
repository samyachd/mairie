"""collapse devis/bon_de_commande/facture into single document table

- Drop devis_id, bon_de_commande_id, facture_id from ordinateur, ecran, office_licence
- Drop devis, bon_de_commande, facture tables
- Create unified document table with type discriminator + optional FKs to each equipment

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-05-04
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, None] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


DOC_TYPE_ENUM = "document_type_enum"
DOC_TYPE_VALUES = ("devis", "bon_de_commande", "facture")


def upgrade() -> None:
    bind = op.get_bind()

    # ── Drop the old per-doc FKs from each equipment ──────────────────────
    for table, cols in [
        ("ordinateur", ["devis_id", "bon_de_commande_id", "facture_id"]),
        ("ecran", ["devis_id", "bon_de_commande_id", "facture_id"]),
        ("office_licence", ["devis_id", "bon_de_commande_id", "facture_id"]),
    ]:
        for col in cols:
            # FK constraint names auto-generated inline in initial migration —
            # use a DO block to drop whichever name PG chose.
            op.execute(
                f"""
                DO $$
                DECLARE c_name text;
                BEGIN
                    SELECT conname INTO c_name
                    FROM pg_constraint
                    WHERE conrelid = '{table}'::regclass
                      AND contype = 'f'
                      AND pg_get_constraintdef(oid) ILIKE '%({col})%';
                    IF c_name IS NOT NULL THEN
                        EXECUTE format('ALTER TABLE {table} DROP CONSTRAINT %I', c_name);
                    END IF;
                END$$;
                """
            )
            op.drop_column(table, col)

    # ── Drop the three legacy doc tables ──────────────────────────────────
    op.drop_table("devis")
    op.drop_table("bon_de_commande")
    op.drop_table("facture")

    # ── Create the new unified document table ─────────────────────────────

    # 3. Create the Enum Type in Postgres
    values_str = ", ".join([f"'{v}'" for v in DOC_TYPE_VALUES])
    op.execute(f"""
        DO $$ 
        BEGIN 
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{DOC_TYPE_ENUM}') THEN
                CREATE TYPE {DOC_TYPE_ENUM} AS ENUM ({values_str});
            END IF;
        END $$;
    """)
    
    # 4. Define the SQLAlchemy Type object
    # We use create_type=False because we handled creation via the DO block above

    sa_doc_type = postgresql.ENUM(*DOC_TYPE_VALUES, name=DOC_TYPE_ENUM, create_type=False)

    # 5. Create the unified table

    op.create_table(
        "document",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("type", sa_doc_type,nullable=False),
        sa.Column("nom", sa.String(255), nullable=False),
        sa.Column("numero", sa.String(50), nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("date_document", sa.Date(), nullable=False),
        sa.Column("montant_ttc", sa.Float(), nullable=True),
        sa.Column("montant_ht", sa.Float(), nullable=True),
        sa.Column("ordinateur_id", sa.Integer(), nullable=True),
        sa.Column("ecran_id", sa.Integer(), nullable=True),
        sa.Column("office_licence_id", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["ordinateur_id"], ["ordinateur.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["ecran_id"], ["ecran.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["office_licence_id"], ["office_licence.id"], ondelete="SET NULL"),
        sa.CheckConstraint(
            "(CASE WHEN ordinateur_id IS NOT NULL THEN 1 ELSE 0 END "
            "+ CASE WHEN ecran_id IS NOT NULL THEN 1 ELSE 0 END "
            "+ CASE WHEN office_licence_id IS NOT NULL THEN 1 ELSE 0 END) <= 1",
            name="ck_document_single_owner",
        ),
        sa.CheckConstraint(
            "type = 'facture' OR (montant_ttc IS NULL AND montant_ht IS NULL)",
            name="ck_document_montant_only_facture",
        ),
    )
    
# ── Create Indexes Safely ─────────────────────────────────────────────
    indexes = [
        ("ix_document_type", "document", "type"),
        ("ix_document_numero", "document", "numero"),
        ("ix_document_ordinateur_id", "document", "ordinateur_id"),
        ("ix_document_ecran_id", "document", "ecran_id"),
        ("ix_document_office_licence_id", "document", "office_licence_id"),
    ]

    for name, table, col in indexes:
        op.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {table} ({col})")


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_index("ix_document_office_licence_id", table_name="document")
    op.drop_index("ix_document_ecran_id", table_name="document")
    op.drop_index("ix_document_ordinateur_id", table_name="document")
    op.drop_index("ix_document_numero", table_name="document")
    op.drop_index("ix_document_type", table_name="document")
    op.drop_table("document")
    sa.Enum(name=DOC_TYPE_ENUM).drop(bind, checkfirst=True)

    # Recreate legacy tables (matching the initial schema)
    for tbl in ("devis", "bon_de_commande"):
        op.create_table(
            tbl,
            sa.Column("nom", sa.String(255), nullable=False),
            sa.Column("numero", sa.String(50), nullable=False),
            sa.Column("path", sa.String(255), nullable=False),
            sa.Column("date_document", sa.Date(), nullable=False),
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("path"),
            sa.UniqueConstraint("numero", name=f"uq_{tbl}_numero"),
        )

    op.create_table(
        "facture",
        sa.Column("montant_ttc", sa.Float(), nullable=True),
        sa.Column("montant_ht", sa.Float(), nullable=True),
        sa.Column("nom", sa.String(255), nullable=False),
        sa.Column("numero", sa.String(50), nullable=False),
        sa.Column("path", sa.String(255), nullable=False),
        sa.Column("date_document", sa.Date(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("path"),
        sa.UniqueConstraint("numero", name="uq_facture_numero"),
    )

    for table in ("ordinateur", "ecran", "office_licence"):
        op.add_column(table, sa.Column("devis_id", sa.Integer(), nullable=True))
        op.add_column(table, sa.Column("bon_de_commande_id", sa.Integer(), nullable=True))
        op.add_column(table, sa.Column("facture_id", sa.Integer(), nullable=True))
        op.create_foreign_key(None, table, "devis", ["devis_id"], ["id"], ondelete="SET NULL")
        op.create_foreign_key(None, table, "bon_de_commande", ["bon_de_commande_id"], ["id"], ondelete="SET NULL")
        op.create_foreign_key(None, table, "facture", ["facture_id"], ["id"], ondelete="SET NULL")
