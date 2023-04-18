from typing import Optional

ASK_PARTNERSHIP_OFFER = '''
Оставьте сообщение с предложением о сотрудничестве.
'''


def ASK_DOCS(docs_count: int = 0):
    text = '''
Скачайте прикрепленные документы и пришлите сканы с подписью.

Нажмите "Продолжить", когда все документы будут отправлены.
'''
    if docs_count:
        text += f'\nЗагружено <b>{docs_count}</b> документов.'

    return text


ASK_DOCS_CONFIRMATION = '''
Подтвердите отправку документов, когда все документы будут отправлены.
'''

ASK_CONTAINER_TYPE = '''
Введите тип контейнера:
'''

ASK_TERMINAL = '''
Введите терминал постановки:
'''

ASK_WAREHOUSE = '''
Адрес склада выгрузки или погрузки контейнера:
'''

ASK_TERMINAL_DELIVERY = '''
Введите терминал сдачи ('-' если не требуется):
'''

ASK_WEIGHT = '''
Введите вес контейнера (в тоннах):
'''

ASK_INCORRECT_WEIGHT = '''
Некорректный вес. 
Введите вес контейнера (в тоннах):
'''

ASK_SPECIAL_CONDITIONS = '''
Введите особые условия:
'''


def ASK_CONTACTS(username: Optional[str]):
    if username is None:
        return '''
Укажите контакты для связи:
'''

    return f'''
Если хотите, вы можете указать дополнительные контакты для связи.
Текущий контакт: https://t.me/{username}
'''


ASK_CONFIRMATION = '''
Подтвердите введенные данные:
'''

REJECT = '''
Данные отклонены
'''

SUCCESS_APPLICATION = '''
Заявка отправлена администраторам.
'''


def APPLICATION_PICKUP_DATA(
    container_type: str,
    terminal: str,
    warehouse: str,
    terminal_delivery: str,
    weight: str,
    special_conditions: str,
    contacts: str
):
    return f'''
<b>Тип контейнера:</b> {container_type}
<b>Терминал постановки:</b> {terminal}
<b>Склад:</b> {warehouse}
<b>Терминал сдачи:</b> {terminal_delivery}
<b>Вес:</b> {weight}
<b>Особые условия:</b> {special_conditions}
<b>Контакты:</b> {contacts}
'''


def APPLICATION_PARTNERSHIP_DATA(
    partnership_offer: str,
    contacts: str
):
    return f'''
<b>Предложение о сотрудничестве:</b> {partnership_offer}
<b>Контакты:</b> {contacts}
'''
