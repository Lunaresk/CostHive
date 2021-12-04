from copy import deepcopy
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

TEMPFILE = "scans.json"

TIMEOUT = 60  # Number of seconds for a timeout after being logged in


def main(TEMP: list = None) -> None:
    while True:
        user = input("Enter Login: ")
        if user == "quit":
            break
        if not connection.check_login(user):
            LOGGER.debug("Login failed")
            continue  # Send Error that login wasn't possible
        LOGGER.debug("Login successful")
        scanned = scanning()
        scanned = group_scanning(scanned)
        result = connection.send_scan(user, scanned)
        if result != True:
            result['date'] = str(date.today())
            TEMP.append(result)
        if TEMP:
            TEMP = group_temp(TEMP)
            for bought in list(TEMP):
                result = connection.send_scan(bought['user'], bought['items'], bought['date'])
                TEMP.remove(bought)
                if result != True:
                    TEMP.append(result)
            with open(TEMPFILE, "w") as file:
                jdump(TEMP, file)
        elif exists(TEMPFILE):
            remove(TEMPFILE)
        LOGGER.info(TEMP)


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
                    match scan:
                        case "delete":
                            try:
                                scanned.pop()
                            except IndexError as e:
                                LOGGER.exception(e)
                        case _:
                            try:
                                scanned.remove(scan)
                            except ValueError as e:
                                LOGGER.exception(e)
            case _:
                scanned.append(scan)
    return scanned

def group_temp(TEMP: list):
    NEWTEMP = []
    for temp in TEMP:
        found = False
        for newtemp in NEWTEMP:
            if newtemp['date'] == temp['date'] and newtemp['user'] == temp['user']:
                for key, value in temp['items'].items():
                    if key in newtemp['items']:
                        newtemp['items'][key] += value
                    else:
                        newtemp['items'][key] = value
                found = True
                break
        if not found:
            NEWTEMP.append(deepcopy(temp))
    return NEWTEMP

def group_scanning(scanned: list[int]) -> dict[int: int]:
    scan_dict = {}
    for scan in scanned:
        if scan not in scan_dict:
            scan_dict[scan] = 1
        else:
            scan_dict[scan] += 1
    return scan_dict

if __name__ == '__main__':
    TEMP = None
    if exists(TEMPFILE):
        with open(TEMPFILE, "r") as file:
            TEMP = jload(file)
    main(TEMP)