# Find com-port in range(0-256) 2020-07-29
import serial
import time


def find_com_ports():
    """ Сейчас не используется! Проверка всех портов.
        Вместо неё работает test_com_port
    """
    print("Поиск доступных Com-портов (от 0 до 256 - в МБУЗ ГБСМП и где-нибудь ещё :))")
    print("Searching for available Com-ports...")
    found = False
    for i in range(257):
        try:
            port_name = 'Com' + str(i)
            print('\r... поиск порта ' + port_name + ' ...', end='')
            time.sleep(0.03)
            # print('\r{}'.format(time.strftime("%H:%M:%S")), end='')
            ser = serial.Serial(port_name)
            ser.close()
            print('\rНайден последовательный порт ' + port_name + '.')
            found = True
        except serial.serialutil.SerialException:
            pass
    if not found:
        print('Последовательных портов не обнаружено!')
    print('\rКонец.')


# def test_time():
#     while True:
#         print('\r{}'.format(time.strftime("%H:%M:%S")), end='')
#         time.sleep(1)

if __name__ == "__main__":
    find_com_ports()
    # test_time()
