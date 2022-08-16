""" Скрипт для выгрузки фото из альбома ВК """
import os, time
from exceptions import InvalidEnv, TooManyCount
from datetime import datetime
from urllib.request import urlretrieve
from vk_api import VkApi
from settings import VK_LOGIN, VK_PASSWORD, VK_ALBUM_URL, VK_APP_ID


login = VK_LOGIN
password = VK_PASSWORD
album_url = VK_ALBUM_URL

if login is None:
    login = input("Введите номер телефона: ")
if password is None:
    password = input("Введите пароль: ")
if album_url is None:
    album_url = input("Введите url альбома: ")
if VK_APP_ID is None:
    raise InvalidEnv("Неверный идентификатор приложения ВК")


vk_session = VkApi(login=login, password=password, app_id=int(VK_APP_ID))
vk_session.auth()

vk = vk_session.get_api()

# Разбираем ссылку
album_id = album_url.split('/')[-1].split('_')[1]
owner_id = album_url.split('/')[-1].split('_')[0].replace('album', '')

photos_data = vk.photos.getAlbums(owner_id=owner_id, album_ids=album_id)
photos_count = photos_data['items'][0]['size']
if photos_count >= 1000:
    raise TooManyCount("Пока нельзя скачать фотографии из альбома, в котором больше 1000 фото")
album_created_at = photos_data['items'][0]['created']
album_created_at = datetime.utcfromtimestamp(album_created_at).strftime('%Y-%m-%d %H:%M:%S')
counter = 0 # текущий счетчик
prog = 0 # процент загруженных
breaked = 0 # не загружено из-за ошибки
time_now = time.time() # время старта

# Создадим каталоги, если их ещё нет
if not os.path.exists('saved_albums'):
    os.mkdir('saved_albums')
photo_folder = f'saved_albums/album{owner_id}_{album_id}'
if not os.path.exists(photo_folder):
    os.mkdir(photo_folder)

# Получаем список фото
photos = vk.photos.get(owner_id=owner_id,
                       album_id=album_id,
                       count=photos_count,
                       offset=0)['items']
for photo in photos:
    counter += 1
    url = photo['sizes'][0]['url'] # Получаем адрес изображения
    print(f'Загружается {counter}/{photos_count}. Прогресс: {prog}%')
    prog = round(100/photos_count*counter,2)
    try:
        urlretrieve(url, photo_folder + "/" + os.path.split(url)[1])
    except Exception:
        print('Произошла ошибка, файл пропущен.')
        breaked += 1
        continue

time_for_dw = time.time() - time_now
print(f"\nЗагружено {photos_count-breaked} файлов, {breaked} не удалось загрузить.\
Затрачено времени: {round(time_for_dw,1)} сек.")
