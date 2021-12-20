from os.path import dirname
from yaml import safe_load


DIR = dirname(__file__) + "/"

class Barcode_CodeID:
    with open(DIR + "config.yaml", 'r') as file:
        data = safe_load(file)['options']
    CODEID_POS = data['barcode']['codeid']['position'] if data and 'barcode' in data and 'codeid' in data['barcode'] and 'position' in data['barcode']['codeid'] else None
    CODE128 = data['barcode']['codeid']['Code128'] if data and 'barcode' in data and 'codeid' in data['barcode'] and 'Code128' in data['barcode']['codeid'] else "A"
    EAN8 = data['barcode']['codeid']['EAN8'] if data and 'barcode' in data and 'codeid' in data['barcode'] and 'EAN8' in data['barcode']['codeid'] else "C"
    EAN13 = data['barcode']['codeid']['EAN13'] if data and 'barcode' in data and 'codeid' in data['barcode'] and 'EAN13' in data['barcode']['codeid'] else "D"
    del(data)

class Offline_Login:
    with open(DIR + "config.yaml", 'r') as file:
        data = safe_load(file)['options']
    OFFLINE_LOGIN = data['users'] if "users" in data else ""
    del(data)

class Scan_Options:
    DELETE = "delete"
    LOGOUT = "logout"