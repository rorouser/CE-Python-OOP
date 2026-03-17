"""Añadir puntuacion_usuario a scooters

Revision ID: 002_add_puntuacion
Revises: 001_initial
Create Date: 2025-01-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "002_add_puntuacion"
down_revision: Union[str, None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("scooters", sa.Column("puntuacion_usuario", sa.Float(), nullable=True))


def downgrade() -> None:
    op.drop_column("scooters", "puntuacion_usuario")
