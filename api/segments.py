import argparse
import constants
import json
import os
from helper import http

SEGMENTS_API_NAME="segments"

class Rest:

    CMD_LIST = 'list'
    CMD_LIST_STORE = 'liststore'
    
    COMMANDS = [CMD_LIST, CMD_LIST_STORE]

    api_base = constants.TOP_LEVEL_URL + "/service/rest/segments/"

    def __init__(self, appid):
        self.appid = appid

    def process(self, input_args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--cmd', dest='cmd', help='Command', default=Rest.CMD_LIST, choices=Rest.COMMANDS)
        parser.add_argument('--limit', dest='limit', help='Number of segments', default=3, type=int)
        parser.add_argument('--path', dest='path', help='Path where to read and write data', default='data')

        args = parser.parse_args(input_args)

        if args.cmd == Rest.CMD_LIST:
            response = http.get_json(self.api_base, "list", {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': args.limit})})
            print json.dumps(response, sort_keys=True, indent=2)
        elif args.cmd == Rest.CMD_LIST_STORE:
            if args.path != None:
                app_path = os.path.join(args.path, self.appid, 'segments')
                if not os.path.isdir(app_path):
                    os.makedirs(app_path)
                response = http.get_json(self.api_base, "list", {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': args.limit})})
                response = http.get_json(self.api_base, "list", {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': response["totalLength"]})})
                list_json = open(os.path.join(app_path, "list.json"), 'w')
                list_json.write(json.dumps(response, sort_keys=True, indent=2))
                list_json.close()
            else:
                print 'missing path argument'
        else:
            print "unknown command " + args.cmd
