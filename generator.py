import random


def generate_password(length=32) -> str:
    """
    Функция для генерации сложных паролей. Итоговый пароль состоит минимум
     из одной цифры, маленькой буквы, заглавной буквы и спец. символа.
    :param length: длина пароля.
    :return: пароль.
    """
    alphabet = r"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!$&()*+<=>?@[]_{|}"
    password = random.choice('abcdefghijklmnopqrstuvwxyz')
    password += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    password += random.choice('0123456789')
    password += random.choice('!$&()*+<=>?@[]_{|}')
    for i in range(length - 4):
        password += random.choice(alphabet)
    password_list = list(password)
    random.shuffle(password_list)
    return ''.join(password_list)
