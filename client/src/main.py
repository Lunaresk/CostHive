from constants import Barcode_CodeID, Offline_Login, Scan_Options
from copy import deepcopy
from datetime import date
from json import dump as jdump, load as jload
from os import makedirs, remove
from os.path import dirname, exists
from select import select as timedInput
from sys import stdin
from yaml import safe_load
import connection
import logging


DIR = dirname(__file__) + "/"

if not exists(DIR + "../logs"):
    makedirs(DIR + "../logs")

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

fileHandler = logging.FileHandler(DIR + "../logs/client.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
LOGGER.addHandler(consoleHandler)

TEMPFILE = DIR + "scans.json"

TIMEOUT = 60  # Number of seconds for a timeout after being logged in
SET_AMOUNTS = ["1", "2", "5", "10"]


def main() -> None:
    while True:
        user = login()
        if not user:
            continue
        LOGGER.debug("Login successful")
        scanning(user)

def delete(scanned: list[dict[int: int]]):
    amount = 1
    while True:
        i, _, _ = timedInput([stdin], [], [], TIMEOUT)
        if not i:
            return  #TODO send a short timeout message before return
        scan = stdin.readline().strip()
        codeid, scan = split_codeid(scan, "")
        match codeid:
            case Barcode_CodeID.EAN8:
                try:
                    scanned.remove({scan: amount})
                except ValueError as e:
                    scanned.insert(0, {scan: -amount})
                    LOGGER.debug(f"Tried to delete {scan} with amount {amount}.")
                finally:
                    break
            case Barcode_CodeID.EAN13:
                try:
                    scanned.remove({scan: amount})
                except ValueError as e:
                    scanned.insert(0, {scan: -amount})
                    LOGGER.debug(f"Tried to delete {scan} with amount {amount}.")
                finally:
                    break
            case Barcode_CodeID.CODE128:
                match scan:
                    case Scan_Options.DELETE:
                        try:
                            scanned.pop()
                        except IndexError as e:
                            LOGGER.exception("")
                        finally:
                            break
                    case _:
                        try:
                            amount += int(scan)
                        except ValueError as e:
                            LOGGER.exception("")

def group_previous_scans(previous_scans: list[dict[any: any]]):
    for i in range(len(previous_scans))[::-1]:
        for j in range(len(previous_scans[i:])-1):
            j = i+j+1
            if previous_scans[i]['date'] == previous_scans[j]['date'] and previous_scans[i]['user'] == previous_scans[j]['user']:
                for key, value in previous_scans[i]['items'].items():
                    if key in previous_scans[j]['items']:
                        previous_scans[j]['items'][key] += value
                    else:
                        previous_scans[j]['items'][key] = value
                del(previous_scans[i])
                break

def group_scanning(scanned: list[dict[int: int]]) -> dict[int: int]:
    scan_dict = {}
    for scan in scanned:
        for key, value in scan.items():
            if key not in scan_dict:
                scan_dict[key] = value
            else:
                scan_dict[key] += value
    for key, value in scan_dict.items():
        if value <= 0:
            del(scan_dict[key])
    return scan_dict

def login(user: str = None):
    if not user:
        user = input("Enter Login: ")
        codeid, user = split_codeid(user, Barcode_CodeID.CODE128)
    else:
        codeid = Barcode_CodeID.CODE128
    if codeid != Barcode_CodeID.CODE128:
        return None
    if not connection.check_login(user):
        LOGGER.debug("Login failed")
        if not user in Offline_Login.OFFLINE_LOGIN:
            return None
        LOGGER.debug("Using local login")
    return user

def scanning(user: str) -> dict[int: int]:
    scan, scanned = "", []
    amount = 1
    while True:
        i, _, _ = timedInput([stdin], [], [], TIMEOUT)
        if not i:
            break  # send a short timeout message before break
        scan = stdin.readline().strip()
        codeid, scan = split_codeid(scan, Barcode_CodeID.EAN8)
        match codeid:
            case Barcode_CodeID.EAN8:
                scanned.append({scan: amount})
                amount = 1
            case Barcode_CodeID.EAN13:
                scanned.append({scan: amount})
                amount = 1
            case Barcode_CodeID.CODE128:
                match scan:
                    case Scan_Options.LOGOUT:
                        break
                    case Scan_Options.DELETE:
                        delete(scanned)
                    case _:
                        try:
                            if scan in SET_AMOUNTS:
                                amount = int(scan)
                            else:
                                amount += int(scan)
                        except:
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

def send_scan(user: str, scanned: dict[int: int], previous_scans: list[dict[any: any]] = None):
    if not previous_scans:
        previous_scans = []
    if exists(TEMPFILE):
        with open(TEMPFILE, "r") as file:
            previous_scans.extend(jload(file))
    if scanned:
        result = connection.send_scan(user, scanned)
        if result != True:
            result['date'] = str(date.today())
            previous_scans.append(result)
    if previous_scans:
        group_previous_scans(previous_scans)
        for bought in deepcopy(previous_scans):
            result = connection.send_scan(bought['user'], bought['items'], bought['date'])
            previous_scans.remove(bought)
            if result != True:
                previous_scans.append(result)
    if previous_scans: # if previous scans still present, save it
        with open(TEMPFILE, "w") as file:
            jdump(previous_scans, file)
    elif exists(TEMPFILE): # if no scans remain, delete the json
        remove(TEMPFILE)
    LOGGER.info(previous_scans)

def split_codeid(scan: str, default_codeid: str = ""):
    match Barcode_CodeID.CODEID_POS:
        case "prefix":
            return(scan[0], scan[1:])
        case "suffix":
            return(scan[-1], scan[:-1])
        case _:
            return(default_codeid, scan)

if __name__ == '__main__':
    main()