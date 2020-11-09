# Lib_Log.py
from configparser import ConfigParser
import configparser  # импортируем библиотеки
import time
import os
import Lib_global


def write_log(str_log):
    """ запись в лог-файл переданной строки
    лог-файл находится в каталоге, заданном в ini-файле, далее в каталоге Год-месяц,
    в нём файл вида: BCS_Год-месяц-день.txt
    :param str_log: строка, записываемая в лог-файл.
    :return:
    """
    path_abs = os.path.abspath('.')  # возвращает нормализованный абсолютный путь
    # print('path_abs=' + path_abs)  # path_abs=D:\_KDL_\Python\Test01
    gm: str = "%4d-%02d" % time.localtime()[0:2]  # gm=2020-07
    global _path_log
    path: str = _path_log + "\\" + gm
    if not os.path.exists(path):
        os.mkdir(path)
    gmd = "%4d-%02d-%02d" % time.localtime()[0:3]  # gmd=2020-07-20
    gmd_time: str = "%4d-%02d-%02d %02d:%02d:%02d" % time.localtime()[0:6]
    log_fn: str = _path_log + "\\" + gm + "\\BCS_" + gmd + ".txt"
    with open(log_fn, 'a') as f:  # менеджер контекста
        f.write(gmd_time + " " + str_log + "\n")


def write_err_log(str_log):
    """ запись в ini-файл последней ошибки
    :param str_log: строка, записываемая в ini-файл, секция Statistics
    :return:
    """
    config: ConfigParser = configparser.ConfigParser()  # создаём объекта парсера
    global _path_ini_file
    config.read(_path_ini_file)  # читаем конфиг
    config.set("Statistics", "ErrDate", "%04d.%02d.%02d, %02d:%02d:%02d." % time.localtime()[0:6])
    config.set("Statistics", "ErrMsg", str_log)
    with open(_path_ini_file, "w") as config_file:  # Вносим изменения в конфиг. файл.
        config.write(config_file)
