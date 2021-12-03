from requests import get, put, post, delete
from yaml import safe_load
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

fileHandler = logging.FileHandler("../logs/connection.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
LOGGER.addHandler(consoleHandler)


with open("config.yaml", 'r') as file:
    data = safe_load(file)['server']
SERVER = data['host']
PORT = data['port']
del(data)


def check_login(login: str) -> bool:
    response = get(url=":".join([SERVER, str(PORT)]) + '/scan2kasse/login', json={'login': login})
    if response.status_code == 200:
        return True
    return False


def send_scan(login: str, scanned: dict[int: int], date:str = None):
    infos = {'login': login, 'items': scanned}
    if date:
        infos['date'] = date
    try:
        response = put(url=":".join([SERVER, str(
            PORT)]) + '/scan2kasse/insert', json=infos)
        return True if response.status_code == 201 else response.json
    except Exception as e:
        LOGGER.exception(e)
        return False
