"""geraetetraeger eingefuegt

Revision ID: 5641b5080795
Revises: f947b555a565
Create Date: 2022-10-19 19:57:07.635602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5641b5080795'
down_revision = 'f947b555a565'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('kurzpruefung', sa.Column('geraetetraeger', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('kurzpruefung', 'geraetetraeger')
    # ### end Alembic commands ###