from socket import *
from json_module import from_json_bytes_to_dict, from_dict_to_json_byte


def get_archive() -> dict:
    # Тут необходимо получить архив
    result = {'tp': 0, 'Ts': 0.0, 'Tr1': 0.0, 'Tp1': 0.0, 'Tr2': 0.0, 'Tp2': 0.0}
    return result


def form_passed_package(command: str, data: dict):
    dict_for_package = {'command': command, 'data': data}
    result_bytes = from_dict_to_json_byte(dict_for_package)
    return result_bytes


s = socket(AF_INET, SOCK_STREAM)
s.bind(('127.0.0.1', 10000))
s.listen()
while True:
    client, address = s.accept()
    tm = client.recv(1024)
    result_dict = from_json_bytes_to_dict(tm)
    print(result_dict)
    if result_dict['command'] == 'get_archive':
        data_archive = get_archive()
        bytes_data_for_client = form_passed_package('set_archive', data_archive)
        client.send(bytes_data_for_client)