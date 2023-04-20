ASK_PHONE = '''
Укажите телефон, на который хотите получить обратный звонок.
'''


SUCCESS = '''
Спасибо, мы свяжемся с вами в ближайшее время.
'''


def build_admin_notification(full_name: str, phone: str):
    return f'''
Заказ обратного звонка от {full_name}.
Телефон: {phone}
'''
