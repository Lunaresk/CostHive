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
    try:
        response = get(url=":".join([SERVER, str(PORT)]) + '/scan2kasse/login', json={'login': login}, timeout=1)
    except Exception as e:
        LOGGER.debug("Server not reachable.")
        return False
    else:
        if response.status_code == 200:
            return True
        return False


def send_scan(user: str, scanned: dict[int: int], date:str = None):
    infos = {'user': user, 'items': scanned}
    if date:
        infos['date'] = date
    try:
        response = post(url=":".join([SERVER, str(
            PORT)]) + '/scan2kasse/insert', json=infos, timeout=1)
        return True if response.status_code == 201 else response.json()
    except Exception as e:
        LOGGER.exception("")
        return infos
