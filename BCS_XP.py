# BCS_XP.py
#from configparser import ConfigParser
import configparser  # импортируем библиотеки
import serial
import time
import os
import shutil
import sqlite3  # sql lite
import pyodbc  # для MS SQL SERVER - рекомендовано Microsoft
import sys
print("Testing serial port for BCS XP analyzer. Ver 1.06.")

# Существует несколько драйверов SQL для Python.
# Но корпорация Майкрософт сосредоточила все усилия по тестированию и внимание на драйвере pyodbc.
# https://docs.microsoft.com/ru-ru/sql/connect/python/python-driver-for-sql-server?view=sql-server-ver15
#
# глобальные переменные (значения изменяются в read_ini_file)
_path_ini_file: str = "BCS_XP.ini"  # или лучше назвать "settings.ini"?
_path_log: str = "."  # задаётся в ini-файле в секции [LogFiles]
_path_err_log: str = "."
_analyzer_id: int = 911  # задаётся в ini-файле в секции [Connection]
_com_port_name: str = 'no!'
_sql_connect: str = 'yes'
_server: str = 'Asu-911'  # 'tcp:myserver._database.windows.net'
_database: str = 'LabAutoResult'
_username: str = 'sa'
_password: str = '1'
_err_date: str = 'd-m-y'  # задаётся в ini-файле в секции [Statistics]
_err_msg: str = 'xx-x'
_run_count: int = 911
_list_modes: str = '-'  # задаётся в ini-файле в секции [Modes]
_debug: bool = False


def sql_insert(str_sql: str) -> str:
    """ Запись в MS SQL одного результата от анализатора
    :type str_sql: str
    """
    str_insert = str_sql

    history_number = 99000 + _run_count
    result_text = 'тест антитела'
    param_name1 = 'COVID-19'
    param_value1 = 'ОБНАРУЖЕНО'
    str_insert = "INSERT2 INTO [LabAutoResult].[dbo].[AnalyzerResults]" \
                 + "(Analyzer_Id, HistoryNumber, ResultDate, CntParam, ResultText, ParamName1, ParamValue1)Values(" \
                 + str(_analyzer_id) + ", " + str(history_number) + ", GetDate(), 1, '" + result_text + "', '" \
                 + param_name1 + "', '" + param_value1 + "')"
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' \
                              + _server + ';DATABASE=' + _database + ';UID=' + _username + ';PWD=' + _password)
        cursor = conn.cursor()
        if _debug:
            print('proc sql_insert:', str_insert)
        write_log(str_insert)
        cursor.execute(str_insert)
        conn.commit()
    except Exception:
        write_err_log("Ошибка при записи SQL.")
        write_log("Ошибка при записи SQL.")
        if _debug:
            print('Exception: ---', Exception)
        return -1
    return 0
    # row = cursor.fetchone()
    # while row:
    #     print('Inserted Product key is ' + str(row[0]))
    #     row = cursor.fetchone()


def sql_ms():
    # _server = 'localhost\sqlexpress' # for a named instance
    # _server = 'myserver,port' # to specify an alternate port
    # _server = 'Asu-911'  # 'tcp:myserver._database.windows.net'
    # _database = 'LabAutoResult'  # 'mydb'
    # _username = 'sa'  # 'myusername'
    # _password = '1'  # 'mypassword'
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='
                          + _server + ';DATABASE=' + _database + ';UID=' + _username + ';PWD=' + _password)
    cursor = conn.cursor()

    # Sample select query
    cursor.execute("SELECT @@version;")
    row = cursor.fetchone()
    while row:
        print(row[0])
        row = cursor.fetchone()
    print('= 111')

    sql_select: str = "SELECT top 8 [id],[Analyzer_Id], [HistoryNumber],[ResultDate], [CntParam],[ResultText]" + \
                      " ,[ParamName1], [ParamValue1], [ParamMsr1], [ParamName2] ,[ParamValue2], [ParamMsr2]" + \
                      " FROM [LabAutoResult].[dbo].[AnalyzerResults] where analyzer_Id=12" + \
                      " order by ResultDate desc"
    # sql_select = "select  from [LabAutoResult].[dbo].[AnalyzerResults] where analyzer_Id=12 "

    cursor.execute(sql_select)
    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()
    print('= 222')


