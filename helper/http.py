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
    requestUrl = rest_api_base + verb + "?" + payload
    return json.loads(urllib2.urlopen(requestUrl).read())
