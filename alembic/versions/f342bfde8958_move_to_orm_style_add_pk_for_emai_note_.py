"""move to ORM style, add PK for emai, note, phone

Revision ID: f342bfde8958
Revises: 0a8235634ed0
Create Date: 2021-10-24 12:21:18.393854

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Text, Date
from sqlalchemy.orm import declarative_base, Column, relationship, sessionmaker
from app.settings import conn_str

engine = create_engine(conn_str, echo=True)
Base = declarative_base()
DBSession = sessionmaker(bind=engine, expire_on_commit=False)

# revision identifiers, used by Alembic.
revision = 'f342bfde8958'
down_revision = '0a8235634ed0'
branch_labels = None
depends_on = None


def upgrade():
    class Abonent(Base):
        __tablename__ = 'abonent'
        abonent_id = Column('abonent_id', Integer, primary_key=True)
        name = Column('name', Text, nullable=False)
        birthday = Column('birthday', Date)
        address = Column('address', Text)

        phone = relationship('Phone', backref='abonent',
                             cascade='all, delete, delete-orphan')
        email = relationship('Email', backref='abonent',
                             cascade='all, delete, delete-orphan')
        note = relationship('Note', backref='abonent',
                            cascade='all, delete, delete-orphan')

        def phones(self):
            with DBSession() as session:
                phones = self.phone
                ph_list = [p.phone for p in phones]
            return ph_list

        def emails(self):
            with DBSession() as session:
                emails = self.email
                em_list = [e.email for e in emails]
            return em_list

        def notes(self):
            with DBSession() as session:
                notes = self.note
                notes_list = [(n.date, n.note_text) for n in notes]
            return notes_list

        def __repr__(self):
            return f'Abonent id={self.abonent_id}, name: {self.name}'


class Phone(Base):
    __tablename__ = 'phone'
    phone_id = Column('phone_id', Integer, primary_key=True)
    abonent_id = Column('abonent_id', Integer, ForeignKey(
        'abonent.abonent_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    phone = Column('phone', String(30))

    def __repr__(self):
        return f'phone: {self.phone}'


class Email(Base):
    __tablename__ = 'email'
    email_id = Column('email_id', Integer, primary_key=True)
    abonent_id = Column('abonent_id', Integer, ForeignKey(
        'abonent.abonent_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    email = Column('email', String(60))

    def __repr__(self):
        return f'email: {self.email}'


class Note(Base):
    __tablename__ = 'note'
    note_id = Column('note', Integer, primary_key=True)
    abonent_id = Column('abonent_id', Integer,
                        ForeignKey('abonent.abonent_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    date = Column('date', Date, nullable=False)
    note_text = Column('note_text', Text)

    def __repr__(self):
        return f' date: {self.date}, note: {self.note_text}'


def downgrade():
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
