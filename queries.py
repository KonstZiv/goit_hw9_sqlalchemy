from sqlalchemy import delete, or_
from sqlalchemy.sql.expression import update, select
from sqlalchemy.sql.sqltypes import Integer
from init_db import Abonent, DBSession, Phone, Note, Email
from datetime import date


def create_abonent(name: str, birthday: date = None, address: str = None, phones: list = [], emails: list = [], note: str = None, DBSession=DBSession):
    """Добавляет новго абонентаив базу данных

    Параметры:
    name - имя, абонента. Обязательный параметр. При отсутствии или неверном типе данных 
    функция генерирует TypeError
    birthday - необязательный параметр
    address - необязательный параметр
    phones - необязательный параметр, тип list, должен содержать строковые выражения телефонов
    emails - необязательный параметр, тип list, должен содержать строковые выражения email
    note - необязательный параметр. При записи в БД будет установлена временная метка внесения записи,
    которая будет доступна при отображении и поиске
    DBSession - необязательный параметр, экземпляр 'фабрики сессий, связанный с конкретной БД'
    """
    with DBSession() as session:
        if not isinstance(name, str):
            raise TypeError('take name argument, name must have type str')
        abonent_instance = Abonent(
            name=name, birthday=birthday, address=address)
        session.add(abonent_instance)
        session.flush()
        # insert emails:
        if emails:
            for email in emails:
                email_instance = Email(
                    abonent_id=abonent_instance.abonent_id, email=email)
                session.add(email_instance)
        # insert phones:
        if phones:
            for phone in phones:
                phone_instance = Phone(
                    abonent_id=abonent_instance.abonent_id, phone=phone)
                session.add(phone_instance)
        # insert note:
        if note:
            note_instance = Note(
                abonent_id=abonent_instance.abonent_id, date=date.today(), note_text=note)
            session.add(note_instance)

        session.commit()


def read_abonents(pattern: str = '', date_min: date = None, date_max: date = None) -> list:
    """Ищет и возвращает список экземпляров записей типа Abonent, соотвествующих параметрам поиска.
    Параметры поиска задаются паттерном 'pattern' и временным интервалом date_min ... date_max. Если 
    pattern == '' (пустая строка - состояние по умолчанию), поиск осуществляется только с учетом 
    временных меток. Поиск по паттерну проходит по всем текстовым и строковым полям БД: name, 
    address, phone, email, note.
    Поиск по временным отметкам осуществляется по полям Abonent.birthday и Note.date (дата создания заметки)
    Поиск по временным отметкам реализуется по правилам:
    - date_min == None and date_max == None - состояние по умолчанию. Поиск по времени не осуществляется.
    - date_min == None and date_max == date - в результаты поиска включаются записи, временные отметки которых
    соотвествуют условию < date_max
    - date_min == date and date_max == None -  в результаты поиска включаются записи, временные отметки которых
    соотвествуют условию > date_min
    - date_min == date_1 and date_max == date_2 -  в результаты поиска включаются записи, временные отметки которых
    соотвествуют условию BETWEEN date_1 AND date_2 (попадающие в интервал, включая границы)
    - date_min == date_max (тип данных - date) - в выборку попадут записи в которых временные метки равны date_min
     DBSession - необязательный параметр, экземпляр 'фабрики сессий, связанный с конкретной БД'
    """
    with DBSession() as session:
        if pattern == '':
            results = session.query(Abonent)\
                .join(Phone, Abonent.abonent_id == Phone.abonent_id, full=True)\
                .join(Email, Abonent.abonent_id == Email.abonent_id, full=True)\
                .join(Note, Abonent.abonent_id == Note.abonent_id, full=True)
        else:
            results = session.query(Abonent)\
                .join(Phone, Abonent.abonent_id == Phone.abonent_id, full=True)\
                .join(Email, Abonent.abonent_id == Email.abonent_id, full=True)\
                .join(Note, Abonent.abonent_id == Note.abonent_id, full=True).filter(or_(
                    Abonent.name.ilike('%'+pattern+'%'),
                    Abonent.address.ilike('%'+pattern+'%'),
                    Phone.phone.ilike('%'+pattern+'%'),
                    Email.email.ilike('%'+pattern+'%'),
                    Note.note_text.ilike('%'+pattern+'%')
                ))
        if date_min is None and date is None:
            fin = results
        elif date_min == date_max and isinstance(date_min, date):
            fin = results.filter(or_(
                Abonent.birthday == date_min,
                Note.date == date_min
            )).all()
            for f in fin:
                print(type(f))
                print(f)

        elif date_min is None and isinstance(date_max, date):
            fin = results.filter(or_(
                Abonent.birthday < date_max,
                Note.date < date_max
            ))
        elif isinstance(date_min, date) and date_max is None:
            fin = results.filter(or_(
                Abonent.bithday.between > date_min,
                Note.date > date_min
            ))
        elif isinstance(date_min, date) and isinstance(date_max, date) and date_min <= date_max:
            fin = results.filter(or_(
                Abonent.birthday.between(date_min, date_max),
                Note.date.between(date_min, date_max)
            )).all()
        else:
            raise TypeError(
                'parameters function search_abonents date_min or date_max has wrong type')
        #fin_new = [str(a) for a in fin]

        session.commit()
    print(type(fin))
    # print(fin_new)
    return fin


