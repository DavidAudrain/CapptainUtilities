import argparse
import constants
import json
import os
from helper import http

SEGMENTS_API_NAME="segments"

class Rest:

    CMD_LIST = 'list'
    CMD_LIST_STORE = 'liststore'
    CMD_SEGMENT = 'segment'
    CMD_SEGMENT_CREATE = 'segmentcreate'
    CMD_SEGMENT_DELETE = 'segmentdelete'
    
    COMMANDS = [CMD_LIST, CMD_LIST_STORE, CMD_SEGMENT, CMD_SEGMENT_CREATE,CMD_SEGMENT_DELETE]
    
    VERB_LIST = "list"
    VERB_SEGMENT = "get"
    VERB_SEGMENT_CREATE = "createOrRename"
    VERB_SEGMENT_DELETE = "delete"
    VERB_CRITERION_CREATE = "criterion/createOrUpdate"

    api_base = constants.TOP_LEVEL_URL + "/service/rest/segments/"

    def __init__(self, appid):
        self.appid = appid
        
    def get_list_path(self, path):
        return os.path.join(path, self.appid, 'segments', 'list.json')
    def get_segment_path(self, path, segment_id):
        return os.path.join(path, self.appid, 'segments', 'segment_' + str(segment_id) + '.json')

    def process(self, input_args):
        parser = argparse.ArgumentParser()
        parser.add_argument('--cmd', dest='cmd', help='Command', default=Rest.CMD_LIST, choices=Rest.COMMANDS)
        parser.add_argument('--limit', dest='limit', help='Number of segments', default=3, type=int)
        parser.add_argument('--path', dest='path', help='Path where to read and write data', default='data')
        parser.add_argument('--id', dest='id', help='Id of the segment', default=1664, type=int)
        parser.add_argument('--definition', dest='definition', help='Definition of the segment', type=argparse.FileType('r'))

        args = parser.parse_args(input_args)

        if args.cmd == Rest.CMD_LIST:
            response = http.get_json(self.api_base, Rest.VERB_LIST, {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': args.limit})})
            print json.dumps(response, sort_keys=True, indent=2)
        elif args.cmd == Rest.CMD_LIST_STORE:
            app_path = os.path.join(args.path, self.appid, 'segments')
            if not os.path.isdir(app_path):
                os.makedirs(app_path)
            response = http.get_json(self.api_base, Rest.VERB_LIST, {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': args.limit})})
            response = http.get_json(self.api_base, Rest.VERB_LIST, {'config':json.dumps({'sortField': 'name', 'sortDirection': 'asc', 'limit': response["totalLength"]})})
            list_json_path = self.get_list_path(args.path)
            list_json = open(list_json_path, 'w')
            list_json.write(json.dumps(response, sort_keys=True, indent=2))
            list_json.close()
            print "List of segments saved to " + list_json_path
        elif args.cmd == Rest.CMD_SEGMENT:
            list_json = open(self.get_list_path(args.path), 'r')
            json_content = json.load(list_json)
            list_json.close()
            list_of_segments = json_content["data"]
            
            filtered_segments = filter(lambda seg: seg["id"] == args.id, list_of_segments)
            print "Found " + str(len(filtered_segments))
            if len(filtered_segments) > 0:
                response = http.get_json(self.api_base, Rest.VERB_SEGMENT, {'id':args.id})
                segment_json_path = self.get_segment_path(args.path, args.id)
                list_json = open(segment_json_path, 'w')
                list_json.write(json.dumps(response, sort_keys=True, indent=2))
                list_json.close()
                print "Segment " + str(args.id) + " saved to " + segment_json_path
            else:
                print "Did not find any segment " + str(args.id) + ". Call liststore first."
        elif args.cmd == Rest.CMD_SEGMENT_CREATE:
            json_content = json.load(args.definition)
            segment_name = json_content["name"]
            print "Create segment " + segment_name
            response = http.put_json(self.api_base, Rest.VERB_SEGMENT_CREATE, {'segment':json.dumps({'name': segment_name})}, {})
            if response["name"] == segment_name:
                segment_id = response["id"]
                print "segment created " + str(segment_id)
                segment_criteria = json_content["criteria"]
                for criteria in segment_criteria:
                    response = http.put_json(self.api_base, Rest.VERB_CRITERION_CREATE, {'segmentId':segment_id, 'criterion':json.dumps(criteria)}, {})
                    print "criterion created " + str(response)
            else:
                print "segment not created"
        elif args.cmd == Rest.CMD_SEGMENT_DELETE:
            response = http.put_json_no_response(self.api_base, Rest.VERB_SEGMENT_DELETE, {'id':args.id}, {})
            print "segment deleted " + str(args.id)
        else:
            print "unknown command " + args.cmd
