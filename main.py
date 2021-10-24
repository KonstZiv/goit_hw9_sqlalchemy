from sqlalchemy.sql.expression import update, select
from init_db import Abonent, engine, DBSession
from queries import create_abonent, delete_abonent, update_abonent, read_abonents
from datetime import datetime, date


if __name__ == '__main__':
    name = "XXXXXXXXXXXXXXXX"
    address = "YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY"
    note = "Мастер по ремонту всего неработающего"
    """note = 'очень хороший человек'
    phones = ["+38-050-555-44-33", "+38-067-111-22-33"]
    emails = ["ivan1985@fm.ua"]
    add_abonent(name=name, note=note, address=address,
                phones=phones, emails=emails)
    delete_abonent([1, 2, 3])
    with DBSession() as session:
        ab_15 = session.execute(
            select(Abonent).filter_by(abonent_id=15)).scalar_one()
        print(ab_15)
        print(ab_15.phone[0])
        ab_15.name = 'Белкина Полина Хартоновна'
        ab_15.phone[0] = '123456789'
        ab_15 = session.execute(
            select(Abonent).filter_by(abonent_id=15)).scalar_one()
        ab_15.phone[0] = '123456789'
        print(ab_15.phone[0])

    print('-' * 119)
    print(ab_15)"""

    #update_abonent(abonent_id=34, phones=['новый телефон 1'])
    date_min = datetime.strptime('01-01-1970', '%d-%m-%Y').date()
    date_max = datetime.strptime('20-12-1980', '%d-%m-%Y').date()
    update_abonent(abonent_id=10, phones=[
                   'новый телефон 3', 'новый телефон 4'])
"""    for r in res:
        print(type(r))
        print(r)"""
