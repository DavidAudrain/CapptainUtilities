import argparse
import constants
import json
import os
import time
from helper import http

API_NAME="device"

class Rest:

    CMD_QUERY = 'query'
    CMD_GET = 'get'
    
    COMMANDS = [CMD_QUERY, CMD_GET]
    
    VERB_QUERY = "query"
    VERB_GET = "show"

    api_base = constants.TOP_LEVEL_API_URL + "/device/0/app/"

    def __init__(self, appid, apikey):
        self.appid = appid
        self.apikey = apikey
        
    def sign_request(self, data):
        from hashlib import sha1
        import hmac

        print "hash " + str(data) + " with " + self.apikey
        hashed = hmac.new(key=bytearray(self.apikey, 'utf-8'),
            msg=bytearray(str(data), 'utf-8'),
            digestmod=sha1)
        # The signature
        return hashed.hexdigest() #.encode("base64").rstrip('\n')
    
    def getByDeviceId(self, ts, key, deviceid):       
        arguments = {'ts':ts, 'key':key, 'appid':self.appid, 'deviceid':deviceid}
        return http.get_json(self.api_base, Rest.VERB_GET, arguments)
    
    def process(self, input_args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--cmd', dest='cmd', help='Command', default=Rest.CMD_QUERY, choices=Rest.COMMANDS)
        parser.add_argument('--definition', dest='definition', help='Definition of the query', type=argparse.FileType('r'))
        parser.add_argument('--deviceid', dest='deviceid', help='deviceid to get')

        args = parser.parse_args(input_args)

        ts = int(time.time()) 
        key = self.sign_request(ts)
        if args.cmd == Rest.CMD_QUERY:
            # json_content = json.load(args.definition)
            # TODO Implement a better device matching capability by using an external json
            #query = json.dumps({"appInfo": [ "_s41518" ], "modifiedAfter": 1458432000000, "returnArray": True })
            arguments = {'ts':ts, 'key':key, 'appid':self.appid, 'query':query}
            response = http.get_json(self.api_base, Rest.VERB_QUERY, arguments)

            #filtered_elts = filter(lambda elt: elt["appInfo"]["_s41518"] == "true", response)
            #for elt in filtered_elts:
            #    ts = int(time.time()) 
            #    key = self.sign_request(ts)
            #    print json.dumps(self.getByDeviceId(ts, key, elt["deviceId"])) 

            #print json.dumps(response, sort_keys=True, indent=2)
            
        elif args.cmd == Rest.CMD_GET:
            print json.dumps(self.getByDeviceId(ts, key, args.deviceId))
        else:
            print "unknown command " + args.cmd
