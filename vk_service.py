""" Сервис работы с ВК """
import os, time
from datetime import datetime
from vk_api import VkApi
from urllib.request import urlretrieve

from exceptions import TooManyCount
from settings import ALBUMS_DIR


def download_album(login: str, password: str, album_url: str, app_id: int):
    vk_session = VkApi(login=login, password=password, app_id=int(app_id))
    vk_session.auth()
    vk = vk_session.get_api()
    # Разбираем ссылку
    album_id = album_url.split('/')[-1].split('_')[1]
    owner_id = album_url.split('/')[-1].split('_')[0].replace('album', '')
    photos_data = vk.photos.getAlbums(owner_id=owner_id, album_ids=album_id)
    photos_count = photos_data['items'][0]['size']
    
    
    
    photos_count -= 315
    
    
    
    
    if photos_count >= 1000:
        raise TooManyCount("Пока нельзя скачать фотографии из альбома, в котором больше 1000 фото")
    album_created_at = photos_data['items'][0]['created']
    album_created_at = datetime.utcfromtimestamp(album_created_at).strftime('%Y-%m-%d %H:%M:%S')
    counter = 0 # текущий счетчик
    prog = 0 # процент загруженных
    breaked = 0 # не загружено из-за ошибки
    time_now = time.time() # время старта

    # Создадим каталоги, если их ещё нет
    if not os.path.exists(ALBUMS_DIR):
        os.mkdir(ALBUMS_DIR)
    photo_folder = os.path.join(ALBUMS_DIR, f"album{owner_id}_{album_id}")
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
