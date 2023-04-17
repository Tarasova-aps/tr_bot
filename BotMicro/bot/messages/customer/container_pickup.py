ASK_DOCS = '''
Скачайте прикрепленные документы и пришлите сканы с подписью.
'''

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
Введите склад:
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

ASK_CONFIRMATION = '''
Подтвердите введенные данные:
'''

REJECT = '''
Данные отклонены
'''

SUCCESS_APPLICATION_PICKUP = '''
Заявка отправлена администраторам.
'''


def APPLICATION_PICKUP_DATA(
    container_type: str,
    terminal: str,
    warehouse: str,
    terminal_delivery: str,
    weight: str,
    special_conditions: str
):
    return f'''
<b>Тип контейнера:</b> {container_type}
<b>Терминал постановки:</b> {terminal}
<b>Склад:</b> {warehouse}
<b>Терминал сдачи:</b> {terminal_delivery}
<b>Вес:</b> {weight}
<b>Особые условия:</b> {special_conditions}
'''