def delete_abonent(abonents_id: list, DBSession=DBSession):
    """Удаляет записи в с id = abonents_id[i], i from 0 to len(aboonents_ID) в таблице
    abonent и связанніе записи во всех остальніх таблицах БД (phone, email, note)
    Парпметры:
    abonents_id - обязательный. Содержит список id (type(id) == Integer) записей для удаления
    DBSession - необязательный параметр, экземпляр 'фабрики сессий, связанный с конкретной БД'
    """
    with DBSession() as session:
        for abonent_id in abonents_id:
            abonent = session.get(Abonent, abonent_id)
            session.delete(abonent)
            session.commit()


def update_abonent(abonent_id: int,
                   name: str = None,
                   birthday: date = None,
                   address: str = None,
                   phones: list = None,
                   emails: list = None,
                   note: str = None,
                   DBSession=DBSession):
    """Обновляет данные по абоненту.
    - abonent_id - обязательный парпметр, должен соотвествоать первичному ключу записи в
    таблице abonent, которая должна быть обновлена. Остальные параметры - необязательны.
    Если значение других параметов равно None - над соотвествующими полями в таблицах не 
    совершается никаких действияй. Если:
    - birthday != None (type(birthday) == date) - в поле abonent.birthday записывается новое значение
    - address != None (type(address) == str) - в поле abonent.address записывается новое значение
    - note != None (type(note) == str) - в таблицу note добавляется новая запись с внешним ключем 
    note.abonent_id = abonent_id, note.date = 'текущая дата', note.note_text = note (переданное в 
    аргументах функции значение). Данные таблицы note удаляются только во время удаления абонента,
    в остальніх ситуациях - накапливаются с датами внесения в БД
    - phones != None and phones = [str_1, str_2, ...] - в таблице phone удаляются все записи, 
    у которых phone.abonent_id == abonent_id (переданный в параметрах функции) и создаются новые записи с 
    внешними ключами, равными abonent_id (переданный в параметрах функции) и значениями в полях phone.phone
    равными str_1, str_2, ...
    - emails != None and emails = [str_1, str_2, ...] - в таблице email удаляются все записи, 
    у которых email.abonent_id == abonent_id (переданный в параметрах функции) и создаются новые записи с 
    внешними ключами, равными abonent_id (переданный в параметрах функции) и значениями в полях email.email
    равными str_1, str_2, ...

    перезаписывая содержание полей в таблице abonent. данные в таблицах
    phone и email - уничтожаются на на основе
    """
    with DBSession() as session:
        if not isinstance(abonent_id, int):
            raise TypeError('Type of abonent_id is not Integer')
        if not (name is None) or not (birthday is None) or not (address is None):
            abonent = session.execute(
                select(Abonent).filter_by(abonent_id=abonent_id)).scalar_one()
            abonent.name = name if name else abonent.name
            abonent.birthday = birthday if birthday else abonent.birthday
            abonent.address = address if address else abonent.address
        if not (note is None):
            # insert new note:
            current_date = date.today()
            note_instance = Note(
                abonent_id=abonent_id, date=current_date, note_text=note)
            session.add(note_instance)
            session.flush()
        if not (phones is None):
            del_existing_phones = delete(Phone).where(
                Phone.abonent_id == abonent_id)
            #print('удаляю телефоны: ', del_existing_phones)
            session.execute(del_existing_phones)
            for phone in phones:
                phone_instans = Phone(abonent_id=abonent_id, phone=phone)
                session.add(phone_instans)

        if not (emails is None):
            del_existing_emails = delete(Email).where(
                Email.abonent_id == abonent_id)
            print('удаляю emails: ', del_existing_emails)
            session.execute(del_existing_emails)
            for email in emails:
                email_instans = Email(abonent_id=abonent_id, email=email)
                session.add(email_instans)

        session.commit()
