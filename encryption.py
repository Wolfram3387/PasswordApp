from cryptography.fernet import Fernet
from secret_key import KEY


def encrypt_password(password) -> bytes:
    """
    Функция для шифрования пароля
    :param password: пароль
    :return: зашифрованный токен
    """
    f = Fernet(KEY)
    return f.encrypt(bytes(password, encoding='utf-8'))


def decrypt_password(token) -> str:
    """
    Функция для дешифрования пароля
    :param token: зашифрованный токен
    :return: пароль
    """
    f = Fernet(KEY)
    return str(f.decrypt(token))[2:-1]
