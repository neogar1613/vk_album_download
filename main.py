""" Скрипт для выгрузки фото из альбома ВК и загрузки в Яндекс Диск """
from exceptions import InvalidEnv
from settings import (
    VK_LOGIN,
    VK_PASSWORD,
    VK_ALBUM_URL,
    VK_APP_ID,
    YA_TOKEN
)
from vk_service import download_album
from ya_service import upload_folders

# Инициализация необходимых переменных

if VK_APP_ID is None:
    raise InvalidEnv("Неверный идентификатор приложения ВК")
if YA_TOKEN is None:
    raise InvalidEnv("Неверный токен приложения Яндекса")
if VK_LOGIN is None:
    VK_LOGIN = input("Введите номер телефона: ")
if VK_PASSWORD is None:
    VK_PASSWORD = input("Введите пароль: ")
if VK_ALBUM_URL is None:
    VK_ALBUM_URL = input("Введите url альбома: ")

download_album(login=VK_LOGIN,
               password=VK_PASSWORD,
               album_url=VK_ALBUM_URL,
               app_id=VK_APP_ID)
upload_folders(app_token=YA_TOKEN)
