import argparse
import base64
import json
import urllib
import urllib2
from helper import http
from api import constants 
from api import segments


def application_process_arguments(appid, apikey, arguments):
    http.setbasicauthentication(top_level_url=constants.TOP_LEVEL_URL, appid=appid, apikey=apikey)

    if known_args.api == segments.SEGMENTS_API_NAME:
        segments_api = segments.Rest(appid)
        segments_api.process(unknown_args)
    else:
        print "unknown api" 
    

parser = argparse.ArgumentParser()
parser.add_argument('--appid', dest='appid', help='Application ID. See Capptain application settings page.')
parser.add_argument('--apikey', dest='apikey', help='API Key')
parser.add_argument('--appregistry', dest='appregistry', help='JSON file listing appid and apikey by appname')
parser.add_argument('--apps', dest='apps', help='List of app names to apply the command')
parser.add_argument('--api', required=True, dest='api', help='API', choices=[segments.SEGMENTS_API_NAME])

# Parse known arguments at this point
# other arguments may be known of underlying API
(known_args, unknown_args) = parser.parse_known_args()

if (known_args.appid != None and known_args.apikey != None):
    application_process_arguments(known_args.appid, known_args.apikey, unknown_args)
elif (known_args.appregistry != None):
    list_json = open(known_args.appregistry, 'r')
    json_content = json.load(list_json)
    list_json.close()
    list_of_apps = json_content["apps"]
    if (known_args.apps != None):
        apps = known_args.apps.split(";")
        filtered_apps = filter(lambda app: app["name"] in apps, list_of_apps)
    else:
        filtered_apps = list_of_apps
    for app in filtered_apps:
        print "Process app " + app["name"]
        application_process_arguments(app["appid"], app["apikey"], unknown_args)
else:
    parser.print_help() 
