from models.application import Application
from utils.datetime import get_msc_formatted_datetime


def APPLICATION_NOTIFY(application: Application) -> str:
    text = '<b>Новая заявка</b>'
    text += '\n'.join(f'<b>{key}</b>: <code>{value}</code>' for key, value in application.data.items())

    create_time = get_msc_formatted_datetime(application.created_at)
    text += f'\n<b>Создана</b>: <code>{create_time}</code>'

    return text
