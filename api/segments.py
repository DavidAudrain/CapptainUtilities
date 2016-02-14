import constants
import json
from helper import http
class Segments:

    api_base = constants.TOP_LEVEL_URL + "/service/rest/segments/"

    def __init__(self, appid):
        self.appid = appid

    def fetch_list(self):
        return http.get_json(self.api_base, "list", {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': 3})})