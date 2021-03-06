"""Init revision

Revision ID: 0a8235634ed0
Revises:
Create Date: 2021-10-18 13:28:58.442636

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Text, Date


# revision identifiers, used by Alembic.
revision = '0a8235634ed0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('abonent',
                    sa.Column('id', Integer, primary_key=True),
                    sa.Column('name', Text, nullable=False),
                    sa.Column('birthday', Date),
                    sa.Column('address', Text),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('phone',
                    sa.Column('id', Integer, ForeignKey(
                        'abonent.id'), nullable=False),
                    sa.Column('phone', String(30))
                    )
    op.create_table('email',
                    sa.Column('id', Integer, ForeignKey(
                        'abonent.id'), nullable=False),
                    sa.Column('email_addr', String(40))
                    )
    op.create_table('note',
                    sa.Column('id', Integer, ForeignKey(
                        'abonent.id'), nullable=False),
                    sa.Column('date', Date, nullable=False),
                    sa.Column('note_text', Text)
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email')
    op.drop_table('note')
    op.drop_table('phone')
    op.drop_table('abonent')
    # ### end Alembic commands ###
