from psycopg2 import connect as psyconn, ProgrammingError, errors
from yaml import safe_load
import logging


LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)
logFormatter = logging.Formatter(
    "%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

fileHandler = logging.FileHandler("../logs/database.log")
fileHandler.setFormatter(logFormatter)
fileHandler.setLevel(logging.INFO)
LOGGER.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.DEBUG)
LOGGER.addHandler(consoleHandler)


class Database:

    def __init__(self, **kwargs):
        pass

    def connect(self, **kwargs):
        with open('config.yaml', 'r') as file:
            data = safe_load(file)['database']
        LOGGER.debug('Merging passed arguments with default arguments.')
        for key, value in data.items():
            if key not in kwargs or not kwargs[key]:
                kwargs[key] = value
        LOGGER.info('Connecting to Database.')
        self.conn = psyconn(host=kwargs["host"], port=kwargs["port"], dbname=kwargs["database"],
                            user=kwargs["user"], password=kwargs["password"])
        self.conn.autocommit = True

    def test_connection(self):
        if not hasattr(self, "conn"):
            LOGGER.info("Connection was not set, setting...")
            self.connect()
        else:
            with self.conn.cursor() as cursor:
                try:
                    cursor.execute("SELECT 1;")
                    cursor.fetchall()
                except:
                    LOGGER.warn(
                        'Connection seem to timed out, reconnecting...')
                    self.connect()

    def connectionpersistence(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            self.test_connection()
            return func(*args, **kwargs)
        return wrapper

    @connectionpersistence
    def get_user(self, **kwargs):
        result = ()
        if 'login' in kwargs:
            query = "SELECT login FROM users WHERE login = %(login)s;"
            with self.conn.cursor() as cursor:
                cursor.execute(query, kwargs)
                try:
                    result = cursor.fetchall()
                except ProgrammingError as e:
                    LOGGER.exception("")
                except Exception as e:
                    LOGGER.exception("")
        return result

    @connectionpersistence
    def get_report(self, **kwargs) -> list:
        query = "SELECT u.name, bp.date, i.name, bp.amount, bp.price FROM bought_with_prices bp INNER JOIN items i ON bp.item = i.id INNER JOIN users u ON bp.user = u.login"
        if kwargs:
            query += " WHERE "
            tempquery = []
            if "user" in kwargs and kwargs['user']:
                tempquery.append(f"bp.user = '{kwargs['user']}'")
            if "year" in kwargs and kwargs['year']:
                tempstring = "bp.date BETWEEN "
                if "month" in kwargs and kwargs['month']:
                    tempstring += f"'{kwargs['year']}-{kwargs['month']}-01' AND "
                    tempstring += f"'{kwargs['year']+1}-01-01'" if kwargs['month'] == 12 else f"'{kwargs['year']}-{kwargs['month']+1}-01'"
                else:
                    tempstring += f"'{kwargs['year']}-01-01' AND '{kwargs['year']+1}-01-01'"
                tempstring += "::date - INTERVAL '1' DAY"
                tempquery.append(tempstring)
            query += " AND ".join(tempquery)
        query += " ORDER BY u.name, bp.date, i.name ASC;"
        LOGGER.debug(f"Executing query: {query}")
        result = []
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            try:
                result = cursor.fetchall()
            except ProgrammingError as e:
                LOGGER.exception("")
            except Exception as e:
                LOGGER.exception("")
        return result

    @connectionpersistence
    def insert_bought_items(self, user: str, items: dict, date: str = None):
        temp = ['"user", item, amount', "%(user)s, %(item)s, %(amount)s",
                "bought.user = %(user)s AND bought.item = %(item)s AND bought.date = " + ("%(date)s" if date else "NOW()::date")]
        if date:
            temp[0] += ", date"
            temp[1] += ", %(date)s"
            values = [{'user': user, 'item': int(key), 'amount': value, 'date': date} for key, value in items.items()]
        else:
            values = [{'user': user, 'item': int(key), 'amount': value} for key, value in items.items()]
        query = f"INSERT INTO bought({temp[0]}) VALUES({temp[1]}) ON CONFLICT ON CONSTRAINT bought_user_item_date DO UPDATE SET amount = bought.amount + %(amount)s WHERE {temp[2]};"
        with self.conn.cursor() as cursor:
            failed = {}
            for value in values:
                try:
                    cursor.execute(query, value)
                except errors.ForeignKeyViolation as e:
                    if failed:
                        failed['items'][value['item']] = value['amount']
                    else:
                        failed = {'user': user, 'items': {value['item']: value['amount']}}
                        if date:
                            failed['date'] = date
                    LOGGER.exception("")
                except Exception as e:
                    LOGGER.exception("")
        return failed

    def __delete__(self):
        self.conn.close()
