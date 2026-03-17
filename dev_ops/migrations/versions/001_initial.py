"""Crear tablas iniciales

Revision ID: 001_initial
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tabla zones
    op.create_table(
        "zones",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.Column("codigo_postal", sa.String(), nullable=False),
        sa.Column("limite_velocidad", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_zones_id"), "zones", ["id"], unique=False)

    # Tabla scooters
    op.create_table(
        "scooters",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero_serie", sa.String(), nullable=False),
        sa.Column("modelo", sa.String(), nullable=False),
        sa.Column("bateria", sa.Float(), nullable=False),
        sa.Column(
            "estado",
            sa.Enum("disponible", "en_uso", "mantenimiento", "sin_bateria", name="scooterstatus"),
            nullable=False,
        ),
        sa.Column("zona_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["zona_id"], ["zones.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_scooters_id"), "scooters", ["id"], unique=False)
    op.create_index(op.f("ix_scooters_numero_serie"), "scooters", ["numero_serie"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_scooters_numero_serie"), table_name="scooters")
    op.drop_index(op.f("ix_scooters_id"), table_name="scooters")
    op.drop_table("scooters")
    op.drop_index(op.f("ix_zones_id"), table_name="zones")
    op.drop_table("zones")