def sql_lt_not_wokred():
    """sql_lt - sqlite3 notwokred! Вместо неё - import pyodbc  """
    global _list_modes, _debug
    if _list_modes.find('debug') != -1:
        print('*** debug *** _db_sql=' + _sql_connect)
        print('_debug=', _debug)

    conn = sqlite3.connect(_sql_connect)

    # if _list_modes.find('debug') != -1:
    #     print('*** conn:', conn)
    if _debug:
        print('*** conn:', conn)

    # Создаем курсор - это специальный объект который делает запросы и получает их результаты
    cursor = conn.cursor()
    sql_select: str = "SELECT top 99 [id],[Analyzer_Id], [HistoryNumber],[ResultDate], [CntParam],[ResultText]" + \
                      " ,[ParamName1], [ParamValue1], [ParamMsr1], [ParamName2] ,[ParamValue2], [ParamMsr2]" + \
                      " FROM [LabAutoResult].[dbo].[AnalyzerResults] where analyzer_Id=12" + \
                      " order by ResultDate desc"
    sql_select = "select top 10 from [LabAutoResult].[dbo].[AnalyzerResults] where analyzer_Id=12 "
    #  "order by ResultDate DESC "

    cursor.execute(sql_select)

    # Получаем результат сделанного запроса
    results = cursor.fetchall()
    results2 = cursor.fetchall()

    print(results)  # [('A Cor Do Som',), ('Aaron Copland & London Symphony Orchestra',), ('Aaron Goldberg',)]
    print(results2)  # []

    # Не забываем закрыть соединение с базой данных
    conn.close()


def read_ini_file():  # описание - ...
    """ Читаем  параметры в ini-файле
      :returns: 0 - OK, 1 - Не найден ini-файл
    """
    global _path_ini_file
    if not os.path.exists(_path_ini_file):
        mes: str = "Ошибка 1001: не найден файл конфигурации " \
                   + _path_ini_file + ". Программа завершила работу!"
        print(mes)
        # write_err_log(mes) - comment, because of ini-file does not exist and I cannot write in it :)
        exit(1001)
    config: configparser.ConfigParser = configparser.ConfigParser()  # создаём объекта парсера
    # config.sections()
    config.read(_path_ini_file)  # читаем конфиг
    # print(config["Connection"]["Analyzer_Id"])  # обращаемся как к обычному словарю!
    try:
        global _path_log, _path_err_log, _analyzer_id, _com_port_name, _sql_connect, _debug, _list_modes
        _analyzer_id = int(config["Connection"]["Analyzer_Id"])
        _com_port_name = config["Connection"]["ComPort"]
        _sql_connect = config["Connection"]["DbSQL"]
        global _server, _database, _username, _password
        _server = config["Connection"]["server"]  # 'Asu-911'  # 'tcp:myserver._database.windows.net'
        _database = config["Connection"]["database"]
        _username = config["Connection"]["username"]
        _password = config["Connection"]["password"]
        _path_log = config["LogFiles"]["path_log"]
        _path_err_log = config["LogFiles"]["path_err_log"]
        _list_modes = config["Modes"]["list_modes"]
        _debug = _list_modes.find('debug') != -1
    except:
        mes: str = "Ошибка 2001: нет нужного параметра в ini-файле: " + _path_ini_file + \
                   ". Программа завершила работу!"
        print(mes)
        write_err_log(mes)
        write_log(mes)
        exit(2001)

    if not os.path.exists(_path_log):
        mes: str = "Ошибка: не найден путь логов: " + _path_log + \
                   ". Программа завершила работу!"
        print(mes)
        write_err_log(mes)
        exit(1002)
    global _run_count
    _run_count = int(config.get("Statistics", "Run")) + 1
    # print("количество запусков:", _run_count)
    config.set("Statistics", "Run", str(_run_count))
    config.set("Statistics", "TimeStart", "Начало: %04d.%02d.%02d, %02d:%02d:%02d." % time.localtime()[0:6])
    # "GPS-%4d-%02d-%02d_%02d-%02d-%02d.csv" % time.localtime()[0:6]
    with open(_path_ini_file, "w") as config_file:  # Вносим изменения в конфиг. файл.
        config.write(config_file)
    return 0


