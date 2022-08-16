""" Кастомные ошибки """

class InvalidEnv(Exception):
    """ Неверное или пустое значение переменной """

class TooManyCount(Exception):
    """ Фотографий в альбоме больше 1000 """