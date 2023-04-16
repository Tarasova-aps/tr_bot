USERS_LIST_TITLE = '''
<b>Управление аккаунтами</b>
'''


ASK_ADMIN_NAME = '''
Введите имя нового администратора:
'''


SUCCESS_DELETE_USER = '''
Аккаунт успешно удалён.
'''


def SUCCESS_CREATE_ADMIN(name: str, user_key: str):
    return f'''
Администратор <b>{name}</b> успешно создан.

Ключ доступа: <code>{user_key}</code>
'''


def USER_PAGE(name: str, user_key: str):
    return f'''
<b>{name}</b>

Ключ доступа: <code>{user_key}</code>
'''
