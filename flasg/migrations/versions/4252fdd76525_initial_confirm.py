"""initial confirm

Revision ID: 4252fdd76525
Revises: 456a945560f6
Create Date: 2015-12-01 20:25:22.254000

"""

# revision identifiers, used by Alembic.
revision = '4252fdd76525'
down_revision = '456a945560f6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    ### end Alembic commands ###