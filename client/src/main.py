from datetime import date
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

TIMEOUT = 60  # Number of seconds for a timeout after being logged in


def main() -> None:
    while True:
        login = input("Enter Login: ")
        if not connection.check_login(login):
            continue  # Send Error that login wasn't possible
        scanned = scanning()
        scanned = group_scanning(scanned)
        if not connection.send_scan(login, scanned):
            TEMP.append({'login': login, 'items': scanned, 'date': str(date.today())})
        if TEMP:
            for bought in TEMP:
                if connection.send_scan(bought['login'], bought['items'], bought['date']):
                    TEMP.remove(bought)


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
    main()