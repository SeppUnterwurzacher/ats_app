"""Geraete Spalte id_feuerwehr anlegen

Revision ID: 260b6d36783c
Revises: 7f6fc7696dc6
Create Date: 2022-10-29 11:31:45.443159

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '260b6d36783c'
down_revision = '7f6fc7696dc6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('geraete', sa.Column('id_feuerwehr', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'geraete', 'feuerwehren', ['id_feuerwehr'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'geraete', type_='foreignkey')
    op.drop_column('geraete', 'id_feuerwehr')
    # ### end Alembic commands ###