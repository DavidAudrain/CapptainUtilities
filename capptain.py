import argparse
import base64
import json
import urllib
import urllib2
from helper import http
from api import constants 
from api import segments

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--appid', dest='appid', help='Application ID')
parser.add_argument('--apikey', dest='apikey', help='API Key')

args = parser.parse_args()

print constants.TOP_LEVEL_URL

http.setbasicauthentication(top_level_url=constants.TOP_LEVEL_URL, appid=args.appid,apikey=args.apikey)

segments_api = segments.Segments(args.appid)

print json.dumps(segments_api.fetch_list(), sort_keys=True, indent=2)
