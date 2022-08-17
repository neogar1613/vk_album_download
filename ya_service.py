""" Сервис работы с Яндекс Диском """
import yadisk
import os

from exceptions import InvalidEnv
from settings import ALBUMS_DIR


def upload_folders(app_token: str):
    # Проверка актуальности токена
    ya = yadisk.YaDisk(token=app_token)
    if ya.check_token() is False:
        raise InvalidEnv("Неверный или простроченный токен приложения Яндекса")
    # print('*'*20)
    # print(ya.get_disk_info())
    # print('*'*20)
    dir_counter = 0
    files_counter = 0
    broken_counter = 0
    try:
        ya.mkdir(ALBUMS_DIR)
    except yadisk.exceptions.DirectoryExistsError:
        print(f'::: Directory "{ALBUMS_DIR}" exists. Skip...')
    albums: list[str] = next(os.walk(ALBUMS_DIR))[1]
    for alb in albums:
        ya_path = os.path.join(ALBUMS_DIR, alb)
        try:
            ya.mkdir(ya_path)
        except yadisk.exceptions.DirectoryExistsError:
            print(f'::: Directory "{ya_path}" exists. Skip...')
        files_in_dir: list[str] = os.listdir(ya_path)
        dir_counter += 1
        for fil in files_in_dir:
            filepath = os.path.join(os.getcwd(), ya_path, fil)
            ya_file_path = os.path.join(ya_path, fil)
            files_counter += 1
            try:
                ya.upload(filepath, ya_file_path)
            except yadisk.exceptions.PathExistsError:
                broken_counter += 1
                print(f'::: File "{ya_file_path}" exists. Skip...')
    print(':'*10)
    print(f'Загруженно {files_counter-broken_counter} файлов \
из {dir_counter} альбомов\nПропущенно фалов {broken_counter}')
    print(':'*10)
