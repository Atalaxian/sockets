from socket import *
import sqlite3
import pickle
from json_module import from_json_bytes_to_dict, from_dict_to_json_byte

# Таблица: raw_data, поля: (params BLOB), (datetime REAL)
conn = sqlite3.connect("server_archive.db")

cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS raw_data(
   params BLOB,
   datetime REAL PRIMARY KEY);
""")


def get_archive(service_information) -> dict:
    time_bd = (service_information['time_bd'],)
    cursor.execute("SELECT params FROM raw_data WHERE datetime = ?;", time_bd)
    one_result = cursor.fetchone()
    one_result = one_result[0]
    result_data = pickle.loads(one_result)
    return result_data


def form_passed_package(command: str = None, data: dict = None, service_information: dict = None) -> bytes:
    dict_for_package = {'command': command, 'data': data, 'service_information': service_information}
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
        data_archive = get_archive(result_dict['service_information'])
        bytes_data_for_client = form_passed_package('set_archive', data_archive, None)
        client.send(bytes_data_for_client)
    client.close()
