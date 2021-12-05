from copy import deepcopy
from datetime import date
from json import dump as jdump, load as jload
from os import makedirs, remove
from os.path import exists
from select import select as timedInput
from sys import stdin
from yaml import safe_load
import connection
import logging


if not exists("../logs"):
    makedirs("../logs")

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

with open("config.yaml", 'r') as file:
    data = safe_load(file)['options']
CODEID_POS = data['barcode']['codeid_position']

TEMPFILE = "scans.json"

TIMEOUT = 60  # Number of seconds for a timeout after being logged in


def main() -> None:
    while True:
        user = login()
        if not user:
            continue
        if user == "quit":
            break
        LOGGER.debug("Login successful")
        scanning(user)

def delete(scanned: list):
    i, _, _ = timedInput([stdin], [], [], TIMEOUT)
    if not i:
        return  #TODO send a short timeout message before return
    scan = stdin.readline().strip()
    codeid, scan = split_codeid(scan, "A")
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

def group_scanning(scanned: list[int]) -> dict[int: int]:
    scan_dict = {}
    for scan in scanned:
        if scan not in scan_dict:
            scan_dict[scan] = 1
        else:
            scan_dict[scan] += 1
    return scan_dict

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

def login(user: str = None):
    if not user:
        user = input("Enter Login: ")
        codeid, user = split_codeid(user, "D")
    else:
        codeid = "D"
    if codeid != "D":
        return None
    if not connection.check_login(user):
        LOGGER.debug("Login failed")
        if not ("users" in data and user in data['users']):
            return None
        LOGGER.debug("Using local login")
    return user

def scanning(user: str) -> dict[int: int]:
    scan, scanned = "", []
    while True:
        i, _, _ = timedInput([stdin], [], [], TIMEOUT)
        if not i:
            break  # send a short timeout message before break
        scan = stdin.readline().strip()
        codeid, scan = split_codeid(scan, "A")
        match codeid:
            case "A":
                scanned.append(scan)
            case "D":
                match scan:
                    case "logout":
                        break
                    case "delete":
                        delete(scanned)
                    case _:
                        altuser = login(scan)
                        if not altuser:
                            continue
                        LOGGER.debug("Login successful")
                        scanning(altuser)
                        break
            case _:
                LOGGER.debug(f"Unknown barcode scanned: {codeid}_{scan}")
    scanned = group_scanning(scanned)
    send_scan(user, scanned)

def send_scan(user: str, scanned: list, temp: list[dict] = []):
    if exists(TEMPFILE):
        with open(TEMPFILE, "r") as file:
            temp.extend(jload(file))
    result = connection.send_scan(user, scanned)
    if result != True:
        result['date'] = str(date.today())
        temp.append(result)
    if temp:
        temp = group_temp(temp)
        for bought in list(temp):
            result = connection.send_scan(bought['user'], bought['items'], bought['date'])
            temp.remove(bought)
            if result != True:
                temp.append(result)
    if temp: # if temp still present, save it
        with open(TEMPFILE, "w") as file:
            jdump(temp, file)
    elif exists(TEMPFILE):
        remove(TEMPFILE)
    LOGGER.info(temp)

def split_codeid(scan: str, default_codeid: str = ""):
    match CODEID_POS:
        case "prefix":
            return(scan[0], scan[1:])
        case "suffix":
            return(scan[-1], scan[:-1])
        case _:
            return(default_codeid, scan)

if __name__ == '__main__':
    main()