from datetime import date
from json import dump as jdump, load as jload
from os import remove
from os.path import exists
from select import select as timedInput
from sys import stdin
import connection
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

fileHandler = logging.FileHandler("../logs/client.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
LOGGER.addHandler(consoleHandler)

TEMP = []
TEMPFILE = "scans.json"

TIMEOUT = 60  # Number of seconds for a timeout after being logged in


def main() -> None:
    while True:
        login = input("Enter Login: ")
        if login == "quit":
            break
        if not connection.check_login(login):
            continue  # Send Error that login wasn't possible
        scanned = scanning()
        scanned = group_scanning(scanned)
        result = connection.send_scan(login, scanned)
        if result != True:
            result['date'] = str(date.now())
            TEMP.append(result)
        if TEMP:
            for bought in TEMP:
                result = connection.send_scan(bought['login'], bought['items'], bought['date'])
                TEMP.remove(bought)
                if result != True:
                    TEMP.append(result)
            with open(TEMPFILE, "w") as file:
                jdump(TEMP, file)
        elif exists(TEMPFILE):
            remove(TEMPFILE)


def scanning() -> list:
    scan, scanned = "", []
    while True:
        i, _, _ = timedInput([stdin], [], [], TIMEOUT)
        if not i:
            break  # send a short timeout message before break
        scan = stdin.readline().strip()
        match scan:
            case "logout":
                break
            case "delete":
                while True:
                    i, _, _ = timedInput([stdin], [], [], TIMEOUT)
                    if not i:
                        break  # send a short timeout message before break
                    scan = stdin.readline().strip()
                    try:
                        scanned.remove(scan)
                    except ValueError as e:
                        pass
            case _:
                scanned.append(scan)
    return scanned


def group_scanning(scanned: list[int]) -> dict[int: int]:
    scan_dict = {}
    for scan in scanned:
        if scan not in scan_dict:
            scan_dict[scan] = 1
        else:
            scan_dict[scan] += 1
    return scan_dict

if __name__ == '__main__':
    if exists(TEMPFILE):
        with open(TEMPFILE, "r") as file:
            TEMP = jload(file)
    main()