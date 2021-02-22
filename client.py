from socket import *
import sqlite3
import pickle
from json_module import from_json_bytes_to_dict, from_dict_to_json_byte
# Таблица: raw_data, поля: (params BLOB)
conn = sqlite3.connect("client_archive.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS raw_data(
   params BLOB PRIMARY KEY);
""")


def set_archive(package_from_serv: dict) -> None:
    data = package_from_serv['data']
    print(data)
    byte_data = pickle.dumps(data)
    cursor.execute("INSERT INTO raw_data (params) VALUES(?);", (byte_data,))
    conn.commit()


s = socket(AF_INET, SOCK_STREAM)
server_address = ('127.0.0.1', 10000)
s.settimeout(2.0)

try:
    test_data = from_dict_to_json_byte({'command': 'get_archive', 'data': None,
                                        'service_information': {'time_bd': 1614010025.7442386}})
    s.connect(server_address)
    tm = s.send(test_data)
    data_from_serv = s.recv(1024)
    package_from_serv = from_json_bytes_to_dict(data_from_serv)
    if package_from_serv['command'] == 'set_archive':
        set_archive(package_from_serv)
    s.close()
except OSError:
    print('Нет данных')
