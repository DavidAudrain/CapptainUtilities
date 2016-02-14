import argparse
import base64
import json
import urllib
import urllib2
from helper import http
from api import constants 
from api import segments

parser = argparse.ArgumentParser()
parser.add_argument('--appid', required=True, dest='appid', help='Application ID')
parser.add_argument('--apikey', required=True, dest='apikey', help='API Key')
parser.add_argument('--api', required=True, dest='api', help='API', choices=[segments.SEGMENTS_API_NAME])

# Parse known arguments at this point
# other arguments may be known of underlying API
(known_args, unknown_args) = parser.parse_known_args()

http.setbasicauthentication(top_level_url=constants.TOP_LEVEL_URL, appid=known_args.appid, apikey=known_args.apikey)

if known_args.api == segments.SEGMENTS_API_NAME:
    segments_api = segments.Rest(known_args.appid)
    segments_api.process(unknown_args)
else:
    print "unknown api" 
