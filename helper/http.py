import json
import urllib
import urllib2

def setbasicauthentication(top_level_url, appid, apikey):
    # create a password manager
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

    # Add the username and password.
    # If we knew the realm, we could use it instead of None.
    password_mgr.add_password(None, top_level_url, appid, apikey)

    handler = urllib2.HTTPBasicAuthHandler(password_mgr)

    # create "opener" (OpenerDirector instance)
    opener = urllib2.build_opener(handler)

    # Install the opener.
    # Now all calls to urllib2.urlopen use our opener.
    urllib2.install_opener(opener)

def get_json(rest_api_base, verb, json_content):
    payload = urllib.urlencode(json_content)
    request_url = rest_api_base + verb + "?" + payload
    return json.loads(urllib2.urlopen(request_url).read())

def put_json(rest_api_base, verb, json_content, json_post_content):
    payload = urllib.urlencode(json_content)
    post_payload = json.dumps(json_post_content)
    request_url = rest_api_base + verb + "?" + payload
    #response = urllib2.urlopen(request_url, payload, {'Content-Type': 'application/json'})
    try:
        response = urllib2.urlopen(request_url, post_payload)
        return json.loads(response.read())
    except urllib2.HTTPError, err:
        print err.code
        print err.reason
        print err.read()

def put_json_no_response(rest_api_base, verb, json_content, json_post_content):
    payload = urllib.urlencode(json_content)
    post_payload = json.dumps(json_post_content)
    request_url = rest_api_base + verb + "?" + payload
    #response = urllib2.urlopen(request_url, payload, {'Content-Type': 'application/json'})
    try:
        response = urllib2.urlopen(request_url, post_payload)
    except urllib2.HTTPError, err:
        print err.code
        print err.reason
        print err.read()