def show_parameters():
    """ Показать параметры конфигурации    """
    print('Параметры:')
    print("_analyzer_id=", _analyzer_id, sep='')
    print("_com_port_name=" + _com_port_name)
    # print("_db_sql=" + _db_sql)
    # Data Source=Asu-911;Initial Catalog=LabAutoResult;User ID=sa;Password=12345)
    # 0123456789 123456789 123456789
    n_equal = _sql_connect.find('=')
    n_semicolon = _sql_connect.find(';')
    srv_name = _sql_connect[n_equal + 1: n_semicolon]
    # print('n_equal=', n_equal,'n_semicolon=',n_semicolon)
    print("srv_name=" + srv_name)


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
    config = configparser.ConfigParser()  # создаём объекта парсера
    global _path_ini_file
    config.read(_path_ini_file)  # читаем конфиг
    config.set("Statistics", "ErrDate", "%04d.%02d.%02d, %02d:%02d:%02d." % time.localtime()[0:6])
    config.set("Statistics", "ErrMsg", str_log)
    with open(_path_ini_file, "w") as config_file:  # Вносим изменения в конфиг. файл.
        config.write(config_file)


def test_com_ports():
    """ Сейчас не используется! Проверка всех портов.
        Вместо неё работает test_com_port
    """
    found = False
    for i in range(12):
        try:
            port_name = 'com' + str(i)
            ser = serial.Serial(port_name)
            ser.close()
            print("Найден последовательный порт:", port_name)
            found = True
        except serial.serialutil.SerialException:
            pass
    if not found:
        print('Последовательных портов не обнаружено!')
    print(found, port_name)


def recCode(data):
    if data == (b'\x05sRR\r\n'):
        print(u'я получил сообщение ')
    else:
        # print('Get:', data.decode("utf-8"))   # т.к. можнт быть тип None
        print('Get:', data)



def test_com_port():
    """проверка порта _com_port_name """
    try:
        ser = serial.Serial(_com_port_name)
        # в Питоне-3 не следует производить одновременно инициализацию порта и установку скорости
        # https://zhevak.wordpress.com/2015/10/29/python-3-x-и-модуль-serial/
        ser.baudrate = 9600
        ser.timeout = None
        print("Открыт порт " + _com_port_name + ".")
        # return 0
    except serial.serialutil.SerialException:
        print(serial.serialutil.SerialException)
        mes = "Ошибка 1003: не могу открыть порт " + _com_port_name + "."
        print(mes)
        write_log(mes)
        write_err_log(mes)
        exit(1003)
    print('>>> test_com_port')
    print(ser)
    k_an = 0
    k_byte = 0
    str_get = []
    # data = ser.read(ser.inWaiting)    # https://codecamp.ru/documentation/python/5744/python-serial-communication-pyserial
    data = None
    while True:
        while ser.inWaiting() > 0:  # даже если мы поставим без условия
            data = ser.readline()
        recCode(data)
        # print('Прочитали:', data)


    # while True:
    #     for line in ser.readline():
    #         k_byte += 1
    #         str_get.append(line)
    #         # print(line)
    #     if k_byte >= 25:
    #         break
    # print('Прочитали:', str_get) # Прочитали: [97, 115, 100, 51, 50, 49, 10, 97, 115, 100, 51, 50, 49, 10, 97, 115, 100, 51, 50, 49, 10, 97, 115, 100, 51, 50, 49, 10]



def com_port_sets():
    """ Установка праметров сом-порта, заданного в ini-файле """
    # Serial takes these two parameters: serial device and baudrate
    # ser = serial.Serial('com1', 9600)
    # в Питоне-3 не следует производить одновременно инициализацию порта и установку скорости.
    # см. https://zhevak.wordpress.com/2015/10/29/python-3-x-и-модуль-serial/
    port_name = serial.Serial(_com_port_name)
    port_name.baudrate = 9600
    port_name.timeout = 0.2
    port_name.timeout = None    # порт будет ждать данные до тех пор, пока они не появятся
    print('>>> com_port_sets Параметры:', port_name)



def test_samle_01():
    """Тестовая функция"""
    # https://pythonworld.ru/moduli/modul-shutil.html
    src = 'tmp1'
    dst = 'tmp2'
    if os.path.exists(src):
        shutil.copyfile(src, dst, follow_symlinks=True)


if __name__ == "__main__":
    read_ini_file()
    write_log("Начало.")
    # print(ReadIniFile.__doc__)
    show_parameters()
    com_port_sets()
    test_com_port()
    # test_samle_01()
    # sql_lt()  # sql lite
    # sql_ms()
    # rc = sql_insert('ddd')
    # print('rc=', rc)

    # fname = "GPS-%4d-%02d-%02d_%02d-%02d-%02d.csv" % time.localtime()[0:6]
    # print(fname)
    # print(time.localtime())
    # print(time.localtime()[0:6])
    print('--- Конец.')

"""  коды возврата:
1001 - не найден ini-файл
1002 - не найден путь логов.
1003 - Ошибка при открытии пота /нет com-порта
1004 - 
 ...
0 - All ok.
"""
