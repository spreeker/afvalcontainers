"""site_id to filllevel enevo

Revision ID: ca54373f9692
Revises: 79cb4b3c0ff9
Create Date: 2019-01-30 13:22:35.827797

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ca54373f9692'
down_revision = '79cb4b3c0ff9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('enevo_filllevel', sa.Column('site_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_enevo_filllevel_site_id'), 'enevo_filllevel', ['site_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_enevo_filllevel_site_id'), table_name='enevo_filllevel')
    op.drop_column('enevo_filllevel', 'site_id')
    # ### end Alembic commands ###