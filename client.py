from socket import *
from json_module import from_json_bytes_to_dict, from_dict_to_json_byte


def set_archive(package_from_serv: dict) -> None:
    data = package_from_serv['data']
    print(data)


s = socket(AF_INET, SOCK_STREAM)
server_address = ('127.0.0.1', 10000)
s.settimeout(2.0)

try:
    test_data = from_dict_to_json_byte({'command': 'get_archive', 'data': None})
    s.connect(server_address)
    tm = s.send(test_data)
    data_from_serv = s.recv(1024)
    package_from_serv = from_json_bytes_to_dict(data_from_serv)
    if package_from_serv['command'] == 'set_archive':
        set_archive(package_from_serv)
    s.close()
except OSError:
    print('Нет данных')
