"""added salesinfo

Revision ID: eebf20bdf319
Revises: 0e20df829504
Create Date: 2020-04-21 14:29:31.017962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eebf20bdf319'
down_revision = '0e20df829504'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_device_type'), 'device', ['type'], unique=False)
    op.add_column('repair', sa.Column('sale_info_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'repair', 'sale_info', ['sale_info_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'repair', type_='foreignkey')
    op.drop_column('repair', 'sale_info_id')
    op.drop_index(op.f('ix_device_type'), table_name='device')
    # ### end Alembic commands ###
