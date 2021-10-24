from sqlalchemy import create_engine, Column, Text, Integer, Date, ForeignKey, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref


from app.settings import conn_str

if conn_str:
    engine = create_engine(conn_str, echo=True)
else:
    print("DB ERROR: conn_str is empty.")

Base = declarative_base()

metadata = Base.metadata
DBSession = sessionmaker(bind=engine, expire_on_commit=False)


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


if __name__ == '__main__':
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
    print('Tables created')
