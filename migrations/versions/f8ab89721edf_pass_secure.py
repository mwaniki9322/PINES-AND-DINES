"""pass secure

Revision ID: f8ab89721edf
Revises: 2016fba43230
Create Date: 2021-08-24 08:20:50.627252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8ab89721edf'
down_revision = '2016fba43230'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('pass_secure', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'pass_secure')
    # ### end Alembic commands ###