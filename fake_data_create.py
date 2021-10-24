from sqlalchemy.orm import session
from sqlalchemy.orm.session import Session
from init_db import Abonent, DBSession, Phone, Note, Email
from faker import Faker
from random import randrange

fake = Faker(['uk-UA', 'ru-RU', 'en-US'])


def insert_fake_abonents(num=10):
    with DBSession() as session:
        for _i in range(num):
            name = fake.name()
            birthday = fake.date_between(start_date='-80y', end_date='-10y')
            address = fake.address()
            abonent_instance = Abonent(
                name=name, birthday=birthday, address=address)
            session.add(abonent_instance)
            session.flush()
            print(f'abonent_instance.id = {abonent_instance.abonent_id}')
            # insert (0...3) emails:
            for _ in range(randrange(0, 4)):
                email = fake.ascii_email()
                email_instance = Email(
                    abonent_id=abonent_instance.abonent_id, email=email)
                session.add(email_instance)
            # insert (0...3) phones:
            for _ in range(randrange(0, 4)):
                phone = fake.phone_number()
                phone_instance = Phone(
                    abonent_id=abonent_instance.abonent_id, phone=phone)
                session.add(phone_instance)
            # insert (0...1) note:
            for _ in range(randrange(0, 2)):
                note = fake.sentence(nb_words=10, variable_nb_words=True)
                date = fake.date_between(
                    start_date='-5y', end_date='today')
                note_instance = Note(
                    abonent_id=abonent_instance.abonent_id, date=date, note_text=note)
                session.add(note_instance)
            session.flush()
            session.commit()


if __name__ == '__main__':
    insert_fake_abonents(10)
