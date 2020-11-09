# Lib_Com.py
# -*- coding: windows-1251 -*-
import serial
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


def test_com_port(_com_port_name):
    """проверка порта _com_port_name """
    try:
        ser = serial.Serial(_com_port_name)
        print("Открыт порт " + _com_port_name + ".")
        return 0
    except serial.serialutil.SerialException:
        print(serial.serialutil.SerialException)
        mes = "Ошибка 1003: не могу открыть порт " + _com_port_name + "."
        print(mes)
        write_log(mes)
        write_err_log(mes)
        exit(1003)


def com_port_sets(_com_port_name):
    """ Установка праметров сом-порта, заданного в ini-файле """
    # Serial takes these two parameters: serial device and baudrate
    # ser = serial.Serial('com1', 9600)
    # в Питоне-3 не следует производить одновременно инициализацию порта и установку скорости.
    # см. https://zhevak.wordpress.com/2015/10/29/python-3-x-и-модуль-serial/
    port_name = serial.Serial(_com_port_name)
    port_name.baudrate = 9600
    port_name.timeout = 0.2
    port_name.timeout = None  # порт будет ждать данные до тех пор, пока они не появятся


