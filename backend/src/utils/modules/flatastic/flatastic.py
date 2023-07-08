import json
import requests
from datetime import datetime


class Flatastic:
    api_url = "https://api.flatastic-app.com/index.php/api/"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=utf-8",
            "x-api-key": api_key,
            "x-api-version": "2.0.0"
        }

    def add_shoppinglist_item(self, name: str, bought: int = 0):
        payload = {"name": name, "bought": bought}
        response = requests.post(Flatastic.api_url + "shoppinglist", headers=self.headers, data=json.dumps(payload))
        return response

    def get_shoppinglist(self):
        try:
            response = requests.get(Flatastic.api_url + "shoppinglist", headers=self.headers)
        except:
            raise("Connection failed")
        else:
            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError:
                raise("No JSON")
            else:
                return response_json

    def add_chores_item(self, title: str, users: list[int], rotationTime: int = -1):
        payload = {"name": title, "rotationTime": rotationTime}
        response = requests.post(Flatastic.api_url + "chores", headers=self.headers, data=json.dumps(payload))
        return response
    
    def get_chores(self):
        try:
            response = requests.get(Flatastic.api_url + "chores", headers=self.headers)
        except:
            raise("Connection failed")
        else:
            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError:
                raise("No JSON")
            else:
                return response_json

    # Not finished yet
    # def add_cashflow(self, name: str, users: list[int], date: datetime = None):
    #     if not date:
    #         date = datetime.utcnow()
    #     payload = {"name": name, "date": date}
    #     response = requests.post(Flatastic.api_url + "chores", headers=self.headers, data=json.dumps(payload))
    #     return response

    def get_cashflow(self):
        try:
            response = requests.get(Flatastic.api_url + "cashflow", headers=self.headers)
        except:
            raise("Connection failed")
        else:
            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError:
                raise("No JSON")
            else:
                return response_json